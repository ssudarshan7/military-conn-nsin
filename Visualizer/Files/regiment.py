class Regiment(object):
    def __init__(self, name, users, start, end):
        self.name = name
        self.users = users #users in the regiment - array
        self.start = start #date at which user[i] joined
        self.end = end #date at which user[i] left