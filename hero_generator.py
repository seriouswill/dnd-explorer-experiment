from confluent_kafka import Consumer, KafkaError
import json
import random

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

def select_hero_specialty():
    """Prompt the user to select a hero specialty."""
    print("Choose a Hero's specialty to counter the upcoming monster attacks:")
    for idx, specialty in enumerate(HERO_SPECIALTIES.keys(), 1):
        print(f"{idx}. {specialty}")
    
    choice = int(input("\nEnter your choice (1-6): "))
    chosen_hero = list(HERO_SPECIALTIES.keys())[choice - 1]
    print(f"You have chosen the {chosen_hero}!")
    return chosen_hero

def combat_monster(monster_data, chosen_hero):
    """Determine the effectiveness of the chosen hero against the monster."""
    continent_modifier = CONTINENT_MODIFIERS.get(monster_data["continent"], "INT")
    hero_modifier = HERO_SPECIALTIES[chosen_hero]
    
    if continent_modifier == hero_modifier:
        # The chosen hero's specialty matches the continent's modifier.
        # This results in a high reduction in monster's damage.
        reduction_percentage = random.uniform(0.7, 1)
    else:
        # Partial reduction in damage if the hero's specialty doesn't perfectly match.
        reduction_percentage = random.uniform(0.3, 0.6)
    
    reduced_damage = monster_data["damage"] * reduction_percentage
    print(f"The {chosen_hero} countered the {monster_data['monster_name']} in {monster_data['country']} and reduced its damage from {monster_data['damage']} to {int(reduced_damage)}!\n")
    return reduced_damage

def main():
    chosen_hero = select_hero_specialty()

    # Configuration for Kafka Consumer
    conf = {
        'bootstrap.servers': 'b-1.monstercluster1.6xql65.c3.kafka.eu-west-2.amazonaws.com:9092',  # Replace with your broker URLs
        'group.id': 'hero-group',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(conf)

    consumer.subscribe(['monster-damage'])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f"Reached end of partition {msg.partition()}.")
                else:
                    print(f"Error while consuming message: {msg.error()}")
            else:
                monster_data = json.loads(msg.value().decode('utf-8'))
                combat_monster(monster_data, chosen_hero)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
