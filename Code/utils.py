import pandas as pd 
import numpy as np


def Line_fill_rate_cal(df):
    Total_Line_fill_rate = df.loc[df['delivery_qty']>=df['order_qty']].shape[0]
    Total_Line_fill_rate_pct = round(((Total_Line_fill_rate/df.shape[0])*100),2)
    return Total_Line_fill_rate_pct

def Volume_fill_rate_cal(df):
    return round((df['delivery_qty'].sum() / df['order_qty'].sum()*100),2)


def ord_delivery_metric(df,value):
    val=df.loc[df[value]==1,['order_id']].nunique()
    totalOrder=df['order_id'].nunique()
    return round((val/totalOrder*100),2)

# chart 1 
def Mom_order_level_metric(df):
    copy_s=df.drop_duplicates(subset=['order_id'])
    new_df = (copy_s
              .assign(order_placement_date = lambda x: pd.to_datetime(x['order_placement_date']))
              .assign(order_placement_month = lambda x: x['order_placement_date'].dt.strftime('%Y-%m'))
          .groupby('order_placement_month')
          .agg(
              ontime=('ord_on_time', lambda x:(x==1).sum()),
              infull=('ord_in_full', lambda x:(x==1).sum()),
              ontimeinfull=('ord_otif', lambda x:(x==1).sum()),
              total_orders=('order_id', 'nunique')
          )
          .reset_index()
          # Correct syntax: no quotes for new names, matching the aggregated names
          .assign(
              ontime_pct = lambda x: round((x['ontime'] / x['total_orders']) * 100, 2),
              infull_pct = lambda x: round((x['infull'] / x['total_orders']) * 100, 2),
              otif_pct   = lambda x: round((x['ontimeinfull'] / x['total_orders']) * 100, 2)
          )
              
         )
    return new_df[['order_placement_month','ontime_pct','infull_pct','otif_pct']] 




#chart 2
def total_orders_by_catgory(df):
    new_df=(df
            .groupby('category').agg(Total_orders=('order_id','nunique')).reset_index())
    return new_df
            
# chart3 
def top_bottom_product_by_otif(df,rank_method):
    new_df=(df
            .groupby('customer_name')
            .agg(Otif=('ord_otif', lambda x:(x==1).sum()),
                total_order_cx=('order_id','nunique'))
            .reset_index()
            .assign(OTIF_pct = lambda x :round(x ['Otif']/x['total_order_cx']*100,2)))
    if rank_method=='Top':
        new_df['rank']=new_df['OTIF_pct'].rank(method='first',ascending=False)
        final_df=new_df.loc[new_df['rank']<=5].sort_values(by='rank')
    else:
        new_df['rank']=new_df['OTIF_pct'].rank(method='first')
        final_df=new_df.loc[new_df['rank']<=5].sort_values(by='rank')
        
    
    return final_df[['customer_name','OTIF_pct']]


# chart 4
def product_distribution_by_vol_fill_rate(df,rank_method):
    new_df=(df
            .assign(is_delivered_qty_fulfiled= np.where(df['delivery_qty']>=df['order_qty'],1,0))
            .groupby('product_name')
            .agg(line_fill_rate=('is_delivered_qty_fulfiled','sum'),
                 total_order=('order_id','count')
                )
            .reset_index()
            .assign(line_fill_rate_pct=lambda x : round(x['line_fill_rate']/x['total_order']*100,2))
           )
    if rank_method=='Top':
        new_df['rank']=new_df['line_fill_rate_pct'].rank(method='first',ascending=False)
        final_df=new_df.loc[new_df['rank']<=5].sort_values(by='rank')
    else:
        new_df['rank']=new_df['line_fill_rate_pct'].rank(method='first')
        final_df=new_df.loc[new_df['rank']<=5].sort_values(by='rank')
    
    return final_df
            
    
