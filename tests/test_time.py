from app.commands.time import time_command
import re


def test_time_command():
    result = time_command()

    assert isinstance(result, str)
    pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
    assert re.match(pattern, result), (
        f"Expected format: YYYY-MM-DD HH:MM:SS, got: {result}"
    )
    assert len(result) == 19

    return None
