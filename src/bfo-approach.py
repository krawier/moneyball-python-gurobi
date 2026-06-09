import random
import pandas as pd
from data import (
    df_batters,
    df_pitchers,
    idx_C,
    idx_1B,
    idx_2B,
    idx_3B,
    idx_SS,
    idx_OF,
    idx_SP,
)

B_idx = df_batters.index.tolist()
P_idx = df_pitchers.index.tolist()

totalBudget = 50000

# TUNED WITH OPTUNA
S = 20  # Number of bacteria (population size)
N_c = 30  # Number of chemotactic steps
N_s = 2  # Swim length
N_re = 6  # Number of reproduction steps
N_ed = 3  # Number of elimination-dispersal steps
P_ed = 0.35  # Elimination-dispersal probability

pos_pools = {
    "C": idx_C,
    "1B": idx_1B,
    "2B": idx_2B,
    "3B": idx_3B,
    "SS": idx_SS,
    "OF": idx_OF,
    "SP": idx_SP,
}

# fast dictionaries
b_dict = df_batters[["Value", "Salary"]].to_dict("index")
p_dict = df_pitchers[["Value", "Salary"]].to_dict("index")


# helpers
def get_random_team():
    return {
        "C": [random.choice(idx_C)],
        "1B": [random.choice(idx_1B)],
        "2B": [random.choice(idx_2B)],
        "3B": [random.choice(idx_3B)],
        "SS": [random.choice(idx_SS)],
        "OF": random.sample(idx_OF, 3),
        "SP": [random.choice(idx_SP)],
    }


def evaluate_team(team):
    total_val = 0
    total_sal = 0

    for pos, players in team.items():
        for p in players:
            if pos == "SP":
                total_val += p_dict[p]["Value"]
                total_sal += p_dict[p]["Salary"]
            else:
                total_val += b_dict[p]["Value"]
                total_sal += b_dict[p]["Salary"]
    return total_val, total_sal


def fitness(val, sal):
    if sal <= totalBudget:
        return val
    else:
        return val - (sal - totalBudget) * 10


def get_neighbor(team):
    new_team = {k: list(v) for k, v in team.items()}
    pos_to_swap = random.choice(list(pos_pools.keys()))

    if pos_to_swap == "OF":
        drop_idx = random.choice(new_team["OF"])
        new_team["OF"].remove(drop_idx)
        available = list(set(pos_pools["OF"]) - set(new_team["OF"]))
        if available:
            new_team["OF"].append(random.choice(available))
    else:
        current_player = new_team[pos_to_swap][0]
        available = list(set(pos_pools[pos_to_swap]) - {current_player})
        if available:
            new_team[pos_to_swap] = [random.choice(available)]

    return new_team


# initialization
bacteria = []
for _ in range(S):
    team = get_random_team()
    val, sal = evaluate_team(team)
    fit = fitness(val, sal)
    bacteria.append(
        {"team": team, "fit": fit, "val": val, "sal": sal, "health": 0}
    )

best_team_overall = None
best_fit_overall = -float("inf")
best_val_overall = 0
best_sal_overall = 0

# Main BFO Loop
for ell in range(N_ed):  # elimination-dispersal loop
    for k in range(N_re):  # reproduction loop
        for j in range(N_c):  # chemotaxis loop

            for i in range(S):
                # tumble (Take a random step)
                new_team = get_neighbor(bacteria[i]["team"])
                new_val, new_sal = evaluate_team(new_team)
                new_fit = fitness(new_val, new_sal)

                if new_fit > bacteria[i]["fit"]:
                    bacteria[i].update(
                        {
                            "team": new_team,
                            "fit": new_fit,
                            "val": new_val,
                            "sal": new_sal,
                        }
                    )

                    # swim and keep going in same direction if improving
                    m = 0
                    while m < N_s:
                        m += 1
                        swim_team = get_neighbor(bacteria[i]["team"])
                        swim_val, swim_sal = evaluate_team(swim_team)
                        swim_fit = fitness(swim_val, swim_sal)

                        if swim_fit > bacteria[i]["fit"]:
                            bacteria[i].update(
                                {
                                    "team": swim_team,
                                    "fit": swim_fit,
                                    "val": swim_val,
                                    "sal": swim_sal,
                                }
                            )
                        else:
                            break  # stop swimming if it gets worse

                # update accumulated health for reproduction
                bacteria[i]["health"] += bacteria[i]["fit"]

                # check Global Best
                if (
                    bacteria[i]["fit"] > best_fit_overall
                    and bacteria[i]["sal"] <= totalBudget
                ):
                    best_fit_overall = bacteria[i]["fit"]
                    best_team_overall = {
                        k_pos: list(v_pos)
                        for k_pos, v_pos in bacteria[i]["team"].items()
                    }
                    best_val_overall = bacteria[i]["val"]
                    best_sal_overall = bacteria[i]["sal"]

        # reproduction Step
        bacteria.sort(key=lambda x: x["health"], reverse=True)
        half_S = S // 2
        for i in range(half_S):
            # best half splits and replaces the worst half
            bacteria[i + half_S] = {
                "team": {
                    k_pos: list(v_pos)
                    for k_pos, v_pos in bacteria[i]["team"].items()
                },
                "fit": bacteria[i]["fit"],
                "val": bacteria[i]["val"],
                "sal": bacteria[i]["sal"],
                "health": 0,
            }
            bacteria[i]["health"] = 0  # reset health for next gen

    # elimination-dispersal step
    for i in range(S):
        if random.random() < P_ed:
            team = get_random_team()
            val, sal = evaluate_team(team)
            fit = fitness(val, sal)
            bacteria[i] = {
                "team": team,
                "fit": fit,
                "val": val,
                "sal": sal,
                "health": 0,
            }

# results
print("\n" + "=" * 50)
print("OPTIMAL ROOSTER (BFO METAHEURISTIC)")
print("=" * 50)
print(f"Total team value: {best_val_overall:.2f}")
print("-" * 50)

selected_players = []

for pos, players in best_team_overall.items():
    for p in players:
        if pos == "SP":
            name, team, val, sal = (
                df_pitchers.loc[p, "Name"],
                df_pitchers.loc[p, "Team"],
                df_pitchers.loc[p, "Value"],
                df_pitchers.loc[p, "Salary"],
            )
        else:
            name, team, val, sal = (
                df_batters.loc[p, "Name"],
                df_batters.loc[p, "Team"],
                df_batters.loc[p, "Value"],
                df_batters.loc[p, "Salary"],
            )

        selected_players.append(
            {
                "Position": pos,
                "Name": name,
                "Team": team,
                "Value": val,
                "Salary": sal,
            }
        )

for p in selected_players:
    print(
        f"[{p['Position']:<2}] {p['Name']:<20} ({p['Team']:<3}) "
        f"| Value: {p['Value']:>6.2f} | Cost: ${p['Salary']}"
    )

print("-" * 50)
print(f"Used budget: ${best_sal_overall} / ${totalBudget}\n")

results_df = pd.DataFrame(selected_players)
results_df.to_csv("../data/bfo_results.csv", index=False)
