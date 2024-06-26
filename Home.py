"""
Roger Lera
19/10/2023
"""
import os
import numpy as np
import pandas as pd
from definitions import *
from matrices import array_creation
from problem import problem_cvxpy,solve_problem,job_affinity,job_affinity_single
from utils import plot_schedule,skills_list
import time
import csv
from read_files import *
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def pie_chart(fa):
    #st.write(f"##### Skills required by this job field that you would acquire if you follow this learning pathway: {fa:.0f} %")
    df_fa = pd.DataFrame({'name':['Skills Aprendidas','Skills No Aprendidas'],'percentage':[fa,100-fa]})
    pie = px.pie(df_fa, values='percentage', names='name',color='name',
                color_discrete_map={'Skills Aprendidas':'green',
                                'Skills No Aprendidas':'red'},
                category_orders={'name':['Skills Aprendidas','Skills No Aprendidas']})
    pie = px.pie(df_fa, values='percentage', names='name',color='name',
                category_orders={'name':['Skills Aprendidas','Skills No Aprendidas']})
    pie.update_layout(legend=dict(font=dict(size=16)),
                    font_size=16)
    
    st.plotly_chart(pie)
    return None

def bar_chart(ja_dict,j_trans):
    #st.write(f"##### Skills Aprendidas")
    ja_df = pd.DataFrame({'ja':ja_dict.values(),'Trabajos':[j_trans[j_id] for j_id in ja_dict.keys()]})
    print(ja_df)
    bar = px.bar(ja_df, x='ja', y='Trabajos', orientation='h')
    bar.update_xaxes(title_text = "Porcentage de skills aprendidas en (%)",
                    range=[0, 100],
                    tickfont=dict(size=14))
    bar.update_yaxes(tickfont=dict(size=14))
    bar.update_layout(yaxis=dict(title=dict(font=dict(size=16))),
                    xaxis=dict(title=dict(font=dict(size=16))))
    st.plotly_chart(bar)
    return None


path = os.getcwd()
foulder = os.path.join(path,'data')
file1 = os.path.join(foulder,"courses.json")
file2 = os.path.join(foulder,"jobs.json")
file3 = os.path.join(foulder,"sfia.json")
file4 = os.path.join(foulder,"units.json")

files = [file1,file2,file3,file4]


try:
    course = st.session_state['course']
    U = st.session_state['U']
    S = st.session_state['S']
    J = st.session_state['J']
    #j_dict = st.session_state['j_dict']
    j_trans = st.session_state['j_trans']
    s_trans = st.session_state['s_trans']
    u_trans = st.session_state['u_trans']
    
except:
    course,U,S,J = data_dict(files)
    #j_dict = {j.id:j.name for j_id,j in J.items()}
    j_trans,s_trans,u_trans = read_translations()
    st.session_state['course'] = course   
    st.session_state['U'] = U
    st.session_state['S'] = S
    st.session_state['J'] = J
    #st.session_state['j_dict'] = j_dict
    st.session_state['s_trans'] = s_trans
    st.session_state['u_trans'] = u_trans

st.write("# Planea Tu Grado :books:")
st.write("## Grado en Tecnologías de la Información y la Comunicación")

st.write(
    """
        Escoge tu(s) trabajo deseado y descubre qué asignaturas debes cursar 
        para terminar el grado más preparado.  
    """
    )

c_T = 240
n_sem = 6
fs = 'au'
m_lev = 7
seasons = ["au","sp"]
solver_ = 'GLPK_MI'



job_id = st.multiselect("Trabajo(s) deseado",
               j_trans.keys(), default=None, 
               format_func=lambda x : j_trans[x],
               key=None, help=None, on_change=None, args=None, kwargs=None, 
               max_selections=5, placeholder="Escoje una opción", disabled=False, label_visibility="visible"
)


if len(job_id) > 0:
    with st.spinner(text="Calculando..."):
        matrices = array_creation(course,U,S,J,job_id,seasons,n_sem,f_sem=fs,m_cred=40,max_level=m_lev)
        L,x_keys,B,P,C,D,d,R,or_,r,E,F,f,G,g,t,A,K,keys = matrices
        problem,x,v,y,z = problem_cvxpy(matrices)
        obj_value,xx,vv,yy,zz,solve_time = solve_problem(problem,x,y,v,z,solver_,solvertime=30,max_iter=1000,verbose=False)

    df = plot_schedule(xx,x_keys,L,u_trans)
    styler = df.style.hide_index()
    
    st.write(styler.to_html(escape=False, index=False), unsafe_allow_html=True)

    ja = job_affinity(t,zz)
    st.write(f"##### Skills Aprendidas:")

    dicts = j_trans,s_trans,u_trans

    df_s = skills_list([J[j_id] for j_id in job_id],xx,x_keys,dicts)
    
    pie_chart(ja)

    styler = df_s.style.hide_index()
    st.write(styler.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    if len(job_id) > 1:
        ja_dict = job_affinity_single(t,zz,J,S,job_id)
        bar_chart(ja_dict,j_trans)