from jsonschema import validate, FormatChecker
from jsonschema.exceptions import ValidationError
from werkzeug.exceptions import BadRequest


def validate_email_format(email):
    # Simple email format validation
    return '@' in email


def validate_json(instance, schema):
    format_checker = FormatChecker()
    format_checker.checks("email")(validate_email_format)
    try:
        validate(instance=instance, schema=schema,
                 format_checker=format_checker)
    except ValidationError as e:
        raise BadRequest(e.message)
