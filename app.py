import csv
import pprint

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

from apikey import *

# The api is free
mykey = apikey


def get_ships():
    # price = st.slider("select ship price",max_value=None,value=60)

    url3 = f"https://api.starcitizen-api.com/{mykey}/v1/live/ships?page_max=1?crew_max=1?"  # price_max={price}"
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url3, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data['data'] is None:
            st.error("Error: Unable to retrieve data. waiting on starcitizen-api.com for fix")
            return
        pprint.pprint(data)

        df = pd.DataFrame(data['data'])
        df.to_csv()

        # fig = px.bar(df, x='name', y='afterburner_speed')
        fig = px.bar(df, x='name', y='max_crew', color='focus', labels={'name': 'Name', 'max_cre': 'Max Crew'})
        fig1 = px.scatter(df, x='afterburner_speed', y='cargocapacity', color='name')

        df.drop('compiled', inplace=True, axis=1)
        df.drop('manufacturer', inplace=True, axis=1)
        df.drop('zaxis_acceleration', inplace=True, axis=1)
        df.drop('yaxis_acceleration', inplace=True, axis=1)
        df.drop('yaw_max', inplace=True, axis=1)
        df.drop('xaxis_acceleration', inplace=True, axis=1)
        df.drop('url', inplace=True, axis=1)
        df.drop('time_modified_unfiltered', inplace=True, axis=1)
        df.drop('time_modified', inplace=True, axis=1)
        df.drop('roll_max', inplace=True, axis=1)
        df.drop('production_note', inplace=True, axis=1)
        df.drop('manufacturer_id', inplace=True, axis=1)
        df.drop('id', inplace=True, axis=1)
        df.drop('chassis_id', inplace=True, axis=1)
        df.drop('beam', inplace=True, axis=1)
        df.drop('media', inplace=True, axis=1)
        df.set_index("name", inplace=True)

        data_display = st.radio("Choose a graph or table", ('Bar Graph', 'Scatter Plot', 'Table'))

        if data_display == 'Bar Graph':
            st.plotly_chart(fig)

        if data_display == 'Scatter Plot':
            st.plotly_chart(fig1)

        if data_display == 'Table':
            st.dataframe(df)

    else:
        # Request was not successful
        st.warning(f"Request failed with status code {response.status_code}")
        print(f"Request failed with status code {response.status_code}")


def get_mychar():
    users = st.sidebar.selectbox("Pick a Member to see their Information",
                                 options=["SurlyGent", "Sentifer", "Gollejo"])

    st.sidebar.write(
        "Join Sentifer, SurlyGent, and Gollejo - a passionate group of experienced Star Citizen pilots - "
        "in exploring the galaxy and helping new players discover the wonders of this incredible game.  "
        "Whether you're a beginner or an experienced player, we're here to help you learn the basics, "
        "team up for thrilling missions, and make new friends in the galaxy. "
        "Join us now and let's conquer the universe together!")
    print(users)
    url1 = f"https://api.starcitizen-api.com/{mykey}/v1/live/user/{users}"
    headers = {
        "Accept": "application/json"
    }
    print(url1)
    response = requests.get(url1, headers=headers)

    col1, col2 = st.columns(2)
    with col1:

        if response.status_code == 200:
            # Request was successful
            data = response.json()
            if data['data'] is None:
                st.error(f"Response was {response.status_code} "
                         f"\n\nError: Data is empty, waiting on starcitizen-api.com for fix")

                return
            print(data)
            st.header(data['data']['profile']['display'])
            st.image(data['data']['profile']['image'])
            if 'name' in data['data']['organization']:
                st.subheader(data['data']['organization']['name'])
                st.write(data['data']['organization']['rank'])

            st.write(data['data']['profile']['badge'])
            st.image(data['data']['profile']['badge_image'])

            parser = csv.reader(data['data']['profile']['fluency'])

            for fields in parser:
                for i, f in enumerate(fields):
                    print(i, f)
                    st.write(f)

        else:
            # Request was not successful
            st.warning(f"Request failed with status code {response.status_code}")
            print(f"Request failed with status code {response.status_code}")

    with col2:
        st.header("Main Ship")
        if users == "SurlyGent":
            image_url = "https://media.starcitizen.tools/9/90/Corsair_flying_above_clouds.png"
            st.image(image_url, use_column_width="auto", caption="Drake Corsair")
            st.write("The Drake Corsair is a tough, industrial-style exploration ship that boasts a spacious "
                     "interior and large cargo hold. Its exposed wires and pipes give it a rugged look, and it "
                     "lacks the sleek elegance of other ships. It's slow and difficult to steer but packs a punch, "
                     "accommodating up to four crew members in its functional living quarters. The Corsair is "
                     "equipped with scanning suites and quantum fuel tanks, making it a reliable option for "
                     "exploring even the harshest environments.")

        if users == "Sentifer":
            image_url = "https://media.starcitizen.tools/a/a4/Drake_Cutter_-_Flying_through_Area_18_-_ISC_2022-11-18" \
                        ".jpg"
            st.image(image_url, use_column_width="auto", caption="Drake Cutter")
            st.write("The Drake Cutter is a small but versatile single-seat starter ship perfect for fledgling "
                     "pilots. Its flexible frame is ideal for various roles, including FPS missions such as "
                     "clearing bunkers and caves. The Cutter's compact size enables easy landings near "
                     "objectives, making it ideal for gathering loot. The ship's cargo hold can carry light "
                     "freight, and the living quarters are adequate for longer missions. "
                     "The Cutter is armed with guns and missiles, providing ample defense.")

        if users == "Gollejo":
            image_url = "https://media.starcitizen.tools/5/59/Nomad_Flying_Concept.jpg"
            st.image(image_url, use_column_width="auto", caption="Consolidated Outlands Nomad")
            st.write("Description: The Nomad, created by Consolidated Outlands, "
                     "is a versatile and innovative freighter that combines multiple features in a compact and "
                     "sleek design. With its spacious cargo bay, advanced hover technology, and cozy habitation "
                     "area, the Nomad is a prime example of self-reliance and ingenuity. The cargo bay's open "
                     "design gives the ship a distinctive truck-like appearance, adding to its versatility and "
                     "practicality.")

    st.subheader("Introduction:")
    if users == "SurlyGent":
        st.write("Greetings, fellow space enthusiasts! "
                 "I'm SurlyGent, "
                 "a seasoned Star Citizen player with a wealth of experience in cargo-trading, mining, salvaging, "
                 "FPS combat missions, and box delivery missions. "
                 "If you're new to the game, you've come to the right place. "
                 "I'm here to help you navigate the vastness of space, "
                 "learn the ins and outs of the game's mechanics, and have a blast while doing it. "
                 "Whether you're looking to explore new worlds, rack up credits, or engage in thrilling dogfights, "
                 "there's always something new to discover in this incredible universe. "
                 "So, let's gear up, blast off, and make some memories among the stars")
    if users == "Sentifer":
        st.write("Heya fellow space explorers! "
                 "I'm Sentifer, a spunky Star Citizen pilot who loves nothing more than FPS cave missions, combat, "
                 "and mining for valuable resources. If you're new to this amazing universe, "
                 "don't worry - I'm here to help you navigate the galaxy "
                 "and make the most of your adventures among the stars! "
                 "Whether you want to take on dastardly villains in intense combat missions or "
                 "fill up your trusty backpack with sparkling minerals, "
                 "there's always something new and exciting to discover in this vast and wondrous universe. "
                 "The thrill of filling my backpack to the brim with precious resources during a mining expedition is "
                 "unbeatable, but I also love the challenge of taking out the bad guys on the way into a cave mission. "
                 "So, let's don our space suits and get ready for some out-of-this-world adventures - together, "
                 "we'll conquer the galaxy and come out on top!")
    if users == "Gollejo":
        st.write("Im a bum that never plays!")

    contact_us = st.button('Contact us')
    if contact_us:
        st.write(data['data']['profile']['page']['url'], "\n\n Please Enter your email address.")

        email = st.text_input("Email Address", placeholder="sample@domain.com")

        if email != "":
            st.success(f"Thank you {email}.  \n\n Expect a reply soon")


