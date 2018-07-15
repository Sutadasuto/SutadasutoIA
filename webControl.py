from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
from random import random

import pokemon as poke
import battleControl as battle

global username
global password
global showdown
global driver
global wait
global debug_flag

username = 'SutadasutoIA'
password = 'Stardust_1'
showdown = 'http://play.pokemonshowdown.com'
wait = 10
debug_flag = True


def prepareBrowser():
    global driver
    global wait
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 120)
    driver.implicitly_wait(2)
    driver.get(showdown)
    return driver


def debug(s):
    if debug_flag:
        print(s)


def login():
    wait.until(EC.element_to_be_clickable((By.NAME, 'login')))
    driver.find_element_by_name('login').click()
    userFlag = False
    while userFlag is False:
        userFlag = True
        try:
            driver.find_element_by_name('username').send_keys(username)            
        except:
            userFlag = False
    driver.find_element_by_css_selector('button[type=submit]').click()
    driver.implicitly_wait(2)
    passFlag = False
    while passFlag is False:
        passFlag = True
        try:
            driver.find_element_by_name('password').send_keys(password)            
        except:
            passFlag = False
    driver.find_element_by_css_selector('button[type=submit]').click()
    logFlag = False
    while logFlag is False:
        try:
            if driver.find_element_by_class_name('username').text == username:
                debug("Logged in.")
                logFlag = True
        except:
            null = 0


def load_team(name=None):
    if name is None:
        name = 'MyTeam'        
    debug("Loading team")
    team = open('team.txt', 'r')
    driver.find_element_by_css_selector('.mainmenu2').click()    
    wait.until(EC.element_to_be_clickable((By.NAME, 'newTop')))
    driver.find_element_by_name('newTop').click()    
    driver.find_element_by_css_selector('.teambuilderformatselect').click()
    driver.find_element_by_css_selector('ul.popupmenu:nth-child(1) > li:nth-child(13) > button:nth-child(1)').click()
    driver.find_element_by_name('import').click()
    driver.find_element_by_css_selector('.teamedit > textarea.textbox').send_keys(Keys.CONTROL + 'a')
    driver.find_element_by_css_selector('.teamedit > textarea.textbox').send_keys(team.readlines())    
    driver.find_element_by_name('saveImport').click()
    driver.find_element_by_css_selector('input.textbox.teamnameedit').send_keys(Keys.CONTROL + 'a')
    time.sleep(1)
    driver.find_element_by_css_selector('input.textbox.teamnameedit').send_keys(name)
    time.sleep(1)    
    driver.find_element_by_name('closeRoom').click()


def join_battle(user=None):
    if user is None:
        wait.until(EC.element_to_be_clickable((By.NAME, 'format')))
        driver.find_element_by_name('format').click()
        debug("Looking for Battle Spot")
        driver.find_element(By.XPATH, "//*[@name='selectFormat'][@value='gen7battlespotsingles']").click()
        debug("Search for battle")
        wait.until(EC.element_to_be_clickable((By.NAME, 'search')))
        driver.find_element_by_name('search').click()        

    else:
        wait.until(EC.element_to_be_clickable((By.NAME, 'finduser')))
        driver.find_element_by_name('finduser').click()    
        driver.find_element_by_name('data').send_keys(user)
        driver.find_element_by_css_selector('p.buttonbar:nth-child(2) > button:nth-child(1)').click()        
        debug("Requesting challenge vs " + user)
        wait.until(EC.element_to_be_clickable((By.NAME, 'challenge')))
        driver.find_element_by_name('challenge').click()
					
        driver.implicitly_wait(1)
        driver.find_element_by_css_selector('.challenge > form:nth-child(1) > p:nth-child(2) ' +
                                            '> button:nth-child(2)').click()
        driver.implicitly_wait(1)
        #driver.find_element_by_css_selector('ul.popupmenu:nth-child(1) > li:nth-child(14) ' +
         #                                   '> button:nth-child(1)').click()
        driver.find_element(By.XPATH, "//*[@name='selectFormat'][@value='gen7battlespotsingles']").click()
        driver.implicitly_wait(1)
        driver.find_element_by_name('makeChallenge').click()
        print('Waiting for opponent')


def select_pokemon():    
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.switchmenu > button:nth-child(1)')))
    debug("Battle Found")
    debug("Selecting Pokemon")
    driver.find_element_by_css_selector('.switchmenu > button:nth-child(1)').click()
    driver.find_element_by_css_selector('.switchmenu > button:nth-child(2)').click()
    driver.find_element_by_css_selector('.switchmenu > button:nth-child(3)').click()


