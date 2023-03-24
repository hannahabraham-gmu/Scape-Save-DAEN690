import pandas as pd
import re
import requests

def careeronestop_data():
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import StaleElementReferenceException
    import time

    from bs4 import BeautifulSoup


    chromeOptions = Options()
    chromeOptions.headless = False

    keywords = ['Chief Information Security Officer (CISO)', 'Cybersecurity Analyst',
                'Penetration Tester', 'Cybersecurity Engineer', 'Security Architect',
                'Computer Forensics Analyst', 'Network Security Architect', 'Cybersecurity Architect', 'Information Security Consultant',
                'Cybersecurity Consultant', 'Cybersecurity Advisor', 'Ethical Hacker', 'Information Security Specialist',
                'Information Security Architect', 'Security Analyst', 'Information Security Analyst', 'Information Security Engineer']

    driver = webdriver.Chrome(options=chromeOptions)

    job_postings = []
    time.sleep(2)
    try:
        for keyword in keywords:
            driver.get('https://www.careeronestop.org/JobSearch/job-search.aspx')
            search_box = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'FindaJobNowkeyword')))
            search_box.send_keys(keyword)
            search_box.send_keys(Keys.RETURN)
            driver.implicitly_wait(10)
            soup1 = BeautifulSoup(driver.page_source, 'html.parser')
            page_ul = soup1.find('ul', {"class": 'cos-page'})
            num_pages = 0
            if page_ul is not None:
                last_page_link = page_ul.find_all('a')[-1]
                num_pages = int(last_page_link.text)
            cc = driver.current_url
            for page_num in range(1, num_pages + 1):
                current_url = cc + '&currentpage=' + str(page_num)
                print("current_url:::", current_url)
                driver.get(current_url)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                table = soup.find("table", {"class": "cos-table-responsive"})
                if table is not None:
                    tbody = table.find('tbody')
                    if tbody is not None:
                        count = 0
                        for row in tbody.find_all("tr"):
                            job_posting = {"keyword": "", "job_title": "", "company": "", "location": "", "date_posted": "", "job_link": "", "description": ""}
                            try:
                                count += 1
                                print("keyword::", keyword, "page num::", page_num, "job count::", count)
                                columns = row.find_all("td")
                                if columns is not None:
                                    job_posting["keyword"] = keyword
                                    # job_posting["job_title"] = columns[0].text.strip()
                                    # job_posting["company"] = columns[1].text.strip().split('\n')[0]
                                    # job_posting["location"] = columns[2].text.strip()
                                    if columns[0].find("a") is not None:

                                        url = 'https://www.careeronestop.org'+columns[0].find("a")["href"].replace(' ', '%20')
                                        if url:
                                            job_posting["job_link"] = re.sub(r'lang=[a-z]{2}', 'lang=en', url)
                                            # driver = webdriver.Chrome()
                                            driver.get(job_posting["job_link"])
                                            job_details_html = driver.page_source
                                            job_details_soup = BeautifulSoup(job_details_html, "html.parser")
                                            if job_details_soup.find('span', {'id': 'ctl17_lblJobTitle'}) is not None:
                                                job_posting['job_title'] = job_details_soup.find('span', {'id': 'ctl17_lblJobTitle'}).text.strip()
                                            if job_details_soup.find('span', {'id': 'ctl17_lblCompany'}) is not None:
                                                job_posting['company'] = job_details_soup.find('span', {'id': 'ctl17_lblCompany'}).text.strip()
                                            if job_details_soup.find('span', {'id': 'ctl17_lblLocation'}) is not None:
                                                job_posting['location'] = job_details_soup.find('span', {'id': 'ctl17_lblLocation'}).text.strip()
                                            if job_details_soup.find('span', {'id': 'ctl17_lblDate'}) is not None:
                                                job_posting['date_posted'] = job_details_soup.find('span', { 'id': 'ctl17_lblDate'}).text.strip()
                                            if job_details_soup.find("div", {"id": "ctl17_lblDesc"}) is not None:
                                                job_posting["description"] = job_details_soup.find("div", { "id": "ctl17_lblDesc"}).text.strip()
                                            # print(job_posting)
                                            # driver.quit()
                                            job_postings.append(job_posting)
                            except TypeError:
                                pass
                            # break
                        if keyword == 'Network Security Architect' and page_num == 52:
                            break
                        if keyword == 'Cybersecurity Architect' and page_num == 129:
                            break
                        if keyword == 'Information Security Consultant' and page_num == 9:
                            break
                        if keyword == 'Cybersecurity Consultant' and page_num == 83:
                            break
                        if keyword == 'Cybersecurity Advisor' and page_num == 44:
                            break
                        if keyword == 'Information Security Specialist' and page_num == 50:
                            break
                        if keyword == 'Information Security Architect' and page_num == 4:
                            break
                        if keyword == 'Security Analyst' and page_num == 95:
                            break
                        if keyword == 'Information Security Analyst' and page_num == 125:
                            break
                        if keyword == 'Information Security Engineer' and page_num == 77:
                            break
                        if keyword == 'Chief Information Security Officer (CISO)' and page_num == 6:
                            break
                        if keyword == 'Cybersecurity Analyst' and page_num == 40:
                            break
                        if keyword == 'Cybersecurity Engineer' and page_num == 94:
                            break
                        if keyword == 'Penetration Tester' and page_num == 1:
                            break
                        if keyword == 'Security Architect' and page_num == 128:
                            break
                        if keyword == 'Computer Forensics Analyst' and page_num == 100:
                            break
            # search_box.clear()
            driver.back()
            time.sleep(10)
    except StaleElementReferenceException:
        pass
    driver.quit()
    df = pd.DataFrame(job_postings)

    with pd.ExcelWriter('careeronestop_data.xlsx') as writer:
        df.to_excel(writer, index=False)
    driver.quit()