def get_species():
    url2 = f"https://api.starcitizen-api.com/{mykey}/v1/live/starmap/species"
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url2, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['data'] is None:
            st.error("Error: Unable to retrieve data. waiting on starcitizen-api.com for fix")
            return

        df = pd.DataFrame(data['data'])
        df.to_csv('species_data.csv', index=False)
        print(data)
        st.dataframe(df)
    else:
        # Request was not successful
        st.warning(f"Request failed with status code {response.status_code}")
        print(f"Request failed with status code {response.status_code}")


def get_stats():
    url3 = f"https://api.starcitizen-api.com/{mykey}/v1/live/stats"
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url3, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['data'] is None:
            st.error("Error: Unable to retrieve data. waiting on starcitizen-api.com for fix")
            return
        df = pd.DataFrame(data['data'], index=[0])
        df.to_csv('stats.csv', index=True)
        df.drop('current_etf', inplace=True, axis=1)
        df.drop('fleet', inplace=True, axis=1)

        df.rename(columns={"current_live": "Live Build Number",
                           "current_ptu": "Test Build Number",
                           "fans": "Players",
                           "funds": "Funds Raised"}, inplace=True)
        st.write(df)

    else:
        # Request was not successful
        st.warning(f"Request failed with status code {response.status_code}")
        print(f"Request failed with status code {response.status_code}")


def add_style():
    st.markdown(
        f""" <style> .stApp {{ background-image: url(
        "https://robertsspaceindustries.com/media/d6r27wy3vettyr/wallpaper_1920x1080/Source.jpg"); 
        background-attachment: fixed; background-size: cover; background-color: #f0f0f0; color: black;
           
            
            
        }}
        .stTabs [data-baseweb="tab-highlight"] {{
        background-color:transparent;
        }}
        .stCheckbox {{
        background-color:lightblue;
        }}
        .stRadio {{
        background-color:lightblue;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def main():
    add_style()

    st.markdown("# :blue[Star Citizen Helpers]")
    st.markdown("## :blue[Tiza Space Group]")

    my_char, game_info = st.tabs([
        "Members",
        "Game Information"
    ])
    with my_char:  # Include 3 characters
        get_mychar()

    with game_info:  # Include species, stats, ships
        st.header("")
        st.markdown("### :blue[General Game Information]")
        species = st.checkbox("Species of The Galaxy")
        if species:
            get_species()
        stats = st.checkbox("Game Version, Players and Funding")
        if stats:
            get_stats()
        ships = st.checkbox("Some of the current available ships")
        if ships:
            get_ships()
        data = {'lat': [53.47893720412131, 30.3096728399394, 34.03097237099766],
                'lon': [-2.2558235729373206, -97.9393061157291, -118.45570880597623]}
        df = pd.DataFrame(data)
        st.subheader("")
        st.markdown("### :blue[Cloud Imperium Office locations]")
        st.map(df)


if __name__ == '__main__':
    main()
