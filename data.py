from gurobipy import *
from pybaseball import batting_stats 
from pybaseball import pitching_stats
import random
import pandas as pd

#first we take the batters who appear at the plate regurarly and we shorten the data bc the orignal dataset has over 200 stats
batting_data = batting_stats(2023)
df_batters = batting_data[batting_data['PA'] > 100].copy() 
df_batters = df_batters[['Name', 'Team', 'PA', 'OBP', 'wOBA', 'HR']].reset_index(drop=True)

#and now the same for pitchers
pitching_data = pitching_stats(2023)
df_pitchers = pitching_data[pitching_data['IP'] > 50].copy()
df_pitchers = df_pitchers[['Name', 'Team', 'IP', 'ERA', 'SO', 'WAR']].reset_index(drop=True)

#player positions
batters_positions = ['C', '1B', '2B', '3B', 'SS', 'OF', 'OF', 'OF']
df_batters['Pos'] = [random.choice(batters_positions) for _ in range(len(df_batters))]
df_pitchers['Pos'] = 'SP'



def normalize(column):
    return (column - column.min()) / (column.max() - column.min())

df_batters['wOBA_norm'] = normalize(df_batters['wOBA'])
df_batters['OBP_norm'] = normalize(df_batters['OBP'])
df_batters['HR_norm'] = normalize(df_batters['HR'])
df_batters['PA_norm'] = normalize(df_batters['PA'])

df_batters['Value'] = (
    (df_batters['wOBA_norm'] * 0.40) +  
    (df_batters['OBP_norm'] * 0.25) +  
    (df_batters['HR_norm'] * 0.20) + 
    (df_batters['PA_norm'] * 0.15)      
) * 100

df_batters['Salary'] = [random.randint(4000, 10000) for _ in range(len(df_batters))]

df_pitchers['WAR_norm'] = normalize(df_pitchers['WAR'])
df_pitchers['SO_norm'] = normalize(df_pitchers['SO'])
df_pitchers['IP_norm'] = normalize(df_pitchers['IP'])
df_pitchers['ERA_norm'] = (df_pitchers['ERA'].max() - df_pitchers['ERA']) / (df_pitchers['ERA'].max() - df_pitchers['ERA'].min())

df_pitchers['Value'] = (
    (df_pitchers['WAR_norm'] * 0.35) +  
    (df_pitchers['ERA_norm'] * 0.30) +  
    (df_pitchers['SO_norm'] * 0.20) +   
    (df_pitchers['IP_norm'] * 0.15)     
) * 100

df_pitchers['Salary'] = [random.randint(4000, 10000) for _ in range(len(df_pitchers))]

idx_C  = df_batters[df_batters['Pos'] == 'C'].index.tolist()
idx_1B = df_batters[df_batters['Pos'] == '1B'].index.tolist()
idx_2B = df_batters[df_batters['Pos'] == '2B'].index.tolist() 
idx_3B = df_batters[df_batters['Pos'] == '3B'].index.tolist() 
idx_SS = df_batters[df_batters['Pos'] == 'SS'].index.tolist() 
idx_OF = df_batters[df_batters['Pos'] == 'OF'].index.tolist()
idx_SP = df_pitchers[df_pitchers['Pos'] == 'SP'].index.tolist()