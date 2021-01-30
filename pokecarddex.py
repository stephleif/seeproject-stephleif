"""
HEADS UP this is the version for trying to see the pokemon cards on a web page
NOT the version submitted for the project

PokeCardDex template.  This is a template file that is used to define the classes and functions
to work with Pokemon cards and lists of Pokemon cards called PokeCardDex
"""
import json
import os.path
import os
import pathlib
import random
import re
import math


def extractMaximum(ss)-> int:
    """
    Extracts the maximum number from a string of alphanumeric text
    function copied from https://www.geeksforgeeks.org/extract-maximum-numeric-value-given-string/
                                
    returns max int found, if no int found returns 0

    Keyword Arguments
    (ss) string to be parsed
    """

    num, res = 0, 0
    # start traversing the given string
    for i in range(len(ss)):
        if ss[i] >= "0" and ss[i] <= "9":
            num = num * 10 + int(int(ss[i]) - 0)
        
        else:
            res = max(res, num)
            num = 0
        
    return max(res, num)


def extractMinimum(ss) -> int:
    """
    Extracts the minimum number from a string of alphanumeric text
    changed extractMaximum to get it
                                
    returns min int found, if no int found returns 0

    Keyword Arguments
    (ss) string to be parsed
    """
    num = 0
    res = 0
    x = re.search("-", ss)
    if not x == None:
        res = -1 * extractMaximum(ss)
    
    else:
        for i in range(len(ss)):
            if ss[i] >= "0" and ss[i] <= "9":
                num = num * 10 + int(int(ss[i]) - 0)
            
            else:
                res = min(res, num)
                num = 0
            
    return min(res, num)
    


