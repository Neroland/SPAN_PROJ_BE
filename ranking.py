import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from ast import literal_eval

import os.path

# Fetch the service account key JSON file contents
cred = credentials.Certificate('span-backend-project-1-fce35fc4c9b3.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://span-backend-project-1-default-rtdb.europe-west1.firebasedatabase.app/'
})

#split the team data into "Team Name" and "Team Score"
def team_split(s):
    head = s.rstrip('0123456789')
    tail = s[len(head):]
    return head, tail

def update_data_from_db(reference_name):
    # As an admin, the app has access to read and write all data, regradless of Security Rules
    ref_data = db.reference(reference_name)
    return ref_data

def print_points(data):
    # This will take the array, split it up and print each team in order the winning statistics
    for number, team in enumerate(data):
        print(str(number+1)+".", team[0]+',',team[1],'pts')
    print()

def start(run_me):
    print("START")

    # Added this function for the unit testing but is not needed. The code can be reused but it would have been easier to use | ref = db.reference("AllTournaments") | in its place.
    ref=update_data_from_db('AllTournaments')

    while(run_me):
        # Get option from user
        menu = input("Options:\n\n1 - Add Tournament Results\n2 - View Previous Tournaments\n3 - Delete Past Tournament\n\n9 - Exit\n\n")

        # Menu 1 is for the Adding of Results
        if(menu=='1'):
            # Get file location of scores
            results = input("Please input file location:\n")

            # Checks if it can access the file
            if(os.path.exists(results)):
                print("Here are the results:\n")
                # Initializing data as empty/zero
                points=[]
                team_1_points = 0
                team_2_points = 0
                # Reading the data from the file
                with open(results, "r") as f:
                    # Reads data line by line
                    for line in f:
                        # Splits each line into seperate arrays
                        teams = line.strip().split(", ")
                        # Splits the seperate arrays into Team Name and Team Score
                        team_1 = team_split(teams[0])
                        team_1_name = team_1[0].rstrip()
                        team_2 = team_split(teams[1])
                        team_2_name = team_2[0].rstrip()

                        # Calculates points based of the game played
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
                        
                        # Zero out count and set team indexes to out of range
                        count=0
                        team_1_index = -1
                        team_2_index = -1

                        # Checks to see if the team is in the array and sets it's indexes accordingly
                        for teams in points:
                            if teams[0]==team_1_name:
                                team_1_index = count
                                teams[1] = teams[1] + team_1_points 
                            if teams[0]==team_2_name:
                                team_2_index = count
                                teams[1] = teams[1] + team_2_points
                            count += 1
                        
                        # If no team is found in the array, the team will be added to the array
                        if team_1_index==-1:
                            points.append([team_1_name,team_1_points])
                        
                        if team_2_index==-1:
                            points.append([team_2_name,team_2_points])
                
                # First Lamda function sorts the teams in alphabetical order
                points.sort(key=lambda row:(row[0]))
                # Second Lamda function sorts the teams in numerical order (Winning team first)
                points.sort(key=lambda row:(row[1]), reverse=True)

                # This fuction prints the points of the array as a "Table" to see who won
                print_points(points)

                # Sends the array data (of points) to the server/database
                new_tournament = ref.child('Tournaments')
                new_tournament.push(str(points))
        
        # Menu 2 is for viewing all the past tournaments (The tournaments listed in the database)
        if(menu=='2'):
            # Gets list of all past tournaments
            past_tournaments = ref.get()

            # It will not do anything if there are no tournaments
            if(past_tournaments==None):
                print("No previous tournament information available\n")
            else:
                # Here it will print all the previous tournaments
                print("Previous Tournaments:")
                # First we create a dictionary of all the data
                temp = dict(past_tournaments)
                # I then take the data and extract just the tournaments
                all_tournaments = list(temp["Tournaments"])
                # Count me just numbers the tournaments instead of the random ids generated by firebase
                count_me = 1
                for key in all_tournaments:
                    # The key is the random id generated by firebase
                    print("\nTournament Number "+str(count_me)+"\n")        
                    temp_str = ''
                    # Here it makes a string verstion of the array to get the data from the dictionary
                    for i in temp["Tournaments"][key]:
                        temp_str = temp_str + str(i)

                    # Here it parses the string and makes it into an array
                    past_tournament_data = literal_eval(temp_str)

                    # Here the function yet again prints the points of the array as a "Table" to see who won
                    print_points(past_tournament_data)
                    
                    # Onto the next tournament :)
                    count_me+= 1

        # Menu 3 will allow the user to delete tournamets from the database
        if(menu=='3'):
            # Get the tournament data from the database
            ref = update_data_from_db('AllTournaments')
            past_tournaments = ref.get()

            # Checks whether there are any tournaments available in the database
            if past_tournaments!=None:
                # Creates a dictionary of tournaments available in the database
                temp = dict(past_tournaments)
                # Extracst just the tournament data
                all_tournaments = list(temp["Tournaments"])
                # Get the user to chose which tournament to delete
                delete_tournament = input("Which tournament would you like to delete? (Enter the number, eg: 3)\n")
                # Validates that the tournament exists
                if((int(delete_tournament)-1 > len(all_tournaments)-1)or(int(delete_tournament) < 1)):
                    print("Please enter a valid tournament number.\n")
                else:
                    # Confirms that the user actually wants to delete the tournament
                    confirm = input("Are you sure you want to delete tournament# "+delete_tournament+"? (Y/n)\n")
                    if(confirm == "Y"):  
                        # Deletes the tournament
                        ref = db.reference('AllTournaments')
                        temporary = ref.child('Tournaments').child(str(all_tournaments[int(delete_tournament)-1]))
                        temporary.delete()
                        print("\nSuccessfully deleted\n")
            else:
                print("No tournaments to delete, returning to menu...\n")

        # Menu 9 exits the program
        if(menu=='9'):
            run_me=False
    
    print("END")
    exit()

if __name__ == "__main__":
    start(True)