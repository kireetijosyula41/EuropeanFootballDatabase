# intermediatepython-finalproj-kireetijosyula41

Section 1: Project Proposals 

Project idea #1: 
I would want to develop an API that helps doctors, specifically neuroscientists, analyze data from relevant brain studies, by following: 
1. Accessing brain imaging data from EEG, fMRI or MRI scans, and returning lists of categorized data based on regions of interest for each scan
2. Allow optional filtering based on scan methods and brain region
3. Return a list of studies directly or indirectly related to a query input brain region name (e.g: hippocampus, amygdala) or a disease (e.g Alzheimer’s, Parkinson’s, etc.) that would be specified on input
4. Take a list of cognitive functions (such as memory, attention, gaze, etc.) and return lists that contain the relevant imaging data for tests of those tasks
5. Take a dataset ID as a string or an integer, and provide the user with the overview or hypothesis of the experiment
   
Project idea #2: 
I would maybe want to develop a European football player performance analysis API that can be given to fans of european football, so that they may be able to track their favorite stars and their performances
1. Returning a list of matches played by a team between some queried dates or by some queried opponent. There are online databases that can hold this kind of information (most notably Opta)
2. Can take in a name of a player, and return their performance stats individually, as well as their percentile performance relative to other players from similar positions
3. Returning a list containing the recent injury history of a given player when queried with its name, where the data holds the type of injury and the duration of the injury
4. Returning a list containing the recent performance match data to predict performance on a certain match in the future (THIS ONE IS REALLY HAIRY)!



Section 2: Project Timeline 

By the end of week 4, I will have looked into possible soccer database references (FBref, FiveThirtyEight, Sofascore) that can give me access to player data such as names, clubs, goals, assists, nationalities, positions, as well as matches
By the end of week 5, I will try to have a setup for the homescreen, where a person can query a specific team or player
By the end of week 6, I will work on the implementation of the team, which will return the team's last 10 matches, their current form, their players and kit numbers, and their upcoming matches with appropriate times.
By the end of week 7, I will work on the implementation of the players. When a player is queried, I will have the player name, nationality, position, and team displayed. From there, if the user wants more information (injury history, goals, assists, etc.), they can access through clickable links. 
By the end of week 8, I will have a "ratings" scheme down for players in a particular match, so that a user can click on a player from a match, and give the player a rating from 1 to 10 (float1 number). 
By the end of week 9, I try to have the percentile performance of players on certain stats (goals scored, assists made, passes completed, defensive actions), displayed on the player's home page. This will be relevant for the current season. 