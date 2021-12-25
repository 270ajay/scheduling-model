# Add License info here
"""This file contains the functions that store data."""


class Data:
    """Stores data for building the model."""

    def __init__(self):
        """Initializes this class."""

        self.max_hours_before_break = 6

        self.demand_for_hour = {
            1: 2,
            2: 2,
            3: 2,
            4: 2,
            5: 2,
            6: 2,
            7: 2,
            8: 2,
            9: 2,
            10: 2,
            11: 2,
            12: 2,
            13: 2,
            14: 2,
            15: 2,
            16: 2
        }

        self.hours_available_for_person = {
            "Person1": 8,
            "Person12": 8,
            "Person16": 8,
            "Person17": 8,
            "Person20": 8,
            "Person2": 8,
            "Person10": 8,
            "Person6": 8,
            "Person25": 8,
            "Person18": 8,
            "Person22": 4,
            "Person7": 8,
            "Person8": 8,
            "Person9": 8,
            "Person13": 8,
            "Person19": 8,
            "Person23": 8,
            "Person24": 8,
            "Person5": 8,
            "Person11": 8,
            "Person14": 8,
            "Person3": 4,
            "Person4": 8,
            "Person15": 8,
            "Person21": 8
        }

        self.hour_info_for_person = {
            "Person1": _HourInfo(1, 9),
            "Person12": _HourInfo(1, 9),
            "Person16": _HourInfo(1, 9),
            "Person17": _HourInfo(1, 9),
            "Person20": _HourInfo(1, 9),
            "Person2": _HourInfo(1, 17),
            "Person10": _HourInfo(1, 17),
            "Person6": _HourInfo(1, 17),
            "Person25": _HourInfo(1, 17),
            "Person18": _HourInfo(1, 9),
            "Person22": _HourInfo(1, 17),
            "Person7": _HourInfo(1, 17),
            "Person8": _HourInfo(1, 9),
            "Person9": _HourInfo(1, 17),
            "Person13": _HourInfo(9, 17),
            "Person19": _HourInfo(9, 17),
            "Person23": _HourInfo(1, 9),
            "Person24": _HourInfo(1, 9),
            "Person5": _HourInfo(1, 17),
            "Person11": _HourInfo(9, 17),
            "Person14": _HourInfo(9, 17),
            "Person3": _HourInfo(1, 17),
            "Person4": _HourInfo(1, 17),
            "Person15": _HourInfo(1, 17),
            "Person21": _HourInfo(1, 17)
        }

        print("Finished storing data")


class _HourInfo:
    """Stores start and end hour."""

    def __init__(self, start_hour, end_hour):
        """Initializes this class."""
        self.start_hour = start_hour
        self.end_hour = end_hour
