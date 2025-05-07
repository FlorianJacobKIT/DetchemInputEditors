
class OutOfBoundError(Exception):
    def __str__(self):
        return self.message

    def __init__(self, value_name:str, value:float, lower_bound:float, upper_bound:float):
        self.message="Value for -" + value_name + "=" + str(value) + "- not inside bounds of " + str(lower_bound) + " and " + str(upper_bound)

