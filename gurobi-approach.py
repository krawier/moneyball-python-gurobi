from gurobipy import *
from data import *
import pandas as pd

B_idx = df_batters.index.tolist()
P_idx = df_pitchers.index.tolist()

totalBudget = 50000

problem = Model("Moneyball_Problem")

x_batters = problem.addVars(B_idx, vtype=GRB.BINARY)
x_pitchers = problem.addVars(P_idx, vtype=GRB.BINARY)

#objective function
problem.setObjective(
    quicksum(df_batters.loc[i, 'Value'] * x_batters[i] for i in B_idx) + 
    quicksum(df_pitchers.loc[i, 'Value'] * x_pitchers[i] for i in P_idx), 
    GRB.MAXIMIZE
)

#Constraint no 1 -> Budeget Constraint
problem.addConstr(
    quicksum(df_batters.loc[i, 'Salary'] * x_batters[i] for i in B_idx) + 
    quicksum(df_pitchers.loc[i, 'Salary'] * x_pitchers[i] for i in P_idx) <= totalBudget, 
    "Budget_Constraint"
)

#Constraint no 2 -> Cardinality Constraint
problem.addConstr(quicksum(x_batters[i] for i in idx_C) == 1, "Exactly_1_Catcher")
problem.addConstr(quicksum(x_batters[i] for i in idx_1B) == 1, "Exactly_1_First_Baseman")
problem.addConstr(quicksum(x_batters[i] for i in idx_2B) == 1, "Exactly_1_Second_Baseman")
problem.addConstr(quicksum(x_batters[i] for i in idx_3B) == 1, "Exactly_1_Third_Baseman") 
problem.addConstr(quicksum(x_batters[i] for i in idx_SS) == 1, "Exactly_1_Shortstop") 
problem.addConstr(quicksum(x_batters[i] for i in idx_OF) == 3, "Exactly_3_Outfielders")

problem.addConstr(quicksum(x_pitchers[i] for i in idx_SP) == 1, "Exactly_1_Starting_Pitcher")

problem.optimize()

if problem.status == GRB.OPTIMAL:
    print("\n" + "="*50)
    print("OPTIMAL ROOSTER")
    print("="*50)
    print(f"Total team value: {problem.objVal:.2f}")
    print("-" * 50)

    selected_players = []
    total_cost = 0

    for i in P_idx:
        if x_pitchers[i].x > 0.5:
            name, team, pos, val, sal = df_pitchers.loc[i, 'Name'], df_pitchers.loc[i, 'Team'], df_pitchers.loc[i, 'Pos'], df_pitchers.loc[i, 'Value'], df_pitchers.loc[i, 'Salary']
            total_cost += sal
            selected_players.append({'Position': pos, 'Name': name, 'Team': team, 'Value': val, 'Salary': sal})

    for i in B_idx:
        if x_batters[i].x > 0.5:
            name, team, pos, val, sal = df_batters.loc[i, 'Name'], df_batters.loc[i, 'Team'], df_batters.loc[i, 'Pos'], df_batters.loc[i, 'Value'], df_batters.loc[i, 'Salary']
            total_cost += sal
            selected_players.append({'Position': pos, 'Name': name, 'Team': team, 'Value': val, 'Salary': sal})

    for p in selected_players:
        print(f"[{p['Position']:<2}] {p['Name']:<20} ({p['Team']:<3}) | Value: {p['Value']:>6.2f} | Koszt: ${p['Salary']}")

    print("-" * 50)
    print(f"Used budget: ${total_cost} / ${totalBudget}\n")

    results_df = pd.DataFrame(selected_players)

    results_df.to_csv('gurobi_results.csv', index=False)
    print("Resutls saved to 'gurobi_results.csv' ")
else:
    print("Model didn't find an optimal solution. Budget too small, or constraints too rigorious!")