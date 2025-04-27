# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
#from snowflake.snowpark import Session

# title
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
"""Choose the fruits you want in your custom Smoothie!
  """
)

# input name
input_name = st.text_input('Name on Smoothie')
st.write("Name on Smoothie will be:",input_name)
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())
sf_sf = st.dataframe(smoothiefroot_response.json(), use_container_width = True)

# multi-select fruit ingredients
cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections= 5
)

# load into database
if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    space = ' '
    
    st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + input_name + """')"""

    #submut order button
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {input_name}!', icon="✅")
        
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
