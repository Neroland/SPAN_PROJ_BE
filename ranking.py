from typing import Counter
from unittest import result
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import os.path

def team_split(s):
    head = s.rstrip('0123456789')
    tail = s[len(head):]
    return head, tail

def startUp(run_me):
    print("START")
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('span-backend-project-1-fce35fc4c9b3.json')
    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://span-backend-project-1-default-rtdb.europe-west1.firebasedatabase.app/'
    })

    # As an admin, the app has access to read and write all data, regradless of Security Rules
    ref = db.reference('restricted_access/secret_document')
    past_tournaments = ref.get()
    
    while(run_me):
        menu = input("Options:\n\n1 - Add Tournament Results\n2 - List Past Tournaments\n\n9 - Exit\n")
        print()
        #menu='1'
        if(menu=='1'):
            results = input("Please input file location:\n")
            print()
            #results = 'scores.txt'
            if(os.path.exists(results)):
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

                points.sort(key=lambda row:(row[1]), reverse=True)
 
                for number, team in enumerate(points):
                    print(number+1, team[0]+',',team[1],' pts')
                
                print()
                    
        if(menu=='2'):
            if(past_tournaments==None):
                print("No past tournament information available\n")
            else:
                print(past_tournaments)

        if(menu=='9'):
            run_me=False
    
    print("END")
    exit()

if __name__ == "__main__":
    startUp(True)