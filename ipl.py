import pandas as pd
import numpy as np
import json


ipl = pd.read_csv('ipl_deliveries.csv')
df = pd.read_csv('iplv1.csv')
# name_replace = {'Delhi Daredevils': 'Delhi Capitals',
#                 'Kings XI Punjab': 'Punjab Kings',
#                 }
win_replace = {'Rising Pune Supergiants':'Rising Pune Supergiant'}
df['WinningTeam'].replace(win_replace,inplace=True)
ipl['batter'].replace({'RG Sharma':'R Sharma'},inplace=True)
ipl['player_out'].replace({'RG Sharma':'R Sharma'},inplace=True)

df1 = pd.merge(ipl,df[['ID','Season']],how='inner',on='ID')


def teams_name():
    teams =  list(df['Team1'].unique())
    team_dict = {
        'teams':teams
    }
    return team_dict

def team1Vsteam2(team1,team2):
    t1 = df[((df['Team1'] == team1) & (df['Team2'] == team2)) | ((df['Team2'] == team1) & (df['Team1'] == team2))] 
    d = {}
    total_matches = t1.shape[0]
    win = t1['WinningTeam'].value_counts() 
    draw = total_matches - (win.values[0] + win.values[1])
    playerofmatch = t1['Player_of_Match'].value_counts()
    d['Total Matches'] = str(t1.shape[0]) 
    d[win.index[0]] = str(win.values[0])
    d[win.index[1]] = str(win.values[1])
    d['Most player of match'] = playerofmatch.index[0]
    d['Draw'] = str(draw)
    return json.dumps(d)


def team_record(team):
    t1 = df[(df['Team1'] == team) | (df['Team2'] == team )]
    wins = t1[t1['WinningTeam'] == team]
    loss = t1[t1['lossingTeam'] == team]
    final = t1[t1['MatchNumber'] == 'Final']
    trophy = final[final['WinningTeam']  == team ]
        
    draw = t1.shape[0] - (wins.shape[0] + loss.shape[0] )
    win_per = round(wins.shape[0]/t1.shape[0] * 100,2)
    d = {}
    d['Number of Trophies Won'] = str(trophy.shape[0])
    d['Total Matches'] = str(t1.shape[0])
    d['Total Wins'] = str(wins.shape[0])
    d['Tota loss']  = str(loss.shape[0])
    d['Win%'] = str(win_per)
    d['Draws'] = str(draw)
   
    return json.dumps(d)


df1['IsBatsmanBall'] = df1['extra_type'].apply(lambda x: 1 if x != 'wides' else 0)

def batsman_record(batter):
    batsman  = df1[df1['batter'] == batter].copy()
    l = batsman.groupby('ID')['batsman_run'].sum().to_list()
    batsman['IsBatsmanOut'] = batsman.batter == batsman.player_out
    batsman_runs = batsman['batsman_run'].sum()
    batsman_ballface = batsman['IsBatsmanBall'].sum()
    strike_rate = round(batsman_runs/batsman_ballface * 100,2)
    batsman_out = batsman['IsBatsmanOut'].sum()
    average = round(batsman_runs/batsman_out,2)
    s = batsman[batsman['batsman_run'] == 6]
    f = batsman[batsman['batsman_run'] == 4]
    sixes = s['batsman_run'].count()
    fours = f['batsman_run'].count()
    highest_run = batsman.groupby(['Season','ID'])[['batsman_run']].sum()[['batsman_run']].max()
    matches = batsman['ID'].nunique()
    d = {}

    d['Innings'] = str(matches)
    d['Runs'] = str(batsman_runs)
    d['Highest Score'] = str(highest_run.values[0])
    d['Avg'] = str(average)
    d['Strike Rate'] = str(strike_rate)
    d['Sixes'] = str(sixes)
    d['Fours'] = str(fours)
    d['30s'] = 0
    d['50s'] = 0
    d['100s'] = 0


    for run in l:
        if  30 <= run < 50:
            d['30s'] +=1
        
        elif 50 <= run < 100:
            d['50s'] += 1
        
        elif run >= 100:
            d['100s'] +=1
    d['30s'] = str(d['30s'])
    d['50s'] = str(d['50s'])
    d['100s'] = str(d['100s'])
    
    return json.dumps(d)

df1['IsbowlerWicket'] = df1['kind'].apply(lambda x: 1 if x in ['caught','stumped','caught and bowled','bowled','lbw','hit wicket'] else 0)
df1['IslegalBall'] = df1['extra_type'].apply(lambda x: 0 if x in ['noballs','wides'] else 1)
df1['IsbowlerRuns'] = df1['extra_type'].apply(lambda x: 0 if x in ['legbyes','byes'] else 1) * df1['total_run']

def bowler_records(bowler): 
    b = df1[df1['bowler'] == bowler].copy()
    overs = b.groupby(['ID','overs'], as_index=False)['total_run'].sum()
    record = b.groupby('ID').agg({
            'IsbowlerRuns': 'sum',
            'IslegalBall':'sum',
            'IsbowlerWicket':'sum'
        })
    best_figures = record[record['IsbowlerWicket'] == record['IsbowlerWicket'].max()][['IsbowlerWicket','IsbowlerRuns']].apply(lambda x: str(x['IsbowlerWicket']) + '/' + str(x['IsbowlerRuns']),axis=1).values[0]
    d = {}
    total_innings = record.shape[0]
    total_balls = record['IslegalBall'].sum()
    total_runs = record['IsbowlerRuns'].sum()
    total_wickets = record['IsbowlerWicket'].sum()
    maidens = overs[overs['total_run'] == 0].shape[0]
    strite_rate = round(total_balls/total_wickets,2) 
    avg = round(total_runs/total_wickets,2)
    eco = round(total_runs/total_balls*6,2)
    d['Innings'] = str(total_innings)
    d['Balls'] = str(total_balls)
    d['Runs'] = str(total_runs)
    d['Maidens'] = str(maidens)
    d['Wickets'] = str(total_wickets)
    d['Avg'] = str(avg)
    d['Eco'] = str(eco)
    d['SR'] = str(strite_rate)
    d['Best Bowling Figues'] = str(best_figures)
    d['3w'] = 0
    d['4w'] = 0
    d['5w'] = 0
    
    for i in record['IsbowlerWicket']:
        if i == 3:
            d['3w']+=1
        elif i == 4:
            d['4w']+=1
        elif i >= 5:
            d['5w']+=1
            
    d['3w'] = str(d['3w'])
    d['4w'] = str(d['4w'])
    d['5w'] = str(d['5w'])
    
    return json.dumps(d)
       