# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 10:04:22 2021

@author: ROGER
"""

"""
In this script there are all the functions that will create the matrices and vectors
for our ILP formalisation
"""
import numpy as np
import os
from read_files import data_dict
from definitions import *


def semesters(course,semesters_available,n_sem=6,max_cred=40,first_semester='au'):
    """
    This function returns a dict with the sequence of 6 semesters. Each semester
    is a dictionary with the season of the 
    """
    sequence = {}
    index_ = semesters_available.index(first_semester)
    for i in range(1,n_sem+1):
        sem = Semester(id=i,season=semesters_available[index_],credits=max_cred)
        sequence.update({i:sem})
        course.semesters.append(sem)
        if index_ == len(semesters_available) - 1:
            index_ = 0
        else:
            index_ += 1
        
    return sequence


def decision_variables(U,L):
    """
    This function returns a dictionary with all the keys of the decision variables
    """

    x_keys = {}
    i=0
    for u in U.keys():
        for l in L.keys():
            x_keys.update({i:(U[u],L[l])})
            i += 1

    return x_keys

def B_matrix(x_dict,U):
    """
    This function returns the B matrix of the formalisation of CPP.
    """
    
    B = []
    keys = {}
    counter = 0
    for u in U.keys():
        row = []
        unit1 = U[u]
        for i in x_dict.keys():
            unit2 = x_dict[i][0]
            if unit1 == unit2:
                row.append(1)
            else:
                row.append(0)
                    
        B.append(row)
        keys.update({f"b{counter}":[unit1]})
        counter += 1
    return np.array(B),keys

def P_matrix(x_dict):
    """
    This function returns the P matrix of the formalisation of CPP.
    """
    P = []
    keys = {}
    counter = 0
    x_list = list(x_dict.keys())
    for i in x_dict.keys():
        row = []
        unit1 = x_dict[i][0]
        l1 = x_dict[i][1]

        for j in x_list:
            unit2 = x_dict[j][0]
            l2 = x_dict[j][1]
            if unit1.id == unit2.id and l1 == l2 and l1.season not in unit1.seasons:
                row.append(1)
            else:
                row.append(0)
                    
        P.append(row)
        keys.update({f"p{counter}":[unit1,l1]})
        counter += 1
    return np.array(P),keys

def C_vector(x_dict):
    """
    This function returns the C vector of the formalisation of CPP.
    """
    C = []
    for i in x_dict.keys():
        unit = x_dict[i][0]
        C.append(unit.credits)
    return np.array(C),{f"c{0}":()}


def D_matrix(x_dict,L):
    """
    This function returns the D matrix of the formalisation of CPP.
    """
    D = []
    keys = {}
    counter = 0
    for l in L.keys():
        l1 = L[l]
        row = []
        for i in x_dict.keys():
            unit2 = x_dict[i][0]
            l2 = x_dict[i][1]
            if l1 == l2:
                row.append(unit2.credits)
            else:
                row.append(0)
                    
        D.append(row)
        keys.update({f"d{counter}":[l1]})
        counter += 1
    
    return np.array(D),keys

def d_vector(L):
    """
    This function returns the d vector of the formalisation of CPP.
    """
    
    d = []
    for l in L.keys():
        d.append(L[l].credits)
            
    return np.array(d)


def R_matrix(x_dict,U,L):
    """
    This function returns the R matrix of the formalisation of CPP regarding 
    the precedence relationships.
    """
    
    or_ = []
    for u in U.keys():
        unit = U[u]
        for prereq in unit.prerequisites:
            if isinstance(prereq,list):
                or_.append((prereq,unit))
            else:
                or_.append(([prereq],unit))
    
    R = []
    keys = {}
    counter = 0
    for prer in or_:
        
        for l in L.keys():
            row = []
            l1 = L[l]
        
            for i in x_dict.keys():
                unit2 = x_dict[i][0]
                l2 = x_dict[i][1]
                if unit2.id in prer[0] and l1.id > l2.id:
                    row.append(1)
                else:
                    row.append(0)
                    
            R.append(row)
            keys.update({f"r{counter}":[prer[1],l1]})
            counter += 1
    
    return np.array(R),or_,keys

def r_matrix(x_dict,L,or_):
    
    """
    This function returns the r vector of the formalisation of CPP regarding 
    the precedence relationships.
    """
    
    r = []
    for prer in or_:
        
        for l in L.keys():
            row = []
            l1 = L[l]
        
            for i in x_dict.keys():
                unit2 = x_dict[i][0]
                l2 = x_dict[i][1]
                if unit2.id == prer[1].id and l1.id == l2.id:
                    row.append(1)
                else:
                    row.append(0)
                    
            r.append(row)
    
    return np.array(r)


def E_matrix(x_dict,course):
    """
    This function returns the E matrix of the formalisation of CPP.
    """
    
    E = []
    keys = {}
    counter = 0
    for unit1 in course.core:
        row = []
        unit_to_save = unit1
        for i in x_dict.keys():
            unit2 = x_dict[i][0]
            if unit1 == unit2.id:
                unit_to_save = unit2
                row.append(1)
            else:
                row.append(0)
                    
        E.append(row)
        keys.update({f"e{counter}":[unit_to_save]})
        counter += 1
    
    return np.array(E),keys

def F_matrix(x_dict,course):
    """
    This function returns the F matrix of the formalisation of CPP.
    """
    
    F = []
    keys = {}
    counter = 0
    for m in course.majors.keys():
        major = course.majors[m]
        for unit1 in major.core:
            row = []
            unit_to_save = unit1
            
            for i in x_dict.keys():
                unit2 = x_dict[i][0]
                if unit1 == unit2.id:
                    unit_to_save = unit2
                    row.append(1)
                else:
                    row.append(0)
                        
            F.append(row)
            keys.update({f"f{counter}":[major,unit_to_save]})
            counter += 1
    
    return np.array(F),keys

def f_matrix(course):
    
    f = []
    i = 0
    for m1 in course.majors.keys():
        major1 = course.majors[m1]
        for unit1 in major1.core:
            row = []
            
            for m2 in course.majors.keys():
                major2 = course.majors[m2]
                if unit1 in major2.core:
                    row.append(1)
                else:
                    row.append(0)
                        
            f.append(row)
    
    return np.array(f)


def G_matrix(x_dict,course):
    """
    This function returns the G matrix of the formalisation of CPP.
    """
    
    G = []
    keys = {}
    counter = 0
    for m in course.majors.keys():
        major = course.majors[m]
        for elec_dict in major.electives:
            row = []
            
            for i in x_dict.keys():
                unit2 = x_dict[i][0]
                if unit2.id in elec_dict['units']:
                    row.append(1)
                else:
                    row.append(0)
                        
            G.append(row)
            keys.update({f"g{counter}":[major,elec_dict]})
            counter += 1

    return np.array(G),keys

def g_matrix(course):
    
    g = []
    for m in course.majors.keys():
        major = course.majors[m]
        for elec_dict in major.electives:
            row = []
            
            for m2 in course.majors.keys():
                major2 = course.majors[m2]
                if major.id == major2.id:
                    row.append(elec_dict['count'])
                else:
                    row.append(0)
                        
            g.append(row)
    
    return np.array(g)


def target(job,S):
    
    t = []
    skill_id = [sk.id for sk in job.skills]
    for s in S.keys():
        skill = S[s]
        if skill.id in skill_id:
            for skill2 in job.skills:
                if skill.id == skill2.id:
                    t.append(skill2.level)
        else:
            t.append(0)
    
    return np.array(t)

def A_matrix(x_dict,S,max_level=7):
    """
    We will compute matrix Amax of the formalisation
    """
    
    A = []
    keys = {}
    counter = 0
    for s in S.keys():
        skill1 = S[s]
        for level in range(1,max_level+1):
            row = []
            for i in x_dict.keys():
                unit2 = x_dict[i][0]
                sk_level = 0
                for skill2 in unit2.skills:
                    if skill1.id == skill2.id:
                        sk_level = skill2.level
                        break
                if sk_level >= level:
                    row.append(1)
                else:
                    row.append(0)
            
            A.append(row)
            keys.update({f"a{counter}":[skill1,level]})
            counter += 1
            
    return np.array(A),keys
                
def K_matrix(S,max_level = 7):
    """
    We will compute matrix Amax of the formalisation
    """
    
    K = []
    keys = {}
    counter = 0
    for s1 in S.keys():
        skill1 = S[s1]
        row = []
        for s2 in S.keys():
            skill2 = S[s2]
            for level in range(1,max_level+1):
                if skill1.id == skill2.id:
                    row.append(1)
                else:
                    row.append(0)
                    
        K.append(row)
        keys.update({f"k{counter}":[skill1]})
        counter += 1
        
    return np.array(K),keys


def merge_dictionaries(dict1, dict2):
    merged_dict = dict1.copy()
    merged_dict.update(dict2)
    return merged_dict


def array_creation(course,U,S,J,job_index,seasons,n_sem=6,f_sem='au',m_cred=40,max_level=7):
    L = semesters(course,seasons,n_sem=n_sem,max_cred=m_cred,first_semester=f_sem)
    x_keys = decision_variables(U,L)
    B,keys = B_matrix(x_keys,U)
    P,keys_new = P_matrix(x_keys)
    keys = merge_dictionaries(keys, keys_new)
    C,keys_new = C_vector(x_keys)
    keys = merge_dictionaries(keys, keys_new)
    D,keys_new = D_matrix(x_keys,L)
    keys = merge_dictionaries(keys, keys_new)
    d = d_vector(L)
    R,or_,keys_new = R_matrix(x_keys,U,L)
    keys = merge_dictionaries(keys, keys_new)
    r = r_matrix(x_keys,L,or_)
    E,keys_new = E_matrix(x_keys,course)
    keys = merge_dictionaries(keys, keys_new)
    F,keys_new = F_matrix(x_keys,course)
    keys = merge_dictionaries(keys, keys_new)
    f = f_matrix(course)
    G,keys_new = G_matrix(x_keys,course)
    keys = merge_dictionaries(keys, keys_new)
    g = g_matrix(course)
    
    t = np.zeros(len(S),dtype=np.int8)
    for job in job_index:
        t_new = target(J[job],S)
        t = np.maximum(t,t_new)
        
    A,keys_new = A_matrix(x_keys,S,max_level)
    keys = merge_dictionaries(keys, keys_new)
    K,keys_new = K_matrix(S,max_level)
    keys = merge_dictionaries(keys, keys_new)

    return L,x_keys,B,P,C,D,d,R,or_,r,E,F,f,G,g,t,A,K,keys

if __name__ == '__main__':
    
    path = os.getcwd()
    foulder = os.path.join(path,'data')
    file1 = os.path.join(foulder,"courses.json")
    file2 = os.path.join(foulder,"jobs.json")
    file3 = os.path.join(foulder,"sfia.json")
    file4 = os.path.join(foulder,"units.json")
    
    files = [file1,file2,file3,file4]
    max_level = 7
    course,U,S,J = data_dict(files)
    seasons = ["au","sp"]
    matrices = array_creation(course,U,S,J,['122'],seasons,n_sem=6,f_sem='au',m_cred=40,max_level=7)
    

    