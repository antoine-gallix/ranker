"""decorator to count calls to a function
"""

import time
import statistics


class profile:
    """Decorator that keeps track of the number of times a function is called.

    The decorator can count calls of multiple functions
    Usage:

    @profile
    def function_to_profile():
        ....

    ...do things...

    nb_calls = function_to_profile.count_calls()

    """

    __instances = {}

    def __init__(self, f):
        self.__f = f
        self.__numcalls = 0
        self.__exec_times = []
        profile.__instances[f] = self

    def __call__(self, *args, **kwargs):
        t0 = time.clock()
        result = self.__f(*args, **kwargs)
        t = time.clock()
        self.__exec_times.append(t - t0)
        self.__numcalls += 1
        return result

    def reset_profile(self):
        "Reset the function's metrics."
        profile.__instances[self.__f].__numcalls = 0
        profile.__instances[self.__f].__exec_times = []

    # base profile metrics

    def count_calls(self):
        "Return the number of times the function f was called."
        return profile.__instances[self.__f].__numcalls

    def execution_times(self):
        "Return the execution times."
        return profile.__instances[self.__f].__exec_times

    # derived metrics

    def average_execution_time(self):
        "Return the mean execution time."
        times = self.execution_times()
        try:
            return statistics.mean(times)
        except(statistics.StatisticsError):
            return None

    def total_execution_time(self):
        "Return the total execution time."
        return sum(profile.__instances[self.__f].__exec_times)
