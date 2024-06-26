# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 16:00:00 2021

@author: ROGER
"""

import json
import os
import numpy as np
from definitions import *


def read_json(filepath):
    """
    This function reads a json file and return the contents in a dictionary.
    """
    with open(filepath,'r',encoding="utf8") as inputfile:
        data = json.loads(inputfile.read())
    return data

def read_docs(files):
    """
    Read all the files extracting all the dictionaries
    """
    
    file1 = files[0]
    file2 = files[1]
    file3 = files[2]
    file4 = files[3]
    
    courses = read_json(file1)
    jobs = read_json(file2)
    sfia = read_json(file3)
    units = read_json(file4)
    
    return courses,jobs,sfia,units

def core_dict(course):
    
    majors = {}
    core = {}
    for elem in course['core']:
        core.update({elem['id']:elem['semester']})
    for elem in course['majors']:
        element_dict = {'name':elem['name'],
                        'core':elem['core'],
                        'electives':elem['electives']}
        majors.update({elem['id']:element_dict})
        
    return core,majors
    
def units_dict(units,U_core,M_a,credits_ = 10):
    """
    Organise all the information of the units: id, name, 
    prerequisites, skills, offer and credits
    """
    units_dict = {}
    i = 1
    for unit in units:
        
        core_ = False
        if unit['id'] in U_core.keys():
            core_ = True

        unit_el = Unit(id=unit['id'],name=unit['name'],credits=credits_,core=core_)
        for s in unit['sfiaSkills']:
            skill = Skill(id=s['id'],name=s['id'],level=s['level'])
            unit_el.skills.append(skill)

        unit_el.prerequisites = unit['prerequisites']
        unit_el.seasons = unit['offer']


        units_dict.update({unit['id']:unit_el})
        
    return units_dict

def course_dict(M_a,U_core):
    """
    This function return a course element
    """
    course = Course(id="BICT",name="Bachelor of Information and Communication Technology")
    course.core = list(U_core.keys())
    for m in M_a.keys():
        major = Major(id=m,name=M_a[m]['name'])
        major.core = M_a[m]['core']
        major.electives = M_a[m]['electives']
        course.majors.update({m:major})
    return course


def job_dict(jobs_):
    
    jobs = {}
    for j in jobs_:
        job = Job(id=j['id'],name=j['name'])
        for s in j['sfia']:
            skill = Skill(id=s['id'],name=s['id'],level=s['level'])
            job.skills.append(skill)
        jobs.update({j['id']:job})
        
    return jobs
    
def skill_dict(skills):
    
    dict_ = {}
    for s in skills:
        skill = Skill(id=s['id'],name=s['name'],level=0)
        dict_.update({s['id']:skill})
        
    return dict_    
    
def data_dict(files):

    courses,jobs,skills,units = read_docs(files)
    U_core, M_a = core_dict(courses[0])
    U = units_dict(units,U_core,M_a,credits_=10)
    S = skill_dict(skills)
    course = course_dict(M_a,U_core)
    J = job_dict(jobs)
    return course,U,S,J

if __name__ == '__main__':
    
    path = os.getcwd()
    foulder = os.path.join(path,'data')
    file1 = os.path.join(foulder,"courses.json")
    file2 = os.path.join(foulder,"jobs.json")
    file3 = os.path.join(foulder,"sfia.json")
    file4 = os.path.join(foulder,"units.json")
    
    files = [file1,file2,file3,file4]
    
    course,U,S,J = data_dict(files)
    print(course,course.name)
    for u in U.keys():
        print(u,U[u].name)

    for s in S.keys():
        print(s,S[s].name)

    for j in J.keys():
        print(j,J[j].name)
    
    
    
    
    
    
    
    
    

    