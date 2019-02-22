# Regex-crawler
# Detailed description.
Regex-crawler is a web crawler to search informations by regular expressions. Program enters on first web site selected by user. Next, program looking for texts, that are matching to regular expressions written by user and for urls addresses from html marker "a href". Searching operations for matching patterns and next urls are making recursively.

# Settings for program.
Settings are saved in text file. Every rule is in one line. You can set following rules:
-First url - First url address, on which program enters.
-Regex - Regular expressions to which sites contents are matched. You can set multiple regular expressions.
-Limit - Maximum number of recursively searching.
-Url regex - regular expressions for found url addresses. For example, you can use it if you want to search informations on only one website. It's additional rule, you don't have to set it. You can also set multiple url regex rules. 
Example settings file, where searching are started from http://localhost/Regex-crawler/index.html for string, that are matching for regex ([A-Fa-f0-9]{2}([A-Fa-f0-9]{4})), with 10000 maximum recursively recursively searching and for urls matching to http://localhost/Regex-crawler/subpage[0-8]{1}\.html regex:

*firstUrl http://localhost/Regex-crawler/index.html
*regex ([A-Fa-f0-9]{2}([A-Fa-f0-9]{4}))
*limit 10000
*urlRegex http://localhost/Regex-crawler/subpage[0-8]{1}\.html

# Usage.
To start program, enter to terminal: [program_name] [config file]
Regex-crawler will generate Sqlite3 database with tables "results" and "urlsNoResults". Every record in table result has: Id, url where result was found, regular expressions for match and regex groups for match. Table urlsNoResults has only urls addresses without any result. Urls that aren't match to any rule *urlRegex will be ignored. 

# Requirements.
To run this program , you need a Python 3.7.2 or newer with installed libares: requests, datetime, os and bs4.