def select_attack(attack):
    while True:
        try:
            ls = driver.find_elements_by_name('chooseMove')
            break
        except NoSuchElementException:
            null = 0
    for element in ls:
        value = element.get_attribute("value")
        if int(value) == attack:
            element.click()
            return 0
    try:
        null = ls[10]
    except IndexError:
        null = 0


def changeTo(pokemon=None):

    if pokemon is None:
        ls = driver.find_elements_by_name('chooseSwitch')
        ls[0].click()
    else:
        ls = driver.find_elements_by_name('chooseSwitch')
        for option in ls:
            if option.text.lower().split('-')[0] == pokemon.lower().split('-')[0]:
                option.click()
                return 0
        print('Hay algo inusual en el programa. Se cambia al primer pokemon disponible')
        try:
            ls[0].click()
        except IndexError:
            null = 0

def getFoeName(team):

    try:
        foe = driver.find_element(By.CSS_SELECTOR, '.lstatbar > strong')
        name = foe.text[0:-4].lower()
        for poke in team:
            if len(poke.split(name)) == 2:
                name = poke
                break
        return name
    except (NoSuchElementException, ValueError):
        return 'Foe pokemon not found!'


def myPokemonName(team):

    try:
        myPokemon = driver.find_element_by_css_selector('.whatdo > strong:nth-child(1)').text.lower()
        for poke in team:
            if len(poke.split(myPokemon)) == 2:
                myPokemon = poke
                return myPokemon.lower()
        return  myPokemon
    except NoSuchElementException:
        return 'My pokemon not found!'


def myHP():
    try:
        myPokeHP = driver.find_element(By.CSS_SELECTOR, '.whatdo > small')
        percentage = myPokeHP.text
        percentage = percentage.split(' ')[1]
        HP = percentage.split('/')[0]
        return HP
    except:
        return 'My HP not found!'


def foeHP():
    try:
        foePokeHP = driver.find_element(By.CSS_SELECTOR, '.lstatbar > div:nth-child(2) > div:nth-child(3)')
        HPpixels = foePokeHP.get_attribute('style')
        HPpixels = HPpixels.split(" ")[1]
        HP = float(HPpixels[0:-3])
        return round(HP * 100/151, 1)
    except:
        return 'HP not found!'


def analyzeCurrentStatus(myPokemon, foePokemon):

    stats = ["atk", "def", "spa", "spd", "spe", "acc", "eva"]
    hs = ["psn", "par", "slp", "brn", "frz"]
    vs = ["confused"]

    inGameMoves = driver.find_elements_by_name('chooseMove')
    for move in inGameMoves:
        if move.is_displayed():
            text = str(move.text).split('\n')
            name = text[0]
            type = text[1]
            currentPP = text[2].split("/")[0]
            for attack in myPokemon.list_attacks:
                if name.lower().replace("-"," ").replace("'","") == attack.name:
                    attack.atype = type.lower()
                    attack.pp = int(currentPP)
    myBoosts = [1] * 7
    foeBoosts = [1] * 7
    myGoodStats = driver.find_elements_by_css_selector('div.statbar.rstatbar>div.hpbar>div.status>span.good')
    foeGoodStats = driver.find_elements_by_css_selector('div.statbar.lstatbar>div.hpbar>div.status>span.good')
    myBadStats = driver.find_elements_by_css_selector('div.statbar.rstatbar>div.hpbar>div.status>span.bad')
    foeBadStats = driver.find_elements_by_css_selector('div.statbar.lstatbar>div.hpbar>div.status>span.bad')
    myHardStatus = "healthy"
    for status in hs:
        if len(driver.find_elements_by_css_selector('div.statbar.rstatbar>div.hpbar>div.status>span.' + status)) > 0:
            myHardStatus = status
            break
    foeHardStatus = "healthy"
    for status in hs:
        if len(driver.find_elements_by_css_selector('div.statbar.lstatbar>div.hpbar>div.status>span.' + status)) > 0:
            foeHardStatus = status
            break

    for boost in myGoodStats:
        value = str(boost.text).lower().split("\xd7 ")
        myBoosts[stats.index(value[1])] = float(value[0])
    myVolatileStatus = []
    for boost in myBadStats:
        value = str(boost.text).lower().split("\xd7 ")
        if len(value) == 2:
            myBoosts[stats.index(value[1])] = float(value[0])
        else:
            myVolatileStatus.append(value[0])

    for boost in foeGoodStats:
        value = str(boost.text).lower().split("\xd7 ")
        foeBoosts[stats.index(value[1])] = float(value[0])
    foeVolatileStatus = []
    for boost in foeBadStats:
        value = str(boost.text).lower().split("\xd7 ")
        if len(value) == 2:
            foeBoosts[stats.index(value[1])] = float(value[0])
        else:
            foeVolatileStatus.append(value[0])

    myPokemon.boosts = myBoosts
    myPokemon.hard_status = myHardStatus
    myPokemon.volatile_status = myVolatileStatus
    foePokemon.boosts = foeBoosts
    foePokemon.hard_status = foeHardStatus
    foePokemon.volatile_status = foeVolatileStatus


