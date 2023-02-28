#O*Net KSA Data Cleaning
import pandas as pd 
Knowledge
knowledge = pd.read_csv("/Users/hanna/Code+Data/knowledge_onet.csv")
knowledge_desc = pd.read_csv("/Users/hanna/Code+Data/knowledge.csv")
#knowledge
#joined with dataframe with knowledge descriptions 
know_j = knowledge.set_index('Element Name').join(knowledge_desc.set_index('Knowledge'))
know_j.drop(columns=['Importance'], inplace=True)
#filtered for cybersecurity-related roles 
know_update = know_j.query("Title == ['Information Security Analysts', 'Chief Executives', 'Computer Network Architects','Computer Systems Analysts', 'Computer and Information Research Scientists', 'Computer and Information Systems Managers','Information Technology Project Managers', 'Intelligence Analysts', 'Training and Development Specialists', 'Computer Systems Engineer/Architects', 'Computer Network Support Specialist'  ]")
know_update
#create list to save scores
scores = []

#run through each row
for i in range(len(know_update)):
    #if scale id is IM
    if know_update['Scale ID'][i] == 'IM':
        #perform data manipulation and append to list
        scores.append(((know_update['Data Value'][i])/5)*100)
    else:
        #perform data manipulation and append to list if not IM
        scores.append(((know_update['Data Value'][i])/7)*100)
#create new column in df w/scores from scores list
know_update.insert(loc=5, column='Scores', value=scores)
        
know_update.reset_index(inplace=True)
know_update
#Skills
skills = pd.read_csv("/Users/hanna/Code+Data/skills_onet.csv")
skills_desc = pd.read_csv("/Users/hanna/Code+Data/skills.csv")
#joined with dataframe with skills descriptions 
skill_j = skills.set_index('Element Name').join(skills_desc.set_index('Skill'))
skill_j.drop(columns=['Importance'], inplace=True)
#filtered for cybersecurity-related roles 
skill_update = skill_j.query("Title == ['Information Security Analysts', 'Chief Executives', 'Computer Network Architects','Computer Systems Analysts', 'Computer and Information Research Scientists', 'Computer and Information Systems Managers','Information Technology Project Managers', 'Intelligence Analysts', 'Training and Development Specialists', 'Computer Systems Engineer/Architects', 'Computer Network Support Specialist'  ]")
#create list to save scores
scores = []

#run through each row
for i in range(len(skill_update)):
    #if scale id is IM
    if skill_update['Scale ID'][i] == 'IM':
        #perform data manipulation and append to list
        scores.append(((skill_update['Data Value'][i])/5)*100)
    else:
        #perform data manipulation and append to list if not IM
        scores.append(((skill_update['Data Value'][i])/7)*100)
#create new column in df w/scores from scores list
skill_update.insert(loc=5, column='Scores', value=scores)
skill_j.reset_index(inplace=True)

#Abilities
ab = pd.read_csv("/Users/hanna/Code+Data/abilities_onet.csv")
ab_desc = pd.read_csv("/Users/hanna/Code+Data/abilities.csv")
#joined with dataframe with knowledge descriptions 
ab_j = ab.set_index('Element Name').join(ab_desc.set_index('Ability'))
ab_j.drop(columns=['Importance'], inplace=True)
#filtered for cybersecurity-related roles 
ab_update = ab_j.query("Title == ['Information Security Analysts', 'Chief Executives', 'Computer Network Architects','Computer Systems Analysts', 'Computer and Information Research Scientists', 'Computer and Information Systems Managers','Information Technology Project Managers', 'Intelligence Analysts', 'Training and Development Specialists', 'Computer Systems Engineer/Architects', 'Computer Network Support Specialist'  ]")
#create list to save scores
scores = []

#run through each row
for i in range(len(ab_update)):
    #if scale id is IM
    if ab_update['Scale ID'][i] == 'IM':
        #perform data manipulation and append to list
        scores.append(((ab_update['Data Value'][i])/5)*100)
    else:
        #perform data manipulation and append to list if not IM
        scores.append(((ab_update['Data Value'][i])/7)*100)
#create new column in df w/scores from scores list
ab_update.insert(loc=5, column='Scores', value=scores)
ab_j.reset_index(inplace=True)