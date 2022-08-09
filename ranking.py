from unittest import result
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from ast import literal_eval

import os.path

def team_split(s):
    head = s.rstrip('0123456789')
    tail = s[len(head):]
    return head, tail

def start(run_me):
    print("START")

    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('span-backend-project-1-fce35fc4c9b3.json')
    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://span-backend-project-1-default-rtdb.europe-west1.firebasedatabase.app/'
    })
    # As an admin, the app has access to read and write all data, regradless of Security Rules
    ref = db.reference('AllTournaments')

    while(run_me):
        menu = input("Options:\n\n1 - Add Tournament Results\n2 - View Previous Tournaments\n3 - Delete Past Tournament\n\n9 - Exit\n")
        print()
        #menu='2'
        if(menu=='1'):
            results = input("Please input file location:\n")
            print()
            #results = 'scores.txt'
            if(os.path.exists(results)):
                print("Here are the results:\n")
                points=[]
                team_1_points = 0
                team_2_points = 0
                with open(results, "r") as f:
                    for line in f:
                        teams = line.strip().split(", ")
                        team_1 = team_split(teams[0])
                        team_1_name = team_1[0].rstrip()
                        team_2 = team_split(teams[1])
                        team_2_name = team_2[0].rstrip()

                        calc = int(team_1[1])-int(team_2[1])
                        if(calc==0):
                            team_1_points = 1
                            team_2_points = 1
                        if(calc>0):
                            team_1_points = 3
                            team_2_points = 0
                        if(calc<0):
                            team_1_points = 0
                            team_2_points = 3
                        
                        count=0
                        team_1_index = -1
                        team_2_index = -1

                        for teams in points:
                            if teams[0]==team_1_name:
                                team_1_index = count
                                teams[1] = teams[1] + team_1_points 
                            if teams[0]==team_2_name:
                                team_2_index = count
                                teams[1] = teams[1] + team_2_points
                            count += 1
                        
                        if team_1_index==-1:
                            points.append([team_1_name,team_1_points])
                        
                        if team_2_index==-1:
                            points.append([team_2_name,team_2_points])
                            
                points.sort(key=lambda row:(row[0]))
                points.sort(key=lambda row:(row[1]), reverse=True)

                #print(points)
 
                for number, team in enumerate(points):
                    print(str(number+1)+".", team[0]+',',team[1],'pts')

                new_tournament = ref.child('Tournaments')
                new_tournament.push(str(points))
                
                print()
    
            #run_me=False
                    
        if(menu=='2'):
            past_tournaments = ref.get()

            if(past_tournaments==None):
                print("No previous tournament information available\n")
            else:
                print("Previous Tournaments:")
                temp = dict(past_tournaments)
                all_tournaments = list(temp["Tournaments"])
                count_me = 1
                for key in all_tournaments:
                    print("\nTournament Number "+str(count_me)+"\n")        
                    temp_str = ''

                    for i in temp["Tournaments"][key]:
                        temp_str = temp_str + str(i)

                    past_tournament_data = literal_eval(temp_str)
                    #print(past_tournament_data)

                    for number, team in enumerate(past_tournament_data):
                        print(str(number+1)+".", team[0]+',',team[1],'pts')
                    count_me+= 1
                    print()
                
            #run_me=False

        if(menu=='3'):
            past_tournaments = ref.get()
            if past_tournaments!=None:
                temp = dict(past_tournaments)
                all_tournaments = list(temp["Tournaments"])
                #print(all_tournaments)
                delete_tournament = input("Which tournament would you like to delete? (Enter the number, eg: 1)\n")
                if((int(delete_tournament)-1 > len(all_tournaments)-1)or(int(delete_tournament) < 1)):
                    print("Please enter a valid tournament number.\n")
                else:
                    #print(all_tournaments[int(delete_tournament)-1])
                    confirm = input("Are you sure you want to delete tournament# "+delete_tournament+"? (Y/n)\n")
                    if(confirm == "Y"):  
                        ref = db.reference('AllTournaments')
                        temporary = ref.child('Tournaments').child(str(all_tournaments[int(delete_tournament)-1]))
                        temporary.delete()
                        print("\nSuccessfully deleted\n")
            else:
                print("No tournaments to delete, returning to menu...\n")


        if(menu=='9'):
            run_me=False
    
    print("END")
    exit()

if __name__ == "__main__":
    start(True)