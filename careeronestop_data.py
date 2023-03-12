from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time

from bs4 import BeautifulSoup
import pandas as pd
import re

chromeOptions = Options()
chromeOptions.headless = False

keywords = ['Chief Information Security Officer (CISO)', 'Cybersecurity Analyst',
            'Penetration Tester', 'Cybersecurity Engineer', 'Security Architect',
            'Computer Forensics Analyst'
            ]
new_keywords = ['Network Security Architect', 'Cybersecurity Architect', 'Information Security Consultant',
                'Cybersecurity Consultant', 'Cybersecurity Advisor', 'Ethical Hacker', 'Information Security Specialist',
                'Information Security Architect', 'Security Analyst', 'Information Security Analyst', 'Information Security Engineer']

driver = webdriver.Chrome(options=chromeOptions)

job_postings = []
time.sleep(2)
try:
    for keyword in new_keywords:
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

