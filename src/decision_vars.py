# Add License info here
"""This file contains the functions that create decision variables."""


class Variables:
    """Creates and stores decision variables."""

    def __init__(self, data, solver):
        """Initializes this class."""

        print("Adding variables to the model...")

        self.start_vars = _create_start_vars(data, solver)
        self.end_vars = _create_end_vars(data, solver)
        self.duration_vars = _create_duration_vars(data, solver)
        self.has_break_vars = _create_has_break_vars(data, solver)
        self.is_working_vars = _create_is_working_vars(data, solver)
        self.is_on_break_vars = _create_is_on_break_vars(data, solver)
        self.demand_vars = _create_demand_vars(data, solver)


def _create_start_vars(data, solver):
    """Creates start vars."""

    start_vars = {}
    for person, info in data.hour_info_for_person.items():
        var_name = f"Start|{person}"
        start_vars[person] = solver.NumVar(lb=info.start_hour,
                                           ub=info.end_hour,
                                           name=var_name)

    print("Added Start vars")
    return start_vars


def _create_end_vars(data, solver):
    """Creates end vars."""

    end_vars = {}
    for person, info in data.hour_info_for_person.items():
        var_name = f"End|{person}"
        end_vars[person] = solver.NumVar(lb=info.start_hour,
                                         ub=info.end_hour + 1,
                                         name=var_name)

    print("Added End vars")
    return end_vars


def _create_duration_vars(data, solver):
    """Creates duration vars."""

    duration_vars = {}
    for person in data.hour_info_for_person:
        var_name = f"Duration|{person}"
        duration_vars[person] = solver.NumVar(lb=0,
                                              ub=solver.infinity(),
                                              name=var_name)

    print("Added Duration vars")
    return duration_vars


def _create_has_break_vars(data, solver):
    """Creates has break vars."""

    has_break_vars = {}
    for person in data.hour_info_for_person:
        var_name = f"HasBreak|{person}"
        has_break_vars[person] = solver.IntVar(lb=0, ub=1, name=var_name)

    print("Added Has Break vars")
    return has_break_vars


def _create_is_working_vars(data, solver):
    """Creates is working vars."""

    is_working_vars = {}
    for person, info in data.hour_info_for_person.items():
        for hour in range(info.start_hour, info.end_hour + 1):
            var_name = f"IsWorking|{person}|{hour}"
            is_working_vars[(person, hour)] = solver.IntVar(lb=0,
                                                            ub=1,
                                                            name=var_name)

    print("Added Is Working vars")
    return is_working_vars


def _create_is_on_break_vars(data, solver):
    """Creates is on break vars."""

    is_on_break_vars = {}
    for person, info in data.hour_info_for_person.items():
        start_hour = info.start_hour
        end_hour = min(start_hour + data.max_hours_before_break, info.end_hour)
        for hour in range(start_hour, end_hour + 1):
            var_name = f"IsOnBreak|{person}|{hour}"
            is_on_break_vars[(person, hour)] = solver.IntVar(lb=0,
                                                             ub=1,
                                                             name=var_name)

    print("Added Is On Break vars")
    return is_on_break_vars


def _create_demand_vars(data, solver):
    """Creates demand vars."""

    demand_vars = {}
    for hour, demand in data.demand_for_hour.items():
        var_name = f"Demand|{hour}"
        demand_vars[hour] = solver.NumVar(lb=demand, ub=demand, name=var_name)

    print("Added Demand vars")
    return demand_vars
