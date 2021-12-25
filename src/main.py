# Add License info here
"""This file contains the entry point of the program.

Uses ORTools solver.
More info: https://developers.google.com/optimization
"""

from ortools.linear_solver import pywraplp

import constraints
import decision_vars
import objectives
import read_data
import utils


def main():
    """Entry point of the program."""

    data = read_data.Data()
    solver = pywraplp.Solver.CreateSolver('SCIP')
    variables = decision_vars.Variables(data, solver)
    constraints.add_constraints(data, solver, variables)
    objectives.add_objectives(data, solver, variables)
    utils.write_lp_file(solver, "scheduling")
    print("Solving...")
    solver.EnableOutput()  # Displays search
    status = solver.Solve()

    if status == solver.OPTIMAL:
        print("Optimization successful")
        utils.print_solution(data, solver, variables)

    elif status == solver.INFEASIBLE:
        print("Model Infeasible")
    elif status == solver.UNBOUNDED:
        print("Model unbounded")
    elif status == solver.ABNORMAL:
        print("Model abnormal")
    elif status == solver.NOT_SOLVED:
        print("Model not solved")
    else:
        print("Unknown error")


if __name__ == '__main__':
    main()
