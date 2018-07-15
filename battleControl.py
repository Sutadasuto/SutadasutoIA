import pokemon as poke


def decideAction(myPokemon, foePokemon, player):

    if poke.vence(foePokemon, myPokemon) and \
            not (poke.masRapido(myPokemon, foePokemon) and poke.cubreA(myPokemon, foePokemon)):
        print(foePokemon.name + ' vence a ' + myPokemon.name + ' porque '
              + foePokemon.name + ' es tipo ' + foePokemon.type1 + '/' + foePokemon.type2)
        print('Ademas ' + myPokemon.name + ' no es mas rapido que y/o no cubre a '
              + foePokemon.name + '. No hay otra que cambiar')
        candidate = cambio(myPokemon, foePokemon, player)
        if candidate is not 0:
            mon = player.list_pokemon[-1*candidate-1]
            if not deboCambiar(mon, foePokemon):
                return candidate
            else:
                print('Pero nuestra mejor opcion es ' + mon.name + ', que tambien estaria obligado a cambiar :(')
        else:
            print('Pero ya no tenemos mas pokemon :(')

    if poke.muroFisico(foePokemon) and poke.muroEspecial(foePokemon):
        if not (poke.sweeperFisico(myPokemon) or poke.sweeperEspecial(myPokemon)):
            print(foePokemon.name + ' es un muro Mixto. ' + myPokemon.name + ' no es tan fuerte como para derribarlo')
            print('No hay otra que cambiar')
            candidate = cambio(myPokemon, foePokemon, player)
            if candidate is not 0:
                    mon = player.list_pokemon[-1*candidate-1]
                    if not deboCambiar(mon, foePokemon):
                        return candidate
                    else:
                        print('Pero nuestra mejor opcion es ' + mon.name + ', que tambien estaria obligado a cambiar :(')
            else:
                print('Pero ya no tenemos mas pokemon :(')
        else:
            if not poke.vence(myPokemon, foePokemon):
                print(foePokemon.name + ' es un muro Mixto y aunque ' + myPokemon.name +
                      'es un sweeper, no puede atacarlo de forma super efectiva')
                print('No hay otra que cambiar')
                candidate = cambio(myPokemon, foePokemon, player)
                if candidate is not 0:
                        mon = player.list_pokemon[-1*candidate-1]
                        if not deboCambiar(mon, foePokemon):
                            return candidate
                        else:
                            print('Pero nuestra mejor opcion es ' + mon.name +
                                  ', que tambien estaria obligado a cambiar :(')
                else:
                    print('Pero ya no tenemos mas pokemon :(')
    else:
        if poke.muroFisico(foePokemon):
            if not (poke.vence(myPokemon, foePokemon) and poke.sweeperFisico(myPokemon)):
                if poke.vence(foePokemon, myPokemon) or poke.resiste(foePokemon, myPokemon):
                    print(foePokemon.name + ' es un muro Fisico. ' + myPokemon.name +
                          ' no es tan fuerte como para derribarlo, y tiene problemas contra el tipo '
                          + foePokemon.type1 + '/' + foePokemon.type2)
                    print('No hay otra que cambiar')
                    candidate = cambio(myPokemon, foePokemon, player)
                    if candidate is not 0:
                        mon = player.list_pokemon[-1*candidate-1]
                        if not deboCambiar(mon, foePokemon):
                            return candidate
                        else:
                            print('Pero nuestra mejor opcion es ' + mon.name +
                                  ', que tambien estaria obligado a cambiar :(')
                    else:
                        print('Pero ya no tenemos mas pokemon :(')

        if poke.muroEspecial(foePokemon):
            if not (poke.vence(myPokemon, foePokemon) and poke.sweeperEspecial(myPokemon)):
                if poke.vence(foePokemon, myPokemon) or poke.resiste(foePokemon, myPokemon):
                    print(foePokemon.name + ' es un muro Especial. ' + myPokemon.name +
                          ' no es tan fuerte como para derribarlo, y tiene problemas contra el tipo '
                          + foePokemon.type1 + '/' + foePokemon.type2)
                    print('No hay otra que cambiar')
                    candidate = cambio(myPokemon, foePokemon, player)
                    if candidate is not 0:
                        mon = player.list_pokemon[-1*candidate-1]
                        if not deboCambiar(mon, foePokemon):
                            return candidate
                        else:
                            print('Pero nuestra mejor opcion es ' + mon.name +
                                  ', que tambien estaria obligado a cambiar :(')
                    else:
                        print('Pero ya no tenemos mas pokemon :(')

    if poke.vence(myPokemon, foePokemon):
        candidates = []
        for i in myPokemon.list_attacks:
            if (i.atype == myPokemon.type1 and poke.vence(i.atype, foePokemon)) or \
                    (i.atype == myPokemon.type2 and poke.vence(i.atype, foePokemon)):
                if i.pp > 0 & poke.vence(i.atype, foePokemon):
                    candidates.append(i)
        foeHP = float(foePokemon.hp)
        beneficio = 0
        for candidate in candidates:
            if foeHP > 25:
                if float(candidate.power) * float(candidate.accuracy) > beneficio:
                    beneficio = float(candidate.power) * float(candidate.accuracy)
                    i = candidate
            else:
                if float(candidate.accuracy) > beneficio:
                    beneficio = float(candidate.accuracy)
                    i = candidate
        if len(candidates) > 0:
            print(myPokemon.name + ' vence a ' + foePokemon.name + ' porque ' + myPokemon.name + ' es tipo ' + i.atype)
            print('Ademas ' + i.name + ' es un ataque tipo ' + i.atype)
            return myPokemon.list_attacks.index(i)+1

    if poke.cubreA(myPokemon, foePokemon):
        lista = []
        for i in myPokemon.list_attacks:
            if poke.vence(i.atype, foePokemon):
                lista.append(i)
        foeHP = float(foePokemon.hp)
        beneficio = 0
        if foeHP > 25:
            for i in lista:
                if float(i.power) * float(i.accuracy) > beneficio and float(i.pp > 0):
                    beneficio = float(i.power) * float(i.accuracy)
                    ataque = i
            try:
                print('El ataque ' + ataque.name + ' es tipo ' + ataque.atype +
                      ', que es fuerte contra un pokemon tipo '
                      + foePokemon.type1 + '/' + foePokemon.type2 + ' como ' + foePokemon.name)
                print('Ademas, como tiene mucha vida, queremos vencerlo de un solo golpe ' +
                      'con un ataque poderoso aunque no tenga mucha precision')
                return myPokemon.list_attacks.index(ataque)+1
            except:
                null = 0
        else:
            for i in lista:
                if float(i.accuracy) > float(beneficio) and float(i.pp > 0):
                    beneficio = float(i.accuracy)
                    ataque = i
            try:
                print('El ataque ' + ataque.name + ' es tipo ' + ataque.atype +
                      ', que es fuerte contra un pokemon tipo '
                      + foePokemon.type1 + '/' + foePokemon.type2 + ' como ' + foePokemon.name)
                print('Ademas, como tiene poca vida, no queremos arriesgarnos ' +
                      'con un ataque fuerte pero de poca precision')
                return myPokemon.list_attacks.index(ataque)+1
            except:
                null = 0

    if not poke.resiste(foePokemon, myPokemon):
            candidates = []
            for i in myPokemon.list_attacks:
                if i.atype == myPokemon.type1 or i.atype == myPokemon.type2:
                    if i.pp > 0 and not poke.resiste(foePokemon, i.atype):
                        candidates.append(i)
            foeHP = float(foePokemon.hp)
            beneficio = 0
            for candidate in candidates:
                if foeHP > 25:
                    if float(candidate.power) * float(candidate.accuracy) > beneficio:
                        beneficio = float(candidate.power) * float(candidate.accuracy)
                        i = candidate
                else:
                    if float(candidate.accuracy) > beneficio:
                        beneficio = float(candidate.accuracy)
                        i = candidate
            if len(candidates) > 0:
                print(myPokemon.name + ' no tiene ataques super efectivos contra ' + foePokemon.name)
                print('Pero podemos atacar con STAB usando ' + i.name + ' sin que lo resista ' + foePokemon.name)
                return myPokemon.list_attacks.index(i)+1

    if (poke.aFisico(myPokemon) and not poke.aEspecial(myPokemon) and poke.dFisico(foePokemon)) or \
            (poke.aEspecial(myPokemon) and not poke.aFisico(myPokemon) and poke.dEspecial(foePokemon)):
        candidate = cambio(myPokemon, foePokemon, player)
        if candidate is not 0:
            mon = player.list_pokemon[-1 * candidate - 1]
            if not deboCambiar(mon, foePokemon):
                if poke.aFisico(myPokemon) and not poke.aEspecial(myPokemon) and poke.dFisico(foePokemon):
                    print('Es mejor cambiar, ' + foePokemon.name + ' es defensivo fisico y '
                           + myPokemon.name + ' ataca por ese lado. Ademas, ' + myPokemon.name +
                           ' no tiene ataques para cubrirlo')
                if poke.aEspecial(myPokemon) and not poke.aFisico(myPokemon) and poke.dEspecial(foePokemon):
                    print('Es mejor cambiar, ' + foePokemon.name + ' es defensivo especial y '
                           + myPokemon.name + ' ataca por ese lado. Ademas, ' + myPokemon.name +
                           ' no tiene ataques para cubrirlo')
                return candidate
            else:
                print('Pero nuestra mejor opcion es ' + mon.name + ', que tambien estaria obligado a cambiar :(')
        else:
            print('Pero ya no tenemos mas pokemon :(')

    if poke.dEspecial(foePokemon):
        for i in myPokemon.list_attacks:
            if i.category == 'physical' and i.pp > 0:
                print('No hay muchas opciones ya. ' + foePokemon.name +
                      ' es defensivo especial, ataquemos por el lado fisico')
                return myPokemon.list_attacks.index(i)+1

    if poke.dFisico(foePokemon):
        for i in myPokemon.list_attacks:
            if i.category == 'special' and i.pp > 0:
                print('No hay muchas opciones ya. ' + foePokemon.name +
                      ' es defensivo especial, ataquemos por el lado fisico')
                return myPokemon.list_attacks.index(i)+1

    for i in myPokemon.list_attacks:
        if i.pp > 0:
            print('La situacion es complicada, no se que hacer. ' +
                  'Elijamos cualquier ataque para ver como se desarrolla la batalla')
            return myPokemon.list_attacks.index(i)+1


