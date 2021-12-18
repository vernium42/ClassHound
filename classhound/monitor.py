from functools import wraps

class Monitor:
    def __init__(self):
        """ Store parameter values of a function when function is used in program.

        Example:
        m = Monitor()
        print = m.function_parameter(print, (None, "end"))
        print("Hi, Bob", end="\n\n")
        print("Hi, Ron", end="\n")
        print(m.values)
        # ['\n\n', '\n']
        """
        self.values = []

    @staticmethod
    def _add_parameter_value(self, param_details, *args, **kwargs):
        if param_details[0] and len(args) > param_details[0]:
            self.values.append(args[param_details[0]])
        elif param_details[1] in kwargs:
            self.values.append(kwargs[param_details[1]])

    def internal_function_parameter(self, func, param_details):
        _self = self
        @wraps(func)
        def method(self, *args, **kwargs):
            _self._add_parameter_value(_self, param_details, *args, **kwargs)
            return func(self, *args, **kwargs)
        return method

    def function_parameter(self, func, param_details):
        @wraps(func)
        def method(*args, **kwargs):
            self._add_parameter_value(self, param_details, *args, **kwargs)
            return func(*args, **kwargs)
        return method

    def sniff_function_parameter(self, func, param_details):
        @wraps(func)
        def method(*args, **kwargs):
            has_self = False
            if "self" in func.__code__.co_varnames:
                _self = args[0]
                args = args[1:]
                has_self = True

            self._add_parameter_value(self, param_details, *args, **kwargs)
            if has_self:
                return func(_self, *args, **kwargs)
            return func(*args, **kwargs)
        return method
