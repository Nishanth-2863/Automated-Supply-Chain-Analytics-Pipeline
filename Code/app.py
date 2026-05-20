import pandas as pd 
import numpy as np
import streamlit as st
import plotly.express as px
import altair as alt

from utils import ord_delivery_metric,Line_fill_rate_cal,Volume_fill_rate_cal,Mom_order_level_metric,total_orders_by_catgory,top_bottom_product_by_otif,product_distribution_by_vol_fill_rate
st.set_page_config(layout="wide")
st.title("Atlart Supply Chain Dashboard")
# Read csv file 
df=pd.read_csv(r"C:\Users\nishanth.k\Documents\Python Scripts for Important Queries\Untitled Folder\summary.csv")
df['country']=np.where(df['city']=='New Jersey, US','Usa','India')
temp_df=df

#side bar filters 
st.sidebar.header("Filters")
country_options = ['All']+list(df['country'].unique())
country_selected =st.sidebar.selectbox("Select Country",country_options)

# Main Dashboard filter 

if country_selected=='All':
    filtered_df=temp_df
else:
    filtered_df=temp_df.loc[temp_df['country']==country_selected]


#KPI Calculation 
Total_Orders = filtered_df['order_id'].nunique()

Total_Line_fill_rate_pct=Line_fill_rate_cal(filtered_df)

Volume_fill_rate_pct = Volume_fill_rate_cal(filtered_df)

#KPI 
Ontime_Delivery_pct=ord_delivery_metric(filtered_df,'ord_on_time')
InTime_Delivery_pct=ord_delivery_metric(filtered_df,'ord_in_full')
InFull_On_Time_Delivery_pct=ord_delivery_metric(filtered_df,'ord_otif')



# # KPI creation 
col_1,col_2,col_3,col_4,col_5,col_6=st.columns(6)
with col_1:
    st.metric(label='Total Orders',value=Total_Orders)
with col_2:
    st.metric(label='Line Fill Rate %',value=Total_Line_fill_rate_pct)

with col_3:
    st.metric(label='Volume Fill Rate %',value=Volume_fill_rate_pct)
    
with col_4:
    st.metric(label='OnTime Delivery  %',value=Ontime_Delivery_pct)

with col_5:
     st.metric(label='InTime Delivery  %',value=InTime_Delivery_pct)

with col_6:
    st.metric(label='On Time In Full  %',value=InFull_On_Time_Delivery_pct)


# Dashboard Charts

chart_col_1,chart_col_2=st.columns([3,3],gap="large")

res=Mom_order_level_metric(filtered_df)
chart_df = res.set_index('order_placement_month')


#chart 3 
chart_3_filter_options= ['Top','Bottom']

#st.dataframe(chart_3)


# Chart 1 
with chart_col_1:
    #chart_1
    st.subheader("MoM Performance Comparison")
    st.bar_chart(chart_df,stack=False)
    st.html("<br>")
    #chart_3
    st.subheader("Customer  distribution by OTIF Pct")
    chart_3_selected_filter=st.selectbox("Select Option",chart_3_filter_options)
    chart_3=top_bottom_product_by_otif(filtered_df,chart_3_selected_filter)
    chart_3_df=chart_3.set_index('customer_name')
    st.bar_chart(chart_3_df.sort_values(by='OTIF_pct'))


    


chart_4_filter_options= ['Top','Bottom']

with chart_col_2:
    orders_by_category=total_orders_by_catgory(filtered_df)
    fig = px.pie(orders_by_category, values='Total_orders', names='category', title='Total Orders Distribution By Category')
    st.plotly_chart(fig)
    st.html("<br>")
    #chart 4
    st.subheader("Product wise distribution by Line Fill rate")
    chart_4_selected_filter=st.selectbox("Select Options",chart_4_filter_options)
    chart_4=product_distribution_by_vol_fill_rate(filtered_df,chart_4_selected_filter)
    st.dataframe(chart_4.set_index('rank'))

