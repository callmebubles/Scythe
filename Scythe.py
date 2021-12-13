#!/usr/bin/env python3

### IMPORT STATEMENTS ###
import sys
import subprocess
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'beautifulsoup4'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'spacy'])
import requests
import re
from bs4 import BeautifulSoup
import spacy
import en_core_web_sm
import tldextract
import csv
nlp = spacy.load('en_core_web_sm')

### HELPER FUNCTIONS (IF NECESSARY) ###
def webscraper(web):
 
  url = web
  response = requests.get(url).text
  soup = BeautifulSoup(response, 'html5lib')
  listing = []
  listed = []
  for script in soup(["script", "style", 'aside']):
    script.extract()
  site = " ".join(re.split(r'[\n\t]+', soup.get_text()))
  names = nlp(site)
  people = [ee for ee in names.ents if ee.label_ == 'PERSON']
  for token in people:
    if len(token) == 2 and token.text != listing:
      listing.append(token.text)
  for one in listing:
    one = " ".join(one.split())
    if one not in listed:
      listed.append(one)

  extracted = tldextract.extract(url)
  ending1 = "{}.{}".format(extracted.domain, extracted.suffix)
  col = ['First name and Last name', "Possible user name 1", "Possible user name 2", "Possible user name 3", "Possible user name 4",  "Possible email 1", "Possible email 2", "Possible email 3"]
  rows = []
  for person in listed:
    employee = []
    username_list = []
    email_list = []
    employee.append(person)
    user1 = str(person.split()[1])[0:3] + str(person.split()[0])[0:3]
    username_list.append(user1)
    user2 = str(person.split()[0])[0:3] + str(person.split()[1])[0:3]
    username_list.append(user2)
    user3 = str(person.split()[0])[0:1] + person.split()[1]
    username_list.append(user3)
    user4 = person.split()[0] + str(person.split()[1])[0:1]
    username_list.append(user4)
    emails1 = person.split()[0] + "." + person.split()[1] + '@' + ending1
    email_list.append(emails1)
    emails2 = str(person.split()[0])[0:1] + "." + person.split()[1] + '@' + ending1
    email_list.append(emails2)
    emails3 = person.split()[0] + "." + str(person.split()[1])[0:1] + '@' + ending1
    email_list.append(emails3)
    
    print(username_list + email_list)
    rows.append(employee + username_list + email_list)

  with open('shows.csv', 'w') as f:
      write = csv.writer(f)
      write.writerow(col)
      write.writerows(rows)

### MAIN FUNCTION ###
def main():
  web = sys.argv[1]
  webscraper(web)

### DUNDER CHECK ###
if __name__ == "__main__":
  main()