class Pokemon():
    def __init__(self, name, start_hp, energy_type, weakness, resistance,
                 moves):
        """
        Initialize a Pokemon
        The following is a summary of the inputs to this class:

        Keyword arguments:
        (Pokemon) self --instance of this class
        (str) name -- name of this pokemon
        (int) starthp -- inital value of healthpoints.  healthpoints change in battles
        (str) energy_type: the energy type of the pokemon (electric, water,
            #   fire, etc,.) - always made lower case
        (str) weakness: the energy type the pokemon is weak against
        (tuple) resistance: the energy types the pokemon is resistant against
        (tuple) moves: a tuple of ((str), (int)) pairs that represent the
         move name and damage amount
        """
        self.name = name
        self.start_hp = start_hp
        self.energy_type = energy_type
        self.weakness = weakness
        self.resistance = resistance
        self.moves = moves
        self.moveindex = 0
        # initialize computed values
        self.hp = start_hp
        self.is_fainted = False
        self.moveindex = 0
        ## end init

    def show_pokemon(self):
        """
        displays the current pokemon
        Keyword arugments:
        (Pokemon) self - the pokemon to display
        """
        print(f"{self.name}:{self.hp} type= {self.energy_type}")
        #energy_type, weakness, resistance, moves
        print(
            f"weakness: {self.weakness}, resistance: {self.resistance}, moves:{self.moves}"
        )
        # end show_pokemon

    def __str__(self):
        """
        print out pokemon all on one line
        Keyword Arguments:
        (Pokemon) self
        """
        return (f"{self.name}:{self.energy_type} with {self.hp} left")

    def movedamage(self) -> int:
        """
        For a pokemon gives the next move that pokemon will make as a tuple
        moves is a list of (name,value)
        Keyword Arguments
        (Pokemon) self
        returns 
        (int) amount of attack damage

        IMPORTANT: movedamage never returns an attack damage of 0.
        We use the instruction: damage defaults to 5
        """
        val = self.moves[self.moveindex]
        if val[1] == 0:
            val[1] = 5
        
        self.moveindex = (self.moveindex + 1) % len(self.moves)
        return (val[1])


    def damage(self, amount):
        """
        inflicts amout of damage on self.  hp doesn't go below 0, is_fainted will be set if hp gets to 0
        Keyword Arguments:
        (Pokemon) self
        (int) amount
        """
        if self.hp - amount > 0:
            self.hp = self.hp - amount
        
        else:
            self.hp = 0
            self.is_fainted = True
        
        ## end damage


    def compute_weakness(self, energytype) -> int:
        """
        computes the weakness of self pokemon to energytype
        returns amount of weakness
        default is 1
        Keyword Arguments
        (pokemon) self
        (str) energytype energy type of the opposing pokemon
        """

        if energytype is None:
            return 1
        
        elif self.weakness is None:
            return 1        
        elif type(self.weakness) == str:
            weak = 1
            return (weak)
        else:
            weak = 1
            thisweak = 1          
            for myweak in self.weakness:
                if 'type' in myweak.keys() and 'value' in myweak.keys():
                    if myweak.get('type') == energytype:
                        this_weak = extractMaximum(myweak.get('value'))
                        weak = max(weak, thisweak)
                    
            return (weak)
           

    def compute_resistance(self, energytype) -> int:
        """
        same idea as weakness, except default resistance is 0
        and resistance values are negative
        Keyword Arguements
        (pokemon) self
        (str) energytype
        """
        if energytype is None:
            return 0
        
        elif self.resistance is None:
            return 0
        
        elif type(self.resistance) == str:
            resist = extractMinimum(self.resistance)
            print(f"got a string for reistance is {self.resistance}")
            return (resist)
        
        else:
            resist = 0
            thisresist = 0
            for myresist in self.resistance:
                if 'type' in myresist.keys() and 'value' in myresist.keys():
                    if myresist.get('type') == energytype:
                        thisresist = int(myresist.get('value'))
                        resist = min(resist, thisresist)
                    
                
            return (resist)
        

    def fight(self, opponent):
        """
        battles oppenent against self, updates self's hp and is_fainted
        reminder: damage is: base_damage * opposing_weakness (default 1) - opposing resistence`
        the types do  need to match
        Keyword arguments:
        (Pokemon) self
        (Pokemon) opponent
        """
        problemPokey = "None"
        

        if opponent.is_fainted:
            return ()
        
        elif self.is_fainted:
            return ()
        
        else:
            if self.name == problemPokey or opponent.name == problemPokey:
                print(f"fight between {self.name} and {opponent.name}")
                self.show_pokemon()
                opponent.show_pokemon()
            
            #self.show_pokemon()
            #opponent.show_pokemon()
            # 1. find move amount of the attack
            attack_amount = opponent.movedamage()
            the_weakness = self.compute_weakness(opponent.energy_type)
            the_resistance = self.compute_resistance(opponent.energy_type)
            if self.name == problemPokey or opponent.name == problemPokey:
                print(
                    f" attack: {attack_amount}, weakness: {the_weakness}, resistance {the_resistance}"
                )
            
            # damage is: base_damage * opposing_weakness (default 1) - opposing resistence`
            attack_amount = (attack_amount * the_weakness) + the_resistance
            self.damage(attack_amount)
            if self.name == problemPokey or opponent.name == problemPokey:
                print(
                    f"- - - After fight between {self.name} and {opponent.name}- - - - - - "
                )
                print(f"self: {self}")
                print(f"opponent: {opponent}")
                print(
                    ". . . . . . . . . . .   .    .    .    .    .   .   .   . . . "
                )
            
        return ()
        
        # end fight

    def heal_pokemon(self):
        """
        heals pokemon back to original hp
        Keyword Arguments
        (Pokemon) self
        """
        self.is_fainted = False
        self.hp = self.start_hp
        # end heal_pokemon