def test_score(playerPokemon, rivalPokemon):
    testScore = 0

    if poke.vence(playerPokemon, rivalPokemon) and poke.masRapido(playerPokemon, rivalPokemon):
        testScore += 10
    if poke.vence(playerPokemon, rivalPokemon) and poke.resiste(playerPokemon, rivalPokemon):
        testScore += 15
    if poke.cubreA(playerPokemon, rivalPokemon) and poke.masRapido(playerPokemon, rivalPokemon):
        testScore += 5
    if poke.cubreA(playerPokemon, rivalPokemon) and poke.resiste(playerPokemon, rivalPokemon):
        testScore += 5
    if (poke.dFisico(rivalPokemon) and not poke.dEspecial(rivalPokemon)) and poke.aEspecial(playerPokemon):
        testScore += 5
    if (poke.dEspecial(rivalPokemon) and not poke.dFisico(rivalPokemon)) and poke.aFisico(playerPokemon):
        testScore += 5
    if not poke.muroEspecial(rivalPokemon) and poke.sweeperEspecial(playerPokemon):
        testScore += 10
    if not poke.muroFisico(rivalPokemon) and poke.sweeperFisico(playerPokemon):
        testScore += 10
    if poke.fragilEspecial(rivalPokemon) and poke.sweeperEspecial(playerPokemon):
        testScore += 15
    if poke.fragilFisico(rivalPokemon) and poke.sweeperFisico(playerPokemon):
        testScore += 15

    if poke.vence(rivalPokemon, playerPokemon) and poke.masRapido(rivalPokemon, playerPokemon):
        testScore -= 20
    if poke.vence(rivalPokemon, playerPokemon) and poke.resiste(rivalPokemon, playerPokemon):
        testScore -= 30
    if poke.cubreA(rivalPokemon, playerPokemon) and poke.masRapido(rivalPokemon, playerPokemon):
        testScore -= 10
    if poke.cubreA(rivalPokemon, playerPokemon) and poke.resiste(rivalPokemon, playerPokemon):
        testScore -= 10
    if (poke.dFisico(playerPokemon) and not poke.dEspecial(playerPokemon)) and poke.aEspecial(rivalPokemon):
        testScore -= 10
    if (poke.dEspecial(playerPokemon) and not poke.dFisico(playerPokemon)) and poke.aFisico(rivalPokemon):
        testScore -= 10
    if not poke.muroEspecial(playerPokemon) and poke.sweeperEspecial(rivalPokemon):
        testScore -= 20
    if not poke.muroFisico(playerPokemon) and poke.sweeperFisico(rivalPokemon):
        testScore -= 20
    if poke.fragilEspecial(playerPokemon) and poke.sweeperEspecial(rivalPokemon):
        testScore -= 30
    if poke.fragilFisico(playerPokemon) and poke.sweeperFisico(rivalPokemon):
        testScore -= 30

    return testScore


