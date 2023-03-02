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

chromeOptions = Options()
chromeOptions.headless = False

keywords = ['Chief Information Security Officer (CISO)',
            'Cybersecurity Analyst',
            'Penetration Tester', 'Cybersecurity Engineer',
            'Security Architect',
            'Computer Forensics Analyst']

driver = webdriver.Chrome(options=chromeOptions)
driver.get('https://www.careeronestop.org/JobSearch/job-search.aspx')
job_postings = []
time.sleep(2)
try:
    for keyword in keywords:
        search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'FindaJobNowkeyword')))
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
        driver.implicitly_wait(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        page_ul = soup.find('ul', {"class": 'cos-page'})
        last_page_link = page_ul.find_all('a')[-1]
        num_pages = int(last_page_link.text)
        for page_num in range(1, num_pages + 1):
            table = soup.find("table", {"class": "cos-table-responsive"})
            tbody = table.find('tbody')
            for row in tbody.find_all("tr"):
                job_posting = {}
                columns = row.find_all("td")
                job_posting["keyword"] = keyword
                job_posting["job_title"] = columns[0].text.strip()
                job_posting["company"] = columns[1].text.strip().split('\n')[0]
                job_posting["location"] = columns[2].text.strip()
                job_posting["job_link"] = 'https://www.careeronestop.org'+columns[0].find("a")["href"].replace(' ', '%20')
                job_postings.append(job_posting)
            if keyword == 'Chief Information Security Officer (CISO)' and page_num == 6:
                break
            if keyword == 'Cybersecurity Analyst' and page_num == 40:
                break
            if keyword == 'Cybersecurity Engineer' and page_num == 94:
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

driver = webdriver.Chrome()
for job_posting in job_postings:
    driver.get(job_posting["job_link"])
    job_details_html = driver.page_source
    job_details_soup = BeautifulSoup(job_details_html, "html.parser")
    job_posting["description"] = job_details_soup.find("div", {"id": "ctl17_lblDesc"})
    if job_posting['description']:
        job_posting['description'] = job_posting['description'].text.strip()
    else:
        job_posting['description'] = ''
df = pd.DataFrame(job_postings)

with pd.ExcelWriter('careeronestop_data.xlsx') as writer:
    df.to_excel(writer, index=False)
driver.quit()
