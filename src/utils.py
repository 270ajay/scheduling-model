# Add License info here
"""This file contains utility classes and functions."""


def print_solution(data, solver, variables):
    """Prints solution to console."""

    end_vars = variables.end_vars
    print(f"Objective value: {solver.Objective().Value()}")

    print("--------------------------------------")
    for person, var in variables.start_vars.items():
        print(f"Start hour of {person}: {var.solution_value()}")
        print(f"End hour of {person}: {end_vars[person].solution_value()}")
        print("````````")

    print("--------------------------------------")
    for (person, hour), var in variables.is_on_break_vars.items():
        if var.solution_value() > 0.5:
            print(f"{person} is on break at hour {hour}")


def write_lp_file(solver, file_name, obfuscate=False):
    """Writes model to lp file."""
    print("Writing lp file...")
    with open(f"{file_name}.lp", "w") as file:
        file.write(str(solver.ExportModelAsLpFormat(obfuscate)))
