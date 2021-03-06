import csv
import requests
from bs4 import BeautifulSoup

url = "http://www.payscale.com/college-salary-report/bachelors?page=65"
r = requests.get(url)  # using request library to interact with the server to get the content.
data = r.text  # using the text we got back from server.

soup = BeautifulSoup(data,
                     "html.parser")  # Beautiful Soup is the library we use to parse the resulsts. in this case we
# parse html.
scripts = soup.find_all("script")

data = open("PayScaleEarnings.csv", "w")
writer = csv.writer(data)
list_to_write = ["Rank", "School Name", "School Type", "Early Career Median Pay", "Mid-Career Median Pay",
                 "% High Job Meaning",
                 "% STEM"]

for script in scripts:
    text = script.text
    start = 0
    end = 0
    if len(text) > 10000:
        while start > -1:
            start = text.find('"School Name":"', start)
            if start == -1:
                break
            start += len('"School Name":"')
            end = text.find('"', start)
            school_name = text[start:end]

            start = text.find('"Early Career Median Pay":"', start)
            start += len('"Early Career Median Pay":"')
            end = text.find('"', start)
            early_pay = text[start:end]

            start = text.find('"Mid-Career Median Pay":"', start)
            start += len('"Mid-Career Median Pay":"')
            end = text.find('"', start)
            mid_pay = text[start:end]

            start = text.find('"Rank":"', start)
            start += len('"Rank":"')
            end = text.find('"', start)
            rank = text[start:end]

            start = text.find('"% High Job Meaning":"', start)
            start += len('"% High Job Meaning":"')
            end = text.find('"', start)
            high_job = text[start:end]

            start = text.find('"School Type":"', start)
            start += len('"School Type":"')
            end = text.find('"', start)
            school_type = text[start:end]

            start = text.find('"% STEM":"', start)
            start += len('"% STEM":"')
            end = text.find('"', start)
            stem = text[start:end]

            list_to_write.append([rank, school_name, school_type, early_pay, mid_pay, high_job, stem])
writer.writerows(list_to_write)
data.close()
print(data)
"""
Prototype:
    Data Prep:
        1.Scrape payscale as a data source
        2. use/scrape USnews as a data source
        3. merge the sets into a dataframe
            Merge cells by fuzzy match:
                Match rows by similaritiy of the name of the school.

"""
