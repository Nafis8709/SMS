"""Small helpers shared by the domain modules to check request fields."""


def is_positive_int(value):
    # bool is a subclass of int in Python, so True must be rejected explicitly
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def is_text(value, max_length):
    return isinstance(value, str) and 0 < len(value.strip()) <= max_length


def field_error(pointer, message):
    return {"pointer": pointer, "message": message}


def failure_detail(errors):
    if len(errors) == 1:
        return "1 field is invalid."
    return f"{len(errors)} fields are invalid."
