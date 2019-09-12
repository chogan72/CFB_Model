import csv
import os

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

#Stores old directory and changes current
first_directory = os.getcwd()
change_directory('/Database/')

#Headings
boxscore_head = ['Year', 'Week', 'Home', 'Home Score', 'Away', 'Away Score', 'ID']
win_head = ['Year', 'Team', 'Win Totals', 'Actual Wins', 'Actual Losses']
spread_head = ['Year','Week','Home','Away','Spread','Total']

#Create lists of database
boxscore_list = database_reader('CFB-Boxscore-Database.csv', boxscore_head)
win_list = database_reader('CFB-Win-Total-Database.csv', win_head)
spread_list = database_reader('CFB-Spread-Database.csv', spread_head)

for team in win_list:
    OR = 0
    OOR = 0
    SOS = 0
    OR_Games = 0
    OOR_Games = 0
    for game in boxscore_list:
        if game[0] == team[0]:
            if team[1] == game[2]:
                for t2 in win_list:
                    if t2[0] == team[0] and t2[1] == game[4]:
                        OR += int(t2[3])
                        OR_Games += int(t2[3]) +int(t2[4])
                        for g2 in boxscore_list:
                            if g2[2] == t2[1] and g2[0] == team[0]:
                                for t3 in win_list:
                                    if g2[4] == t3[1] and t3[0] == team[0]:
                                        OOR += int(t3[3])
                                        OOR_Games += int(t3[3]) +int(t3[4])
                            elif g2[4] == t2[1] and g2[0] == team[0]:
                                for t3 in win_list:
                                    if g2[2] == t3[1] and t3[0] == team[0]:
                                        OOR += int(t3[3])
                                        OOR_Games += int(t3[3]) +int(t3[4])
                                        
            elif team[1] == game[4]:
                for t2 in win_list:
                    if t2[0] == team[0] and t2[1] == game[2]:
                        OR += int(t2[3])
                        OR_Games += int(t2[3]) +int(t2[4])
                        for g2 in boxscore_list:
                            if g2[2] == t2[1] and g2[0] == team[0]:
                                for t3 in win_list:
                                    if g2[4] == t3[1] and t3[0] == team[0]:
                                        OOR += int(t3[3])
                                        OOR_Games += int(t3[3]) +int(t3[4])
                            elif g2[4] == t2[1] and g2[0] == team[0]:
                                for t3 in win_list:
                                    if g2[2] == t3[1] and t3[0] == team[0]:
                                        OOR += int(t3[3])
                                        OOR_Games += int(t3[3]) +int(t3[4])

    SOS = ((2*(OR/OR_Games))+(OOR/OOR_Games))/3
    print(team[0],team[1],SOS)