def deboCambiar(myPokemon, foePokemon):

    if poke.vence(foePokemon, myPokemon) and \
            not (poke.masRapido(myPokemon, foePokemon) and poke.cubreA(myPokemon, foePokemon)):
        return True

    if poke.muroFisico(foePokemon) and poke.muroEspecial(foePokemon):
        if not (poke.sweeperFisico(myPokemon) or poke.sweeperEspecial(myPokemon)):
            return True
        else:
            if not poke.vence(myPokemon, foePokemon):
                return True
    else:
        if poke.muroFisico(foePokemon):
            if not (poke.vence(myPokemon, foePokemon) and poke.sweeperFisico(myPokemon)):
                if poke.vence(foePokemon, myPokemon) or poke.resiste(foePokemon, myPokemon):
                    return True
        if poke.muroEspecial(foePokemon):
            if not (poke.vence(myPokemon, foePokemon) and poke.sweeperEspecial(myPokemon)):
                if poke.vence(foePokemon, myPokemon) or poke.resiste(foePokemon, myPokemon):
                    return True

    return False


def cambio(myPokemon, rivalPokemon, player):
    score = -69969
    for i in player.list_pokemon:
        if i is not myPokemon:
            testScore = test_score(i, rivalPokemon)
            #print (i.name + ': ' + str(testScore))
            if testScore > score:
                score = testScore
                choice = i
    try:
        print('CAMBIO!')
        return -1*(player.list_pokemon.index(choice)+1)
    except:
        return 0


