users = {}

def register(username, password):
    users[username] = password

def login(username, password):
    return users.get(username) == password