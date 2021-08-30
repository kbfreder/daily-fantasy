from collections import OrderedDict
import numpy as np
import pandas as pd
import time

from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable


pd.set_option('mode.chained_assignment', None)


budget = 50000

wk_df['flex_ind'] = np.where(wk_df['position'].isin(flex_pos), 1, 0)


def solve_model(pos_reqs, wk_df, budget=BUDGET):
    # derive things
    wk_dict = wk_df.to_dict(orient='index')
    lineup_size = np.sum(list(pos_reqs.values()))
    
    # Define the decision variables
    # --------------------------------
    ## number of players
    num_players = len(wk_dict)
    p = {i: LpVariable(name=f"p{i}", cat="Binary") for i in range(num_players)}

    # ## positions
    # pos_dict_list = []
    # for pos in pos_reqs.keys():
    #     pos_idx = list(wk_df[wk_df['position'] == pos].index)
    #     pos_dict = {i: LpVariable(name=f"{pos}{i}", cat='Binary') for i in (pos_idx)}
    #     pos_dict_list.append(pos_dict)
    
    pos_var_dict = OrderedDict()
    for pos in mod_reqs.keys():
        pos_idx = list(wk_df[wk_df['position'] == pos].index)
        pos_dict = {i: LpVariable(name=f"{pos}{i}", cat='Binary') for i in (pos_idx)}
        pos_var_dict[pos] = pos_dict

    # Define the model & add constraints & objective
    # --------------------------------
    model = LpProblem(name="lineup", sense=LpMaximize)

    model += (lpSum([p[i] * (wk_dict[i]['salary']) for i in range(num_players)]) <= budget,
              "Constraint: Salary")

    model += (lpSum([p[i] * (wk_dict[i]['points']) for i in range(num_players)]),
              "Objective: Maximize points")

    model += (lpSum(p.values()) == lineup_size,
              "Constraint: Total number of Players")

    for pos, num in mod_reqs.items():
        d = pos_var_dict[pos]
        model += (lpSum(d.values()) == num,
                  f"Constraint: Number of {pos}")

        # constrain player[i] to == pos[i] 
        for i in d.keys():
            model += d[i] == p[i]

    # Solve the optimization problem
    # --------------------------------
    start_time = time.time()
    status = model.solve()
    end_time = time.time()
    elapsed_time = (end_time - start_time)
    print(f"status: {model.status}, {LpStatus[model.status]}")
    print(f"Solved in {elapsed_time} seconds.")

    # Collect results
    # --------------------------------
    for name, constraint in model.constraints.items():
        if 'Salary' in name:
            money_spent = (budget + constraint.value())
    #         print(f"Budget spent: ${(budget + constraint.value()):,.0f}")

    # print(f"Predicted number of points: {model.objective.value():.2f}")
    pred_points = model.objective.value()

    lineup_data = []

    for var in model.variables():
        if (var.name[:1] == 'p') & (var.value() == 1):
            i = int(var.name[1:])
            lineup_data.append(wk_dict[i])
    return {'model': model,
            'pred_points': pred_points,
            'money_spent': money_spent,
            'lineup': lineup_data
           }


def format_lineup_df(lineup_data):
    lineup_df = pd.DataFrame(lineup_data)
    lineup_df.drop(columns=['gid', 'week', 'year', 'dfs_site'], inplace=True)
    lineup_df = lineup_df.sort_values(by='salary', ascending=False)
    return lineup_df


# this assumes there is only 1 flex position
lineup_reqs = OrderedDict({'QB':1, 'RB':2, 'WR':3, 'TE':1, 'Def': 1})
flex_pos = {'RB', 'WR', 'TE'}

results = []
for pos in flex_pos:
    print(pos)
    mod_reqs = lineup_reqs.copy()
    mod_reqs[pos] += 1
    res_dict = solve_model(mod_reqs, wk_df)
    results.append(res_dict)

results.sort(key=lambda d: d['pred_points'], reverse=True)
best_result = results[0]
best_ldf = format_lineup_df(best_result['lineup'])