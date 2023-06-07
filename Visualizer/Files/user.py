class User(object):
    def __init__(self, first, last, address, email, phone, university, regiments, events, direct):
        self.first = first
        self.last = last
        self.address = address
        self.email = email
        self.phone = phone
        self.university
        self.regiments = regiments #list of regiments that the user was once a part of 
        self.events = events
        self.direct = direct