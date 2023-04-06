import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
import string
import re


def clean_job_title(job_title):
    if job_title:
        job_title = job_title.replace('/', ' / ').replace(',', ' , ').replace('(', ' ( ').replace(')', ' ) ')\
                            .replace('-', ' - ')
        job_title = re.sub(r'\d+', '', job_title)

        job_title = job_title.translate(str.maketrans('', '', string.punctuation))
        job_title = job_title.lower()
        words = word_tokenize(job_title)

        stop_words = set(stopwords.words('english'))
        words = [word for word in words if not word in stop_words]
        lemmatizer = nltk.stem.WordNetLemmatizer()
        words = [lemmatizer.lemmatize(token) for token in words]
        job_title = ' '.join(words)

        return job_title


def map_job_title(job_title):
    words = ['senior', 'sr', 'junior', 'jr', 'entry level', 'mid level', 'summer', 'mid',
             'intermediate', 'remote', 'contract', 'midwest', 'west', 'midlevel', 'expert', 'associate', 'principal']
    new_text = ''
    pattern = '|'.join(words)
    new_text = re.sub(pattern, "", job_title.lower())
    new_text = ' '.join(new_text.split()).strip()
    return new_text


def extract_job_titles():
    import spacy
    from spacy.matcher import PhraseMatcher
    nlp = spacy.load('en_core_web_sm')
    phrase_list = ['Chief Information Security Officer',
                   'information security officer', 'intern cyber security', 'cyber security intern',
                   'cybersecurity intern', 'Penetration Tester', 'Ethical Hacker', 'penetration testing', 'penetration test'
                                                                                                          'Network Forensics Cybersecurity Analyst', 'Computer Forensics Analyst', 'Forensics Analyst', 'Cloud Forensics Analyst',
                   'Network Forensic Analyst', 'Network Forensics Analyst', 'Cyber Forensics Analyst',
                   'Information Security Consultant', 'Cybersecurity Consultant',
                   'Cybersecurity Advisor', 'security advisor'
                                            'Information Security Specialist', 'cyber security specialist', 'cybersecurity specialist', 'security specialist',
                   'Information Security Analyst', 'cybersecurity technologist', 'lead solutions architect', 'lead solution architect',
                   'cybersecurity analyst', 'Security Analyst', 'cyber security analyst', 'Information Systems Security Engineer',
                   'cybersecurity software engineer',
                   'Information Security Engineer', 'Cybersecurity Engineer', 'cyber security engineer',
                   'network security engineer', 'cloud security engineer', 'security engineer', 'IT Security Engineer', 'security solutions architect', 'security solution architect'
                    'architect cyber security', 'architect cybersecurity', 'cybersecurity hashivault architect',
                   'Network Security Architect', 'Cyber Network Architect', 'Cybersecurity Architect', 'Cyber security Architect', 'Information Security Architect',
                   'Security Architect', 'IT Security Architect', 'Application Security Engineer', 'lead solution architect',
                   'information security manager', 'information system security manager', 'information system security officer', 'cybersecurity manager', 'cybersecurity Systems Engineer'
                   ]
    phrase_list = [x.lower() for x in phrase_list]
    matcher = PhraseMatcher(nlp.vocab, attr='LOWER')

    for phrase in phrase_list:
        phrase_pattern = nlp(phrase)
        matcher.add(phrase, None, phrase_pattern)
    # df = pd.read_csv('/Users/akhilreddy/PycharmProjects/Scape-Save-DAEN690/Datasets/indeed_cleaned.csv.gz',
    #                  compression='gzip')
    df = pd.read_excel('/Users/akhilreddy/PycharmProjects/Scape-Save-DAEN690/Datasets/careeronestop_data.xlsx')
    # unique_titles = df['job_title'].unique()
    # job_titles = [x.lower() for x in job_titles]
    # unique_titles = list(set([title for title in unique_titles]))
    dict_list = []
    d = {}
    for each_title in df['job_title'].fillna(''):
        if each_title:
            # d['original_job_title'] = each_title
            title = clean_job_title(each_title)
            title = map_job_title(title)
            doc = nlp(title)
            matches = matcher(doc)
            max_length = 0
            matched_phrase = None
            for match_id, start, end in matches:
                length = end - start
                if length > max_length:
                    max_length = length
                    matched_phrase = doc[start:end]
            if matched_phrase:
                title = matched_phrase.text

            title = ' '.join(title.split()).strip()
            dd = {'cybersecurity engineer': ['cyber security engineer', 'engineer cyber security', 'engineer cybersecurity'],
                  'cybersecurity architect': ['cyber security architect', 'architect cybersecurity', 'architect cyber security',
                                              'cybersecurity hashivault architect'],
                  'security solutions architect': ['security solution architect'],
                  'information security architect': ['it security architect', 'security information architect'],
                  'cybersecurity analyst': ['cyber security analyst'],
                  'cybersecurity intern': ['cyber security intern', 'intern cyber security'],
                  'cybersecurity specialist': ['cyber security specialist', 'security specialist'],
                  'cybersecurity consultant': ['cyber security consultant'],
                  'cyber security advisor': ['security advisor'],
                  'network security engineer': ['security network engineer'],
                  'penetration tester': ['penetrfation testing'],
                  'cyber forensics analyst': ['cyber forensic analyst'],
                  'forensics analyst': ['forensic analyst'],
                  'network forensic analyst': ['network forensics analyst'],
                  'cybersecurity manager': ['cyber security manager'],
                  'cybersecurity systems engineer': ['cyber security systems engineer', 'cybersecurity system engineer', 'cyber security system engineer'],
                  'information security manager': ['information system security manager issm', 'information system security manager'],
                  'lead solutions architect': ['lead solution architect']}
            for i, v in dd.items():
                for each_v in v:
                    if title == each_v:
                        title = i
            # print(title)
            if title not in d.keys():
                d[title] = 1
            else:
                d[title] += 1
            # d['cleaned_job_title'] = title
            # dict_list.append(d)

    # print(dict_list)
    # print(d)
    sorted_data = sorted(d.items(), key=lambda x: x[1], reverse=True)
    print(sorted_data)
    df1 = pd.DataFrame(sorted_data)
    with pd.ExcelWriter('careeronestop_job_titles_freq.xlsx') as writer:
        df1.to_excel(writer, index=False)


extract_job_titles()
