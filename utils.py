import pandas as pd


def plot_schedule_old_en(xx,x_keys,L):

    name = []
    sem = []
    cred = []
    for l,l_ob in L.items():
        for i in range(len(xx)):
            if xx[i] > 0.5:
                u_a = x_keys[i][0]
                l_a = x_keys[i][1]
                if l_ob.id == l_a.id:
                    name += [u_a.name]
                    sem += [l_a.id]
                    cred += [u_a.credits]

    return pd.DataFrame({'Asignatura':name,'Semestre':sem,"Creditos":cred})

def plot_schedule_en(xx,x_keys,L):

    dict_ = {}
    for l,l_ob in L.items():
        sem_ = []
        for i in range(len(xx)):
            if xx[i] > 0.5:
                u_a = x_keys[i][0]
                l_a = x_keys[i][1]
                if l_ob.id == l_a.id:
                    sem_ += [u_a.name]
        dict_.update({l_ob:sem_})

    s1 = []
    s2 = []
    s3 = []
    s4 = []
    semester = []
    for l,list_ in dict_.items():
        s1 += [list_[0]]
        s2 += [list_[1]]
        s3 += [list_[2]]
        s4 += [list_[3]]
        if l.season == 'au':
            seas_ = 'Oto.'
        if l.season == 'sp':
            seas_ = 'Prim.'

        semester += [f"{l.id}º ({seas_})"]


    return pd.DataFrame({'Semestre':semester,'1':s1,'2':s2,'3':s3,'4':s4})

def plot_schedule(xx,x_keys,L,u_dict):

    dict_ = {}
    for l,l_ob in L.items():
        sem_ = []
        for i in range(len(xx)):
            if xx[i] > 0.5:
                u_a = x_keys[i][0]
                l_a = x_keys[i][1]
                if l_ob.id == l_a.id:
                    sem_ += [u_dict[u_a.id]]
        dict_.update({l_ob:sem_})

    s1 = []
    s2 = []
    s3 = []
    s4 = []
    semester = []
    for l,list_ in dict_.items():
        s1 += [list_[0]]
        s2 += [list_[1]]
        s3 += [list_[2]]
        s4 += [list_[3]]
        if l.season == 'au':
            seas_ = 'Oto.'
        if l.season == 'sp':
            seas_ = 'Prim.'

        semester += [f"{l.id}º ({seas_})"]


    return pd.DataFrame({'Semestre':semester,'1':s1,'2':s2,'3':s3,'4':s4})


def skills_list_en(J,xx,x_keys):

    skill = []
    al = []
    rl = []
    units = []
    for j in J:
        for s in j.skills:
            skill += [s.name]
            rl += [s.level]
            max_level = 0
            unit_name = ''
            for i in range(len(xx)):
                if xx[i] > 0.5:
                    u_a = x_keys[i][0]
                    for s_u in u_a.skills:
                        if s_u.id == s.id:
                            if s_u.level > max_level:
                                max_level = s_u.level
                                unit_name = u_a.name
            
            al += [max_level]
            units += [unit_name]
                    
    return pd.DataFrame({'Skill':skill,'Nivel Objetivo':rl,'Nivel Adquirido':al,'Asignatura':units})

def skills_list(J,xx,x_keys,dicts):

    j_trans,s_trans,u_trans = dicts

    skill = []
    al = []
    rl = []
    units = []
    for j in J:
        for s in j.skills:
            skill += [s_trans[s.id]]
            rl += [s.level]
            max_level = 0
            unit_name = ''
            for i in range(len(xx)):
                if xx[i] > 0.5:
                    u_a = x_keys[i][0]
                    for s_u in u_a.skills:
                        if s_u.id == s.id:
                            if s_u.level > max_level:
                                max_level = s_u.level
                                unit_name = u_trans[u_a.id]
            
            al += [max_level]
            units += [unit_name]
                    
    return pd.DataFrame({'Skill':skill,'Nivel Objetivo':rl,'Nivel Adquirido':al,'Asignatura':units})