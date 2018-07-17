import csv
import copy

chart = []

with open('KB/chart.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        chart.append(row)


def init(rival=None):
        pokedex = []
        db_attacks = []
        if rival is None:
                rivalPokemon = []
        else:
                rivalPokemon = rival
    
        with open('KB/pokedex.csv') as f:
                reader = csv.reader(f)
                for row in reader:
                        pokedex.append(row)
        with open('KB/moves.csv') as f:
                reader = csv.reader(f)
                for row in reader:
                        db_attacks.append(row)
        team = open('team.txt', 'r')
        misPokemon = getTeam(team, 3, pokedex, db_attacks)
        team.close()
        pool = open('pool.txt', 'r')
        pokePool = getTeam(pool, -1, pokedex, db_attacks)
        pool.close()
        jugadores = User(misPokemon, rivalPokemon)
        return [pokedex, db_attacks, jugadores, pokePool]


class Attack:
    def __init__(self, attid, name, atype, category, pp, power, accuracy, max_pp, priority, target, effect,
                 side_effect_prob):
        self.attid = attid
        self.name = name
        self.atype = atype
        self.category = category
        self.pp = pp
        self.power = power
        self.accuracy = accuracy
        self.max_pp = max_pp
        self.priority = priority
        self.target = target
        self.effect = effect
        self.side_effect_prob = side_effect_prob

    def make_attack(self):
        self.pp -= 1


class Pokemon:
    def __init__(self, pkid, name, type1, type2, hp, attack, defense, sp_attack, sp_defense, speed,
                 hard_status, volatile_status, boosts):
        self.pkid = pkid
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sp_attack = sp_attack
        self.sp_defense = sp_defense
        self.speed = speed
        self.list_attacks = []
        self.hard_status = hard_status
        self.volatile_status = volatile_status
        self.boosts = boosts

    def learn_attack(self, new_attack):
                name = new_attack.name
                exist = False
                for attack in self.list_attacks:
                        if attack.name == name:
                                print(self.name + ' ya sabe ' + name + '!')
                                exist = True
                if not exist:
                        if len(self.list_attacks) >= 4:
                                self.list_attacks.pop()
                        self.list_attacks.append(new_attack)

    def receive_damage(self, damage_points):
        if self.hp <= damage_points:
            self.hp = 0
        else:
            self.hp = self.hp - damage_points


class User:
    def __init__(self, list_pokemon, list_rival):
        self.list_pokemon = list_pokemon
        self.list_rival = list_rival


def busca_efectividad(a1, a2):
    if not a1 or not a2:
        print("Aviso: Tipo no valido")
        return 0
    x = -1
    y = -1
    for i in range(len(chart[0])):
        if chart[i][0] == a1:
            x = i
        if chart[0][i] == a2:
            y = i
    if x == -1 or y == -1:
        print("Aviso: No se encontro alguno de los tipos")
        return 0
    else:
        return chart[x][y]


def vence(x, y):
    l1 = []
    l2 = []
    multiplicador = 1
    if type(x) is Pokemon:
        l1.append(x.type1)
        if x.type2:
            l1.append(x.type2)
    else:
        l1.append(x)
    if type(y) is Pokemon:
        l2.append(y.type1)
        if y.type2:
            l2.append(y.type2)
    else:
        l2.append(y)
    for i in range(len(l1)):
        efectividad = 1
        for j in range(len(l2)):
            efectividad *= float(busca_efectividad(l1[i], l2[j]))
        multiplicador = max(multiplicador, efectividad)
    if multiplicador > 1:
        return True
    else:
        return False


def masRapido(x, y):
    if x.speed > y.speed:
        return True
    else:
        return False


def cubreA(x, y):
    lista = copy.copy(x.list_attacks)
    for i in lista:
        if vence(i.atype, y):
            return True
    return False


def aFisico(x):
        if len(x.list_attacks) == 0:
                if int(x.attack) >= int(x.sp_attack):
                        return True
                else:
                        return False
        for attack in x.list_attacks:
                if attack.category == 'physical':
                        return True
        return False


def aEspecial(x):
        if len(x.list_attacks) == 0:
                if int(x.sp_attack) >= int(x.attack):
                        return True
                else:
                        return False
        for attack in x.list_attacks:
                if attack.category == 'special':
                        return True
        return False


def dFisico(x):
    if int(x.defense) >= int(x.sp_defense):
        return True
    else:
                if int(x.defense) + 10 >= int(x.sp_defense):
                        return True
                return False


def dEspecial(x):
    if int(x.sp_defense) >= int(x.defense):
        return True
    else:
                if int(x.sp_defense) + 10 >= int(x.defense):
                        return True
                return False


def muroFisico(x):
        if int(x.defense) > 100:
                return True
        else:
                return False


def muroEspecial(x):
        if int(x.sp_defense) > 100:
                return True
        else:
                return False


def sweeperFisico(x):
        if int(x.attack) > 100:
                return True
        else:
                return False


def sweeperEspecial(x):
        if int(x.sp_attack) > 100:
                return True
        else:
                return False


def fragilFisico(x):
        if int(x.defense) < 60:
                return True
        else:
                return False


def fragilEspecial(x):
        if int(x.sp_defense) < 60:
                return True
        else:
                return False


def resiste(x, y):
    efectividad = [1, 1]
    l1 = []
    l2 = []
    if type(x) is Pokemon:
        l1.append(x.type1)
        if x.type2:
            l1.append(x.type2)
    else:
        l1.append(x)
    if type(y) is Pokemon:
        l2.append(y.type1)
        if y.type2:
            l2.append(y.type2)
    else:
        l2.append(y)
    for i in range(len(l2)):
        for j in range(len(l1)):
            efectividad[i] *= float(busca_efectividad(l2[i], l1[j]))
    if float(efectividad[0]) < 1:
                if len(l2) == 2:
                        if float(efectividad[1]) < 1:
                                return True
                else:
                        return True
    else:
        return False


def counter(x, y):
    lista = []
    for i in x.list_attacks:
        if vence(i.atype, y):
            lista.append(i)
    return lista


def get_this_pokemon(name, pokedex):
    for i in range(len(pokedex)):
        if pokedex[i][1].lower() == name:
            return get_pokemon(i, pokedex)
    print("No se encontro el pokemon " + name)
    return get_pokemon(130, pokedex)


def get_this_attack(name, db_attacks):
    if len(name.split("hidden power")) > 1:
        name = "hidden power"
    for j in range(len(db_attacks)):
        if db_attacks[j][1].replace("-", " ") == name:
            return get_attack(j, db_attacks)
    print("No se encontro el ataque " + name)
    return get_attack(1, db_attacks)


def getTeam(team, chosen, pokedex, db_attacks):
        if chosen < 0:
                counter = 999
        pkmn = []
        lines = team.readlines()
        pk1 = lines[0]
        name = pk1.strip().split('@')[0].lower()
        if name.strip()[-4:] == " (m)" or name.strip()[-4:] == " (f)":
            pkmn.append(name.strip()[:-4])
        else:
            pkmn.append(name.strip())
        counter = chosen
        indices = []
        for line in range(len(lines)):
            if lines[line].strip() == '':
                indices.append(line)
                counter -= 1
                if counter == 0:
                    break
                try:
                    pk = lines[line+1]
                except:
                    if chosen > 0:
                            print('No hay suficientes pokemon en el archivo')
                            print('Regresando ' + str(len(indices)) + ' de ' + str(len(indices)) + ' disponibles')
                    break
                name = pk.strip().split('@')[0].lower()
                if name.strip()[-4:] == " (m)" or name.strip()[-4:] == " (f)":
                    pkmn.append(name.strip()[:-4])
                else:
                    pkmn.append(name.strip())
                                          
        pokemonList = []
        for nombre in pkmn:
            pokemonList.append(get_this_pokemon(nombre, pokedex))
        
        pokemon = 0
        for indice in indices:                
                ataques = []
                for i in range(indice-4, indice):
                        string = lines[i].strip()[2:].lower()
                        ataques.append(string.replace("-", " "))
                for nombre in ataques:
                    pokemonList[pokemon].learn_attack(get_this_attack(nombre.replace("'",""), db_attacks))
                pokemon += 1

        return pokemonList


def get_pokemon(poke_id, pokedex):
    pkid = pokedex[poke_id][0]
    name = pokedex[poke_id][1].lower()
    types = pokedex[poke_id][2].split(" ")
    type1 = types[0].lower()
    try:
        type2 = types[1].lower()
    except IndexError:
        type2 = ""
    hp = int(pokedex[poke_id][3])
    attack = int(pokedex[poke_id][4])
    defense = int(pokedex[poke_id][5])
    spattack = int(pokedex[poke_id][6])
    spdefense = int(pokedex[poke_id][7])
    speed = int(pokedex[poke_id][8])
    hard_status = "healthy"
    volatile_status = []
    boosts = [1,1,1,1,1,1,1] #Atk, Def, SpAtk, SpDef, Spe, Acc, Eva

    p = Pokemon(pkid, name, type1, type2, hp, attack, defense, spattack, spdefense, speed,
                hard_status, volatile_status, boosts)
    return p


def get_attack(attack_id, db_attacks):

    typeCode = []
    with open('KB/types.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            typeCode.append(row)

    categoryCode = []
    with open('KB/categories.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            categoryCode.append(row)

    effectCode = []
    with open('KB/move_effect_prose.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            effectCode.append(row)

    targetCode = []
    with open('KB/move_targets.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            targetCode.append(row)

    attid = int(db_attacks[attack_id][0])
    name = db_attacks[attack_id][1].replace("-", " ")
    atype = db_attacks[attack_id][2]
    for row in typeCode:
        if row[0] == atype:
            atype = row[1]
            break
    cat = db_attacks[attack_id][3]
    for row in categoryCode:
        if row[0] == cat:
            cat = row[1]
            break
    pp = int(db_attacks[attack_id][4])  # max pp is assumed
    power = db_attacks[attack_id][5]
    if power == "":
        power = 0
    else:
        power = int(power)
    acc = db_attacks[attack_id][6]
    if acc == "":
        acc = 100.0
    else:
        acc = float(acc)/100.0
    mpp = int(db_attacks[attack_id][4]) * 8/5
    priority = int(db_attacks[attack_id][7])
    target = db_attacks[attack_id][8]
    for row in targetCode:
        if row[0] == target:
            target = row[1]
            break
    effect = db_attacks[attack_id][9]
    for row in effectCode:
        try:
            if row[0] == effect:
                effect = row[1]
                break
        except IndexError:
            effect = ""
    side_effect_prob = db_attacks[attack_id][10]
    if side_effect_prob == "":
        side_effect_prob = 0.0
    else:
        side_effect_prob = float(side_effect_prob)/100

    a = Attack(attid, name, atype, cat, pp, power, acc, mpp, priority, target, effect,
                 side_effect_prob)
    return a


def myPokemon(name, players):
        for pokemon in players.list_pokemon:
                if name == pokemon.name:
                        return pokemon
        print('No tienes ese pokemon!')
        return pokemon


def foePokemon(name, players):
        for pokemon in players.list_rival:
                if name == pokemon.name:
                        return pokemon
        print('No tiene ese pokemon!')
        return pokemon


def appendPokemon(name, playerList, pokedex):
        flag = True
        for pokemon in playerList:
                if name == pokemon.name:
                        flag = False
        if flag:
                try:
                        newPokemon = get_this_pokemon(name, pokedex)
                        playerList.append(newPokemon)
                except:
                        print('El pokemon a agregar es desconocido')
