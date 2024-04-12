# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session // not needed in normal Streamlit
from snowflake.snowpark.functions import col
# Display nutrition info
import requests




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

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections = 5
)

ingredients_string = ''

if ingredients_list:

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    st.write(ingredients_string)


    my_insert_stmt = """
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
        VALUES ('""" + ingredients_string + """', '""" + name_on_order + """', False, order_seq.nextval)
        """
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon = "✅")
    
    
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())
fv_df = st.dataframe(date=fruityvice_response.json(), use_container_width=True)



