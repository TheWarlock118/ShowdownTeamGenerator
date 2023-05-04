import os
import shutil
import urllib.request
import Levenshtein
import random
import math
import traceback

# Gather necessary data for the movesets according to the given month
def get_data_movesets(url):
    url = url + "moveset/"
    html_string = str(urllib.request.urlopen(url).read())

    print("Gathering Necessary Data from " + str(url) + "...")
    file_names = []
    file_name_start = 0
    for i in range(len(html_string)):
        if html_string[i] == '"':
            if file_name_start == 0:
                file_name_start = i
            else:
                file_names.append(html_string[file_name_start+1:i])
                file_name_start = 0

    local_folder = "downloaded_stats/moveset/"
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)
    else:
        shutil.rmtree(local_folder, ignore_errors=True)
        
    for file_name in file_names:
        try:
            file_url = url + file_name
            local_path = os.path.join(local_folder, file_name)
            urllib.request.urlretrieve(file_url, local_path)
        except:
            pass

# Gather necessary data for Pokemon usage according to the given month
def get_data(url):
    os.system('cls')
    print("Note: This is only necessary the first time the program is run,")
    print("or after a new month of data is selected.")
    print("Gathering Necessary Data from " + str(url) + "...")
    html_string = str(urllib.request.urlopen(url).read())

    file_names = []
    file_name_start = 0
    for i in range(len(html_string)):
        if html_string[i] == '"':
            if file_name_start == 0:
                file_name_start = i
            else:
                file_names.append(html_string[file_name_start+1:i])
                file_name_start = 0

    local_folder = "downloaded_stats"
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)
    else:        
        shutil.rmtree(local_folder, ignore_errors=True)
        
    for file_name in file_names:
        try:
            file_url = url + file_name
            local_path = os.path.join(local_folder, file_name)
            urllib.request.urlretrieve(file_url, local_path)
        except:
            pass

    get_data_movesets(url)

    return file_names

def cull_empty_data():
    print("Culling Empty Data")
    usage_folder = "downloaded_stats/"
    moveset_folder = "downloaded_stats/moveset/"

    for filename in os.listdir(usage_folder):
        file_path = os.path.join(usage_folder, filename)
        if(os.path.isfile(file_path) and os.path.getsize(file_path) == 0):
            os.remove(file_path)

    for filename in os.listdir(moveset_folder):
        file_path = os.path.join(moveset_folder, filename)
        if(os.path.isfile(file_path) and os.path.getsize(file_path) == 0):
            os.remove(file_path)

# Print all tiers
def print_tiers():
    local_folder = "downloaded_stats/moveset"
    for item in os.listdir(local_folder):
        tier_name = str(item).replace('.txt', '')
        print(tier_name)

# Helper function for selecting tier
def select_tier(pokemon):
    local_folder = "downloaded_stats"
    tier_chosen = False
    print("\tHere, you will choose a tier you wish to generate a team for.")
    print("\tThe tier determines both the Pokemon available to use and the rulesets applied during battle.")
    print("\tThe number following the tier, such as 1760 in gen1ou-1760,")
    print("\trepresents the ELO rank of the players from which the data was gathered, higher being better.")
    print("\tIf no Pokemon is selected, you may select from any tier.")
    print("\tIf a Pokemon is selected, you must select from tiers that Pokemon is used in.")

    potential_tiers = get_potential_tiers(pokemon)
    while(not tier_chosen):    
        print("\tTo view viable tiers, enter 'view'")
        tier_input = input("Enter your tier choice:")

        if(tier_input == 'view'):
            for tier in potential_tiers:
                print(tier)
        else:
            if(tier_input in potential_tiers):                                    
                tier_chosen = True
        
            if(tier_chosen == False):
                print("Tier not found")

    return tier_input

