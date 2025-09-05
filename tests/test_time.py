from app.commands.time import get_current_time
import re


def test_get_current_time():
    """Test that get_current_time returns correct format"""
    result = get_current_time()
    assert isinstance(result, str) 
    
    pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
    assert re.match(pattern, result), (
        f"Expected format YYYY-MM-DD HH:MM:SS, got: {result}"
    )
    assert len(result) == 19
    return None
