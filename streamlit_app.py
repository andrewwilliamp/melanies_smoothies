# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session // not needed in normal Streamlit
from snowflake.snowpark.functions import col
# Display nutrition info
import requests

import pandas as pd




# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name of your Smoothie will be: ' + name_on_order)

cnx = st.connection("snowflake")
#session = get_active_session()
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# Convert to pandas df
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections = 5
)

ingredients_string = ''

if ingredients_list:

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    st.write(ingredients_string)


    my_insert_stmt = """
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
        VALUES ('""" + ingredients_string + """', '""" + name_on_order + """', False, order_seq.nextval)
        """
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon = "✅")
    
    




