import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime

template = 'https://in.indeed.com/jobs?q={}&l={}'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

def get_url(position, location):
    """Generate a url from position and location"""
    template = 'https://in.indeed.com/jobs?q={}&l={}'
    url = template.format(position, location)
    return url

def get_record(card):
    job_Title = card.find('h2', {'class':'jobTitle-color-purple'}).text.strip()
    print(job_Title)
    job_url = 'https://in.indeed.com'+card.get('href')
    print(job_url)
    company = card.find('span', {'class':'companyName'}).text.strip()
    print(company)
    try:
        rating = card.find('span', {'class':'ratingNumber'}).text.strip()
        print(rating)
    except AttributeError:
        rating = ''    
    job_Location = card.find('div', {'class':'companyLocation'}).text.strip()
    print(job_Location)
    job_Summary = card.find('div', {'class':'job-snippet'}).text.strip()
    print(job_Summary)
    post_Date = card.find('span', {'class':'date'}).text.strip()
    print(post_Date)
    today = datetime.today().strftime('%Y-%m-%d')
    print(today)
    try:
        job_salary = card.find('span',{'class':'salary-snippet'}).text.strip()
        print(job_salary)
    except AttributeError:
        job_salary =''   
    record = (job_Title, job_Summary, company, rating, today,job_salary, job_Location, post_Date, job_url)
    return record  

def main(position, location):
    records = []
    url = get_url(position, location)  
    while True:
        response = requests.get(url, headers=headers)
        print(response)
        # print(response.reason)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('a',{'class':'tapItem'}) 
        print(len(cards))
        for card in cards:
            record = get_record(card)
            records.append(record) 
        try:
            # url = soup.find('a',{'aria-label':'Next'})
            # url = soup.find('a',{'aria-label':'Next'}).get('href')
            url = 'https://in.indeed.com'+soup.find('a',{'aria-label':'Next'}).get('href')
            print(url)
        except AttributeError:
            break    

        # print(records[0])           
        print(len(records))  
    with open('indeed.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['job_Title', 'job_Summary', 'company', 'rating', 'today','job_salary', 'job_Location', 'post_Date', 'job_url'])  
        writer.writerows(records)

main('python', 'noida')
