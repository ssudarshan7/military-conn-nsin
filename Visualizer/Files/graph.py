import university
import regiment
import user

class Graph(object):
    def __init__(self):
        self.adj = {}
        self.regiments = []
        self.universities = []
    
    def addUser(self, user):
        self.adj[user] = [user.university]
        for regiment in user.regiments:
            self.adj[user].append(regiment)
  
    def findPastOverlap(self, user, other):
        '''for regiment in user.regiments:
            for regimentO in other.regiments:
                if (regiment.name == regiment0.name):
                    first = max(regiment.getUser(user).start, regiment.getUser'''

    
    def sameUniversity(self, user, other):
        return user.university == other.university
    
    def getEventOverlap(self, user, other):
        answer = []
        for event in user.events:
            for eventO in other.events:
                if (event == event0):
                    answer.append(event)
        return answer
    
    def getRegigmentNames(self, regiment):
        return regiment.users
    
    def getUniversityStudents(self, university):
        return university.students
    