# Helper function for selecting starting Pokemon
def select_starting_pokemon(tier):
    pokedex_altered = get_potential_pokemon(tier)

    print("\tHere, you will select a starting Pokemon.")
    print("\tThis Pokemon will be used as a basis to build the rest of your team.")
    print("\tIf no tier is selected, then you may choose any starting Pokemon.")
    print("\tIf a tier is selected, then you can only choose Pokemon used in that tier.")
    chosen_value = False
    while(not chosen_value):
        print("\tTo view viable Pokemon, enter 'view'")
        starting_mon = input("Enter your starting Pokemon:")

        if(starting_mon == "view"):
            for mon in get_potential_pokemon(tier):
                print(mon)
        elif(starting_mon in pokedex_altered):
            chosen_value = True
        else:
            min_distance = float("inf")
            best_guess = ""
            for line in pokedex_altered:
                distance = Levenshtein.distance(starting_mon, line)
                if distance < min_distance:
                    min_distance = distance                
                    best_guess = line
                    if(best_guess[-1] == '\n'):
                        best_guess = best_guess[:-1]
                                
            re_search_bool = input(str(starting_mon) + " was not found. Did you mean " + str(best_guess) + "? (Y/n)")
            if(re_search_bool == 'Y' or re_search_bool == "" or re_search_bool == 'y'):
                starting_mon = best_guess
                chosen_value = True

    return starting_mon            

# Helper function for selecting starter popularity cutoff
def select_starting_popularity_cutoff():
    print("\tHere, you will choose a popularity cutoff for your starting Pokemon.")
    print("\tThis cutoff will determine the range from which your starting Pokemon is chosen.")
    print("\tFor example, if you choose a cutoff of 1%, then your starting Pokemon will be chosen")
    print("\tfrom the highest 1% of Pokemon within the chosen tier, based on usage.")
    print("\tIf you choose 100%, then your starting Pokemon will be chosen from any Pokemon registered within the tier.")
    print("\tIf a starter Pokemon is manually selected, this value will be ignored.")
    
    chosen_value = False
    while(not chosen_value):
        cutoff = input("Enter your cutoff(1-100):")
        try:
            if(int(cutoff) < 1 or int(cutoff) > 100):
                print("Invalid Choice")
            else:
                chosen_value = True
        except:
            print("Invalid Choice")
    
    
    return cutoff

# Helper function for selecting teammate popularity cutoff
def select_teammate_popularity_cutoff():
    print("\tHere, you will choose a popularity cutoff for your teammate Pokemon.")
    print("\tThis cutoff will determine the range from which your teammate Pokemon are chosen.")
    print("\tFor example, if you choose a cutoff of 1%, then your teammate Pokemon will be chosen")
    print("\tfrom the highest 1% of registered teammates, based on usage.")
    print("\tIf you choose 100%, then your starting Pokemon will be chosen from any Pokemon registered as teammates.")
    
    chosen_value = False
    while(not chosen_value):
        cutoff = input("Enter your cutoff(1-100):")
        try:
            if(int(cutoff) < 1 or int(cutoff) > 100):
                print("Invalid Choice")
            else:
                chosen_value = True
        except:
            print("Invalid Choice")
    
    
    return cutoff

# Helper function for selecting team generation mode
def select_generation_mode():
    print("\tHere you will choose the mode in which your team is generated")
    print("\tThe first mode is Centered, which selects teammates based strictly on your starting Pokemon")
    print("\tThe second mode is Chained, which selects teammates iteratively, based on each next determined teammate")
    print("  1. Centered")
    print("  2. Chained")

    chosen_value = False
    while(not chosen_value):
        chosen_mode = input("Enter your choice:")
        try:
            if(int(chosen_mode) < 1 or int(chosen_mode) > 2):
                print("Invalid Choice")
            else:
                chosen_value = True
        except:
            print("Invalid Choice")
    
    return chosen_mode

