import bs4
import requests
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

game_data = ['Year', 'Week', 'Home', 'Away', 'Spread', 'Total']
vi_list = []
database('CFB-Spread-Database', game_data)

fix_list = ['Win Total','2019 Spread','2018 Spread']
fix_log = database_reader('CFB-Team-Fix.csv', fix_list)

head_list = ['Date','Rot','VH','Team','1st','2nd','3rd','4th','Final','Open','Close','ML','2H']
for year in range(2010,2019):
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
            game_data[2] = game[3]
            if game_data[4] == 'NL' or game[10] == 'NL':
                game_data[4] = ''
                game_data[5] = ''

            else:
                if game_data[4] == 'pk':
                    game_data[4] = 0
                if game[10] == 'pk':
                    game[10] = 0
                if '-' in str(game_data[4]):
                    split = re.split('-', str(game_data[4]))
                    game_data[4] = split[0]
                if '-' in str(game[10]):
                    split = re.split('-', str(game[10]))
                    game[10] = split[0]
                
                if float(game_data[4]) < float(game[10]):
                    game_data[5] = game[10]
                elif float(game_data[4]) > float(game[10]):
                    game_data[5] =  game_data[4]
                    game_data[4] = '-' + str(game[10])
                
            game_data[1] = game[0]
            for tfix in fix_log:
                if game_data[2] == tfix[2]:
                    game_data[2] = tfix[1]
                elif game_data[3] == tfix[2]:
                    game_data[3] = tfix[1]
            today = datetime.date(year,int(game[0][:-2]),int(game[0][-2:])).weekday()
            if today < last_week:
                if year == 2016 and week == 1 and week_fix == 0 or year == 2017 and week == 1 and week_fix == 0 or year == 2018 and week == 1 and week_fix == 0 or year == 2019 and week == 1 and week_fix == 0:
                    week_fix = 1
                else:
                    week += 1
            game_data[1] = week
            if 'Army' in game_data[2] and 'Navy' in game_data[3] or 'Army' in game_data[3] and 'Navy' in game_data[2]:
                week += 1
                last_week = -1
                AN = 1
            elif AN == 0:
                last_week = today
            database('CFB-Spread-Database', game_data)
            index = 0
        elif index == 0:
            game_data[3] = game[3]
            game_data[4] = game[10]
            index = 1

        
#beautifulsoup4 link
os.chdir(first_dir)
change_directory('\\Database\\')
for year in range(2019,2020):
    for week in range(1,14):
        BS_link = 'http://www.vegasinsider.com/college-football/matchups/matchups.cfm/week/' + str(week) + '/season/' + str(year)
        sauce = requests.get(BS_link)
        soup = bs4.BeautifulSoup(sauce.text, 'html.parser')
        for player in soup.find_all('td', {"class":["viCellBg2 cellBorderL1 cellTextNorm padCenter", "viHeaderNorm"]}):

            #Splits needed information
            gdata = (player.text)
            gdata = re.split('>|<', gdata)
            gdata = gdata[0].strip()

            #Checks For Home and Away Teams
            if len(gdata) > 5:
                gdata = re.split(' @ ', gdata)
                game_data[2] = gdata[1]
                game_data[3] = gdata[0]
                vi_list = []
                index = 0
                max_len = 100

            #Adds stats to temp list
            else:
                vi_list.append(gdata)
                index += 1

            #Check length of temp list
            if index == 8:
                if '%' in vi_list[6] or '/' in vi_list[6] or vi_list[6] == '':
                    max_len = 8
                else:
                    max_len = 10

            #Writes Spread and Total to Game list
            if len(vi_list) == max_len:
                if '-' in vi_list[1]:
                    game_data[4] = vi_list[1][1:]
                elif vi_list[1] == 'PK':
                    game_data[4] = '0'
                elif '-' not in gdata:
                    game_data[5] = vi_list[1]

                #Long List
                if max_len == 10:
                    if '-' in vi_list[6]:
                        game_data[4] = vi_list[6]
                    elif vi_list[6] == 'PK':
                        game_data[4] = '0'
                    elif '-' not in gdata:
                        game_data[5] = vi_list[6]

                #Short List
                elif max_len == 8:
                    if '-' in vi_list[5]:
                        game_data[4] = vi_list[5]
                    elif vi_list[5] == 'PK':
                        game_data[4] = '0'
                    elif '-' not in gdata:
                        game_data[5] = vi_list[5]

                #Write Year and Week
                game_data[0] = year
                game_data[1] = week
                
                #Writes list to CSV file
                database('CFB-Spread-Database', game_data)
                game_data = ['','','','','','']

