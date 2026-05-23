from gurobipy import *
from data import df_batters, df_pitchers

B_idx = df_batters.index.tolist()
P_idx = df_pitchers.index.tolist()

totalBudget = 50000

problem = Model("Moneyball_Problem")

x_batters = problem.addVars(B_idx, vtype=GRB.BINARY)
x_pitchers = problem.addVars(P_idx, vtype=GRB.BINARY)


#Constraint no 1 -> Budeget Constraint
problem.addConstr(
    quicksum(df_batters.loc[i, 'Salary'] * x_batters[i] for i in B_idx) + 
    quicksum(df_pitchers.loc[i, 'Salary'] * x_pitchers[i] for i in P_idx) <= totalBudget, 
    "Budget_Constraint"
)

#Constraint no 2 -> Cardinality Constraint
problem.addConstr(quicksum(x_pitchers[i] for i in P_idx) == 1, "Exactly_1_Pitcher")
problem.addConstr(quicksum(x_batters[i] for i in B_idx) == 8, "Exactly_8_Batters") 