#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')


# In[2]:


excel_file = 'Data Analytics Assignment.xlsx'
xls = pd.ExcelFile(excel_file)


# In[3]:


def load_app_data(sheet_name):
    """Loading daily data from a specific sheet."""
    df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
    daily_start_idx = df[df[1] == 'Daily Data'].index[0] + 1
    hourly_start_idx = df[df[1] == 'Hourly Data'].index[0]
    
    daily_df = pd.read_excel(excel_file, sheet_name=sheet_name, skiprows=daily_start_idx, nrows=hourly_start_idx - daily_start_idx - 2)
    daily_df = daily_df.iloc[:, 1:].rename(columns={'Date': 'date'})
    daily_df['date'] = pd.to_datetime(daily_df['date'])
    
    numeric_cols = [
        'unique_idfas', 'unique_ips', 'unique_uas', 'total_requests',
        'requests_per_idfa', 'impressions', 'impressions_per_idfa',
        'idfa_ip_ratio', 'idfa_ua_ratio', 'IVT'
    ]
    for col in numeric_cols:
        daily_df[col] = pd.to_numeric(daily_df[col], errors='coerce')
        
    return daily_df


# In[4]:


all_apps_list = []
for sheet_name in xls.sheet_names:
    df = load_app_data(sheet_name)
    df['app_name'] = sheet_name
    df['traffic_type'] = 'Invalid' if 'Invalid' in sheet_name else 'Valid'
    all_apps_list.append(df)

all_apps_df = pd.concat(all_apps_list, ignore_index=True)

print("Consolidated Dataframe Head:")
print(all_apps_df.head())


# In[5]:


ivt_trend_fig = px.line(
    all_apps_df,
    x='date',
    y='IVT',
    color='app_name',
    line_dash='traffic_type',
    title='<b>IVT Score Progression (Daily)</b>',
    labels={'IVT': 'IVT Score', 'date': 'Date', 'app_name': 'App Name'},
    markers=True,
    template='plotly_white'
)
ivt_trend_fig.update_layout(
    font_family="Inter, sans-serif",
    title_font_size=20,
    yaxis_tickformat='.0%'
)


# In[10]:


# IDFA to User-Agent Ratio Trend
idfa_ua_ratio_fig = px.line(
    all_apps_df,
    x='date',
    y='idfa_ua_ratio',
    color='app_name',
    line_dash='traffic_type',
    title='<b>IDFA-to-User-Agent Ratio</b>',
    labels={'idfa_ua_ratio': 'Devices per User-Agent (IDFA/UA Ratio)', 'date': 'Date'},
    markers=True,
    template='plotly_white'
)
idfa_ua_ratio_fig.update_layout(font_family="Inter, sans-serif", title_font_size=20)


# In[11]:


# Box Plot Comparison
box_plot_fig = px.box(
    all_apps_df,
    x='traffic_type',
    y='idfa_ua_ratio',
    color='traffic_type',
    notched=True,
    title='<b>Distribution of IDFA/UA Ratio by Traffic Type</b>',
    labels={'idfa_ua_ratio': 'IDFA/UA Ratio', 'traffic_type': 'Traffic Type'},
    template='plotly_white'
)
box_plot_fig.update_layout(font_family="Inter, sans-serif", title_font_size=20)


# In[12]:


# Scatter Plot to find the threshold
threshold_fig = px.scatter(
    all_apps_df,
    x='idfa_ua_ratio',
    y='IVT',
    color='traffic_type',
    title='<b>IVT Tipping Point: IDFA/UA Ratio vs. IVT Score</b>',
    labels={'idfa_ua_ratio': 'IDFA/UA Ratio', 'IVT': 'IVT Score'},
    template='plotly_white',
    hover_name='app_name'
)
threshold_fig.update_layout(
    font_family="Inter, sans-serif",
    title_font_size=20,
    yaxis_tickformat='.0%'
)
threshold_fig.add_vline(x=2000, line_dash="dash", line_color="red", annotation_text="Approx. IVT Threshold")


# In[ ]:




