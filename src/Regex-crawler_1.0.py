'''
Regex-crawler - v 1.0.
author: Arkadiusz97
'''
import requests
import sys
import re
import sqlite3
import datetime
import os
from urllib.parse import urljoin
from bs4 import BeautifulSoup
def getLinks(url, siteContent, urlRegexs):
     html = BeautifulSoup(siteContent, 'html.parser')
     searchingResult = html.find_all('a', {'href':True})
     toReturn = []
     for i in searchingResult:
          if not urlRegexs:
               toReturn.append(urljoin(url, i['href']))
          else:
               for j in urlRegexs:
                    if not re.search(j, urljoin(url, i['href'])) is None:
                         toReturn.append(urljoin(url, i['href']))
                         break
     return toReturn
def getRegexResults(regexs, url, siteContent):
     toReturn = []
     for i in regexs:
          searchResult = re.findall(i, siteContent)
          for j in searchResult:
               if type(j) is str:
                    toReturn.append([url, i, j])
               else:
                    toReturn.append([url, i])
                    toReturn[-1].extend(k for k in j)
     return toReturn
def search(firstUrl, limit, regexs, urlRegexs):
     checkedUrls = []
     currentUrls = []
     newUrls = []
     results = []
     linksWithoutResults = []
     try:
          response = requests.get(firstUrl, timeout=10)
     except requests.exceptions.RequestException:
          return
     tmpResults = getRegexResults(regexs, firstUrl, response.text)
     if not tmpResults:
          linksWithoutResults.append(firstUrl)
     else:
          results.extend(tmpResults)
     checkedUrls.append(firstUrl)
     currentUrls.extend(getLinks(firstUrl, response.text, urlRegexs))
     for x in range(limit):
          checkedUrls.extend(currentUrls)
          for i in currentUrls:
               try:
                    response = requests.get(i, timeout=10)
               except requests.exceptions.RequestException:
                    linksWithoutResults.append(i)
                    continue
               tmpResults = getRegexResults(regexs, i, response.text)
               links = getLinks(i, response.text, urlRegexs)
               if not tmpResults:
                    if i not in linksWithoutResults:
                         linksWithoutResults.append(i)
               else:
                    results.extend(tmpResults)
               for j in links:
                    if j not in checkedUrls:
                         newUrls.append(j)
          currentUrls.clear()
          currentUrls.extend(newUrls)
          newUrls.clear()
     return results, linksWithoutResults
def getSettingsFromFile(fileName):
     regexs = []
     urlRegexs = []
     firstUrl = ""
     limit = 0
     isValid = True
     with open(fileName, "r", encoding="utf-8") as resultFile:
          for line in resultFile:
               resultFromLine = re.search(r"\*(.*) (.*)", line)
               if resultFromLine.group(1) == 'regex':
                    regexs.append(resultFromLine.group(2))
               elif resultFromLine.group(1) == 'firstUrl':
                    firstUrl = resultFromLine.group(2)
               elif resultFromLine.group(1) == 'limit':
                    limit = int(resultFromLine.group(2))
               elif resultFromLine.group(1) == 'urlRegex':
                    urlRegexs.append(resultFromLine.group(2))
     if limit == 0 or not regexs or firstUrl == "":
          isValid = False
     return firstUrl, limit, regexs, urlRegexs, isValid
def saveToDatabse(results, linksWithoutResults, settings, databaseCursor):
     numberOfGroups = max([re.compile(m).groups for m in settings[2]])
     databaseCursor.execute('CREATE TABLE urlsNoResults(linkId INTEGER PRIMARY KEY, url text);')
     createTableQuery = '''CREATE TABLE results
             (resultId INTEGER PRIMARY KEY, url text, pattern text, group1 text'''
     for i in range(2, numberOfGroups+2, 1):
          createTableQuery += ', group' + str(i)
     createTableQuery += ');'
     databaseCursor.execute(createTableQuery)
     for i in linksWithoutResults:
          databaseCursor.execute('INSERT INTO urlsNoResults(url) VALUES("' + i + '");')
     for i in results:
          insertIntoQuery = 'INSERT INTO results(url, pattern, group1'
          for j in range(2, numberOfGroups+1, 1):
               insertIntoQuery += ', group' + str(j)
          insertIntoQuery += ') VALUES("' + i[0]
          for j in range(1, len(i), 1):
               insertIntoQuery += '","' + i[j]
          insertIntoQuery += '"'
          for j in range(0, 4 - len(i), 1):
               insertIntoQuery += ',""'
          insertIntoQuery += ');'
          databaseCursor.execute(insertIntoQuery)
def main():
     if len(sys.argv) != 2:
          print('Invalid number of arguments. Usage:\n' + os.path.basename(sys.argv[0]) + ' [settings_file_name]')
          return
     firstUrl, limit, regexs, urlRegexs, isValid = getSettingsFromFile(sys.argv[1])
     if(isValid == False):
          print("Invalid settings file.")
          return
     results, linksWithoutResults = search(firstUrl, limit, regexs, urlRegexs)
     fileName = "Regex-crawler-" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f") + ".db"
     conn = sqlite3.connect(fileName)
     c = conn.cursor()
     saveToDatabse(results, linksWithoutResults, (firstUrl, limit, regexs, urlRegexs, isValid), c)
     conn.commit()
     conn.close()
main()
