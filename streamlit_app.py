# Import python packages
import streamlit as st
import requests
import pandas
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


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()


options = st.multiselect(
    "Choose upto 5 ingredients: ",
    my_dataframe,
    max_selections = 5
)


if options:
    
    options_string = ''

    for x in options:
      options_string += x + ' '

      search_on=pd_df.loc[pd_df['FRUIT_NAME'] == x, 'SEARCH_ON'].iloc[0]
      #st.write('The search value for ', x,' is ', search_on, '.')
      
      st.subheader(x + ' Nutrition Information')
      smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
      
      st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
      my_dataframe = session.table("smoothies.public.fruit_options").select(col('SEARCH_ON'),col('FRUIT_NAME'))
      #st.stop()

    #st.write(options_string)

    #my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            #values ('""" + options_string + """','"""+name_on_smoothie+"')"""

    #st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
