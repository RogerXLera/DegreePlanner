# -*- coding: utf-8 -*-
"""
Author: Roger X. Lera Leri
Date: 30/09/2023
"""
from definitions import *
from matrices import array_creation
from read_files import data_dict
import numpy as np
import argparse as ap
import time
import csv
import os
import cvxpy as cp

def problem_cvxpy(matrices):

    L,x_keys,B,P,C,D,d,R,or_,r,E,F,f,G,g,t,A,K,keys_ = matrices

    # creating the model
    keys = list(x_keys.keys())
    len_x = len(keys)
    len_v = np.shape(f)[1]
    len_y = np.shape(A)[0]
    len_z = np.shape(K)[0]
    Delta = len(x_keys)

    ############################VARIABLES#############################
    
    x = cp.Variable(len_x,boolean=True) # set variables as a vector x (start date)
    v = cp.Variable(len_v,boolean=True) # set variables as a vector x' (finish date)
    y = cp.Variable(len_y,boolean=True) # set auxiliary variables as a vector y
    z = cp.Variable(len_z,integer=True) # set auxiliary variables as a vector z
    zl = cp.Variable(len_z,integer=True) # set auxiliary variables as a vector z

    ############################CONSTRAINTS############################

    c1 = [B@x <= np.ones((np.shape(B)[0]))]
    c2 = [P@x == np.zeros((np.shape(P)[0]))]
    c3 = [D@x == d]
    c4 = [R@x >= r@x]
    c5 = [E@x == np.ones((np.shape(E)[0]))]
    c6 = [np.ones((len_v)).T@v >= 1]
    c7 = [F@x >= f@v]
    c8 = [G@x >= g@v]
    c9 = [A@x <= Delta*y]
    c10 = [A@x >= Delta*(y-np.ones((len_y))) + np.ones((len_y))]
    c11 = [z <= K@y - t]
    c12 = [z <= np.zeros((len_z))]
    c13 = [z <= zl]
    c14 = [-zl <= z]

    cs = c1+c2+c3+c4+c5+c6+c7+c8+c9+c10+c11+c12+c13+c14

    problem = cp.Problem(cp.Minimize(np.ones((len_z)).T@zl),cs)

    return problem,x,v,y,z


def solve_problem(problem,x,y,v,z,solver,solvertime=30,max_iter=1000,verbose=True):
    """
        We solve the problem
    """
    st = time.time()
    #problem.solve(solver=solver,verbose=True,cplex_params={},cplex_filename=f"model_{args.p}.lp")
    if solver == 'CPLEX':
        problem.solve(solver=solver,verbose=verbose,cplex_params={'timelimit':solvertime,})
    elif solver == 'ECOS_BB':
        problem.solve(solver=solver,verbose=verbose,mi_max_iters=max_iter)
    elif solver == 'GLPK_MI':
        problem.solve(solver=solver,verbose=verbose,options = {'num_iter':max_iter},tm_limit=solvertime)
    else:
        problem.solve(solver=solver,verbose=verbose)
    obj_value = problem.value
    print("The optimal value is", obj_value)
    xx = np.array(x.value) #list with the results of x (|x| dim)
    vv = np.array(v.value)
    yy = np.array(y.value)
    zz = np.array(z.value)
    solve_time = time.time() - st
    
    
    return obj_value,xx,vv,yy,zz,solve_time
    


def solve_model(model,x,x_keys,docplex=False,cp=False,log=True):
    
    if log:
        model.print_information()
        if args.cp:
            model.export_as_cpo(f'cp.cpo')
        else:
            model.export_as_lp(f'cplex_{docplex}.lp')
            
        mdlsolve = model.solve(log_output=True)
        model.report()
    else:
        if args.cp:
            mdlsolve = model.solve(LogVerbosity='Quiet')
        else:
            mdlsolve = model.solve(log_output=False)

    if args.cp:
        f_ = mdlsolve.get_objective_value()
        sol = mdlsolve.get_all_var_solutions()
        keys = [k for k in x_keys.keys()]
        assignments = {}
        for i in x.keys():
            value = mdlsolve.get_value(x[i])

            if value > 0.5:
                unit = x_keys[i][0]
                l = x_keys[i][1]
                assignments.update({i:(unit,l)})
        
        return assignments,f_,mdlsolve.get_solve_time(),mdlsolve

    else:
        f_ = model.objective_value

        assignments = {}
        for i in x_keys.keys():
            if x[i].solution_value > 0.5:
                unit = x_keys[i][0]
                l = x_keys[i][1]
                assignments.update({i:(unit,l)})

        return assignments,f_,model.solve_details.time,mdlsolve

