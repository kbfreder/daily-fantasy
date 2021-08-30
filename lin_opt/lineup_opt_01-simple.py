

lineup_size = 9
budget = 50000

# Define the decision variables
## number of players
num_players = len(wk_dict)
p = {i: LpVariable(name=f"p{i}", cat="Binary") for i in range(num_players)}

# Define the model & add constraints & objective
model = LpProblem(name="lineup", sense=LpMaximize)

model += (lpSum([p[i] * (wk_dict[i]['salary']) for i in range(num_players)]) <= budget,
          "Constraint: Salary")

model += (lpSum(p.values()) <= lineup_size,
          "Constraint: Number of Players")

model += (lpSum([p[i] * (wk_dict[i]['points']) for i in range(num_players)]),
          "Objective: Maximize points")

# Solve the optimization problem
start_time = time.time()
status = model.solve()
end_time = time.time()
elapsed_time = (end_time - start_time)
print(f"Solved in {elapsed_time} seconds.")

