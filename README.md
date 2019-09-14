# CFB Model

This analysis weekly spreads to determine an edge. This project is based off of my NFL_Model(https://github.com/chogan72/NFL_Model).


## Current Status

As of right now the model is ready to go for the 2019 Season.


## Database Files

* Spread Scraper
  * This is used to scrape http://www.vegasinsider.com/college-football/matchups/matchups.cfm/week/1/season/2019 to find the spreads and totals for 2019 games.
  * Spreads before 2019 are found using the SBR Database(/Database/SBR/).
  * This is used to create Database/CFB-Spread-Database.csv (2010-2019)
* Boxscore API
  * This uses the SBR Database(/Database/SBR/) to pull team stats by games. 
  * This is used to create the files in Database/CFB-Boxscore-Database.csv (2010-2019)
* Win Total Scraper
  * This is used to scrape /Database/Win-Totals.csv to find season win totals.
  * This is used to scrape /Database/CFB-Boxscore-Database.csv to find season actual wins.
  * This is used to create Database/CFB-Win-Total-Database.csv (2014-2019)
* Strength of Schedule
  * This is used to scrape /Database/CFB-Boxscore-Database.csv to find strength of schedule.
  * This is used to create Database/SOS-Model.csv (2014-2019)
  
SBR Database files are pulled from: https://www.sportsbookreviewsonline.com/scoresoddsarchives/ncaafootball/ncaafootballoddsarchives.htm
  
  
## Models

### Weekly Win Total Model

#### Purpose

* This model adjusts the Vegas win total based on Pythagorean Differential and Weekly Point Differential
* This model is loosely based of this article by Adam Chernoff: https://medium.com/@adamchernoff/how-to-create-and-use-nfl-power-ratings-to-beat-the-point-spread-3fa4c3ecdc22
* And this article by Ed Feng: https://thepowerrank.com/guide-cfb-rankings/ 

#### Pythagorean Differential

* If it is Week 1 these equations are run

<p align="center"> Pythagorean Expectation = (Points For^2.37 / (Points For^2.37 + Points Against^2.37)) * Games_Played</p>

<p align="center"> Pythagorean Differential = Last Year Wins - Pythagorean Expectation </p>

<p align="center"> Adjusted Win Total = Vegas Win Total - Pythagorean Differential </p>

#### Point Differential

* After every week the win totals are adjusted
* After a win, Margin of Victory - Spread * .01 is added to the win total
* After a loss, Margin of Victory - Spread * .01 is subtracted from the win total

#### Strength of Schedule

* If week < 10
<p align="center">  SOS_This_Year = (week * .1) * SOS_This_Year</p>
<p align="center">  SOS_Last_Year = (1 - (week * .1)) * SOS_Last_Year</p>
<p align="center">  Current_Win_Total * ((SOS_This_Year + SOS_Last_Year) * 3)</p>

* Else
<p align="center">  Current_Win_Total * (SOS_This_Year*3)</p>

### Prediction Model

* This is used to find the edge

<p align="center"> Home Adjusted Spread = (Away Adjusted Win Total - Home Adjusted Win Total) * 2 - 3 </p>

<p align="center"> Advantage = Real Spread - Home Adjusted Spread </p>

* If the Advantage is negative take the Away Team
* If the Advantage is positive take the Home Team
* If the Advantage is greater than 20 or less than -20 then it is considered a good bet

## Historical Test

#### Purpose

* Historical Prediction Model and Historical Win Total Model pull data for games between 2015 and 2018

#### Historical Test

* Analysis of past seasons to determine the quality of the models
* Current Margin of Victory multiplier .01
* Current best bet is over 20
