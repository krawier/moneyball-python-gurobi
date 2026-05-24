from gurobipy import *
from data import *

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