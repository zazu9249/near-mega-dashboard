import datetime as dt
from email.mime import image
import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
from dateutil import parser


theme_plotly = None

st.set_page_config(page_title='NEAR Mega Dashboard', page_icon= 'Images/near-logo.png', layout='wide')
st.title('NEAR Mega Dashboard')
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] .css-163ttbj e1fqkh3o1l { width: 250px; }
    </style>
    """,
    unsafe_allow_html=True,
)
c1, c2 = st.columns(2)
c1.image(Image.open('Images/NEAR-Protocol.png'))
c2.subheader('What is NEAR?')
c2.write(
    """
    NEAR Protocol is a decentralized application (dApp) platform and Ethereum competitor 
    that focuses on developer and user-friendliness. Its native NEAR tokens are used to pay 
    for transaction fees and storage on the Near crypto platform. NEAR is a Proof-of-Stake 
    blockchain that uses sharding technology to achieve scalability.
    \n 
    NEAR’s native token is also called NEAR, and is used to pay for transaction fees and storage. 
    NEAR tokens can also be staked by token holders who participate in achieving network consensus 
    as transaction validators.
    Projects building on NEAR include Mintbase, a non-fungible token (NFT) minting platform, 
    and Flux, a protocol that allows developers to create markets based on assets, commodities, 
    real-world events, and more.
    """
)
st.subheader('Price Chart')
c1, c2 = st.columns([1,3])
with c1:
    current_price = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/6b0abb21-08e5-4aff-860b-7881ab5213ee/data/latest')
    st.metric(label='**Current Price**', value=str(current_price['HOURLY_PRICE'].values[0]), help='USD')
with c2:
    time_range = st.selectbox(
        'Select the time range',
        [
            "All Time", "24 Hours", "7 Days", "30 Days", "90 Days", "1 Year"
        ],
        key="select_timerange",
    )

hourly_price = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/a0ffdf60-8fb8-4305-bd7e-985c9cfbfd08/data/latest')
df = hourly_price.query("BLOCKCHAIN == 'NEAR'")
df['HOUR'] = pd.to_datetime(df['HOUR'])

if time_range == "All Time":
    df = df
elif time_range == "24 Hours":
    df = df[ df['HOUR'] >= (dt.datetime.now()-pd.Timedelta(hours=24))]
elif time_range == "7 Days":
    df = df[ df['HOUR'] >= (dt.datetime.now()-pd.Timedelta(days=7))]
elif time_range == "30 Days":
    df = df[ df['HOUR'] >= (dt.datetime.now()-pd.Timedelta(days=30))]
elif time_range == "90 Days":
    df = df[ df['HOUR'] >= (dt.datetime.now()-pd.Timedelta(days=90))]
elif time_range == "1 Year":
    df = df[ df['HOUR'] >= (dt.datetime.now()-pd.Timedelta(days=365))]

fig = px.line(df, x='HOUR', y='HOURLY_PRICE', title='Hourly Price Trend of NEAR')
fig.update_layout(legend_title=None, xaxis_title='Hour', yaxis_title='Price (in $)')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

tab2, tab1 = st.tabs(
    [
        "Metrics",
        "Activity over Time"
    ]
)

with tab2:
    st.header("Metrics")
    