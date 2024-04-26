import pandas as pd
import pymongo
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
from pymongo.server_api import ServerApi

icon=Image.open("airbnb.png")
st.set_page_config(page_title= "Airbnb Data Visualization",
                   page_icon= icon,
                   layout= "wide"
                   #initial_sidebar_state= "expanded",
                    #menu_items={'About': """Data has been gathered from mongodb atlas"""}
                  )
selected = option_menu("Menu", ["Home","Overview","Explore"],
                    icons=["house","graph-up-arrow","bar-chart-line"],
                    menu_icon= "menu-button-wide",
                    default_index=0,
                    orientation="horizontal")
uri = "mongodb+srv://yusuff511:Yusuff12345@cluster0.9na32fw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client=pymongo.MongoClient(uri,server_api=ServerApi('1'))
db=client['sample_airbnb']
col=db['listingsAndReviews']

df = pd.read_csv('Airbnb1.csv')

if selected=="Home":
    st.write("# :blue[Domain] : Travel Industry, Property Management and Tourism")
    st.write("# :blue[Technologies used] : Python, Pandas, Plotly, Streamlit, MongoDB")
    st.write("# :blue[Overview] : To analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends. ")

if selected=="Overview":
    tab1,tab2=st.tabs(["Data","Insights"])
    with tab1:
        option=st.radio("Select anyone of the below option to show",["Raw Data","Dataframe"],index=1)
        if option=="Dataframe":
            st.write(df)
        if option=="Raw Data":
            st.write(col.find_one())
    with tab2:
        col1,col2=st.columns(2)
        with col1:
            country=st.multiselect("Select a country",df.Country.unique())
        with col2:
            prop=st.multiselect("Select a Property Type",df.Property_type.unique())
        with col1:
            room=st.multiselect("Select Room Type",df.Room_type.unique())
        with col2:
            price=st.slider("Drag to select the required price range",df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()),step=float(100))
            st.markdown("# ")
        query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'

        col3,col4=st.columns(2,gap="large")
        tab1,tab2,tab3,tab4=st.tabs(['Property types','Hosts','Room Type','Country map'])
        with tab1:
            st.title("Top 10 Property types")
            df1=df.query(query).groupby(["Property_type"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False).sort_index()[:10]
            fig=px.bar(df1,x="Property_type",y="Listings",title="Top 10 Property Types",color='Property_type',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig)
            st.write(":blue[Top 10 Property types Dataframe]")
            st.write(df1)
        with tab2:
            st.title("Top 10 Hosts")
            df2=df.query(query).groupby(["Host_name"]).size().reset_index(name="Listings").sort_values(by="Listings",ascending=False)[:10]
            fig2=px.bar(df2,x="Host_name",y="Listings",title="Top 10 Hosts",color='Host_name',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig2,use_container_width=True)
            st.write(":blue[Top 10 Hosts Dataframe]")
            st.write(df2)
        with tab3:
            st.title("Top 10 listings in each Room type")
            df3=df.query(query).groupby(['Room_type']).size().reset_index(name="Counts")
            fig3=px.pie(df3,names='Room_type',values="Counts",color="Room_type",color_discrete_sequence=px.colors.sequential.Peach)
            st.plotly_chart(fig3)
            st.write(df3)
        with tab4:
            st.title(":blue[Top listings in each country]")
            country_df=df.query(query).groupby(['Country'],as_index=False)['Name'].count().rename(columns={"Name":"Total listings"})
            fig4=px.choropleth(country_df,title="Top listings in each country",locations="Country",locationmode="country names",color="Total listings",
                               color_continuous_scale=px.colors.sequential.Plasma)
            st.plotly_chart(fig4,use_container_width=True)
            st.write(country_df)
if selected=="Explore":
    st.title(":blue[Even more plots about airbnb data]")
    col1,col2=st.columns(2)
    with col1:
        country=st.multiselect("Select a country",df.Country.unique(),df.Country.unique())
    with col2:
        prop=st.multiselect("Select a Property Type",df.Property_type.unique(),df.Property_type.unique())
    with col1:
        room=st.multiselect("Select Room Type",df.Room_type.unique(),df.Room_type.unique())
    with col2:
        price=st.slider("Drag to select the required price range",df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()),step=float(100))
        st.markdown("# ")
    query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'
    
    tab1,tab2=st.tabs(['Price analysis','Scatter geo'])
    with tab1:
        st.markdown("# Price analysis")
        price_df=df.query(query).groupby(["Room_type"],as_index=False)['Price'].mean().sort_values(by="Price")
        fig5 = px.bar(data_frame=price_df,
                x='Room_type',
                y='Price',
                color='Price',
                title='Average Price in each Room type'
            )
        st.plotly_chart(fig5,use_container_width=True)
        st.write(price_df)
        st.markdown("# Availablity")
        fig6 = px.box(data_frame=df.query(query),
                     x='Room_type',
                     y='Availability_365',
                     color='Room_type',
                     title='Availability by Room_type'
                    )
        st.plotly_chart(fig6,use_container_width=True)
    with tab2:
        st.markdown("# Scatter GEO")
        country_df = df.query(query).groupby('Country',as_index=False)['Price'].mean()
        fig7 = px.scatter_geo(data_frame=country_df,
                            locations='Country',
                            color= 'Price', 
                            hover_data=['Price'],
                            locationmode='country names',
                            size='Price',
                            title= 'Avg Price in each Country',
                            color_continuous_scale=px.colors.qualitative.Dark24)
        st.plotly_chart(fig7,use_container_width=True)
        country_df = df.query(query).groupby('Country',as_index=False)['Availability_365'].mean()
        country_df.Availability_365 = country_df.Availability_365.astype(int)
        fig8 = px.scatter_geo(data_frame=country_df,
                                       locations='Country',
                                       color= 'Availability_365', 
                                       hover_data=['Availability_365'],
                                       locationmode='country names',
                                       size='Availability_365',
                                       title= 'Avg Availability in each Country',
                                       color_continuous_scale=px.colors.qualitative.Dark24
                            )
        st.plotly_chart(fig8,use_container_width=False,theme="streamlit")