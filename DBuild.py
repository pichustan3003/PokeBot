import os
import sqlite3
import json
conn = sqlite3.connect('pokemon.db')
c = conn.cursor()
c.execute("""DROP TABLE IF EXISTS pokemon""")
c.execute("""CREATE TABLE IF NOT EXISTS pokemon (ID int, Species TEXT(50), Type1 TEXT(8), Type2 TEXT(8), Ability1 TEXT(50), Ability2 TEXT(50), AbilityHidden TEXT(50),HP int, attack int, defense int, specialAttack int, specialDefense int, speed int)""")

class Pokemon:
    def __init__(self, id : int, species : str, types : list, stats : dict, abilities : dict):
        self.id = id
        self.species = species
        self.type1 = types[0]
        self.type2 = types[1] if len(types) > 1 else None
        self.abil1 = abilities["1"] if "1" in abilities else None
        self.abil2 = abilities["2"] if "2" in abilities else None
        self.abilHid = abilities["3"] if "3" in abilities else None
        self.hp = stats['hp']
        self.attack = stats['attack']
        self.defense = stats['defense']
        self.speed = stats['speed']
        self.specialAttack = stats['special-attack']
        self.specialDefense = stats['special-defense']

    def writeToDB(self):
        c.execute("""INSERT INTO pokemon 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            self.id,
            self.species,
            self.type1,
            self.type2,
            self.abil1,
            self.abil2,
            self.abilHid,
            self.hp,
            self.attack,
            self.defense,
            self.specialAttack,
            self.specialDefense,
            self.speed,
        ))

def monBuilder(relativePath : str):
    with open(relativePath, "r") as f:
        full = json.load(f)
    types = [type["type"]["name"] for type in full["types"]]
    baseStats = {}
    abilitys = {}
    for ability in full["abilities"]:
        abilitys[str(ability["slot"])] = ability["ability"]["name"]
    for stat in full["stats"]:
        baseStats[stat["stat"]["name"]] = stat["base_stat"]
    print(abilitys)
    curMon = Pokemon(full["id"], full["name"], types, baseStats, abilitys)
    curMon.writeToDB()

basePath = r"D:\Python D\PokeBot\pokeapi"
for file in os.listdir(basePath+"\\pokemon\\"):
    monBuilder(basePath+"\\pokemon\\"+file)

conn.commit()
c.close()
conn.close()