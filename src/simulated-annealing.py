import math
import random
import pandas as pd
from data import df_batters, df_pitchers, idx_C, idx_1B, idx_2B, idx_3B, idx_SS, idx_OF, idx_SP

B_idx = df_batters.index.tolist()
P_idx = df_pitchers.index.tolist()

totalBudget = 50000

#symolowane wyrzarzanie 
T = 10000.0 #t0
T_min = 0.1 #tend
alpha = 0.99 #cooling rate
iterations = 100 #in every temp

pos_pools = {
    'C': idx_C, '1B': idx_1B, '2B': idx_2B, '3B': idx_3B, 'SS': idx_SS, 'OF': idx_OF, 'SP': idx_SP
} 

b_dict = df_batters[['Value', 'Salary']].to_dict('index')
p_dict = df_pitchers[['Value', 'Salary']].to_dict('index')

#helper functions

#totaly random first iteration
def get_random_team():
    return {
        'C': [random.choice(idx_C)],
        '1B': [random.choice(idx_1B)],
        '2B': [random.choice(idx_2B)],
        '3B': [random.choice(idx_3B)],
        'SS': [random.choice(idx_SS)],
        'OF': random.sample(idx_OF, 3),
        'SP': [random.choice(idx_SP)]
    }

#calculates total val and total sal
def evaluate_team(team):
    total_val = 0
    total_sal = 0
    
    for pos, players in team.items():
        for p in players:
            if pos == 'SP':
                total_val += p_dict[p]['Value']
                total_sal += p_dict[p]['Salary']
            else:
                total_val += b_dict[p]['Value']
                total_sal += b_dict[p]['Salary']
    return total_val, total_sal

# fitness => if fits in budget return val else return with penalty
def fitness(val, sal):
    if sal <= totalBudget:
        return val
    else:
        return val - (sal - totalBudget) * 10 

# returns new squad woth a exchanged player
def get_neighbor(team):
    new_team = {k: list(v) for k, v in team.items()}
    pos_to_swap = random.choice(list(pos_pools.keys()))
    
    if pos_to_swap == 'OF':
        drop_idx = random.choice(new_team['OF'])
        new_team['OF'].remove(drop_idx)
        available = list(set(pos_pools['OF']) - set(new_team['OF']))
        if available:
            new_team['OF'].append(random.choice(available))
    else:
        current_player = new_team[pos_to_swap][0]
        available = list(set(pos_pools[pos_to_swap]) - {current_player})
        if available:
            new_team[pos_to_swap] = [random.choice(available)]
            
    return new_team

#initialization
current_team = get_random_team()
current_val, current_sal = evaluate_team(current_team)
current_fit = fitness(current_val, current_sal)

best_team = {k: list(v) for k, v in current_team.items()}
best_val, best_sal = current_val, current_sal
best_fit = current_fit

#main loop
while T > T_min:
    for _ in range(iterations):
        new_team = get_neighbor(current_team)
        new_val, new_sal = evaluate_team(new_team)
        new_fit = fitness(new_val, new_sal)
        
        delta = new_fit - current_fit
        #add a random factor to get out of holes
        if delta > 0 or random.random() < math.exp(delta / T):
            current_team = new_team
            current_fit = new_fit
            current_val = new_val
            current_sal = new_sal
            
            if current_fit > best_fit and current_sal <= totalBudget:
                best_team = {k: list(v) for k, v in current_team.items()}
                best_fit = current_fit
                best_val = current_val
                best_sal = current_sal
                
    T = T * alpha 

#results
print("\n" + "="*50)
print("OPTIMAL ROOSTER (METAHEURISTIC)")
print("="*50)
print(f"Total team value: {best_val:.2f}")
print("-" * 50)

selected_players = []

for pos, players in best_team.items():
    for p in players:
        if pos == 'SP':
            name, team, val, sal = df_pitchers.loc[p, 'Name'], df_pitchers.loc[p, 'Team'], df_pitchers.loc[p, 'Value'], df_pitchers.loc[p, 'Salary']
        else:
            name, team, val, sal = df_batters.loc[p, 'Name'], df_batters.loc[p, 'Team'], df_batters.loc[p, 'Value'], df_batters.loc[p, 'Salary']
        
        selected_players.append({'Position': pos, 'Name': name, 'Team': team, 'Value': val, 'Salary': sal})

for p in selected_players:
    print(f"[{p['Position']:<2}] {p['Name']:<20} ({p['Team']:<3}) | Value: {p['Value']:>6.2f} | Coszt: ${p['Salary']}")

print("-" * 50)
print(f"Used budget: ${best_sal} / ${totalBudget}\n")

results_df = pd.DataFrame(selected_players)
results_df.to_csv('../data/sa_results.csv', index=False)
print("Resutls saved to 'sa_results.csv' ")