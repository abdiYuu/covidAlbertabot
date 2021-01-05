#import required libraries + modules and aliases
import datetime
import pytz
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
from os import environ
import sys
from bs4 import BeautifulSoup
import pandas as pd
import emoji
import os
import tweepy


#grab the current date and time, format it for tweeting and data entry 
time = datetime.datetime.now().strftime("%B %d")
timeStatus = datetime.datetime.now().strftime("%B %d, %Y")
timenoUpdate = datetime.datetime.now(pytz.utc)

def browse():
    #this part just makes it so that the Firefox browser doesn't actually open up on the screen whenever you run the code
    noBrowser = Options()
    noBrowser.headless = True
    noBrowser.no_sandbox = True

    #launches the firefox driver with established options and the path to the webdriver.exe and firefox.exe, directs it to the url, obtains the page source, and closes the browser
    driver = webdriver.Firefox(options=noBrowser, executable_path=os.environ.get("DRIVERPATH"), firefox_binary=os.environ.get('FIREFOXPATH'))
    driver.get(os.environ.get("URL"))
    abHealth = driver.page_source
    driver.close()
    return abHealth

abHealth = browse()

def parse():
    #pass the webpage contents to BeautifulSoup for parsing
    soup = BeautifulSoup(abHealth, 'html.parser')
    #identify the table via it's div's ID
    caseTable = soup.find('div', id="goa-grid28054")

    #identify the extra details and comments beneath the table encased in the <em> tag
    global tableInfo
    tableInfo = soup.find('em')

    return caseTable

caseTable = parse()


tableInfo  = str(tableInfo)

#removes the <br/> and <em> tags to recieve the first line of update info beneath the table
lastUpdated = tableInfo.split("<br/>")[0]
lastUpdated = lastUpdated.split("<em>", 1)[-1]

def dataframe():
    #turns the table into a dataframe using pandas + speciFies which table in the div it is via it's index (even if there's only one)
    caseInfo = pd.read_html(str(caseTable))[0]
    return caseInfo

caseInfo = dataframe()

"""
#drop every location except alberta
#drop every column except Active Cases, Hospitalizations, and Deaths

def addDate(df, date):
    infoWithDate = caseInfo.copy()
    infoWithDate.drop([0,2,3,4,5,6,7], axis=0, inplace=True)
    infoWithDate.drop(infoWithDate.columns[[0,1,3,5,7,8]], axis=1, inplace=True)
    infoWithDate.insert(0,'Date', [time], True)

    return infoWithDate

infoWithDate = addDate(caseInfo, time)

#function to add data to the csv file
def addData(df, SQLPATH):

    with open (SQLPATH, 'a') as f:
            #checks to see if the data parsed is identical to previous data - meaning site wasn't updated
            if lastrowCSV.to_string(index=False, header=False) == lastrowCase.to_string(index=False, header=False):
                    print("This is a duplicate entry! The data must not have been updated. Please Check:\n\n\nhttps://www.alberta.ca/covid-19-alberta-data.aspx ")
                    sys.exit()

            #if not, add data
            else:
                infoWithDate.to_sql(f, index=False, header=False)
                print("Data has been updated! Please check the CSV file")
    f.close()


#checks if the file doesn't exist, already exists and is empty, or already exists and is populated
with open (environ.get('SQLPATH'), 'a') as f:
        #if it exists and is empty, add data
        if os.path.isfile(environ.get('SQLPATH')) and os.path.getsize(environ.get('SQLPATH')) == 0:
            infoWithDate.to_sql(f, index=False)
            print('File ' + environ.get('SQLPATH') +  ' Created!')

        #if it exists and is full, grab the last four rows of the last column, call addData
        elif os.path.isfile(environ.get('SQLPATH')) and os.path.getsize(environ.get('SQLPATH')) > 0:
            csvData = pd.read_sql(environ.get('SQLPATH'))
            lastrowCSV = csvData.drop(csvData.columns[[0]], axis=1).tail(1)
            lastrowCase = infoWithDate.drop(infoWithDate.columns[[0]], axis=1)
            
            addData(infoWithDate, environ.get('SQLPATH'))

        #if it doesnt exist, create it and add data
        elif not os.path.isfile(environ.get('SQLPATH')):
            caseInfo.to_sql(f, index=False)

        else:
            print("Something's wrong... Check your code")
            sys.exit()
"""
def locations():
    #store the names of each location
    alberta = caseInfo.values[1,0]
    calgary = caseInfo.values[2,0]
    edmonton = caseInfo.values[3,0]
    central = caseInfo.values[4,0]
    south = caseInfo.values[5,0]
    north = caseInfo.values[6,0]
    
    return alberta, calgary, edmonton, central, south, north

alberta, calgary, edmonton, central, south, north = locations()