# Helper function for selecting bulk generation mode
def select_bulk_generation():
    print("\tAll teams will be based on the currently selected parameters.")
    print("\tEach parameter not given will be randomly selected on a per-team basis.")    


    chosen_value = False
    while(not chosen_value):
        chosen_mode = input("Enter the number of teams to generate (max 1000):")
        try:
            if(int(chosen_mode) < 0 or int(chosen_mode) > 10000):
                print("Invalid choice")
            else:
                chosen_value = True
        except:
            print("Invalid Choice")
    
    return chosen_mode

# From given paramaters, generate missing
def generate_parameters(tier, starting_mon, starting_cutoff, teammate_cutoff, generation_mode, force_generation):
    # Get list of potential tiers
    successful_generation = False
    
    local_folder = "downloaded_stats/moveset"
    list_tiers = []
    for item in os.listdir(local_folder):
        if('.txt' in str(item)):
            list_tiers.append(item.replace('.txt',''))
    
    tier_print = str(tier)
    starting_mon_print = str(starting_mon)
    starting_cutoff_print = str(starting_cutoff)
    teammate_cutoff_print = str(teammate_cutoff)
    generation_mode_print = str(generation_mode)

    generate_tier = False
    generate_starting_mon = False
    generate_starting_cutoff = False
    generate_teammate_cutoff = False
    generate_generation_mode = False

    if(tier == ""):
        generate_tier = True
        tier_print = "none"
    if(starting_mon == ""):
        generate_starting_mon = True
        starting_mon_print = "none"
    if(starting_cutoff == ""):
        generate_starting_cutoff = True
        starting_cutoff_print = "none"
    if(teammate_cutoff == ""):
        generate_teammate_cutoff = True
        teammate_cutoff_print = "none"
    if(generation_mode == 0):
        generate_generation_mode = True
        generation_mode_print = "none"
    
    if(not force_generation):
        print("You have chosen Tier:" + str(tier_print) + ", Starting Pokemon:" + str(starting_mon_print) + ", Starting Pokemon Cutoff:" + str(starting_cutoff_print) + "%, Teammate Cutoff:" + str(teammate_cutoff_print) + "%, and Generation Mode:" + str(generation_mode_print))
        generation_bool = input("Would you like to generate a team with these parameters? Parameters not given will be randomly selected (Y/n):")
    elif(force_generation):
        generation_bool = "Y"


    if(generation_bool == "Y" or generation_bool == "y" or generation_bool == ""):
        while(not successful_generation):
            try:
                if(generate_tier):
                    tier = random.choice(list_tiers)        
                if(generate_starting_cutoff):
                    starting_cutoff = random.randint(1, 100)
                if(generate_teammate_cutoff):
                    teammate_cutoff = random.randint(1, 100)
                if(generate_starting_mon):
                    starting_mon = random.choice(get_potential_pokemon_cutoff(tier, starting_cutoff))
                if(generate_generation_mode):
                    generation_mode = random.randint(1, 2)                
                successful_generation = True
            except:
                pass
    else:
        return -1, -1, -1, -1, -1
    
    return tier, starting_mon, starting_cutoff, teammate_cutoff, generation_mode

# Given a tier, get all the viable Pokemon in that tier
def get_potential_pokemon(tier):
    potential_pokemon = []

    # If no tier provided, return all Pokemon from pokedex
    if(tier == ""):
        pokedex_path = "misc_data/pokedex.txt"
        with open(pokedex_path) as f:
            pokedex_lines = f.readlines()
        
        for line in pokedex_lines:
            if(line[-1] == '\n'):
                potential_pokemon.append(line[:-1])
            else:
                potential_pokemon.append(line)
        return potential_pokemon[1:]
    
    with open('downloaded_stats/moveset/' + tier + ".txt") as f:
        moveset_lines = f.readlines()

    # Enumerate moveset lines to get viable mons
    for i, line in enumerate(moveset_lines):
        if(i < len(moveset_lines) - 1):
            next_line = moveset_lines[i + 1]                   
        if '+-' in line and '+' not in next_line and 'Raw count' not in next_line and 'Abilities' not in next_line and 'Items' not in next_line and 'Spreads' not in next_line and 'Moves' not in next_line and 'Teammates' not in next_line and 'Checks and Counters' not in next_line:            
            potential_pokemon.append(next_line.replace('|','').strip())
    
    return potential_pokemon

