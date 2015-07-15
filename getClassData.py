#!/usr/bin/python3.4

import requests
from bs4 import BeautifulSoup
import time

def get_links(page_url):
    user_agent = {'user-agent': 'Mozilla/5.0'}
    page = requests.get(page_url, headers=user_agent).text
    soup = BeautifulSoup(page)
    links = soup.find_all('a')
    time.sleep(0.5)
    return [a.get('href') for a in links]

def check_url(url, attributes):
    attributes_match = all([a in url for a in attributes])
    if not attributes_match:
        return ""
    if "drexel.edu" not in url and "http" not in url:
        return "https://duapp2.drexel.edu" + url
    else:
        return url

def get_tables(page_url):   
        try:
            user_agent = {'user-agent': 'Mozilla/5.0'}
            table_page = requests.get(page_url, headers = user_agent).text
            time.sleep(2)
        except ConnectionResetError:
            print("connection reset error")
            time.sleep(1)
            table_page = requests.get(page_url).text
        soup = BeautifulSoup(table_page)
        return soup.find_all('table')

def good_tables(soup_tables, col_keyword):
    soup_tables = [t for t in soup_tables
                  if len(t.tr.find_all('td')) == len(col_keyword)]

    good_tables = []
    for t in soup_tables:
        columns = t.tr.find_all('td')
        columns = [a.text.lower() for a in columns]

        keywords_in_columns = [kw in col for col, kw
                               in zip(columns, col_keyword)]
        if all(keywords_in_columns):
            good_tables.append(t)
    return good_tables

def main():
    # assuming the following page order
    # start page -> college page -> table page
    with open("tmsURLS.txt") as t:
        tms_urls = t.read()
        tms_urls = tms_urls.split()

    # getting the college level links from the initial page
    college_links = get_links(tms_urls[0]) 

    # filtering out pages that don't lead to college pages and fixing
    # incomplete urls
    attributes = ["component=collSubj", "page=CollegesSubjects"]
    college_links = [check_url(url, attributes) for url in college_links] 
    college_links = filter(None, college_links)

    print("finished getting links from first page")

    # getting links (to table pages) from college level pages
    table_page_urls = [get_links(a) for a in college_links]

    # flattening url list 
    table_page_urls = [a for sublist in table_page_urls for a in sublist]
    print("Stage 1 complete")
 
    # getting all of the tables from the site 
    attributes = ["component=subjectDetails", "page=CollegesSubjects"]
    college_links = [check_url(url, attributes) for url in table_page_urls]
    college_links = filter(None, college_links)
    data_tables = [get_tables(a) for a in college_links]    
    print("Got %i tables" % len(data_tables))

    # filtering out the tables that do not contain the information needed
    column_keywords = ("subject", "course", "type" , "method","sec", "crn"
                      ,"title", "time", "instructor")
    data_tables = [good_tables(a, column_keywords) for a in data_tables]
    print("finished getting the good tables")

    data_tables = [a for table in data_tables for a in table]
    data_tables = filter(None, data_tables) 

    # converting list of tables to list of rows
    table_rows = [row for table  in data_tables for row in table.find_all('tr')]
    row_text = [" ".join(r.text.split()) for r in table_rows]

    with open("data_rows.txt", "w") as d:
        d.write("\n".join(row_text))
 
if __name__ == "__main__":
    main()
