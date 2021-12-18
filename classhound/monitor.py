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

    def _add_parameter_value(self, param_details, *args, **kwargs):
        if (param_details[0] is not None) and (len(args) > param_details[0]):
            self.values.append(args[param_details[0]])
        elif param_details[1] in kwargs:
            self.values.append(kwargs[param_details[1]])

    def internal_function_parameter(self, func, param_details):
        """ Stores parameter values of functions that require have the self keyword.

        Example:
            import pprint
            from classhound import monitor

            m = Monitor()
            pprint.PrettyPrinter.pprint = m.internal_function_parameter(
                func=pprint.PrettyPrinter.pprint,
                param_details=(0, "object")
            )
            pprint.pprint({"name": "Koos"}, indent=4)

            m.values
            # [{"name": "Koos"}]

        :param func: Function to monitor.
        :param param_details: Parameter location details tuple(<parameter_args_index>, <parameter_name>)
        :return: func
        """

        @wraps(func)
        def method(_self, *args, **kwargs):
            self._add_parameter_value(param_details, *args, **kwargs)
            return func(_self, *args, **kwargs)
        return method

    def function_parameter(self, func, param_details):
        """ Stores parameter values of functions.

        Example:
            import pprint
            from classhound import monitor

            m = Monitor()
            pprint.pprint = m.function_parameter(
                func=pprint.pprint,
                param_details=(2, "indent")
            )
            pprint.pprint({"name": "Koos"}, indent=4)

            m.values
            # [4]

        :param func: Function to monitor.
        :param param_details: Parameter location details tuple(<parameter_args_index>, <parameter_name>)
        :return: func
        """
        @wraps(func)
        def method(*args, **kwargs):
            self._add_parameter_value(param_details, *args, **kwargs)
            return func(*args, **kwargs)
        return method

    def sniff_function_parameter(self, func, param_details):
        """ Stores parameter values of functions and auto checks if the function requires the self
        parameter. Take a look `Monitor.function_parameter` and `Monitor.internal_function_parameter`.

        :param func: Function to monitor.
        :param param_details: Parameter location details tuple(<parameter_args_index>, <parameter_name>)
        :return: func
        """
        @wraps(func)
        def method(*args, **kwargs):
            self._add_parameter_value(param_details, *args, **kwargs)
            if "self" in func.__code__.co_varnames:
                _self = args[0]
                args = args[1:]
                return func(_self, *args, **kwargs)
            return func(*args, **kwargs)
        return method
