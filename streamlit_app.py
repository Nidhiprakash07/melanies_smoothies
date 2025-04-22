# Import python packages
import streamlit as st
import requests
#st.text(smoothiefroot_response)

# Write directly to the app
st.title(f" :cup_with_straw: Customize your smoothie!:cup_with_straw:")
st.write(
  """ **Choose the fruits you want in your custom smoothie**
  """
)


name_on_smoothie = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be", name_on_smoothie)


cnx = st.connection("snowflake")
session = cnx.session()
from snowflake.snowpark.functions import col


options = st.multiselect(
    "Choose upto 5 ingredients: ",
    my_dataframe,
    max_selections = 5
)


if options:
    options_string = ''

    for x in options:
      options_string += x + ' '
      smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
      st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
      my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
        

    st.write(options_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + options_string + """','"""+name_on_smoothie+"')"""

    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
