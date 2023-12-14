# import packages
import numpy as np
import pandas as pd
import streamlit as st
import pydeck as pdk
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static

st.set_page_config(layout="wide")
def home_page():
    st.title('Boston Blue Bike')
    st.header("Welcome to the Blue Bike Data Home page!")
    st.subheader("Use the navigation menu to view data in different forms and provide us with some user input")
    st.image("https://facilities.northeastern.edu/wp-content/uploads/2021/12/Bluebikes-Pic-4-1860x970.jpg",
             caption="BlueBikes", use_column_width=True)

# create a navigation
from streamlit_option_menu import option_menu
selected = option_menu(
    menu_title=None,
    options=["Home", "Raw data", "line Graph", "Pie Chart", "Scatterplot", "Table", "Maps"],
    icons=["house", "book", "table graph","table graph", "table graph", "table graph", "map"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"background-color": "lightblue"},
        "icon": {"color": "Navy"},
        "nav-link": {
        "font-size": "20px",
        "text-align": "center",
        "--hover-color": "lightgrey",
        },
        "nav-link-selected": {"background-color": "lightpink"}
    },

)

# new page - raw data and queries
# load raw data (alphabetical)
def sorted_data():
    raw_data = "202305-bluebikes-tripdata.csv"
    data = 'currrent_bikes.csv'
    user = '202305-bluebikes-tripdata 2.0.csv'
    duration = '202301-bluebikes-tripdata 2.csv'
    df = pd.read_csv(raw_data)
    df_data = pd.read_csv(data)
    df_user = pd.read_csv(user)
    df_duration = pd.read_csv(duration)
    st.write(df)

# query 1
    values = st.select_slider(
        'How often do you use a bluebike?',
     options=['never', 'rarely', 'sometimes', 'often'])
    st.write('I use a bluebike', values)
    # chart 1
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    sns.countplot(x='user type', data=df_user)
    plt.xlabel('User Type')
    plt.ylabel('User Count')
    plt.title('Distribution of User Types')
    st.pyplot(fig1)

# Query 2
    option = st.selectbox(
        'Which pick up district is your favorite?',
        ('Boston', 'Brookline', 'Watertown', 'Somerville', 'Cambridge', 'Everett', 'Newton', 'Chelsea', 'Salem', 'Arlington', 'Medford', 'Malden', 'Revere'))
    st.write('You selected:', option)
    # chart 2
    district_counts = df_data['District'].value_counts().reset_index()
    district_counts.columns = ['District', 'Count']

    # highlight selected
    highlight_color = 'lightpink'
    district_counts['Color'] = district_counts['District'].apply(lambda x: highlight_color if x == option else '')

    fig2 = px.pie(district_counts, names='District', values='Count', color='Color', title=f'Distribution of Favorite Pickup Districts{option}')
    st.plotly_chart(fig2)

# query 3
    time = st.radio(
        "Is your ride time typically 10 or more minutes",
        ["Yes", "No"], key='ride_time_radio', horizontal=True
    )
    if time == "Yes":
        # Query 4
        value = st.select_slider(
            'How long is your typical ride?',
            options=['10-15 minutes', '15-20 minutes', '20-30 minutes', '>30 minutes'],
            key='typical_ride_duration_slider'
        )
        st.write("Your typical ride time is:", value)
    else:
        st.write("Your typical ride is 10 or less minutes", time)

    # Chart 3
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    sns.countplot(x='tripduration', data=df_duration, palette='viridis')  # You can choose a different color palette
    plt.xlabel('Typical Ride Time')
    plt.ylabel('Number of Rides')
    plt.title('Distribution of Typical Ride Times')
    plt.xticks(rotation=45, ha="right", fontsize=8)  # Rotate x-axis labels for better readability
    st.pyplot(fig3)

    comments = st.text_input('Provide suggestions to make your Blue Bikes experience better:')
    if comments:
        st.write(comments)

# new page - line graphs
def dock_deployment():
    st.title('Line graph')
    st.subheader('This line graph displays the deployment year of bike docks in different districts')

    df = pd.read_csv("currrent_bikes.csv")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x="District", y="Deployment Year", data=df, ax=ax)
    plt.xticks(rotation='vertical')
    st.pyplot(fig)