def battleActive():

    return len(driver.find_elements_by_name('instantReplay')) < 1


def fainted():
    hpBar = driver.find_elements_by_css_selector('.rstatbar')
    return not len(hpBar) > 0


def oneBattle(pokedex, attacks, jugadores):

    history = driver.find_elements_by_class_name('battle-history')
    player1 = history[0].text.lower()
    player2 = history[1].text.lower()
    team1 = str(player1).split('\n')[1].split(' / ')
    team2 = str(player2).split('\n')[1].split(' / ')

    turn = 0
    expectedTurn = 1

    while turn != expectedTurn:
        history = driver.find_elements_by_class_name('battle-history')
        try:
            turn = int(history[-1].text.split(" ")[1])
        except ValueError:
            turn = -1
        time.sleep(0.1)
    expectedTurn += 1
    time.sleep(0.1)

    while battleActive():

        foe = getFoeName(team2)
        poke.appendPokemon(foe, jugadores.list_rival, pokedex)
        rival = poke.foePokemon(foe, jugadores)
        print('Foe: ' + rival.name)
        myPkm = myPokemonName(team1)
        active = poke.myPokemon(myPkm, jugadores)
        print('My pokemon: ' + active.name)
        mHP = myHP()
        print('My HP: ' + mHP)
        rival.hp = foeHP()
        print('Foes HP: ' + str(rival.hp) + '%')

        analyzeCurrentStatus(active, rival)

        decision = battle.decideAction(active, rival, jugadores)
        if decision > 0:
            try:
                select_attack(decision)
            except:
                print('Hay algo inusual en el programa. Se usa el primer ataque disponible')
                decision = 1
                select_attack(decision)
            print(active.name + ' uses ' + active.list_attacks[decision - 1].name)
            active.list_attacks[decision - 1].make_attack()
            print(active.list_attacks[decision - 1].name + ': ' +
                  str(active.list_attacks[decision - 1].pp) + '/' + str(active.list_attacks[decision - 1].max_pp))
        else:
            pokemonSelected = jugadores.list_pokemon[-1*decision - 1].name
            print('Change to ' + pokemonSelected)
            active = poke.myPokemon(pokemonSelected, jugadores)
            changeTo(pokemonSelected)
            myPkm = pokemonSelected
        print('Waiting for opponent...')

        while turn != expectedTurn:

            flag = fainted()
            if flag:
                print(myPkm + ' fainted!')
                try:
                    jugadores.list_pokemon.pop(jugadores.list_pokemon.index(active))
                except:
                    null = 0
                print('Quedan vivos: ')
                for pokemon in jugadores.list_pokemon:
                    print(pokemon.name)
                choiceIndex = -1 * battle.cambio(active, rival, jugadores)
                choiceName = jugadores.list_pokemon[choiceIndex - 1].name
                print('Elige a: ' + choiceName)
                changeTo(choiceName)
                while True:
                    if not fainted():
                        break

            if not battleActive():
                break
            history = driver.find_elements_by_class_name('battle-history')
            try:
                turn = int(history[-1].text.split(" ")[1])
            except ValueError:
                turn = -1
            time.sleep(0.1)
        expectedTurn += 1
        time.sleep(0.1)

    try:
        driver.find_element_by_name('showChat').click()
    except:
        null = 0
    log = driver.find_elements_by_css_selector('.battle-history')
    attacksUsed = []
    for line in log:
        event = line.text
        parts = event.split('The opposing ')
        if len(parts) == 2:
            pair = parts[1]
            poke_atk = pair[0:-1].lower().split(' used ')
            if len(poke_atk) == 2:
                attacksUsed.append(poke_atk)

    for line in attacksUsed:
        name = line[0]
        attack = line[1]
        pokemon = poke.foePokemon(name, jugadores)
        pokemon.learn_attack(poke.get_this_attack(attack.replace("'",""), attacks))
    time.sleep(1)
    try:
        driver.find_element_by_name('hideChat').click()
    except:
        null = 0
    time.sleep(3)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.messagebar > p:nth-child(1)')))
    try:
        while True:
            message = driver.find_element_by_css_selector('.messagebar > p:nth-child(1)')
            result = message.text
            if result[-15:] == 'won the battle!':
                break
    except:
        result = 'unknown'
    if result == 'SutadasutoIA won the battle!':
        return []
    driver.find_element_by_name('closeRoom').click()
    driver.quit()
    return jugadores.list_rival
