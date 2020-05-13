from bs4 import BeautifulSoup
import requests
import lxml.html as lh
import re
import numpy as np
import pandas as pd

#Because the page has dynamic elements in it, we can't use beautiful soup to
#scrape the course titles the same way we were able to scrape the course
#information like the credits, times, and professors.

## Made with help from github: alsobay

with open('MECESP2020.html', 'r') as file:
    web_text = file.readlines()

web_string=""
for part in web_text:
    web_string += part

course_names= re.findall("E\d+<br>(.+)<\/b>", web_string)
course_numbers = list(pd.Series(re.findall("(E\d+)", web_string)).drop_duplicates())
list(zip(course_numbers, course_names))


pd.DataFrame({"course_number":course_numbers, "course_title":course_names}).to_csv("Class_features2.csv", index=False)