def print_plan_old(assignments,L):

    print('****************************************')
    print('***************** PLAN *****************')
    print('****************************************')
    print()
    print("------------------------------------")
    for l in L.keys():
        l_ob = L[l]
        print(f"SEMESTER: {l_ob.id}")
        for i in assignments.keys():
            u_a = assignments[i][0]
            l_a = assignments[i][1]
            if l_ob.id == l_a.id:
                print(f"\t {u_a.name}")

        print("------------------------------------")


    return None

def print_plan(xx,x_keys,L):

    print('****************************************')
    print('***************** PLAN *****************')
    print('****************************************')
    print()
    print("------------------------------------")
    for l,l_ob in L.items():
        print(f"SEMESTER: {l_ob.id}")
        for i in range(len(xx)):
            if xx[i] > 0.5:
                u_a = x_keys[i][0]
                l_a = x_keys[i][1]
                if l_ob.id == l_a.id:
                    print(f"\t {u_a.name}")

        print("------------------------------------")


    return None

def z_vec(x,x_keys,S,matrix_sv,mdlsolve):

    if args.docplex:
        z = []
        for i in range(len(S.keys())):

            elem = [matrix_sv[i][j]*x[j].solution_value for j in x.keys()]
            min_ = min([max(elem)-t[i],0])
            z += [min_]

        return np.array(z)
    else:
        z = []
        for i in range(len(S.keys())):

            elem = [matrix_sv[i][j]*mdlsolve.get_value(x[j]) for j,var_e in x_keys.items()]
            min_ = min([max(elem)-t[i],0])
            z += [min_]

        return np.array(z)


      
def job_affinity(t,zz):
    
    sum = 0
    den = 0
    for i in range(0,len(t)):
        
        sum += np.abs(t[i] + zz[i])
        den += np.abs(t[i])
        
    return (sum/den)*100

def job_affinity_single(t,zz,J,S,job_id):

    from matrices import target

    skill_vec_sol = np.zeros(len(t),dtype=np.int8)
    for i in range(0,len(t)):
        skill_vec_sol[i] = np.abs(t[i] + zz[i])

    single_job_affin = {}
    for j_id in job_id:
        t_single = target(J[j_id],S)
        skill_vec_per_job = np.minimum(t_single,skill_vec_sol)
        num = np.sum(skill_vec_per_job)
        den = np.sum(t_single)
        ja = num/den*100
        print(f"Job affinity per job ({j_id}) = {ja:.2f}%")
        single_job_affin.update({j_id:ja})
        
    return single_job_affin
                
        

if __name__ == '__main__':
    
    path = os.getcwd()
    foulder = os.path.join(path,'data')
    file1 = os.path.join(foulder,"courses.json")
    file2 = os.path.join(foulder,"jobs.json")
    file3 = os.path.join(foulder,"sfia.json")
    file4 = os.path.join(foulder,"units.json")
    
    files = [file1,file2,file3,file4]
    
    parser = ap.ArgumentParser()
    parser.add_argument('-n', type=int, default=6, help='n')
    parser.add_argument('-p', type=float, default=1, help='p')
    parser.add_argument('-c', type=int, default=240, help='c')
    parser.add_argument('-l', type=int, default=7, help='l: maximum level. Default: 7')
    parser.add_argument('-j', type=str, default='0', help='Job index')
    parser.add_argument('-s', type=str, choices=['au','sp'], default='au',help='Start semester')
    parser.add_argument('--solver', type=str, choices=['CPLEX','GLPK_MI'], default='GLPK_MI',help='solver')
    parser.add_argument('--docplex', help='docplex transformation', action='store_true')
    parser.add_argument('--cp', help='cp solver', action='store_true')
    parser.add_argument('--log', help='log solver', action='store_true')
    args = parser.parse_args()
    
    if args.p == -1:
        p = 'inf'
    else:
        p = args.p
    
    job_id = args.j.split(',')
    c_T = args.c
    n_sem = args.n
    fs = args.s
    m_lev = args.l

    course,U,S,J = data_dict(files)
    seasons = ["au","sp"]
        
    
    matrices = array_creation(course,U,S,J,job_id,seasons,n_sem,f_sem=fs,m_cred=40,max_level=m_lev)   
    L,x_keys,B,P,C,D,d,R,or_,r,E,F,f,G,g,t,A,K,keys = matrices

    problem,x,v,y,z = problem_cvxpy(matrices)
    obj_value,xx,vv,yy,zz,solve_time = solve_problem(problem,x,y,v,z,args.solver,solvertime=30,max_iter=1000,verbose=True)

    print_plan(xx,x_keys,L)
    print(f"Solving time = {solve_time:.2f}s")
    alpha = job_affinity(t,zz)
    print("------------------------------------")
    print(f"Global Job affinity = {alpha:.2f}%")
    print("------------------------------------")
    job_affinity_single(t,zz,J,S,job_id)
