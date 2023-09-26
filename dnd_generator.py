# regular libraries
import pandas as pd
import random
import time
import json
import datetime
from threading import Thread

# geo libraries and certificate ssl stuff
import certifi
import ssl
import geopy.geocoders
from geopy.geocoders import Nominatim

file = pd.read_csv("./dnd_monsters.csv")
cc_file = pd.read_csv("./countries_continents.csv")

size_dict = {"Tiny":0.5,
    "Small":1,
    "Medium":2,
    "Large":3,
    "Huge":4,
    "Gargantuan":5
    }

# sort out missing values for dex con int etc
file = file.fillna(random.randint(0, 5))

# make a new column for size multiplier
file['size_multiplier'] = file['size'].map(size_dict)

# D20 dice roll
D20 = random.randint(0, 20)

# get population and continent info ( i combined two csvs )
pop_file = pd.read_csv("./population_by_country_2020.csv")

pop_file = pop_file[
    ['Country (or dependency)', 'Population (2020)']
]

# join on country
merged_df = pd.merge(cc_file, pop_file, left_on='Country', right_on='Country (or dependency)')

# rename column
merged_df['Population'] = merged_df['Population (2020)']
merged_df.pop('Population (2020)')

####

# Establish geopy locator and function


ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx
geolocator = Nominatim(user_agent="my_geocoder")

def get_continent(geolocator=geolocator):

    land = False
    while land != True:
        lat = random.randint(-90, 90)
        long = random.randint(-180, 180)

        location = geolocator.reverse((lat, long), language='en')
        try:
            country = location.raw['address']['country']
            land = True
            # print(f"Country: {country}")

            continent_row = cc_file.loc[cc_file['Country']==country]

            continent = continent_row['Continent'].to_list()[0]
            # print(f"Continent: {continent}")
        except:
            print("Monster drowned in the briny depths of the ocean.")
            land = False

    return country, continent


###

# Group continents into 6 categories, Americas (N & S), Europe, Africa, Asia, Australasia & Antarctica.

# They align with STR, DEX, CON, INT, WIS, CHA respectively.

# Flat formula - Size(S1, M2, L3) X d20 roll X continent mulitplier = Damage.

mod = ["str", "dex", "con", "int", "wis", "cha"]
continent_dict = {cc_file['Continent'].unique()[i]: mod[i] for i in range(len(mod))}

# create monster damage based on continent

def create_monster_damage(continent, file=file, continent_dict=continent_dict):
    rand_monster = file.sample()
    monster_name = rand_monster['name'].iloc[0]

    damage = 1000 * D20 * rand_monster['size_multiplier'] * rand_monster[continent_dict[continent]]

    damage = int(damage.iloc[0])

    return monster_name, damage


###

# Emulate a continuous stream of monsters being generated.



def execute_loop(iterations):
    for i in range(iterations):
        # time delay
        time.sleep(1)
        
        # unpack country info
        country, continent = get_continent()
        # country, continent = "Canada", "North America"

        # unpack monster info
        monster_name, damage = create_monster_damage(continent)


        # Update the main DF in order to keep track of running casualties in countries.
        index_loc = merged_df.loc[merged_df['Country']==country].index[0]

        # population info
        population = int(merged_df['Population'].at[index_loc])
        original_population = int(pop_file['Population (2020)'].loc[pop_file['Country (or dependency)']==country])


        # display results
        # print(f"Country: {country}, \nPopulation: {population}, \nMonster: {monster_name.upper()}, \nDamage: {damage} \nUpdated Population: {population - damage}, \nPercent Population Lost: {percent_loss}\n\n---\n")

        # \|/ BELOW IS THE CORRECT WAY TO AMEND VALUES IN A DATAFRAME \|/

        # need to catch minus population numbers 
        if population - damage < 0:
            updated_population = 0
            merged_df.loc[index_loc, 'Population'] = 0
        else:
            updated_population = population - damage
            merged_df.loc[index_loc, 'Population'] -= damage

        
        # calculate percentage population loss !!! CATCH percentages greater than 100
        percent_loss = round((original_population - updated_population) / population * 100, 3)
        if percent_loss > 100:
            percent_loss = 100

        # structure data for stream
        data = {
            "country": country,
            "population": population,
            "monster_name": monster_name.upper(),
            "damage": damage,
            "updated_population": int(updated_population),
            "percent_loss": percent_loss,
            "ts": str(datetime.datetime.now())
        }
        # jsonify
        json_string = json.dumps(data)
        print(json_string)
        # print(f"--- {percent_loss} ---")
    
execute_loop(100)