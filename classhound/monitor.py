from functools import wraps

class Monitor:
    def __init__(self):
        self.values = []

    @staticmethod
    def _add_parameter_value(self, param_name, *args, **kwargs):
        if len(args) > param_name[0]:
            self.values.append(args[param_name[0]])
        elif param_name[1] in kwargs:
            self.values.append(kwargs[param_name[1]])

    def internal_function_parameter(self, func, param_name):
        _self = self
        @wraps(func)
        def method(self, *args, **kwargs):
            _self._add_parameter_value(_self, param_name, *args, **kwargs)
            return func(self, *args, **kwargs)
        return method

    def function_parameter(self, func, param_name):
        @wraps(func)
        def method(*args, **kwargs):
            self._add_parameter_value(self, param_name, *args, **kwargs)
            return func(*args, **kwargs)
        return method

    def sniff_function_parameter(self, func, param_name):
        @wraps(func)
        def method(*args, **kwargs):
            has_self = False
            if "self" in func.__code__.co_varnames:
                _self = args[0]
                args = args[1:]
                has_self = True

            self._add_parameter_value(self, param_name, *args, **kwargs)
            if has_self:
                return func(_self, *args, **kwargs)
            return func(*args, **kwargs)
        return method
