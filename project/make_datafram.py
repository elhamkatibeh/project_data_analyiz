import pandas as pd

def category_data (title , listskill , total_datafram):
    skills = list()
    grade = list()
    Dataframe_skill = total_datafram
    for s in range(len(listskill)):
        skills.append(listskill[s][0])
        if listskill[s][1] == 'مقدماتی': grade.append(1)
        if listskill[s][1] == 'متوسط': grade.append(5)
        if listskill[s][1] == 'پیشرفته': grade.append(10)
    name_job = title
    new_row = {'job_offer': name_job}
    Dataframe_skill = pd.concat([Dataframe_skill, pd.DataFrame([new_row])], ignore_index=True)
    new_index = Dataframe_skill.index[-1]
    for i in range(len(skills)):
         if skills[i] not in Dataframe_skill.columns:
             Dataframe_skill[skills[i]] = None
         Dataframe_skill.at[new_index, skills[i]] = grade[i]
    return Dataframe_skill