# Given a tier and a cutoff, get cutoff% of potential pokemon in that tier
def get_potential_pokemon_cutoff(tier, cutoff):
    potential_all_pokemon = get_potential_pokemon(tier)
    num_pokemon = math.ceil(len(potential_all_pokemon) * (int(cutoff)/100))
    if(num_pokemon < 1):
        return potential_all_pokemon
    return potential_all_pokemon[:num_pokemon]

# Given a Pokemon, get a list of potential tiers that contain that Pokemon
def get_potential_tiers(pokemon):
    local_folder = "downloaded_stats"
    
    tiers = []
    for item in os.listdir(local_folder):
        tier_name = str(item).replace('.txt', '')
        if(not tier_name == "moveset"):
            tiers.append(tier_name)
    
    if(pokemon == ""):
        return tiers

    viable_tiers = []    
    for candidate_tier in tiers:
        if(pokemon in get_potential_pokemon(candidate_tier)):
            viable_tiers.append(candidate_tier)
    
    return viable_tiers

# Main generate_team function
def generate_team(tier, starting_mon, starting_cutoff, teammate_cutoff, generation_mode, force_generation):
    # Generate Parameters
    generated_tier, generated_starting_mon, generated_starting_cutoff, generated_teammate_cutoff, generated_generation_mode = generate_parameters(tier, starting_mon, starting_cutoff, teammate_cutoff, generation_mode, force_generation)    
    if(generated_tier == -1 and generated_starting_mon == -1 and generated_starting_cutoff == -1 and generated_teammate_cutoff == -1 and generated_generation_mode == -1):
        return

    print()
    print("Generating Team with Following Paramaters")
    print("Tier: " + str(generated_tier) + " Starting_Mon: " + str(generated_starting_mon) + " Starting_Cutoff: " + str(generated_starting_cutoff) + " Teammate_Cutoff: " + str(generated_teammate_cutoff) + " Generation_Mode: " + str(generated_generation_mode))
    try:
        generate_team_helper(generated_tier, generated_starting_mon, generated_generation_mode, generated_teammate_cutoff, force_generation)
        return 0
    except Exception as e:        
        folder = 'failure_data/'
        if not os.path.exists(folder):
            os.makedirs(folder)

        files_count = len(os.listdir(folder))
        file_name = folder + "failures-" + str((files_count + 1)) + ".txt"
        print("Writing failure to " + file_name)
        with open(file_name, 'w') as f:
            f.write("Paramaters: ")
            f.write("Tier: " + str(generated_tier) + " Starting_Mon: " + str(generated_starting_mon) + " Starting_Cutoff: " + str(generated_starting_cutoff) + " Teammate_Cutoff: " + str(generated_teammate_cutoff) + " Generation_Mode: " + str(generated_generation_mode) + "\n")
            f.write("Exception: " + str(e) + "\n")            
            f.write("\n")        
            traceback.print_exc(file=f)
        return 1

    

# Class for representing a generated Pokemon
class Pokemon:
    def __init__(self, name, moves, item, ability, spread):
        self.name = name
        self.moves = moves
        self.item = item
        self.ability = ability
        self.spread = spread

    def __str__(self):
        return f"{self.name}: {', '.join(self.moves)}, Item: {self.item}, Ability: {self.ability}, Spread: {self.spread}"

    def __repr__(self):
        return f"{self.name}: {', '.join(self.moves)}, Item: {self.item}, Ability: {self.ability}, Spread: {self.spread}"