class PokeCardDex():
    def __init__(self, json_file_path=None):
        """
        Initializes the pokemon from the info in the the json file
        Keyword arguments:
        self - instance of this class that will be initialized
        (str) json_file_path path to the json_file that has the pokemon information
        """

        # start of init
        # print("PokeCardDex!")
        self.party = list()
        self.num_cards = 0

        if json_file_path == None:
            # NOTE: It is important to handle the case where no path is passed in
            # meaning that json_file_path has a value of None.
            # no cards to read in to the dex, so return empty list and 0
            return (None)
        else:
            filename = json_file_path
            if not os.path.isfile(filename):
                print(f"Error: {filename} not found")
            else:
                # going for the with ... as formulation
                path_filename = pathlib.Path(json_file_path)
                with path_filename.open(mode='r') as the_file:
                    jsondata = the_file.read()
                # with block will close the file. no need to the_file.close()
                all_obj = json.loads(jsondata)
                # obj['key'] gets string
                # print("Starting to parse data")
                # print(f"len all_obj: {len(all_obj)}")
                for iterator in range(len(all_obj)):
                    obj = all_obj[iterator]
                    current_keys = obj.keys()
                    if "name" in current_keys:
                        name = obj["name"]
                    else:
                        print("Failure: No name")
                        print(f"{current_keys}")
                        name = "Null"
                    if "hp" in current_keys:
                        text_hp = obj["hp"]
                        start_hp = extractMaximum(text_hp)
                    else:
                        print("Failure: No hp")
                        print(f"Iterator is: {iterator}")
                        print(f"keys are: {current_keys}")
                        start_hp = 5
                    if "types" in current_keys:
                        energy_type_list = obj["types"]
                        energy_type = energy_type_list[0]
                    else:
                        print("Failure: No types")
                        print(f"Iterator is: {iterator}")
                        print(f"keys are: {current_keys}")
                        energy_type = ""
                    if "weaknesses" in current_keys:
                        weakness = obj["weaknesses"]
                    else:
                        # number 234, 265, 287 have no weaknesses
                        weakness = "None"
                    if "resistances" in current_keys:
                        resistence = obj["resistances"]
                        ##  tuple of ((str), (int)) pairs that represent the
                        ##  move name and damage amount
                        ## I think is stored under "attacks"
                    else:
                        ## 3rd entry has no resistance.  set it to empty tuple
                        resistence = tuple()
                    if "attacks" in current_keys:
                        attacks = obj["attacks"]
                        ## attacks sample looks like this:
                        ## "attacks": [{"cost": ["Grass", "Grass"], "name": "Foul Gas",
                        ##      "text": "Flip a coin. If heads, the Defending Pokemon is now Poisoned; if tails, it is now Confused.",
                        ##      "damage": "10", "convertedEnergyCost": 2}]
                        moves = list()
                        for attack in attacks:
                            attack_keys = attack.keys()
                            if "name" in attack_keys and "damage" in attack_keys:
                                move_name = attack.get("name")
                                ## get the largest number in the string
                                move_damage = extractMaximum(
                                    attack.get("damage"))
                                if move_damage == 0:
                                    move_damage = 5
                                if move_damage > 0:
                                    # make into a tuple
                                    move_tuple = (move_name, move_damage)
                                    moves.append(move_tuple)
                        if not moves:
                            move_tuple = ("Whoops", 5)
                            moves.append(move_tuple)
                    else:
                        moves = list()
                        move_tuple = ("Whoops", 5)
                        moves.append(move_tuple)
                    pokey = Pokemon(name, start_hp, energy_type, weakness,
                                    resistence, moves)
                    self.party.append(pokey)
                    self.num_cards = self.num_cards + 1

    def allfainted(self) -> bool:
        """
        returns true if all cares in the pokedex are fainted
        Keyword Arguements
        (pokedex) self
        returns bool
        """
        for mycard in self.party:
            if not mycard.is_fainted:
                return (False)
        return (True)

    def set_order(self, order):
        """
        set_order changes the order of the cards to be the order of the names in order
        tester script has it called 
             set_order(name_order)
             sorry for the n^2 efficiency

        Keyword Arguements
        (Pokedex) self: the pokedex to be ordered
        (list)  order: description of how to order the Pokedex
        """
        answ = PokeCardDex()
        for n in order:
            # search for name in self
            pindex = 0
            found = False
            while pindex < self.num_cards and not found:
                if n == self.party[pindex].name:
                    answ.add_to_party(self.party[pindex])
                    found = True
                pindex = pindex + 1
            if not found:
                print(f"{n} not found in PokeCardDex ")
        self.party = answ.party
        return (answ)

        # end set_order

    def battle(self, challenger_party):
        """
        battle computes the battle between 2 pokedex
        Keyword Arguments:
        (Pokecarddex) self: the collection of pokemon being attacked
        (Pokecarddex) challenger_party: the collection of pokemon doing the attacking
        """
        print("Welcome to the battle")
        if self == None:
            print("Self is None.  I guess we lost")
            return ("Home team lost.")
        elif challenger_party == None:
            print("challenger_party is none.  I guess we won")
            return ("Home Team is the winner!")
        else:
            print(f"Home team has {self.num_cards} cards")
            print(f"Away team has {challenger_party.num_cards} cards")
            home_index = 0
            away_index = 0
            while not self.allfainted() and not challenger_party.allfainted():
                while home_index < self.num_cards and away_index < challenger_party.num_cards:
                    if not self.party[
                            home_index].is_fainted and not challenger_party.party[
                                away_index].is_fainted:
                        home_hp = self.party[home_index].hp
                        away_hp = challenger_party.party[away_index].hp
                        self.party[home_index].fight(
                            challenger_party.party[away_index])
                        challenger_party.party[away_index].fight(
                            self.party[home_index])
                        if home_hp == self.party[
                                home_index].hp and away_hp == challenger_party.party[
                                    away_index].hp:
                            print("trying to infinite loop in battle.   ")
                            print(f"home card is {self.party[home_index]}")
                            print(
                                f"away card is {challenger_party.party[away_index]}"
                            )
                            home_index = home_index + 1
                    elif self.party[home_index].is_fainted:
                        home_index = home_index + 1
                    elif challenger_party.party[away_index].is_fainted:
                        away_index = away_index + 1
                # end inner while
                if home_index >= self.num_cards:
                    home_index = 0
                if away_index >= challenger_party.num_cards:
                    away_index = 0
            #end outer while
            winner = challenger_party.allfainted()
            if winner:
                print("Home team is the winner")
                return(True)
            else:
                print("Home team lost")
                return(False)
            return
        # end battle

    def heal_party(self):
        """
        Heals the pokecarddex back to initial configuration
        Keyword Arguments
        (Pokecarddex) self: the collection of pokemon to be healed
        """
        for iterator in self.party:
            iterator.heal_pokemon()
        # end heal_party

    def add_to_party(self, pokemon):
        """
        add_to_party adds a pokemon to a pokedex
        Keyword arguments:
        self - instance of this class 
        (Pokemon) pokemon: the pokemon to add to the pokedex
        """
        self.num_cards = self.num_cards + 1
        self.party.append(pokemon)
        #print("added a pokemon card to the party")
        # end add_to_party


