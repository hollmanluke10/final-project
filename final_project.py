"""
Name: Luke Hollman
CS230: Section 1
Data: "Postsecondary_School_Locations_-_Current.csv"
URL:In Process

Description:

This program shows the user the amount of Colleges and Universities that exist in each state in the U.S. in a bar graph.
The user then has the option of selecting a state that they want to view the colleges in via a sidebar select box.
The state that is selected is displayed on the first map, with each of the colleges having their own label with their names.
The use then has the option of selecting a specific school that they would like to view within the previously determined state
also via a side bar select box.
The college that was selected comes up on the second map, also having its own label with it's name.
"""
import streamlit as st
import pandas as pd
import pydeck as pdk

def bar_chart(states_list):
    data = pd.read_csv("Postsecondary_School_Locations_-_Current.csv")
    data_cleanup = data[data.STATE.isin(states_list.keys())]

    countByState = data_cleanup.groupby('STATE')['FID'].count()
    print(countByState)

    st.title('Schools by State:')

    st.bar_chart(countByState)

def map_1and2(data,states_list):
    option = st.sidebar.selectbox("Which state do you want to see Universities/Colleges in for Map #1", list(states_list.keys()))
    state_data = data[data['STATE'] == option]

    st.title(f"Universities and Colleges in {option}")
    st.write(state_data[['NAME', 'STREET', 'CITY', 'STATE']])

    schools = state_data[['X', 'Y', 'NAME']]

    schools.columns = ["lon", "lat", 'University']

    st.write(f"Map #1: Map of Universities and Colleges in {option}")
    view_state = pdk.ViewState(
        latitude=schools['lat'].mean(),
        longitude=schools["lon"].mean(),
        zoom = 10,
        pitch = 0.5)

    layer1 = pdk.Layer('ScatterplotLayer', data=schools, get_position='[lon, lat]', get_radius = 500, get_color=[0,255,255,],
                   pickable=True)

    tool_tip = {"html": "University Name:<br/> <b>{University}</b> ",
                "style": {"backgroundColor": "black", "color": "white"}}

    map_schools = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9', initial_view_state=view_state, layers=[layer1], tooltip=tool_tip)
    st.pydeck_chart(map_schools)
    map_2(option, state_data, data)

def map_2(option, state_data,data):
    option2 = st.sidebar.selectbox(f"Pick a school in {option} for Map #2", list(state_data['NAME']))
    single_school = data[data['NAME'] == option2]
    specific_school = single_school[['X', 'Y', 'NAME']]
    specific_school.columns = ['lon', 'lat', 'University']

    st.write(f"Map #2 Map of {option2}")
    view_state = pdk.ViewState(
        latitude=specific_school['lat'].mean(),
        longitude=specific_school["lon"].mean(),
        zoom = 10,
        pitch = 0.5)

    layer1 = pdk.Layer('ScatterplotLayer', data=specific_school, get_position='[lon, lat]', get_radius = 500, get_color=[255,0,125],
                   pickable=True)

    tool_tip = {"html": "University Name:<br/> <b>{University}</b> ",
            "style": {"backgroundColor": "blue", "color": "white"}}

    map_schools2 = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9', initial_view_state=view_state, layers=[layer1], tooltip=tool_tip)

    st.pydeck_chart(map_schools2)

def main():

    states_list = {'AL': 'Alabama',
    'AK': 'Alaska',
    'AR': 'Arkansas',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Deleware',
    'DC': 'District of Columbia',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI' : 'Hawaii',
    'ID' : 'Idaho',
    'IL' : 'Illinois',
    'IN' : 'Indiana',
    'IA' : 'Iowa',
    'KS' : 'Kansas',
    'KY' : 'Kentucky',
    'LA' : 'Louisiana',
    'ME' : 'Maine',
    'MD' : 'Maryland',
    'MA' : 'Massachusetts',
    'MI' : 'Michigan',
    'MN' : 'Minnesota',
    'MS' : 'Mississippi',
    'MO' : 'Missouri',
    'MT' : 'Montana',
    'NE' : 'Nebraska',
    'NV' : 'Nevada',
    'NH' : 'New Hampshire',
    'NJ' : 'New Jersey',
    'NM' : 'New Mexico',
    'NC' : 'North Carolina',
    'ND' : 'North Dakota',
    'OH' : 'Ohio',
    'OK' : 'Oklahoma',
    'OR' : 'Oregon',
    'PA' : 'Pennsylvania',
    'PR' : 'Puerto Rico',
    'RI' : 'Rhode Island',
    'SC' : 'South Carolina',
    'SD' : 'South Dakota',
    'TN' : 'Tennessee',
    'TX' : 'Texas',
    'UT' : 'Utah',
    'VT' : 'Vermont',
    'VA' : 'Virginia',
    'VI' : 'Virgin Islands',
    'WA' : 'Washington',
    'WV' : 'West Virginia',
    'WI' : 'Wisconsin',
    'WY' : 'Wyoming'}


    st.title("Universities/Colleges in the United States")
    data = pd.read_csv("Postsecondary_School_Locations_-_Current.csv")
    bar_chart(states_list)
    map_1and2(data, states_list)


main()

