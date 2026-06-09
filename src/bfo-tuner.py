import random
import optuna
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

totalBudget = 50000
pos_pools = {
    "C": idx_C,
    "1B": idx_1B,
    "2B": idx_2B,
    "3B": idx_3B,
    "SS": idx_SS,
    "OF": idx_OF,
    "SP": idx_SP,
}

b_dict = df_batters[["Value", "Salary"]].to_dict("index")
p_dict = df_pitchers[["Value", "Salary"]].to_dict("index")


# Helper functions
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
    val, sal = 0, 0
    for pos, players in team.items():
        for p in players:
            if pos == "SP":
                val += p_dict[p]["Value"]
                sal += p_dict[p]["Salary"]
            else:
                val += b_dict[p]["Value"]
                sal += b_dict[p]["Salary"]
    return val, sal


def fitness(val, sal):
    if sal <= totalBudget:
        return val
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


# ========= BFO RUNNER FUNCTION=========
def run_bfo(S, N_c, N_s, N_re, N_ed, P_ed):
    bacteria = []
    for _ in range(S):
        team = get_random_team()
        val, sal = evaluate_team(team)
        bacteria.append(
            {
                "team": team,
                "fit": fitness(val, sal),
                "val": val,
                "sal": sal,
                "health": 0,
            }
        )

    best_fit_overall = -float("inf")
    best_val_overall = 0

    for ell in range(N_ed):
        for k in range(N_re):
            for j in range(N_c):
                for i in range(S):
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
                                break

                    bacteria[i]["health"] += bacteria[i]["fit"]

                    if (
                        bacteria[i]["fit"] > best_fit_overall
                        and bacteria[i]["sal"] <= totalBudget
                    ):
                        best_fit_overall = bacteria[i]["fit"]
                        best_val_overall = bacteria[i]["val"]

            bacteria.sort(key=lambda x: x["health"], reverse=True)
            half_S = S // 2
            for i in range(half_S):
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
                bacteria[i]["health"] = 0

        for i in range(S):
            if random.random() < P_ed:
                team = get_random_team()
                val, sal = evaluate_team(team)
                bacteria[i] = {
                    "team": team,
                    "fit": fitness(val, sal),
                    "val": val,
                    "sal": sal,
                    "health": 0,
                }

    return best_val_overall


# ========= OPTUNA OBJECTIVE FUNCTION\n# =========
def objective(trial):
    S = trial.suggest_int("S", 10, 50, step=10)
    N_c = trial.suggest_int("N_c", 10, 40, step=10)
    N_s = trial.suggest_int("N_s", 2, 8, step=2)
    N_re = trial.suggest_int("N_re", 2, 6, step=2)
    N_ed = trial.suggest_int("N_ed", 1, 3)
    P_ed = trial.suggest_float("P_ed", 0.1, 0.4, step=0.05)

    val = run_bfo(S, N_c, N_s, N_re, N_ed, P_ed)
    return val


if __name__ == "__main__":
    optuna.logging.set_verbosity(optuna.logging.INFO)
    study = optuna.create_study(direction="maximize")

    print("Tunning...\n")
    study.optimize(objective, n_trials=50)

    print("\n" + "=" * 50)
    print("OPTUNA TUNING FINISHED")
    print("=" * 50)
    print(f"Best found 'Value': {study.best_value:.2f}")
    print("Best found parameters:")
    for key, value in study.best_params.items():
        print(f"  {key}: {value}")
