# Add License info here
"""This file contains the functions that create constraints."""


def add_constraints(data, solver, variables):
    """Adds constraints to model."""

    print("Adding constraints to the model...")

    _add_balancing_constraints(data, solver, variables)
    _add_break_constraints(data, solver, variables)
    _add_break_hour_constraints(data, solver, variables)
    _add_demand_constraints(data, solver, variables)
    _add_end_hour_constraints(data, solver, variables)
    _add_start_hour_constraints(data, solver, variables)
    _add_duration_constraints(data, solver, variables)


def _add_balancing_constraints(data, solver, variables):
    """Adds balancing constraints.

    Example:
        Start|Person1
        + Duration|Person1
        + HasBreak|Person1
        = End|Person1
    """
    duration_vars = variables.duration_vars
    has_break_vars = variables.has_break_vars
    start_vars = variables.start_vars
    end_vars = variables.end_vars

    coeff_var_list = []
    for person, start_var in start_vars.items():
        coeff_var_list.append(1 * start_var)
        coeff_var_list.append(1 * duration_vars[person])
        coeff_var_list.append(1 * has_break_vars[person])
        coeff_var_list.append(-1 * end_vars[person])

        ct_name = f"CtBalancing|{person}"
        solver.Add(solver.Sum(coeff_var_list) == 0, ct_name)
        coeff_var_list.clear()

    print("Added Balancing constraints")


def _add_break_constraints(data, solver, variables):
    """Adds break constraints.

    Example:
        Duration|Person1 <= 5 + 2 * HasBreak|Person1
    """
    duration_vars = variables.duration_vars
    has_break_vars = variables.has_break_vars
    max_hours_before_break = data.max_hours_before_break

    coeff_var_list = []
    for person, hours_available in data.hours_available_for_person.items():

        coeff = 0
        rhs = hours_available
        additional_time = hours_available - max_hours_before_break
        if additional_time > 0:
            coeff = -additional_time
            rhs = max_hours_before_break

        coeff_var_list.append(1 * duration_vars[person])
        coeff_var_list.append(coeff * has_break_vars[person])

        ct_name = f"CtBreak|{person}"
        solver.Add(solver.Sum(coeff_var_list) <= rhs, ct_name)
        coeff_var_list.clear()

    print("Added Break constraints")


def _add_break_hour_constraints(data, solver, variables):
    """Adds break hour constraints.

    Example:
        HasBreak|person
        = IsOnBreak|Person1|1
        + IsOnBreak|Person1|2
        + IsOnBreak|Person1|3
        + IsOnBreak|Person1|4
        + IsOnBreak|Person1|5
    """
    has_break_vars = variables.has_break_vars
    is_on_break_vars = variables.is_on_break_vars

    coeff_var_list = []
    for person, info in data.hour_info_for_person.items():

        coeff_var_list.append(1 * has_break_vars[person])

        start_hour = info.start_hour
        end_hour = min(start_hour + data.max_hours_before_break, info.end_hour)
        for hour in range(start_hour, end_hour + 1):
            coeff_var_list.append(-1 * is_on_break_vars[(person, hour)])

        ct_name = f"CtBreakHour|{person}"
        solver.Add(solver.Sum(coeff_var_list) == 0, ct_name)
        coeff_var_list.clear()

    print("Added Break Hour constraints")


def _add_demand_constraints(data, solver, variables):
    """Adds demand constraints.

    Example:
        IsWorking|Person1|5
        + IsWorking|Person2|5
        + IsWorking|Person3|5
        - IsOnBreak|Person1|5
        - IsOnBreak|Person2|5
        - IsOnBreak|Person3|5
        >= Demand|5
    """
    is_working_vars = variables.is_working_vars
    is_on_break_vars = variables.is_on_break_vars
    demand_vars = variables.demand_vars

    coeff_var_list = []
    for hour, demand in data.demand_for_hour.items():
        for person in data.hour_info_for_person:

            if (person, hour) in is_working_vars:
                coeff_var_list.append(1 * is_working_vars[(person, hour)])

            if (person, hour) in is_on_break_vars:
                coeff_var_list.append(-1 * is_on_break_vars[(person, hour)])

        coeff_var_list.append(-1 * demand_vars[(hour)])
        ct_name = f"CtDemandHour|{hour}"
        solver.Add(solver.Sum(coeff_var_list) >= 0, ct_name)
        coeff_var_list.clear()

    print("Added Demand constraints")


def _add_end_hour_constraints(data, solver, variables):
    """Adds end hour constraints.

    If End|Person1 takes value 6,
    then IsWorking|Person|5 would become 0

    Example:
        End|Person1 >= 6 * IsWorking|Person1|5
    """
    end_vars = variables.end_vars
    is_working_vars = variables.is_working_vars

    coeff_var_list = []
    for person, info in data.hour_info_for_person.items():
        for hour in range(info.start_hour, info.end_hour + 1):
            coeff_var_list.append(1 * end_vars[person])
            coeff_var_list.append(-(hour + 1) * is_working_vars[(person, hour)])
            ct_name = f"CtEndHour|{person}|{hour}"
            solver.Add(solver.Sum(coeff_var_list) >= 0, ct_name)
            coeff_var_list.clear()

    print("Added End Hour constraints")


def _add_start_hour_constraints(data, solver, variables):
    """Adds start hour constraints.

    If Start|Person1 takes value 4,
    then IsWorking|Person|3, IsWorking|Person|2, IsWorking|Person|1
    would become 0

    Example:
        Start|Person1 <= 4 + (7 * (1 - IsWorking|Person1|4))
    """
    hours_available_for_person = data.hours_available_for_person
    start_vars = variables.start_vars
    is_working_vars = variables.is_working_vars

    coeff_var_list = []
    for person, info in data.hour_info_for_person.items():
        for hour in range(info.start_hour, info.end_hour + 1):
            max_hours = hours_available_for_person[person]
            coeff_var_list.append(1 * start_vars[person])
            coeff_var_list.append(max_hours * is_working_vars[(person, hour)])
            ct_name = f"CtStartHour|{person}|{hour}"
            solver.Add(solver.Sum(coeff_var_list) <= max_hours + hour, ct_name)
            coeff_var_list.clear()

    print("Added Start Hour constraints")


def _add_duration_constraints(data, solver, variables):
    """Adds duration constraints.

    Example:
        IsWorking|Person1|1
        + IsWorking|Person1|2
        + IsWorking|Person1|3
        + IsWorking|Person1|4
        + IsWorking|Person1|5
        + IsWorking|Person1|6
        + IsWorking|Person1|7
        = Duration|Person1
        + HasBreak|Person1
    """
    is_working_vars = variables.is_working_vars
    duration_vars = variables.duration_vars
    has_break_vars = variables.has_break_vars

    coeff_var_list = []
    for person, info in data.hour_info_for_person.items():
        for hour in range(info.start_hour, info.end_hour + 1):
            coeff_var_list.append(1 * is_working_vars[(person, hour)])

        coeff_var_list.append(-1 * duration_vars[person])
        coeff_var_list.append(-1 * has_break_vars[person])
        ct_name = f"CtDuration|{person}"
        solver.Add(solver.Sum(coeff_var_list) == 0, ct_name)
        coeff_var_list.clear()

    print("Added Duration constraints")
