from bs4 import BeautifulSoup
import requests
from lxml import html
from pyparsing import *
import re
import sys
import pandas as pd


departmental_designation=input("Please input your department code: ")
if departmental_designation.upper()== "MECE":
    print("Maker's Make")
    departmental_designation=departmental_designation.upper()
else:
    print("This department is not available yet")
    sys.exit()


URL="http://www.columbia.edu/cu/bulletin/uwb/sel/MECE_Spring2020_text.html"
page=requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
soup2=soup.text #Get us the most up to date course data in the webpage
#table = soup.find("pre").contents[4]

#Now we need to organize it!
#This is done by creating a parser

x = re.split("\s", soup2)

Plain_text= [] #We generate a list without the white space
for string in x:
    if (string != ""):
        Plain_text.append(string)


#now we create a list that removes the unnecessary and messed up headers on the top
n=34
cleaned_list=Plain_text[n:]
#print(cleaned_list)

department_indices = [i for i, x in enumerate(cleaned_list) if x == departmental_designation or x=='ENME' or x=="MEIE" or x=="MECS"]

#print(department_indices)

#What if we split the giant list after each MECE?
res = [((i), (i + 1) % len(department_indices))
         for i in range(len(department_indices))]
#print(res)

list_of_classes=[]
for (i,j) in res:
    start_index = department_indices[i]
    #print(start_index)
    end_index = department_indices[j]
    #print(end_index)
    sublist = cleaned_list[start_index:end_index-1]
    list_of_classes.append(cleaned_list[start_index:end_index-1])


for i in list_of_classes:
    K=10
    print(i[: len(i) - K])
print(list_of_classes)


total_class_ID=[] #creates a list of all the class IDs
for i in list_of_classes:
    class_name=[]
    class_name.append(i[0])
    class_name.append(" ")
    class_name.append(i[1])
    total_class_ID.append(''.join(class_name))
print(total_class_ID)




total_class_sections=[]
total_callnumber=[]
total_credits=[]

for i in list_of_classes:
    total_class_sections.append(i[2])
    total_callnumber.append(i[3])
    total_credits.append(i[4])
print(total_class_sections)
print(total_callnumber)
print(total_credits)



class_links=[]
for a in soup.find_all('a', href=True):
    print( "Found the URL:", a['href'])
    class_links.append(a['href'])

class_links=class_links[:-5]
url_add="http://www.columbia.edu"
class_links=[url_add + s for s in class_links]


## For the purposes of this project, we just need the class titla and code
dataset={"Course Code": total_class_ID, "Sections":total_class_sections  , "Credits": total_credits,
         'Call_number': total_callnumber, "Class Link": class_links} #converting the reviews list into a dictionary
review_data=pd.DataFrame.from_dict(dataset) #converting this dictionary into a dataframe
review_data.to_csv('Class_features1.csv',index=False)

