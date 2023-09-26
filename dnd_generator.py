import pandas as pd
import random

file = pd.read_csv("./dnd_monsters.csv")
cc_file = pd.read_csv("./countries_continents.csv")

size_dict = {"Tiny":0.5,
    "Small":1,
    "Medium":2,
    "Large":3,
    "Huge":4,
    "Gargantuan":5
    }

# file.iloc[random.randint(0, 200)]['hp']

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