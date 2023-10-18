# Starter Pseudocode for Objective One: Hero Generator Creation and Writing to 'hero-damage'


# Use this group.id in your Kafka Conf in order to receive ALL the monster data and not have it split across mulitple users. Use the same input each time and you will retain the offset from the stream.
user_input = input("Enter your unique name or identifier: ")
group_id = "consumer-" + user_input

# Dictionaries to define hero specialties and continent modifiers.
HERO_SPECIALTIES = {
    "Wizard": "INT",
    "Rogue": "DEX",
    "Necromancer": "CON",
    "Druid": "WIS",
    "Paladin": "CHA",
    "Fighter": "STR"
}

CONTINENT_MODIFIERS = {
    "Americas": "STR",
    "Europe": "DEX",
    "Africa": "CON",
    "Asia": "INT",
    "Australasia": "WIS",
    "Antarctica": "CHA"
}

#! You are not allowed to change the followning function. It is the Hero Damage logic. No cheat codes, no God-mode. This is the damage logic, no tinkering!

def calculate_hero_damage(hero, monster_health, continent_modifier):
    
    # Base damage of hero is a percentage of monster's health
    # e.g., 10% of monster's health
    damage = 0.1 * monster_health
    
    # Hero's specialty based on class
    hero_modifier = HERO_SPECIALTIES[hero['class']]
    
    # Check if hero's specialty matches the continent's modifier (monster's weakness)
    if hero_modifier == continent_modifier:
        # Increase damage for matching specialty
        damage *= random.uniform(0.7, 3)  # 70% to 300% of base damage (so up to 30% of monster's health)
    else:
        # Reduce damage if no match
        damage *= random.uniform(0.3, 0.6)  # 30% to 60% of base damage
    
    return damage

# You will need to use this function in your program.

### NO TINKERING WITH THE FUNCTION! ###

# OBJECTIVE ONE STEPS:

# 1. Connect to Kafka Consumer for the 'monster-damage' topic.
#    - Define Kafka Consumer configurations.
#    - Subscribe to 'monster-damage' topic.

# 2. For each incoming message (monster) from Kafka:
#    - Parse the message to extract monster details (e.g., monster type, location, damage).
#    - Determine which hero class is best suited to counter the monster based on its location (continent).
#    - Optionally: Calculate the chance for a critical hit for the chosen hero.

# 3. Send the chosen hero details (e.g., hero class, damage) to Kafka 'hero-damage' topic.
#    - Serialize hero details into a suitable format (e.g., JSON).
#    - Publish the serialized message to 'hero-damage' topic using Kafka Producer.

# 4. (Optional) Display the chosen hero and the monster it's combating in a user-friendly manner (e.g., console output, GUI).

# TODO: Implement Kafka Consumer and Producer functionality.
# TODO: Implement hero selection logic based on incoming monster details.
# TODO: Implement optional critical hit calculation for hero.
# TODO: Implement data serialization for sending hero details to Kafka.

if __name__ == "__main__":
    # TODO: Write the main execution code.
    pass
