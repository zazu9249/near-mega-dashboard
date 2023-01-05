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

st.header("Methodology")
with st.expander("Method details and data sources"):
    st.write(
        """
        In this mega dashboard, the data has been selected from flipside crypto 
        (https://flipsidecrypto.xyz) data platform using its REST API. These queries are run every 
        3 hours to include the latest data, and the JSON file is imported directly into each visualization.
        This tool's source code is available in the 
        [**GitHub Repository**](https://github.com/zazu9249/near-mega-dashboard).
        A mega dashboard is designed and structured in multiple TABS that can be accessed using the sidebar.
        There are several different segments of the NEAR ecosystem represented on each of these Tabs.
        The NEAR's website allows you to explore each sector (Metrics, Swaps, GAS & Fees, Staking etc.) more deeply.
        All the Metrics have been calculated since the start of NEAR Blockchain.

        Here are the queries for all the visualizations: 
        [**Flipside Collection**](https://app.flipsidecrypto.com/velocity/collections/e124693b-82b5-4ab0-b12e-c24a60f9bf54) 
        """
    )

tab4, tab3, tab2, tab1 = st.tabs(
    [
        "**Metrics**",
        "**Swaps**",
        "**GAS & Fees**",
        "**Staking**"
    ]
)

with tab4:
    st.write(
        """
        Blockchain metrics are used to measure the quality, performance and scalability of 
        blockchain applications and to establish benchmarks for different versions of blockchain 
        applications to be compared against each other.
        
        The following are common metrics, all of which are measured at runtime, while the blockchain application is active.
        """
    )
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

    st.subheader("New Nodes")
    new_nodes = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/3b4a99c8-8bc0-476d-82ed-a78a60242e15/data/latest')
    fig = px.line(new_nodes, x="Join date", y="Cumulative", title="Number of New Nodes vs Cumulative New Nodes", log_y=True)
    fig.add_trace(go.Bar(x=new_nodes["Join date"], y=new_nodes["New Wallets"]))
    fig.update_layout(showlegend=False, legend_title=None, xaxis_title='DATE', yaxis_title='Number of Nodes')
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

