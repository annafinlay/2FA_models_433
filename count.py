# To access test data go to http://127.0.0.1:5000/api_count

api_call_count = 0

def increment_api_call_count():
    global api_call_count
    api_call_count += 1

def get_api_call_count():
    return api_call_count