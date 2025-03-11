api_counter = {"count": 0}

def increment_counter():
    """Increment the API request count."""
    api_counter["count"] += 1

def get_counter():
    """Return the total number of API requests made."""
    return {"api_request_count": api_counter["count"]}