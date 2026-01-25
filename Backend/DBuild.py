import os
import sqlite3
import json
conn = sqlite3.connect('pokemon.db')
c = conn.cursor()
basePath = r"D:\Python D\PokeBot\Pokeapi"


def romanNums2Int(romanNum):
    return {"generation-i": 1, "generation-ii": 2, "generation-iii": 3, "generation-iv": 4, "generation-v": 5,
            "generation-vi": 6, "generation-vii": 7, "generation-viii": 8, "generation-ix": 9}[romanNum]


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


    for file in os.listdir(basePath+"\\pokemon\\"):
        monBuilder(basePath+"\\pokemon\\"+file)

def build_pokemon_species():

    c.execute("""DROP TABLE IF EXISTS pokemon_species""")
    c.execute("""CREATE TABLE pokemon_species (ID INTEGER PRIMARY KEY, Species TEXT(50), isBaby BOOLEAN, isLeg BOOLEAN, isMyth BOOLEAN, generation INTEGER, growthRate TEXT(20), genderRate FLOAT)""")

    class pokemon_species:
        def __init__(self, id, name, isBaby, isLeg, isMyth, genstring, growth, genrate):
            self.id = id
            self.name = name
            self.baby = isBaby
            self.leg = isLeg
            self.myth = isMyth
            self.generation = romanNums2Int(genstring)
            self.growth = growth
            self.genderrate = genrate*12.5
        def writeToDB(self):
            c.execute(f"""INSERT INTO pokemon_species VALUES ({", ".join(["?"] * len(vars(self).values()))})""", tuple(vars(self).values()))

    def mon_species(relativePath : str):
        with open(relativePath, "r") as f:
            full = json.load(f)
        mon = pokemon_species(full["id"], full["name"], full["is_baby"], full["is_legendary"], full["is_mythical"], full["generation"]["name"], full["growth_rate"]["name"], full["gender_rate"])
        mon.writeToDB()
        return mon

    for file in os.listdir(basePath + "\\pokemon-species\\"):
        mon = mon_species(basePath + "\\pokemon-species\\" + file)

def build_move():
    c.execute("""DROP TABLE IF EXISTS move""")
    class move:
        def __init__(self, initial, attribs):

            for attrib in attribs:
                setattr(self, attrib, attribs[attrib])

            if initial:
                dbcmd = buildTBfromClass(self)
                print(dbcmd)
                c.execute(dbcmd)
        def writeToDB(self):
            print(vars(self))
            c.execute(f"""INSERT INTO move VALUES ({", ".join(["?"] * len(vars(self).values()))})""",
                tuple(vars(self).values()))

    def movebuilder(relativePath : str, initial):
        with open(relativePath, "r") as f:
            full = json.load(f)
        attribs = {
            "id":full["id"],
            "name":full["name"],
            "accuracy":full["accuracy"],
            "power":full["power"],
            "pp":full["pp"],
            "priority":full["priority"],
            "type":full["type"]["name"],
            "effect_chance":full["effect_chance"],
            "crit_rate":full["meta"]["crit_rate"] if full["meta"] is not None else None,
            "drain":full["meta"]["drain"] if full["meta"] is not None else None,
            "generation":romanNums2Int(full["generation"]["name"]),
        }
        move(initial, attribs).writeToDB()
    initi = True
    for file in os.listdir(basePath + "\\move\\"):
        movebuilder(basePath + "\\move\\" + file, initi)
        initi = False
def buildTBfromClass(object):
    title = type(object).__name__
    outstr = "CREATE TABLE IF NOT EXISTS "+title+" ("
    varibles = vars(object)
    for var in varibles:
        match type(varibles[var]).__name__:
            case "int":
                outstr += " "+var+" INTEGER,"
            case "float":
                outstr += " "+var+" FLOAT,"
            case "bool":
                outstr += " "+var+" BOOLEAN,"
            case "str":
                outstr += " "+var+" TEXT(50),"
            case "NoneType":
                outstr += " "+var+" TEXT(50),"
    outstr = outstr[:-1]
    outstr += ")"
    return outstr
build_move()
conn.commit()
c.close()
conn.close()