# Given a tier and a Pokemon, generate the moveset (Moves, Item, Ability, and Spread)
def generate_moveset(tier, mon):
    with open('downloaded_stats/moveset/' + tier + ".txt") as f:
        moveset_lines = f.readlines()

    mon_block_starting_index = -1    
    mon_block_ending_index = -1

    # Enumerate moveset lines to get Mon's moveset block
    for i, line in enumerate(moveset_lines):
        if(i < len(moveset_lines) - 1):
            next_line = moveset_lines[i + 1]                   
        if '+-' in line and mon in next_line and mon_block_starting_index == -1:            
            mon_block_starting_index = i            
        if '+-' in line and '+' in next_line and mon_block_starting_index > -1 and mon_block_ending_index == -1:            
            mon_block_ending_index = i
    mon_block = moveset_lines[mon_block_starting_index:mon_block_ending_index]

    # Enumerate mon block lines to get Abilities
    abilities_starting_index = -1
    abilities_ending_index = -1
    for i, line in enumerate(mon_block):
        if(i < len(mon_block) - 1):
            next_line = mon_block[i + 1]
        if '+-' in line and 'Abilities' in next_line and abilities_starting_index == -1:            
            abilities_starting_index = i            
        if '+-' in line and 'Items' in next_line and abilities_starting_index > -1 and abilities_ending_index == -1:            
            abilities_ending_index = i     

    abilities_lines = mon_block[abilities_starting_index:abilities_ending_index]

    # Enumerate mon block lines to get Items
    items_starting_index = -1
    items_ending_index = -1
    for i, line in enumerate(mon_block):
        if(i < len(mon_block) - 1):
            next_line = mon_block[i + 1]
        if '+-' in line and 'Items' in next_line and items_starting_index == -1:            
            items_starting_index = i            
        if '+-' in line and 'Spreads' in next_line and items_starting_index > -1 and items_ending_index == -1:            
            items_ending_index = i     

    items_lines = mon_block[items_starting_index:items_ending_index]

    # Enumerate mon block lines to get Spreads
    spreads_starting_index = -1
    spreads_ending_index = -1
    for i, line in enumerate(mon_block):
        if(i < len(mon_block) - 1):
            next_line = mon_block[i + 1]
        if '+-' in line and 'Spreads' in next_line and spreads_starting_index == -1:            
            spreads_starting_index = i            
        if '+-' in line and 'Moves' in next_line and spreads_starting_index > -1 and spreads_ending_index == -1:            
            spreads_ending_index = i     

    spreads_lines = mon_block[spreads_starting_index:spreads_ending_index]

    # Enumerate mon block lines to get Abilities
    moves_starting_index = -1
    moves_ending_index = -1
    for i, line in enumerate(mon_block):
        if(i < len(mon_block) - 1):
            next_line = mon_block[i + 1]
        if '+-' in line and 'Moves' in next_line and moves_starting_index == -1:            
            moves_starting_index = i            
        if '+-' in line and 'Teammates' in next_line and moves_starting_index > -1 and moves_ending_index == -1:            
            moves_ending_index = i     

    moves_lines = mon_block[moves_starting_index:moves_ending_index]

    abilities_potential = []
    for line in abilities_lines:
        words = line.split(' ')
        if(len(words) > 2):
            percent_index = -1
            for i, word in enumerate(words):
                if(len(word) > 0):
                    if(word[-1] == '%'):
                        percent_index = i
            if(words[2] != 'Abilities' and words[2] != '\n' and words[2] != 'Other'):
                abilities_potential.append((' '.join(words[2:percent_index]), words[percent_index][:-1]))              

    items_potential = []
    for line in items_lines:
        words = line.split(' ')
        if(len(words) > 2):
            percent_index = -1
            for i, word in enumerate(words):
                if(len(word) > 0):
                    if(word[-1] == '%'):
                        percent_index = i
            if(words[2] != 'Items' and words[2] != '\n' and words[2] != 'Other'):
                items_potential.append((' '.join(words[2:percent_index]), words[percent_index][:-1]))                
    
    spreads_potential = []
    for line in spreads_lines:
        words = line.split(' ')
        if(len(words) > 2):
            if(words[2] != 'Spreads' and words[2] != '\n' and words[2] != 'Other'):
                percent_index = -1
                if '%' in words[3]:
                    percent_index = 3
                else:
                    percent_index = 4
                spreads_potential.append((words[2], words[percent_index].replace('%','').replace('|','')))
    
    moves_potential = []
    for line in moves_lines:
        words = line.split(' ')
        if(len(words) > 2):
            percent_index = -1
            for i, word in enumerate(words):
                if(len(word) > 0):
                    if(word[-1] == '%'):
                        percent_index = i
            if(words[2] != 'Moves' and words[2] != '\n' and words[2] != 'Other' and words[2] != 'Nothing'):
                moves_potential.append((' '.join(words[2:percent_index]), words[percent_index][:-1]))

    abilities, weights = zip(*abilities_potential)
    generated_ability = random.choices(abilities, weights=[float(x) for x in weights])[0]

    items, weights = zip(*items_potential)
    generated_item = random.choices(items, weights=[float(x) for x in weights])[0]

    spreads, weights = zip(*spreads_potential)
    generated_spread = random.choices(spreads, weights=[float(x) for x in weights])[0]

    generated_moves = []
    if(len(moves_potential) > 0):
        moves, weights = zip(*moves_potential)

        weights = [i for i in weights if float(i) != float(0)]
        moves = moves[:len(weights)]
        
        if(len(moves) > 4):
            while(len(generated_moves) < 4):
                generated_move = random.choices(moves, weights=[float(x) for x in weights])[0]
                if(generated_move not in generated_moves):
                    generated_moves.append(generated_move)
        else:
            while(len(generated_moves) < len(moves)):
                generated_move = random.choices(moves, weights=[float(x) for x in weights])[0]
                if(generated_move not in generated_moves):
                    generated_moves.append(generated_move)
    else:
        generated_moves = []

    generated_mon = Pokemon(name = mon, moves = generated_moves, item = generated_item, ability = generated_ability, spread = generated_spread)
    return generated_mon

