from ortools.sat.python import cp_model

if __name__ == '__main__':
    model = cp_model.CpModel()
    solver = cp_model.CpSolver()

    #
    # decision variables
    #
    S = model.NewIntVar(0, 9, 'S')
    E = model.NewIntVar(0, 9, 'E')
    N = model.NewIntVar(0, 9, 'N')
    D = model.NewIntVar(0, 9, 'D')
    M = model.NewIntVar(0, 9, 'M')
    O = model.NewIntVar(0, 9, 'O')
    R = model.NewIntVar(0, 9, 'R')
    Y = model.NewIntVar(0, 9, 'Y')

    #
    # constraints
    #
    send = ((S * 10 + E) * 10 + N) * 10 + D
    more = ((M * 10 + O) * 10 + R) * 10 + E
    money = (((M * 10 + O) * 10 + N) * 10 + E) * 10 + Y

    model.Add(send + more == money)
    model.Add(S != 0)
    model.Add(M != 0)
    total = [S, E, N, D, M, O, R, Y]
    for i in range(len(total)):
        for j in range(i):
            a = total[i]
            b = total[j]
            model.Add(a != b)

    status = solver.Solve(model)

    if status == cp_model.FEASIBLE:
        print(solver.Value(send))
        print(solver.Value(more))
        print(solver.Value(money))