def hill_climbing(player, rival, team_num):
    team = []
    pool = list(player)
    if len(pool) < team_num:
        print("No tienes suficietes pokemon")
        return team
    for i in range(team_num):
        best = -69969
        best_i = 0
        h = []
        for x in range(len(pool)):
            h.append(0)
        for k in range(len(pool)):
            for j in rival:
                h[k] += test_score(pool[k], j)
            if h[k] > best:
                best = h[k]
                best_i = k
                #print(k)
        team.append(pool[best_i])
        pool.pop(best_i)
    if len(team) < team_num:
        print("No tienes suficientes pokemon")
    return team


def write_file(team):
    to_file = ""
    pool = open("pool.txt","r")
    lines = pool.readlines()
    for i in team:
        nombre = list(i.name)
        nombre[0] = nombre[0].upper()
        for k in range(len(nombre)-1):
                    if nombre[k] == ' ':
                            nombre[k+1] = nombre[k+1].upper()
        nombre = "".join(nombre)
        flag = 0
        for line in range(len(lines)):
            if flag == 2 and "Nature" in lines[line]:
            	nature = lines[line]
            	break
            if flag == 1 and "Ability" in lines[line]:
            	ability = lines[line]
            	flag = 2
            if flag == 0 and nombre in lines[line]:
            	flag = 1
        to_file = to_file+nombre+"\n"+ability+nature
        for j in i.list_attacks:
            ataque = list(j.name)
            ataque[0] = ataque[0].upper()
            for k in range(len(ataque)-1):
                    if ataque[k] == ' ':
                            ataque[k+1] = ataque[k+1].upper()
            ataque = "".join(ataque)
            ataque = "- "+ataque
            to_file = to_file + ataque+"\n"
        to_file = to_file + "\n"
    squad = open('team.txt', 'w')
    squad.write(to_file)
    squad.close()
    pool.close()