# Below is an example usage for using the classes
if __name__ == "__main__":
    print(
        "                                                  Welcome to the Pokemon games!"
    )

    #print(f"The current working directory is {os.getcwd()}")

    my_dex = PokeCardDex('pokemon_party.json')

    card_dex = PokeCardDex('myParty.json')
    rival_dex = PokeCardDex('rivalParty.json')
    card_dex.battle(rival_dex)
    print("testing battle results")
    for pok in range(card_dex.num_cards):
        print(f"{card_dex.party[pok].name}, {card_dex.party[pok].hp}")
    print("all of the above should be 0")

    test_results = [("Hitmonchan", 0, True), ("Meganium", 45, False),
                    ("Abra", 30, False), ("Zapdos", 90, False),
                    ("Butterfree", 70, False), ("Ekans", 50, False),
                    ("Porygon", 30, False), ("Dewgong", 80, False),
                    ("Feraligatr", 120, False), ("Venomoth", 70, False)]
    ipok = 0
    for pok in range(rival_dex.num_cards):
        print(f"{rival_dex.party[pok]}")
        if ipok < len(test_results):
            print(f"{test_results[ipok]}")
        ipok += ipok


    name_order = [
        'Chikorita',
        'Doduo',
        'Skarmory',
        'Clefable',
        'Weezing',
        'Mareep',
        'Machoke',
        'Persian',
        'Chansey',
    ]


    rival_dex = PokeCardDex('pokemon_master_list.json')
    pikachu = Pokemon('Pikachu', 100, 'electric', None, None,
                      (('electric charge', 30), ))
    #                  name, start_hp, energy_type, weakness, resistance, moves
    # pikachu.show_pokemon()
    rival_dex.battle(my_dex)
    rival_dex.add_to_party(pikachu)
    rival_dex.heal_party()
    my_dex.heal_party()

    my_dex.battle(rival_dex)

    my_dex.heal_party()
    rival_dex.heal_party()
    card_dex.set_order(name_order)
    print(f"type of card_dex.party {type(card_dex.party)}")
    po_iterator = 0
    for name_iterator in name_order:
        if po_iterator >= card_dex.num_cards:
            print("should have had more cards in name check")
        else:
            card_name = card_dex.party[po_iterator].name
            if  not card_name == name_iterator:
                print(f"order did not work, {card_name} isnt {name_iterator}")
        po_iterator = po_iterator +1
    ## so what should happen when you battle yourself?
    rival_dex.battle(rival_dex)
    for poindex in rival_dex.party:
        print(f"{poindex}")

    # end main

