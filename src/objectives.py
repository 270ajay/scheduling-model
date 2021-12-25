# Add License info here
"""This file contains functions that create objectives."""


def add_objectives(data, solver, variables):
    """Adds objectives to the model."""

    print("Adding objective to the model...")

    objective = solver.Objective()

    for var in variables.end_vars.values():
        objective.SetCoefficient(var, 1)

    objective.SetMinimization()
    print("Added objective")
