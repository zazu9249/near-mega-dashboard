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
        "**Metrics**",
        "**Activity over Time**"
    ]
)

with tab2:
    st.subheader("Active Nodes")
    st.write(
        """
        Also known as Active Addresses, this metric is measured by collecting and recording 
        how many unique nodes are active during a predetermined time span, such as per day, 
        per week or per month. In permissionless blockchains, the greater the number, the greater 
        the indication that more nodes are using and trusting the blockchain application. 
        \n
        """
    )
    c1, c2 = st.columns([1,3])
    with c1:
        total_active_nodes = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/43656c5e-7d7b-4986-b03f-fd114ca4b1d5/data/latest')
        st.metric(label='**Total Unique Nodes**', value=str(total_active_nodes['TOTAL_NODES_COUNT'].values[0]))
    with c2:
        time_span = st.selectbox(
            'Select the time span to view the Active Nodes over Time',
            [
                "By Day", "By Week", "By Month"
            ],
            key="select_timespan_nodes",
        )
    active_nodes = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/9cb68077-5821-4e26-8d4b-aa57421d4a1f/data/latest')
    if time_span == "By Day":
        active_nodes = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/9cb68077-5821-4e26-8d4b-aa57421d4a1f/data/latest')
    elif time_span == "By Week":
        active_nodes = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/0a88df20-d8e6-41d3-b5db-7afb983d2716/data/latest')
    elif time_span == "By Month":
        active_nodes = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/e1c1835b-9033-4455-b787-aeaa0ff9cf84/data/latest')
    fig = px.bar(active_nodes,title='Number of Active Nodes over selected Time', x=active_nodes['DAY'], y=active_nodes['NO_OF_ACTIVE_NODES'])
    fig.update_layout(legend_title=None, xaxis_title='Time', yaxis_title='Active Nodes')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader("Blocks per Hour/Day")
    st.write(
        """
        These metrics measure the speed at which records are submitted and stored on the 
        blockchain network and how fast the network can carry out its consensus algorithm. 
        Because the capacity of a block is fixed, the quantity of blocks processed can be 
        calculated accordingly.

        Every block that is created has a timestamp (as per the timestamp header covered earlier 
        in the Understanding Blocks and Chains section). Via the use of timestamps, the blockchain 
        system can measure how many blocks are created and added during specified time periods, 
        such as per hour or per day. The results of these measurements help assess the performance 
        and scalability of the blockchain system. 
        \n
        """
    )
    c1, c2 = st.columns([1,3])
    with c1:
        total_blocks = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/29b93124-ae51-42b7-8db9-5829e8792a95/data/latest')
        st.metric(label='**Total Blocks Created**', value=str(total_blocks['TOTAL_BLOCKS_COUNT'].values[0]))
    with c2:
        time_span = st.selectbox(
            'Select the time span to view the Blocks created over Time',
            [
                "By Hour", "By Day",
            ],
            key="select_timespan_blocks",
        )
    blocks = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/67cdef00-309f-4383-bcfd-485cb5c47f0b/data/latest')
    if time_span == "By Hour":
        blocks = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/67cdef00-309f-4383-bcfd-485cb5c47f0b/data/latest')
    elif time_span == "By Day":
        blocks = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/5b87550e-ae9c-4950-9c27-c8bc884f7cdc/data/latest')
    fig = px.bar(blocks,title='Number of Blocks created over Time', x=blocks['TIME'], y=blocks['TOTAL_BLOCKS_COUNT'])
    fig.update_layout(legend_title=None, xaxis_title='Time', yaxis_title='# of Blocks')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader("Transactions Per Second")
    st.write(
        """
        This metric is used to measure the quantity of records or transaction records 
        submitted and stored per second. It is used to assess the volume of processing 
        a blockchain network is undergoing and to judge its scalability requirements. 
        The quantity of records submitted to the network and the quantity of records stored 
        to the ledger are generally measured separately. 
        \n
        """
    )

    c1, c2 = st.columns([1,1])
    with c1:
        total_trans = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/decb895c-c1b5-45b2-b8f1-4c3911e0175b/data/latest')
        st.metric(label='**Total Number of Transactions**', value=str(total_trans['TOTAL_NO_OF_TRANS'].values[0]))
    with c2:
        total_tps = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/decb895c-c1b5-45b2-b8f1-4c3911e0175b/data/latest')
        st.metric(label='**Transactions Per Second (TPS)**', value=str(total_trans['TPS'].values[0]))

    
    trans_per_day = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/876aa346-8b81-4f88-8d79-c0329e30db9f/data/latest')
    fig = px.line(trans_per_day, x='DAY', y='NO_OF_TRANS', title='Daily Number of Transactions')
    fig.update_layout(legend_title=None, xaxis_title='Day', yaxis_title="# Number of Transactions")
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    tps_per_day = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/876aa346-8b81-4f88-8d79-c0329e30db9f/data/latest')
    fig = px.bar(tps_per_day, x='DAY', y='TPS', title='Daily TPS')
    fig.update_layout(legend_title=None, xaxis_title='Day', yaxis_title="TPS")
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader("Transaction Latency")
    st.write(
        """
        This metric is used to measure the time from which a transaction is submitted to the 
        network until the time that the transaction has been written to the ledger (or rejected). 
        This metric is measured by checking the timestamp of transactions and comparing the time 
        they were submitted to the time they were validated and stored. This metric can also 
        provide insight as to how fast consensus algorithms are being carried out. 
        \n
        """
    )

    avg_latency = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/e2a0f2fb-03fb-462d-9d3c-f1cdfd993bf4/data/latest')
    st.metric(label='**Average Transaction Latency**', value=str(avg_latency['LATENCY'].values[0]))

    latency_per_day = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/1e22c399-612f-4d8b-8134-c029eaa846a8/data/latest')
    fig = px.bar(latency_per_day, x='DAY', y='LATENCY', title='Daily Transaction Latency')
    fig.update_layout(legend_title=None, xaxis_title='Day', yaxis_title="Latency")
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)




