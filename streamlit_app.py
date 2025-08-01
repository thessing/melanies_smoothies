# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f"Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

#option = st.selectbox('How would you like to be contacted?', ('Email', 'Home phone', 'Mobile phone'))
#st.write('You selected:', option)
                    
#option = st.selectbox('What is your favorite fruit?', ('Bananas', 'Strawberries', 'Peaches'))
#st.write('Your favorite fruit is:', option)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

#session = get_active_session()
mytoken="eyJraWQiOiIzNTU4OTQzMDQ1NjIzODE0IiwiYWxnIjoiRVMyNTYifQ.eyJwIjoiMjEyMTI5NTQwOjIxMjEyOTU0MCIsImlzcyI6IlNGOjEwNDkiLCJleHAiOjE3NTUzMDg4Nzh9.pjsljrCxAOQesq2DWTDwRfcUCif10s5pm-3mvb5FVm5_ehdknmxr-IeeL3XnNxbCEXXO9_YskjOjhYlWnvtHUA"
cnx = st.connection("snowflake", token=mytoken)
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)
#smoothiefroot_response = requests.get("https://www.fruityvice.com/api/fruit/watermelon")
#st.text(smoothiefroot_response)
#sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutritional Information')
        smoothiefroot_response = requests.get("https://www.fruityvice.com/api/fruit/"+fruit_choosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    #if ingredients_string:
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:        
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")
    