def usajobs_job_search():
    keywords = ['Information Security Architect', 'Security Analyst','Chief Information Security Officer (CISO)', 'Cybersecurity Analyst',
                'Penetration Tester', 'Cybersecurity Engineer', 'Security Architect',
                'Computer Forensics Analyst','Network Security Architect', 'Cybersecurity Architect', 'Information Security Consultant',
                'Cybersecurity Consultant', 'Cybersecurity Advisor', 'Ethical Hacker',
                'Information Security Specialist',
                'Information Security Architect','Information Security Analyst',
                'Information Security Engineer',
                ]
    url = 'https://data.usajobs.gov/api/Search'
    kk = ["cyber", "cybersecurity", "cyber security", "IT security", "information security", "network security",
                "vulnerability assessment", "security clearance", "top secret clearance",
                "penetration tester", "Penetration Test", "penetration testing", 'Ethical Hacker',
                'Network Security Architect', 'Cybersecurity Architect', 'Security Architect',
                'Information Security Architect',
                'Information Security Consultant', 'Cybersecurity Consultant', 'Cybersecurity Advisor',
                'Information Security Specialist', 'Security Specialist', 'Cybersecurity Specialist', 'Chief Information Security Officer (CISO)', 'CISO',
                'Security Analyst', 'Information Security Analyst', 'Cybersecurity Analyst',
                'Cybersecurity Engineer', 'Information Security Engineer',
                'Computer Forensics Analyst', 'CompTIA Security+', 'CISSP', 'CEH', 'CISM', 'CISM', 'CIPP',
                'Certified Ethical Hacker'
                ]
    kk = [k.lower() for k in kk]
    pattern = re.compile('|'.join(kk))
    job_postings = []
    for keyword in keywords:
        params = {'Keyword': keyword,
                  'LocationName': 'United States',
                  'Page': 1, 'ResultsPerPage': 500
                  }
        headers = {'User-Agent': 'Mozilla/5.0', 'Authorization-Key': 'xgsWiSL9TWYIk5LI00GJ58d+E52vsVr0QjYZuAUZRYk='}
        job_listings = []
        while True:
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            job_listings += data['SearchResult']['SearchResultItems']
            if len(job_listings) == params['Page']:
                break
            params['Page'] += 1
        for job in job_listings:
            job_posting = {"keyword": "", "job_title": "", "company": "", "location": "", "date_posted": "",
                           "job_link": "", "description": ""}
            job_posting['keyword'] = keyword
            job_posting['job_title'] = job['MatchedObjectDescriptor']['PositionTitle']
            job_posting['company'] = job['MatchedObjectDescriptor']['OrganizationName']
            job_posting['location'] = job['MatchedObjectDescriptor']['PositionLocationDisplay']
            job_posting['date_posted'] = job['MatchedObjectDescriptor']['PublicationStartDate']
            job_posting['job_link'] = job['MatchedObjectDescriptor']['PositionURI']
            job_posting['description'] = ' '.join(job['MatchedObjectDescriptor']['UserArea']['Details']['MajorDuties']) + " " + job['MatchedObjectDescriptor']['UserArea']['Details']['Requirements']
            if job['MatchedObjectDescriptor']['UserArea']['Details']['Requirements'] == '':
                job_posting['description'] = ' '.join(job['MatchedObjectDescriptor']['UserArea']['Details']['MajorDuties']) + " " + \
                job['MatchedObjectDescriptor']['UserArea']['Details']['OtherInformation']

            not_found = all(job_posting['job_link'] not in ii.values() for ii in job_postings)
            matches = [match.group() for match in re.finditer(pattern, job_posting['description'].lower())]
            # if not matches:
            #     print("not matched:::", job_posting['job_title'], "::", job_posting['job_link'])
            if not_found and matches:
                job_postings.append(job_posting)

    df = pd.DataFrame(job_postings)
    with pd.ExcelWriter('USAJobs_data.xlsx') as writer:
        df.to_excel(writer, index=False)


# usajobs_job_search()
