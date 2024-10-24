
import requests
import json
import streamlit as st
import math
import os
from main import add_logout_button  # Import the logout function

def show_page_name():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("Please log in to access this page.")
        st.stop()

if __name__ == "__main__":
    show_page_name()

# --- Page Config ---
st.set_page_config(
    page_title="FindLawyer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.logo("logo/sidebar_logo.png", icon_image="logo/only_logo.png")

# --- Header ---
st.title(" 👨🏻‍🎓 Find the Nearest Lawyer")
st.markdown('####')

def print_praise():
        praise_quotes = """
        Team Sahi Jawab

    2nd Year Students,
    B.Tech(Hons) CSE
    GLA UNIVERSITY
        """
        title = "**Developed By -**\n\n"
        return title + praise_quotes

# Sidebar
with st.sidebar.container():
    st.image('logo/Sahi Jawab.png', use_column_width=True, caption='Sahi Jawab : Your Nyaya Mitra 👩🏻‍⚖️📚𓍝')

# Features in an expander
    with st.expander("🚀 Features", expanded=False):
        st.markdown("- Search Nearby Lawyers by State and City")



# API call to fetch cities in India
url = "https://country-state-city-search-rest-api.p.rapidapi.com/cities-by-countrycode"
querystring = {"countrycode": "IN"}

headers = {
    "x-rapidapi-key": "ddbda4b603mshfa1bc12a01f0f30p1331d9jsn88ac65275cd5",
    "x-rapidapi-host": "country-state-city-search-rest-api.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

# Check if request was successful
if response.status_code == 200:
    cities_data = response.json()
    
    # Structure the data properly
    formatted_data = []
    for city in cities_data:
        city_info = {
            "name": city.get('name'),
            "countryCode": city.get('countryCode'),
            "stateCode": city.get('stateCode'),
            "latitude": city.get('latitude'),
            "longitude": city.get('longitude')
        }
        formatted_data.append(city_info)
    
    # Save formatted data to a JSON file
    with open('cities.json', 'w') as f:
        json.dump(formatted_data, f, indent=4)
    
    print("Data saved successfully to cities.json")
else:
    print(f"Failed to fetch data: {response.status_code}")

st.markdown("""
    <style>
    .title {
        text-align: left;
        font-size: 35px;
        font-weight: bold;
        color: black;
    }
    .lawyer-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
        border-left: 5px solid #3498db;
        cursor: pointer;
    }
    .lawyer-card:hover {
        transform: translateY(-5px);
        box-shadow: 10px 16px 18px rgba(0, 0, 0, 0.15);
        background-color: #FFFDD0; /* Optional: Change background on hover */
    }
    .lawyer-name {
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 10px;
        color: #2c3e50;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .lawyer-address {
        font-size: 14px;
        color: #7f8c8d;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
    }
    .slider-label {
        font-size: 30px;
        font-weight: bold;
    }
    .find-lawyers-button {
        background-color: #3498db; /* Blue background */
        color: white; /* White text */
        font-size: 16px; /* Font size */
        padding: 10px 20px; /* Padding */
        border: none; /* Remove default border */
        border-radius: 5px; /* Rounded corners */
        cursor: pointer; /* Pointer cursor on hover */
        transition: background-color 0.3s; /* Smooth transition */
        display: block; /* Make it block level */
        text-align: center; /* Center the text */
    }

    .find-lawyers-button:hover {
        background-color: #2980b9; /* Darker blue on hover */
    }
    
    .custom-selectbox {
        border: 2px solid #4A90E2; /* Change this color to your preference */
        border-radius: 5px;
        padding: 5px; /* Add some padding for better appearance */
        background-color: white; /* Set background color */
    }
    
    </style>
    
    <script>
    function openOlaMaps(latitude, longitude) {
        var url = `https://maps.olamaps.com/?lat=${latitude}&lng=${longitude}&zoom=15`;
        window.open(url, '_blank');
    }
    </script>
    """, unsafe_allow_html=True)

# Mapping of state codes to full state names
state_code_mapping = {
    "AP": "Andhra Pradesh",
    "AR": "Arunachal Pradesh",
    "AS": "Assam",
    "BR": "Bihar",
    "CT": "Chhattisgarh",
    "GA": "Goa",
    "GJ": "Gujarat",
    "HR": "Haryana",
    "HP": "Himachal Pradesh",
    "JK": "Jammu and Kashmir",
    "JH": "Jharkhand",
    "KA": "Karnataka",
    "KL": "Kerala",
    "MP": "Madhya Pradesh",
    "MH": "Maharashtra",
    "MN": "Manipur",
    "ML": "Meghalaya",
    "MZ": "Mizoram",
    "NL": "Nagaland",
    "OR": "Odisha",
    "PB": "Punjab",
    "RJ": "Rajasthan",
    "SK": "Sikkim",
    "TN": "Tamil Nadu",
    "TG": "Telangana",
    "TR": "Tripura",
    "UP": "Uttar Pradesh",
    "UT": "Uttarakhand",
    "WB": "West Bengal",
    "AN": "Andaman and Nicobar Islands",
    "CH": "Chandigarh",
    "DH": "Dadra and Nagar Haveli and Daman and Diu",
    "DL": "Delhi",
    "LD": "Lakshadweep",
    "PY": "Puducherry",
    "LA": "Ladakh"
}


# Load the city data from the JSON file
with open('cities.json', 'r') as f:
    city_data = json.load(f)

# Create a set of unique state codes from the data and map to full state names
states = sorted({state_code_mapping.get(city['stateCode'], city['stateCode']) for city in city_data})

# Streamlit UI for state selection
st.sidebar.write("---")
st.sidebar.markdown('<div class="title">Lawyer Fetcher</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

# State selection in the first column
with col1:
    selected_state = st.selectbox("", ["Select a state"] + states, index=0, key="state_select")

# City selection in the second column
with col2:
    if selected_state and selected_state != "Select a state":
        # Reverse map full state name back to state code
        selected_state_code = next((code for code, name in state_code_mapping.items() if name == selected_state), None)
        filtered_cities = [city['name'] for city in city_data if city['stateCode'] == selected_state_code]
        selected_city = st.selectbox("", ["Select a city"] + filtered_cities, index=0, key="city_select")
    else:
        selected_city = st.selectbox("", ["Select a city"], disabled=True, key="city_select_disabled") 

if selected_city and selected_city != "Select a city":
    city_info = next((city for city in city_data if city['name'] == selected_city), None)

    if city_info:
        # Pass latitude and longitude to Ola Maps API
        latitude = city_info['latitude']
        longitude = city_info['longitude']

        # Display the label with the custom style
        st.markdown('<div class="slider-label">Select search radius (in meters)</div>', unsafe_allow_html=True)
        
        # Slider component
        radius_meters = st.slider('', 10000, 200000, 60000)

        # Convert meters to km for display
        radius_km = radius_meters / 1000

        st.write(f"Searching within a radius of {radius_km:.2f} km")
        

        # Button to trigger lawyer search
        if st.button('Find Lawyers', use_container_width=True):
            # OLA Krutrim API endpoint
            api_key = os.getenv('OLA_API_KEY')
            
            # Constructing the API URL with the correct parameters
            api_url = "https://api.olamaps.io/places/v1/nearbysearch"
            
            params = {
                "layers": "venue",
                "types": "lawyer",
                "location": f"{latitude},{longitude}",
                "radius": radius_meters,
                "api_key": api_key,
                "limit": 50  # Maximum allowed value
            }

            # Making the request to the API
            try:
                response = requests.get(api_url, params=params)
                
                # Check if the response is successful
                if response.status_code == 200:
                    data = response.json()

                    if 'predictions' in data and data['predictions']:
                        st.subheader(f"Lawyers found within {radius_km:.2f} km:")
                        st.markdown("---")

                        num_lawyers = len(data['predictions'])
                        num_rows = math.ceil(num_lawyers / 4)

                        for row in range(num_rows):
                            cols = st.columns(3) 
                            for col in range(3):
                                lawyer_index = row * 3 + col
                                if lawyer_index < num_lawyers:
                                    lawyer = data['predictions'][lawyer_index]
                                    with cols[col]:
                                        # Construct the Google search URL
                                        search_query = f"{lawyer['structured_formatting']['main_text']} {selected_city}"
                                        google_search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                                        # Use an anchor tag to create a clickable card
                                        st.markdown(f"""
                                        <a href="{google_search_url}" target="_blank" style="text-decoration: none;">
                                            <div class="lawyer-card"> 
                                                <div class="lawyer-name">{lawyer['structured_formatting']['main_text']}</div>
                                                <div class="lawyer-address">{lawyer['structured_formatting']['secondary_text']}</div>
                                            </div>
                                        </a>
                                        """, unsafe_allow_html=True)
                        st.markdown("---")
                    else:
                        st.write(f"No lawyers found within {radius_km:.2f} km.")
                else:
                    st.write(f"Error: Unable to fetch data (Status Code: {response.status_code})")
                    st.write(f"Response content: {response.text}")
            except requests.exceptions.RequestException as e:
                st.write(f"An error occurred while making the request: {str(e)}")
            except json.JSONDecodeError:
                st.write("Error: Unable to parse the API response as JSON.")
            except Exception as e:
                st.write(f"An unexpected error occurred: {str(e)}") 
with st.sidebar:
    st.write("---")
    st.success(print_praise())
    st.write("---")
    
    add_logout_button()
    st.write("---")

    st.markdown(
                "<h3 style='text-align: center;'>Developed with ❤️ for GenAI by <a style='text-decoration: none' href='https://www.linkedin.com/in/keshavagrawal595/'>Team Sahi Jawab</a></h3>",
                unsafe_allow_html=True
            )

    st.markdown('''
        <center>
        <h1>Visitors Count : <img src="https://counter8.optistats.ovh/private/freecounterstat.php?c=b2j4e593kabemp2m8eww4c4m63e339lu" title="Free Counter" Alt="web counter" width="100" height="40"  border="0" /></h1>
        </center>
    ''', unsafe_allow_html=True)