with tab3:
    st.write(
        """
        Swap facilitates the instant exchange of two non-native tokens between two unique 
        blockchain protocols without the need of commencing the traditional crypto-to-fiat 
        exchange or token migration. It allows users to swap tokens directly from the official 
        private key wallet or the trading account. In-wallet exchange offers multiple benefits 
        for the traders, such as non-custodial trading, on-chain exchange, faster transactions, 
        and zero network fees.
        """
    )

    c1, c2 = st.columns([1,1])
    total_swaps = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/e27380a3-b603-4eef-ab5f-1bb0a3ed2255/data/latest')
    with c1:
        st.metric(label='**Total Number of Swaps**', value=str(total_swaps['TOTAL_SWAPS'].values[0]))
    with c2:
        st.metric(label='**Total Number of Unique Traders**', value=str(total_swaps['NO_OF_SWAPPERS'].values[0]))

    swap_activity = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/6b8977d0-da7e-404c-bc80-07b45b6e223b/data/latest')
    fig = px.bar(swap_activity, x="DAY", y=["TOTAL_SWAPS", "NO_OF_SWAPPERS"], title="Swap Metrics over Time")
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    c1, c2 = st.columns([1,1])
    with c1:
        top_traders_1 = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/e13bdb4f-4590-4420-a3d3-2e120326c292/data/latest')
        fig = px.pie(top_traders_1, values='NO_OF_SWAPS', names='SWAPPER', title='Top Swappers by Swaps Count')
        fig.update_layout(showlegend = False)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    with c2:
        top_traders_2 = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/1e8af9f9-5fd0-4411-85b8-104f10cbd82a/data/latest')
        fig = px.pie(top_traders_2, values='TOTAL_SWAP_IN_VOLUME_USD', names='SWAPPER', title='Top Swappers by Swap Volume')
        fig.update_layout(showlegend = False)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    st.subheader("SWAPs of NEAR Token")
    c1, c2 = st.columns([1,1])
    near_swaps = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/4c5dbb8e-3d3a-4ecf-a245-c7e36b92f4ea/data/latest')
    with c1:
        st.metric(label='**Total Number of Swaps IN**', value=str(near_swaps['NO_OF_SWAPS_IN'].values[0]))
    with c2:
        st.metric(label='**Total Number of Swaps OUT**', value=str(near_swaps['NO_OF_SWAPS_OUT'].values[0]))
    
    c1, c2 = st.columns([1,1])
    near_swaps_volume = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/b0d1bded-7b96-4c72-b68f-5142044a38cf/data/latest')
    with c1:
        st.metric(label='**Total Swap IN Volume**', value=str(near_swaps_volume['SWAP_IN_VOLUME_USD'].values[0]))
    with c2:
        st.metric(label='**Total Swap OUT Volume**', value=str(near_swaps_volume['SWAP_OUT_VOLUME_USD'].values[0]))
    
    c1, c2 = st.columns([1,1])
    near_swappers = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/fc89e9b0-26d3-491e-b3d8-2351138e9b87/data/latest')
    with c1:
        st.metric(label='**Number of Swappers who swapped into the NEAR**', value=str(near_swappers['NO_OF_SWAPPERS_IN'].values[0]))
    with c2:
        st.metric(label='**Number of Swappers who swapped out the NEAR**', value=str(near_swappers['NO_OF_SWAPPERS_OUT'].values[0]))
    
    c1, c2 = st.columns([1,1])
    with c1:
        top_near_swappers_1 = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/e0fefd99-8536-433f-9c83-fad067a3e2f5/data/latest')
        fig = px.pie(top_near_swappers_1, values='SWAP_IN_VOLUME_USD', names='SWAPPER', title='Top Swappers who Swapped into the NEAR by Volume (in $)')
        fig.update_layout(showlegend = False)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    with c2:
        top_near_swappers_2 = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/1cc3e8ed-b59c-465d-8669-635e6fb53338/data/latest')
        fig = px.pie(top_near_swappers_2, values='SWAP_OUT_VOLUME_USD', names='SWAPPER', title='Top Swappers who Swapped out the NEAR by Volume (in $)')
        fig.update_layout(showlegend = False)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab2:
    st.subheader("What is Transaction Fees?")
    st.write(
        """
        Transaction fees are and have been an essential part of most blockchain systems 
        since their inception. You are most likely to have come across them when sending, 
        depositing, or withdrawing crypto.
        
        The majority of cryptocurrencies use transaction fees for two important reasons. 
        First of all, fees reduce the amount of spam on the network. It also makes large-scale 
        spam attacks costly and expensive to implement. Secondly, transaction fees act as an 
        incentive for users that help verify and validate transactions. Think of it as a reward 
        for helping the network.
        """
    )
    st.subheader("What is GAS Fees?")
    st.write(
        """
        A gas fee is the term given to transaction fees on the Ethereum (CRYPTO:ETH) blockchain 
        network. According to Ethereum’s developer pages, gas is “the fuel that allows the 
        [Ethereum network] to operate, in the same way that a car needs gasoline to run.”
        
        Other cryptocurrencies may simply call these transaction fees, miner fees, or something 
        similar. However, since Ethereum is currently the second-largest crypto by market cap, 
        the term “gas” is often applied when referring to the fees involved in executing work on 
        other blockchains.
        """
    )
    c1, c2, c3 = st.columns([1,1,1])
    near_fees = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/de67356b-c2fa-4d8f-b594-11076d303964/data/latest')
    with c1:
        st.metric(label='**Total Transaction Fee (in NEAR)**', value=str(near_fees['TOTAL_TRANSACTION_FEE'].values[0]))
    with c2:
        st.metric(label='**Total Transaction Fee (in $)**', value=str(near_fees['TOTAL_TRANS_FEE_USD'].values[0]))
    with c3:
        st.metric(label='**Total GAS Used**', value=str(near_fees['TOTAL_GAS_USED'].values[0]))
    
    fees = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/2100bcb8-3a86-425f-a189-8491ba61b513/data/latest')
    fig = px.bar(fees,title='Total Transaction Fees per Week', x=fees['DAY'], y=fees['TOTAL_TRANS_FEE_USD'])
    fig.update_layout(legend_title=None, xaxis_title='Time', yaxis_title='Total Transaction Fee (in $)')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = px.bar(fees,title='Total GAS Used per Week', x=fees['DAY'], y=fees['TOTAL_GAS_USED'])
    fig.update_layout(legend_title=None, xaxis_title='Time', yaxis_title='Total GAS USed (in $)')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    c1, c2 = st.columns([1,1])
    avg_fee_per_tx = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/b3e9b66b-84ce-4b01-ac8e-7de2d34cf48f/data/latest')
    with c1:
        st.metric(label='**Average Transaction Fee per Transaction (in $)**', value=str(avg_fee_per_tx['AVG_FEE_PER_TX'].values[0]))
    with c2:
        st.metric(label='**Average Transaction Fee per User (in $)**', value=str(avg_fee_per_tx['AVG_FEE_PER_TRADER'].values[0]))

    daily_fees = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/b99f37d4-9fd6-4205-99cd-a13f93602e58/data/latest')
    fig = px.line(daily_fees, x="DAY", y=["AVG_FEE_PER_TX", "AVG_FEE_PER_TRADER"], title="Average Transaction Fee per Transaction on Weekly basis", log_y=True)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    # fig = px.line(daily_fees, x="DAY", y="AVG_FEE_PER_TRADER", title="Average Transaction Fee per Trader on Weekly basis")
    # st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab1:
    st.subheader("What is Staking?")
    st.write(
        """
        Staking is when you lock crypto assets for a set period of time to help support the 
        operation of a blockchain. In return for staking your crypto, you earn more cryptocurrency.

        Many blockchains use a proof of stake consensus mechanism. Under this system, network 
        participants who want to support the blockchain by validating new transactions and adding 
        new blocks must “stake” set sums of cryptocurrency.
        """
    )
    st.subheader("Staking on NEAR")
    st.write(
        """
        Staking allows you to earn NEAR rewards in return for delegating your tokens with a validator. 
        This is an essential process in Proof-of-Stake (PoS) blockchains which is required to ensure 
        security and decentralisation. Staking is an important aspect of blockchains with a Proof-of-Stake 
        mechanism, like NEAR.

        Proof-of-Stake (PoS) is a consensus mechanism to determine which users get to create new 
        blocks on the NEAR blockchain. New block creators are selected by the amount of NEAR they’ve 
        locked-up in the network.

        In the NEAR network, a decentralized pool of validators keeps the network secure by 
        processing transactions and in return these validators receive a reward.

        **Validators & Delegators:**

        Validators are pieces of hardware, ran by individuals, groups, or organisations, 
        which serve to secure, maintain, and run the NEAR blockchain.\n
        Delegators are those who commit their NEAR to a validator to assist in securing the 
        network and to earn rewards in the process.
        """
    )
    
    c1,c2 = st.columns([1,1])
    with c1:
        total_pools = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/3ea466a6-6f61-4893-8a09-38bec66030ef/data/latest')
        st.metric(label='**Total Number of Staking Pools**', value=str(total_pools['TOTAL_NO_OF_POOLS'].values[0]))
    with c2:
        validators = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/80ce068a-dcc9-42e3-bd84-fee610dbba09/data/latest')
        st.metric(label='**Total Number of Validators**', value=str(validators['NO_OF_VALIDATORS'].values[0]))
    
    c1,c2,c3 = st.columns([1,1,1])
    pools = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/80ce068a-dcc9-42e3-bd84-fee610dbba09/data/latest')
    with c1:
        st.metric(label='**Minimum Size of the Pool**', value=str(pools['MIN_POOL'].values[0]))
    with c2:
        st.metric(label='**Maximum Size of the Pool**', value=str(pools['MAX_POOL'].values[0]))
    with c3:
        st.metric(label='**Median Size of the Pool**', value=str(pools['MEDIAN_POOL'].values[0]))


    c1,c2 = st.columns([1,1])
    with c1:
        stakes = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/7e8e8862-c09d-441b-b135-42a985b284b9/data/latest')
        fig = px.pie(stakes, values='TX_COUNT', names='ACTION', title='Total Number of Stakes/Unstakes')
        fig.update_layout(showlegend = False)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        stakes = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/7e8e8862-c09d-441b-b135-42a985b284b9/data/latest')
        fig = px.pie(stakes, values='VOLUME', names='ACTION', title='Statking/Unstaking Volume')
        fig.update_layout(showlegend = False)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    stakes_over_time = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/44b84544-01f0-4489-8c34-18578a28f838/data/latest')
    fig = px.bar(stakes_over_time, x='DATE', y='TX_COUNT', color='ACTION', title='Number of Stakes/Unstakes on Weekly basis')
    fig.update_layout(showlegend=False, xaxis_title='WEEK', yaxis_title='Stakes/Unstakes')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    fig = px.bar(stakes_over_time, x='DATE', y='VOLUME', color='ACTION', title='Staking/Unstaking Volume on Weekly basis')
    fig.update_layout(showlegend=False, xaxis_title='WEEK', yaxis_title='Staking Volume')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    validators_over_time = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/ff352b3d-ec72-4735-a563-7182990901a6/data/latest')
    fig = px.line(validators_over_time, x="DATE", y="VALIDATOR", title="Number of Validators over Time")
    fig.update_layout(xaxis_title='WEEK', yaxis_title='Number of Validators')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)







    
