import Functions
import os

os.system('cls')
print("Welcome to the Pokemon Showdown Team Generator!")
print("_______________________________________________")
print("We will begin by gathering the necessary data.")

stats_url = "https://www.smogon.com/stats/"

data_chosen = False
while(not data_chosen): 
    print('\n')   
    print("Smogon data begins at 2014-11. Enter a year and month combo in the format yyyy-mm,")
    year_month = input("or simply press enter to use the currently gathered data:")    
    if(year_month == ""):
        if(len(os.listdir("downloaded_stats")) == 0):
            print("There is no currently gathered data")                    
        else:
            data_chosen = True
            year_month = "Existing Data"
    else:
        try:
            data_chosen = True        
            Functions.get_data(stats_url + str(year_month) + '/')
        except Exception as e:            
            data_chosen = False
            print(e)
            print("That data was not found. Try a different year-month combo.")

os.system('cls')
print("Data Gathered - " + str(year_month))

Functions.cull_empty_data()

exit_bool = False

chosen_tier = ""
chosen_starting_mon = ""
chosen_starting_popularity_cutoff = ""
chosen_teammate_popularity_cutoff= ""
chosen_generation_mode = ""
chosen_generation_mode_int = 0

int_choice = 0
while(not exit_bool):
    
    if(not int_choice == "1" and not int_choice == '7' and not int_choice == '8'):
        os.system('cls')
    print()
    print("Options:")
    print("1. View Tiers")
    print("2. Select Tier - " + str(chosen_tier))
    print("3. Select Starting Pokemon - " + str(chosen_starting_mon))
    print("4. Select Starting Pokemon Popularity Cutoff - " + str(chosen_starting_popularity_cutoff) + "%")
    print("5. Select Teammate Popularity Cutoff - " + str(chosen_teammate_popularity_cutoff) + "%")
    print("6. Select Generation Mode - " + str(chosen_generation_mode))
    print("7. Generate Team")
    print("8. Bulk Generation")
    print("9. Exit")
    print()
    int_choice = input("Enter your choice:")

    if(int_choice == "1"):
        Functions.print_tiers()

    if(int_choice == "2"):
        chosen_tier = Functions.select_tier(chosen_starting_mon)

    if(int_choice == "3"):
        chosen_starting_mon = Functions.select_starting_pokemon(chosen_tier)

    if(int_choice == "4"):
        chosen_starting_popularity_cutoff = Functions.select_starting_popularity_cutoff()

    if(int_choice == "5"):
        chosen_teammate_popularity_cutoff = Functions.select_teammate_popularity_cutoff()

    if(int_choice == "6"):
        chosen_generation_mode_int = Functions.select_generation_mode()
        if(chosen_generation_mode_int == "1"):
            chosen_generation_mode = "Centered"
        else:
            chosen_generation_mode = "Chained"

    if(int_choice == "7"):
        try:
            Functions.generate_team(chosen_tier, chosen_starting_mon, chosen_starting_popularity_cutoff, chosen_teammate_popularity_cutoff, chosen_generation_mode_int, False)
        except Exception as e:
            print("Team Generation Failed")
            print("Exception: " + str(e))
    
    if(int_choice == "8"):
        chosen_generation_count = Functions.select_bulk_generation()                
        fail_count = 0        
        for i in range(int(chosen_generation_count)):
            
            failure_status = Functions.generate_team(chosen_tier, chosen_starting_mon, chosen_starting_popularity_cutoff, chosen_teammate_popularity_cutoff, chosen_generation_mode_int, True)
            if(failure_status == 1):
                fail_count += 1
                         
        
        print("Generation Finished")
        print("Failed Teams: " + str(fail_count))

    if(int_choice == "9"):
        exit_bool = True

    

