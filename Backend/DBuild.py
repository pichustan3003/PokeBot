import os
import sqlite3
import json
conn = sqlite3.connect('pokemon.db')
c = conn.cursor()
def build_pokemon():
    c.execute("""DROP TABLE IF EXISTS pokemon""")
    c.execute("""CREATE TABLE IF NOT EXISTS pokemon (ID INTEGER PRIMARY KEY, Species TEXT(50), Type1 TEXT(8), Type2 TEXT(
    8), Ability1 TEXT(50), Ability2 TEXT(50), AbilityHidden TEXT(50),HP INTEGER, attack INTEGER, defense INTEGER, 
    specialAttack INTEGER, specialDefense INTEGER, speed INTEGER, BST INTEGER, EVHP INTEGER, EVattack INTEGER, 
    EVdefense INTEGER, EVspecialAttack INTEGER, EVspecialDefense INTEGER, EVspeed INTEGER)""")


    class Pokemon:
        def __init__(self, id : int, species : str, types : list, stats : dict, abilities : dict, evs : dict):
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
            self.bst = sum(stats.values())
            self.evhp = evs['hp']
            self.evattack = evs['attack']
            self.evdefense = evs['defense']
            self.evspeed = evs['speed']
            self.evspecialAttack = evs['special-attack']
            self.evspecialDefense = evs['special-defense']

        def writeToDB(self):
            c.execute("""INSERT INTO pokemon 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
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
                self.bst,
                self.evhp,
                self.evattack,
                self.evdefense,
                self.evspecialAttack,
                self.evspecialDefense,
                self.evspeed,
            ))

    def monBuilder(relativePath : str):
        with open(relativePath, "r") as f:
            full = json.load(f)
        types = [type["type"]["name"] for type in full["types"]]
        baseStats = {}
        abilitys = {}
        evs = {}
        for ability in full["abilities"]:
            abilitys[str(ability["slot"])] = ability["ability"]["name"]
        for stat in full["stats"]:
            baseStats[stat["stat"]["name"]] = stat["base_stat"]
            evs[stat["stat"]["name"]] = stat["effort"]
        curMon = Pokemon(full["id"], full["name"], types, baseStats, abilitys, evs)
        curMon.writeToDB()

    basePath = r"D:\Python D\PokeBot\pokeapi"
    for file in os.listdir(basePath+"\\pokemon\\"):
        monBuilder(basePath+"\\pokemon\\"+file)

def build_pokemon_species():

    c.execute("""DROP TABLE IF EXISTS pokemon_species""")
    c.execute("""CREATE TABLE pokemon_species (ID INTEGER PRIMARY KEY, Species TEXT(50), isBaby BOOLEAN, isLeg BOOLEAN, isMyth BOOLEAN)""")

    class pokemon_species:
        def __init__(self, id, name, isBaby, isLeg, isMyth):
            self.id = id
            self.name = name
            self.baby = isBaby
            self.leg = isLeg
            self.myth = isMyth

        def writeToDB(self):
            c.execute("""INSERT INTO pokemon_species VALUES (?, ?, ?, ?, ?)""", (self.id,self.name,self.baby,self.leg,self.myth))

    def mon_species(relativePath : str):
        with open(relativePath, "r") as f:
            full = json.load(f)
        mon = pokemon_species(full["id"], full["name"], full["is_baby"], full["is_legendary"], full["is_mythical"])
        mon.writeToDB()

    basePath = r"D:\Python D\PokeBot\pokeapi"
    for file in os.listdir(basePath + "\\pokemon-species\\"):
        mon_species(basePath + "\\pokemon-species\\" + file)
build_pokemon_species()
conn.commit()
c.close()
conn.close()