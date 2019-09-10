import re
import csv
import os
import datetime

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

game_data = ['Year', 'Week', 'Home', 'Home Score', 'Away', 'Away Score']
vi_list = []
database('CFB-Boxscore-Database', game_data)

fix_list = ['Win Total','2019 Spread','2018 Spread']
fix_log = database_reader('CFB-Team-Fix.csv', fix_list)

head_list = ['Date','Rot','VH','Team','1st','2nd','3rd','4th','Final','Open','Close','ML','2H']
for year in range(2010,2020):
    week = 0
    AN = 0
    last_week = 7
    week_fix = 0
    change_directory('\\SBR\\')
    game_data[0] = year
    game_log = database_reader('ncaa football ' + str(year) + '.csv', head_list)
    os.chdir(first_dir)
    change_directory('\\Database\\')
    index = 0
    for game in game_log:
        if index == 1:
            game_data[4] = game[3]
            game_data[5] = game[8]
            for tfix in fix_log:
                if game_data[2] == tfix[2]:
                    game_data[2] = tfix[1]
                elif game_data[4] == tfix[2]:
                    game_data[4] = tfix[1]
            today = datetime.date(year,int(game[0][:-2]),int(game[0][-2:])).weekday()
            if today < last_week:
                if year == 2016 and week == 1 and week_fix == 0 or year == 2017 and week == 1 and week_fix == 0 or year == 2018 and week == 1 and week_fix == 0 or year == 2019 and week == 1 and week_fix == 0:
                    week_fix = 1
                else:
                    week += 1
            game_data[1] = week
            if 'Army' in game_data[2] and 'Navy' in game_data[4] or 'Army' in game_data[4] and 'Navy' in game_data[2]:
                week += 1
                last_week = -1
                AN = 1
            elif AN == 0:
                last_week = today
            database('CFB-Boxscore-Database', game_data)
            index = 0
        elif index == 0:
            game_data[2] = game[3]
            game_data[3] = game[8]
            index = 1
