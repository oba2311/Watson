# FuzzyMain.py

import csv
from fuzzywuzzy import fuzz
import sys
import subprocess
import pandas as pd

Payscalelist = []
EarningsList = []


def scrap():
    # run the script called "Scraping Payscale", to obtain expected earnings after graduation:
    PayScaleEarnings = subprocess.check_output([sys.executable, "scrape payscale.py"])
    df = pd.read_csv("PayScaleEarnings.csv")
    # create lists of the names and payment:
    for index, row in df.iterrows():
        Payscalelist.append(row['School Name'])
    for index, row in df.iterrows():
        EarningsList.append(row['Early Career Median Pay'])
    return Payscalelist, EarningsList


USNewsNames = []
USNewsAcceptance = []


def dataPrep():
    # Use the provided dataset from USNews to obtain acceptance rates per college:
    df1 = pd.read_csv('110.Final.csv')
    for index, row in df1.iterrows():
        USNewsNames.append(row['name'])
        USNewsAcceptance.append(row['Fall 2015 acceptance rate'])

    return USNewsNames, USNewsAcceptance


#########################
# Fuzzy:

#########
# def fuzzy(driver):
# 	tbl = []
# 	for college, earnings in zip(Payscalelist, EarningsList):
# 		max_token = 0
# 		max_acc_rate = 0
# 		for us_name, acc_rate in zip(USNewsNames,USNewsAcceptance):
# 			token = fuzz.token_set_ratio(college, us_name)
# 			if token > max_token:
# 				max_token = token
# 				max_acc_rate = acc_rate
# 		tbl.append([college, earnings, max_acc_rate])

# slow fuzzy:
def fuzzy(driver):
    tbl = []
    for college, earnings in zip(Payscalelist, EarningsList):
        items = []
        for us_name, acc_rate in zip(USNewsNames, USNewsAcceptance):
            items.append([acc_rate, fuzz.token_set_ratio(college, us_name)])
        items = sorted(items, key=lambda x: x[1], reverse=True)
        tbl.append([college, earnings, items[0][0]])


# with open(driver, "wb") as f:
# 		writer = csv.writer(f)
# 		writer.writerows(tbl)

scrap()
dataPrep()
fuzzy("CollegeAcceptanceVSIncome.csv")

# Requirements:
# fuzzywuzzy form: https://pypi.python.org/pypi/fuzzywuzzy#downloads
# BeautifulSoup from: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# Requests from: http://docs.python-requests.org/en/master/
# Python-Levenstein from:
# USnews DataSet from: https://github.com/Shengjiezh/Scraping-USNews-College-Ranking/blob/master/ranking_university_USnews.csv