#new page - Pie Chart
def location_docks():
    st.title('Pie chart depicting locations with highest number of docks')
    data = {
    'District': ['Boston', 'Brookline', 'Watertown', 'Somerville', 'Cambridge', 'Everett', 'Newton', 'Chelsea', 'Salem', 'Arlington', 'Medford', 'Malden', 'Revere'],
    'Docks': [4511, 200, 113, 592, 1668, 196, 194, 67, 204, 66, 66, 33, 44]
}
    df_pie = pd.DataFrame(data)
    fig_pie = px.pie(df_pie, values='Docks', names='District', title='Number of bike docks within a district')
    st.plotly_chart(fig_pie)


# new page - scatterplots
def total_docks():
    st.title('Scatter Plot')
    st.write('Total docks in the boston locations')
    df = pd.read_csv("boston_data.csv")

    x_axis_val = 'Total docks'
    y_axis_val = 'Name'

    fig = px.scatter(df, x=x_axis_val, y=y_axis_val, labels={'Total Docks': 'Total Docks', 'Name': 'Location Name'})
    st.plotly_chart(fig)




# new page - tables
def most_popular():
    st.title("The most popular Blue Bike Stations")
    file_path = "most popular stations.csv"
    df_table = pd.read_csv(file_path)
    st.table(df_table)

# new page - maps
def marker_color(row):
    if row['District'] == 'Boston':
        return 'darkgreen'
    elif row['District'] == 'Cambridge':
        return 'red'
    elif row['District'] == 'Brookline':
        return 'cadetblue'
    elif row['District'] == 'Watertown':
        return 'orange'
    elif row['District'] == 'Somerville':
        return 'purple'
    elif row['District'] == 'Everett':
        return 'gray'
    elif row['District'] == 'Newton':
        return 'pink'
    elif row['District'] == 'Chelsea':
        return 'darkpurple'
    elif row['District'] == 'Salem':
        return 'green'
    elif row['District'] == 'Arlington':
        return 'black'
    elif row['District'] == 'Medford':
        return 'white'
    elif row['District'] == 'Malden':
        return 'beige'
    elif row['District'] == 'Revere':
        return 'lightblue'
    else:
        return
def bike_locations():
    st.title("Blue Bike Locations")
    file_path = "currrent_bikes.csv"
    df = pd.read_csv(file_path)
    df['Color'] = df.apply(marker_color, axis=1)

# map-key
    st.markdown("""
    <style>
    .map-key {
    display: flex;
    flex-direction: row;
    margin-top: 20px;
    }
    .map-key-item {
    display: flex;
    align-items: center;
    margin-bottom: 5px;
    }
    .color-box {
    width: 20px;
    height: 20px;
    margin-right: 10px;
    border: 1px solid #000;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='map-key'>", unsafe_allow_html=True)

    for district, color in zip(df['District'].unique(), df['Color'].unique()):
        st.markdown(f"<div class='map-key-item'><div class='color-box' style='background-color:{color};'></div>{district}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# search
    search_query = st.text_input("Search by District Name:")
    search_button = st.button("Search")

    if search_button:
        filtered_df = df[df['Name'].str.contains(search_query, case=False)]
    else:
        filtered_df = df

# map markers
    my_map = folium.Map(location=[42.36, -71.05], zoom_start=11)

    for index, row in df.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=row['Name'],
            icon=folium.Icon(color=row['Color'])).add_to(my_map)

    folium_static(my_map)


# new pages
def home():
    pass
def raw_data():
    sorted_data()
def line_graphs():
    dock_deployment()
def pie_chart():
    location_docks()
def scatter_plot():
    total_docks()
def tables():
    most_popular()
def maps():
    bike_locations()


if selected == 'Home':
    home_page()
elif selected == 'Raw data':
    raw_data()
elif selected == 'line Graph':
    line_graphs()
elif selected == 'Pie Chart':
    pie_chart()
elif selected == 'Scatterplot':
    scatter_plot()
elif selected == 'Table':
    tables()
elif selected == 'Maps':
    maps()



