"""
Roger Lera
27/01/2023
"""

class Skill:
    """
    This class stores the information about skills and its level.
    """

    def __init__(self,id,name,level):
        self.id = id
        self.name = name
        self.level = level

    def __str__(self):
        string_ = f"{self.id}: \t Skill: {self.name} \t Level: {self.level}"
        return string_
    
    def __repr__(self) -> str:
        return self.id

    def check_skill(self,skill_list):
        """
            This function checks if a given skill is in a list and returns the skill
            and its level or the self skill and level 0 if it is not found
        """
        for s in skill_list:
            if s.id == self.id: #skill found in list returning level
                return s,s.level
        
        return self,0 # skill not found, returning level 0
    
    def add_skill(self,skill_list):
        """
            This function adds a given skill in a list and updates it's level if it is higher
        """
        s,lev_ = self.check_skill(skill_list)
        if lev_ == 0: #skill not found
            skill_list.append(self)
        else: #skill found, check level and update
            if self.level > s.level: #update
                skill_list.remove(s)
                skill_list.append(self)


class Unit:
    """
    This class stores the information about units and its methods.
    """

    def __init__(self,id,name,credits=10,core=False):
        self.id = id
        self.name = name
        self.skills = [] #skills obtained after completing activity
        self.prerequisites = [] #units required to do the activity
        self.credits = credits #time slots to complete the activity
        self.core = core
        self.seasons = [] #semesters offered
    
    def __str__(self):
        string_ = f"{self.id} \t Unit: {self.name} \n Time: {self.credits}"        
        return string_
    
    def __repr__(self) -> str:
        return self.id
    
class Semester:
    """
    This class stores the information about semesters.
    """
    def __init__(self,id,season,credits=40):
        self.id = id
        self.season = season
        self.credits = credits
    
    def __str__(self):
        return f"{self.id}:{self.season}"
    
    def __repr__(self) -> int:
        return self.id
    
class Major:
    """
    This class stores the information about a major.
    """
    def __init__(self,id,name):
        self.id = id
        self.name = name
        self.core = []
        self.electives = []
    
    def __str__(self) -> float:
        return f"{self.id}"
    
    def __repr__(self) -> int:
        return self.id
    

class Course:
    """
    This class stores the information about a major.
    """
    def __init__(self,id,name,credits=240):
        self.id = id
        self.name = name
        self.core = []
        self.credits = credits
        self.semesters = []
        self.majors = {}
    
    def __str__(self) -> float:
        return f"{self.id}"
    
    def __repr__(self) -> int:
        return self.id
    
class Job:
    """
    This class stores the information about Jobs and its methods.
    """

    def __init__(self,id,name,descriptor=None):
        self.id = id
        self.name = name
        self.descriptor = descriptor
        self.skills = [] #skills needed for obtaining the job

    def __str__(self):
        string_ = f"Job: {self.name} ({self.id})"
        return string_
    
    def __repr__(self) -> int:
        return self.id

