import re
import csv
import os

first_dir = os.getcwd()
def change_directory(folder):
    #Change Databse Directory
    dirpath = os.getcwd()
    dirpath = dirpath + folder
    os.chdir(dirpath)

def database(path, item_list):
    #Writes Players to CSV file
    with open(path + '.csv', 'a', newline='') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerow(item_list)

def database_reader(current_file, head_list):
    #Read Database Files
    database_players = []
    with open(current_file) as csvfile:
        reader = csv.DictReader(csvfile)
        #Reads rows of CSV file
        for row in reader:
            index = 0
            player_list = []
            #Sets row to proper information
            while index < len(row):
                player_list.append(row[head_list[index]])
                index += 1
            database_players.append(player_list)
    return(database_players)

change_directory('\\Database\\')

game_data = ['Year', 'Team', 'Win Totals', 'Actual Wins']
vi_list = []
database('CFB-Win-Total-Database', game_data)

head_list = ['Year', 'Team', 'Win Total', 'Actual Wins']
game_log = database_reader('Win-Totals.csv', head_list)

box_list = ['Year','Week','Home','Home Score','Away','Away Score']
box_log = database_reader('CFB-Boxscore-Database.csv', box_list)

for team in game_log:
    for score in box_log:
        if team[0] == score[0]:
            if team[1] == score[2]:
                if int(score[3]) > int(score[5]):
                    team[3] = int(team[3]) + 1
            elif team[1] == score[4]:
                if int(score[5]) > int(score[3]):
                    team[3] = int(team[3]) + 1
                    
    database('CFB-Win-Total-Database', team)
