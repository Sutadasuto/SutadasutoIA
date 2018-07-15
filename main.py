from webControl import *

def main():
    [pokedex, attacks, jugadores, pool] = poke.init()
    prepareBrowser()
    login()
    load_team()
    #join_battle('SutadasutoIAQ')
    join_battle()
    select_pokemon()
    rivalTeam = oneBattle(pokedex, attacks, jugadores)
    if len(rivalTeam) == 0:
        print('OBJETIVO LOGRADO')
    else:
        print('OBJETIVO NO LOGRADO')


if __name__ == '__main__':
    main()
