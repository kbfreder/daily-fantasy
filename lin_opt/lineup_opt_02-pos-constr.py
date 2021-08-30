from collections import OrderedDict


budget = 50000

pos_reqs = OrderedDict({'QB':1, 'RB':2, 'WR':3, 'TE':1, 'Def': 1}) # , 'FLEX': 1, }
# arbitrarily increment a flex position's number by 1:
mod_reqs = pos_reqs.copy()
pos = 'RB'
mod_reqs[pos] += 1
lineup_size = np.sum(list(mod_reqs.values()))

# Define the decision variables
# --------------------------------
## number of players
num_players = len(wk_dict)
p = {i: LpVariable(name=f"p{i}", cat="Binary") for i in range(num_players)}

## positions
pos_dict_list = []
for pos in pos_reqs.keys():
    pos_idx = list(wk_df[wk_df['position'] == pos].index)
    pos_dict = {i: LpVariable(name=f"{pos}{i}", cat='Binary') for i in (pos_idx)}
    pos_dict_list.append(pos_dict)


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


# Print results
# --------------------------------
for name, constraint in model.constraints.items():
    if 'Salary' in name:
        print(f"Budget spent: ${(budget + constraint.value()):,.0f}")

print(f"Predicted number of points: {model.objective.value():.2f}")

print("Lineup:")
lineup_data = []

for var in model.variables():
    if (var.name[:1] == 'p') & (var.value() == 1):
        i = int(var.name[1:])
        lineup_data.append(wk_dict[i])

lineup_df = pd.DataFrame(lineup_data)
lineup_df.drop(columns=['gid', 'week', 'year', 'dfs_site'], inplace=True)
lineup_df.sort_values(by='salary', ascending=False)