# Given a pokemon, get all the teammates for it from the moveset data
def get_moveset_teammates(tier, starting_mon):
    with open('downloaded_stats/moveset/' + tier + ".txt") as f:
        moveset_lines = f.readlines()
    mon_block_starting_index = -1    
    mon_block_ending_index = -1

    # Enumerate moveset lines to get Mon's moveset block
    for i, line in enumerate(moveset_lines):
        if(i < len(moveset_lines) - 1):
            next_line = moveset_lines[i + 1]                   
        if '+-' in line and starting_mon in next_line and mon_block_starting_index == -1:            
            mon_block_starting_index = i            
        if '+-' in line and '+-' in next_line and mon_block_starting_index > -1 and mon_block_ending_index == -1:            
            mon_block_ending_index = i            
            
        
    mon_block = moveset_lines[mon_block_starting_index:mon_block_ending_index]        
    if(len(mon_block) == 0):
        print("Moveset data for " + starting_mon + " was not found. Please try another.")
        return []
    

    # Enumerate mon block lines to get teammates
    teammates_starting_index = -1
    teammates_ending_index = -1
    for i, line in enumerate(mon_block):
        if(i < len(mon_block) - 1):
            next_line = mon_block[i + 1]
        if '+-' in line and 'Teammates' in next_line and teammates_starting_index == -1:            
            teammates_starting_index = i            
        if '+-' in line and 'Checks and Counters' in next_line and teammates_starting_index > -1 and teammates_ending_index == -1:            
            teammates_ending_index = i     

    teammates_lines = mon_block[teammates_starting_index:teammates_ending_index]

    # Isolate teammates from teammate lines
    teammates_potential = []    
    for line in teammates_lines:
        words = line.split(' ')
        
        if(len(words) > 3):                
            if('%' in words[3]):
                if(words[2] != 'Teammates' and words[2] != '\n'):
                    teammate = words[2].strip()
                    teammates_potential.append(teammate)
            else:
                if(words[2] != 'Teammates' and words[2] != '\n'):
                    teammate = str(words[2]) + " " + str(words[3])
                    teammate = teammate.strip()
                    teammates_potential.append(teammate)

    viable_pokemon = get_potential_pokemon(tier)
    teammates_potential = [x for x in teammates_potential if x in viable_pokemon]

    return teammates_potential

