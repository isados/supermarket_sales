# %%
import pandas as pd
import streamlit as st
import plotly.express as px

# %%
st.set_page_config(page_title='Sales Analysis Board',
                page_icon=':bar_chart:',
                layout='wide')

st.title(':bar_chart: Sale Analysis board')
st.markdown('##')
# %%

@st.cache_data
def get_data_from_csv():
    df = pd.read_csv('supermarkt_sales.csv')
    df['hour'] = pd.to_datetime(df['Time'], format='%H:%M').dt.hour
    return df

df = get_data_from_csv()

# --- SIDEBARD --- #
st.sidebar.header('Please filter here:')
city = st.sidebar.multiselect('City:',
                            options=df['City'].unique(),
                            default=df['City'].unique())

gender = st.sidebar.multiselect('Gender:',
                            options=df['Gender'].unique(),
                            default=df['Gender'].unique())

cust_type = st.sidebar.multiselect('Customer Type:',
                            options=df['Customer_type'].unique(),
                            default=df['Customer_type'].unique())


df_selection = df.query(
    "City == @city & Gender == @gender & Customer_type == @cust_type"
)




# TOP KPIs
total_sales = int(df_selection['Total'].sum())
average_rating = round(df_selection['Rating'].mean(),1)
average_sales = int(df_selection['Total'].mean())


left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.subheader('Total Sales')
    st.subheader(f'US $ {total_sales}')

with middle_column:
    st.subheader('Average Rating')
    st.subheader(':star:' * int(average_rating) + str(average_rating))

with right_column:
    st.subheader('Average Sales for Transaction')
    st.subheader(f'US $ {average_sales}')

# --- SALES BY PRODUCT LINE [BAR] --- #
sales_by_product_line = df_selection.groupby('Product line').sum()[['Total']].sort_values('Total')
fig_product_sales = px.bar(
    sales_by_product_line,
    x='Total',
    y=sales_by_product_line.index,
    orientation='h',
    title='<b>Sales by Product Line</b>',
    color_discrete_sequence=['#0083BB'] * len(sales_by_product_line),
    template='plotly_white',
)
fig_product_sales.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False)),
)

# --- SALES BY HOuR [BAR] --- #
sales_by_hour = df_selection.groupby('hour').sum()[['Total']].sort_values('Total')
fig_hourly_sales = px.bar(
    sales_by_hour,
    y='Total',
    x=sales_by_hour.index,
    title='<b>Sales by Hour</b>',
    color_discrete_sequence=['#0083B8'] * len(sales_by_hour),
    template='plotly_white',
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode='linear'),
    yaxis=dict(showgrid=False)
)


# --- COMBINING ALL CHARTS ABOVE --- #
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_product_sales, use_container_width=True)
right_column.plotly_chart(fig_hourly_sales, use_container_width=True)


# --- HIDE STREAMLIT STYLE --- #
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