def cases():
    #stores the values of total and active cases by location
    albertaTotal = caseInfo.values[1,1]
    albertaActive = caseInfo.values[1,2]
    calgaryTotal = caseInfo.values[2,1]
    calgaryActive = caseInfo.values[2,2]
    edmontonTotal = caseInfo.values[3,1]
    edmontonActive = caseInfo.values[3,2]
    centralTotal = caseInfo.values[4,1]
    centralActive = caseInfo.values[4,2]
    southTotal = caseInfo.values[5,1]
    southActive = caseInfo.values[5,2]
    northTotal = caseInfo.values[6,1]
    northActive = caseInfo.values[6,2]
    
    return albertaTotal, albertaActive, calgaryTotal, calgaryActive, edmontonTotal, edmontonActive, centralTotal, centralActive, southTotal, southActive, northTotal, northActive

albertaTotal, albertaActive, calgaryTotal, calgaryActive, edmontonTotal, edmontonActive, centralTotal, centralActive, southTotal, southActive, northTotal, northActive = cases()

def hospitalizations():
    #stores the values of current hospitalizations by location
    albertaHospital = caseInfo.values[1,4]
    calgaryHospital = caseInfo.values[2,4]
    edmontonHospital = caseInfo.values[3,4]
    centralHospital = caseInfo.values[4,4]
    southHospital = caseInfo.values[5,4]
    northHospital = caseInfo.values[6,4]

    return albertaHospital, calgaryHospital, edmontonHospital, centralHospital, southHospital, northHospital

albertaHospital, calgaryHospital, edmontonHospital, centralHospital, southHospital, northHospital = hospitalizations()


def deaths():
    #stores the values of total deaths by location
    albertaDeaths = caseInfo.values[1,6]
    calgaryDeaths = caseInfo.values[2,6]
    edmontonDeaths = caseInfo.values[3,6]
    centralDeaths = caseInfo.values[4,6]
    southDeaths = caseInfo.values[5,6]
    northDeaths = caseInfo.values[6,6]

    return albertaDeaths, calgaryDeaths, edmontonDeaths, centralDeaths, southDeaths, northDeaths

albertaDeaths, calgaryDeaths, edmontonDeaths, centralDeaths, southDeaths, northDeaths = deaths()



def authenticateTwitter():
    #Authenticate to Twitter using the API keys you obtained from your developer account - stored in environment variables
    auth = tweepy.OAuthHandler(os.environ.get("CONSUMER_KEY"), 
    os.environ.get("CONSUMER_SECRET"))
    auth.set_access_token(os.environ.get("ACCESS_TOKEN"), 
    os.environ.get("ACCESS_TOKEN_SECRET"))

    #create an authenticated object to interact with twitter's API
    global covidAlberta
    covidAlberta = tweepy.API(auth)



#tweet the update results
def tweet():

    try:
        caseUpdate = covidAlberta.update_status(emoji.emojize(
""":medical_symbol: Alberta Covid-19 Update - %s

Active Cases:
        
%s in %s

%s in %s

%s in %s
        
%s in %s
        
%s in %s

%s in %s

#COVID19AB""" %(timeStatus,
                    f"{int(albertaActive):,d}", alberta[3:10], 
                    f"{int(calgaryActive):,d}", calgary, 
                    f"{int(edmontonActive):,d}", edmonton, 
                    f"{int(centralActive):,d}", central, 
                    f"{int(southActive):,d}", south, 
                    f"{int(northActive):,d}", north)))
        caseUpdate
    
        
        hospitalUpdate = covidAlberta.update_status(
"""Current Hospitalizations:
        
%s in %s

%s in %s

%s in %s
        
%s in %s
        
%s in %s

%s in %s

#COVID19AB""" %(f"{int(albertaHospital):,d}", alberta[3:10], 
                        f"{int(calgaryHospital):,d}", calgary, 
                        f"{int(edmontonHospital):,d}", edmonton, 
                        f"{int(centralHospital):,d}", central, 
                        f"{int(southHospital):,d}", south, 
                        f"{int(northHospital):,d}", north), in_reply_to_status_id=caseUpdate.id)
    
        hospitalUpdate

        deathUpdate = covidAlberta.update_status(
"""Total Deaths:
        
%s in %s

%s in %s

%s in %s
        
%s in %s
        
%s in %s

%s in %s

#COVID19AB""" %(f"{int(albertaDeaths):,d}", alberta[3:10], 
                        f"{int(calgaryDeaths):,d}", calgary, 
                        f"{int(edmontonDeaths):,d}", edmonton, 
                        f"{int(centralDeaths):,d}", central, 
                        f"{int(southDeaths):,d}", south, 
                        f"{int(northDeaths):,d}", north), in_reply_to_status_id=hospitalUpdate.id)

        deathUpdate

        moreInfo = covidAlberta.update_status(
"""For more detailed information, please visit:
#COVID19AB
https://www.alberta.ca/covid-19-alberta-data.aspx""", in_reply_to_status_id=deathUpdate.id)
    
        moreInfo

    except tweepy.TweepError as error:
        if error.api_code == 187:
            #print a notice
            print("Either no new updates or something else is wrong. Check code and Alberta Health website:")
        else:
            raise error




authenticateTwitter()
tweet()