# The main function for generating teams
def generate_team_helper(tier, starting_mon, generation_mode, teammate_cutoff, force_generation):
    team_mons = [starting_mon]
    if(int(generation_mode) == 1):
        teammates_potential = get_moveset_teammates(tier, starting_mon)
        
        # Get potential teammates_potential via cutoff - minimum 5 because we need a full team of six
        print(teammates_potential)

        num_potential_teammates = math.ceil(len(teammates_potential) * (int(teammate_cutoff)/100))
        if(num_potential_teammates) < 5:
            num_potential_teammates = 5
        teammates_potential = teammates_potential[:num_potential_teammates]

        if(len(teammates_potential) < 5):
            teammates = teammates_potential
        else:                
            teammates = random.sample(teammates_potential, 5)
        if(teammates == []):
            return
                
        team_mons = team_mons + teammates
        team = []
        for pokemon in team_mons:
            team.append(generate_moveset(tier, pokemon))

    if(int(generation_mode) == 2):                
        while(len(team_mons) < 6):
            teammates_potential = get_moveset_teammates(tier, team_mons[-1])
            teammates_potential = list(set(teammates_potential) - set(team_mons))
            num_potential_teammates = math.ceil(len(teammates_potential) * (int(teammate_cutoff)/100))            
            teammates_potential = teammates_potential[:num_potential_teammates]
            if(len(teammates_potential) < 1):
                break
            team_mons.append(random.choice(teammates_potential))
        
        team = []
        for pokemon in team_mons:
            team.append(generate_moveset(tier, pokemon))
                
    file_name = write_to_file(team, tier)
    if(not force_generation):
        print("\nGenerated Team:")
        for mon in team:
            print(mon)
        print("Team saved to " + file_name)
        print("You can copy it from there to import and use on play.pokemonshowdown.com!")
        print("Note: It is advised to look over the team and make final adjustments.")
    

# Write a generated team to a file
def write_to_file(team, tier):
    folder = 'generated_teams/' + tier + '/'
    if not os.path.exists(folder):
        os.makedirs(folder)

    files_count = len(os.listdir(folder))
    file_name = folder + tier + "-" + str((files_count + 1)) + ".txt"
    with open(file_name, 'w') as f:
        for mon in team:
            if(mon.item != "Nothing"):
                f.write(mon.name + " @ " + mon.item + '\n')
            else:
                f.write(mon.name + "\n")

            if(mon.ability != "No Ability"):
                f.write("Ability: " + mon.ability + '\n')

            spread_list = mon.spread.split(':')
            nature = spread_list[0]
            stats = spread_list[1]
            stats_list = stats.split('/')

            f.write("EVs: " + str(stats_list[0]) + " HP / " + str(stats_list[1]) + " Atk / " + str(stats_list[2]) + " Def / " + str(stats_list[3]) + " Spa / " + str(stats_list[4]) + " SpD / " + str(stats_list[5]) + " Spe\n" )
            f.write(str(nature) + " Nature\n")
            
            for move in mon.moves:
                f.write("- " + str(move) + "\n")
            
            f.write("\n")

    return file_name    


    

