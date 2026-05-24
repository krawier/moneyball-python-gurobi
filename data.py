from gurobipy import *
import random
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

#first we take the batters who appear at the plate regurarly and we shorten the data bc the orignal dataset has over 200 stats
teams = ['NYY', 'LAD', 'ATL', 'HOU', 'BAL', 'TEX', 'PHI', 'TOR']

df_batters = pd.DataFrame({
    'Name': [f'Batter_{i}' for i in range(1, 151)],
    'Team': [random.choice(teams) for _ in range(150)],
    'PA': [random.randint(150, 650) for _ in range(150)],
    'OBP': [round(random.uniform(0.250, 0.420), 3) for _ in range(150)],
    'OPS': [round(random.uniform(0.600, 1.050), 3) for _ in range(150)],
    'HR': [random.randint(0, 45) for _ in range(150)]
})

#and now the same for pitchers
df_pitchers = pd.DataFrame({
    'Name': [f'Pitcher_{i}' for i in range(1, 51)],
    'Team': [random.choice(teams) for _ in range(50)],
    'IP': [random.randint(60, 220) for _ in range(50)],
    'ERA': [round(random.uniform(2.50, 6.00), 2) for _ in range(50)],
    'SO': [random.randint(50, 250) for _ in range(50)],
    'WAR': [round(random.uniform(-1.0, 6.5), 1) for _ in range(50)]
})

#player positions
batters_positions = ['C', '1B', '2B', '3B', 'SS', 'OF', 'OF', 'OF']
df_batters['Pos'] = [random.choice(batters_positions) for _ in range(len(df_batters))]
df_pitchers['Pos'] = 'SP'

def normalize(column):
    return (column - column.min()) / (column.max() - column.min())

df_batters['OPS_norm'] = normalize(df_batters['OPS'])
df_batters['OBP_norm'] = normalize(df_batters['OBP'])
df_batters['HR_norm'] = normalize(df_batters['HR'])
df_batters['PA_norm'] = normalize(df_batters['PA'])

df_batters['Value'] = (
    (df_batters['OPS_norm'] * 0.40) +  
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