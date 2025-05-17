from functools import wraps
import inspect


def strict(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_signature = inspect.signature(func)
        parameters = func_signature.parameters
        return_type = func_signature.return_annotation
        for i, parameter_name in enumerate(parameters):
            expected_parameter_type = parameters[parameter_name].annotation
            try:
                real_parameter_type = type(kwargs[parameter_name])
            except KeyError:
                real_parameter_type = type(args[i])
            if (
                expected_parameter_type != inspect._empty
                and expected_parameter_type != real_parameter_type
            ):
                raise TypeError
        result = func(*args, **kwargs)
        if return_type != inspect._empty and return_type != type(result):
            raise TypeError
        return result

    return wrapper
