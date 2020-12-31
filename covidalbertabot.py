#import required libraries + modules and aliases
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import json
import tweepy
import datetime
import emoji
from os import environ

#grab the current date and time, format 
time = datetime.datetime.now().strftime("%A %B %d, %Y")

def browse():
    #this part just makes it so that the Firefox browser doesn't actually open up on the screen whenever you run the code
    noBrowser = Options()
    noBrowser.headless = True

    #launches the firefox driver with established options and the path to the webdriver.exe, directs it to the url, obtains the page source, and closes the browser
    driver = webdriver.Firefox(options=noBrowser, executable_path=environ.get("DRIVERPATH"))
    driver.get(environ.get("URL"))
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
    auth = tweepy.OAuthHandler(environ.get("CONSUMER_KEY"), 
    environ.get("CONSUMER_SECRET"))
    auth.set_access_token(environ.get("ACCESS_TOKEN"), 
    environ.get("ACCESS_TOKEN_SECRET"))

    #create an authenticated object to interact with twitter's API
    global covidAlberta
    covidAlberta = tweepy.API(auth)

#tweet the update results
def tweet():
    caseUpdate = covidAlberta.update_status(emoji.emojize(":medical_symbol: Alberta COVID-19 Update - " + time + "\nActive Cases:\n\n" + f"{int(albertaActive):,d}" + " in " + alberta[3:10] + "." + 
    "\n\n" + f"{int(calgaryActive):,d}" + " in the " + calgary + "." +
    "\n\n" + f"{int(edmontonActive):,d}" + " in the " + edmonton + "." +
    "\n\n" + f"{int(centralActive):,d}" + " in the " + central + "." +
    "\n\n" + f"{int(southActive):,d}" + " in the " + south + "." + 
    "\n\n" + f"{int(northActive):,d}" + " in the " + north + "."))

    caseUpdate
    
    hospitalUpdate = covidAlberta.update_status("Current Hospitalizations:\n\n" + 
    f"{int(albertaHospital):,d}" + " in " + alberta[3:10] + "." +
    "\n\n" + f"{int(calgaryHospital):,d}" + " in the " + calgary + "." +
    "\n\n" + f"{int(edmontonHospital):,d}" + " in the " + edmonton + "." +
    "\n\n" + f"{int(centralHospital):,d}" + " in the " + central + "." +
    "\n\n" + f"{int(southHospital):,d}" + " in the " + south + "." +
    "\n\n" + f"{int(northHospital):,d}" + " in the " + north + ".", in_reply_to_status_id=caseUpdate.id)
    
    hospitalUpdate

    deathUpdate = covidAlberta.update_status("Total Deaths:\n\n" + 
    f"{int(albertaHospital):,d}" + " in " + alberta[3:10] + "." +
    "\n\n" + f"{int(calgaryDeaths):,d}" + " in the " + calgary + "." +
    "\n\n" + f"{int(edmontonDeaths):,d}" + " in the " + edmonton + "." +
    "\n\n" + f"{int(centralDeaths):,d}" + " in the " + central + "." +
    "\n\n" + f"{int(southDeaths):,d}" + " in the " + south + "." +
    "\n\n" + f"{int(northDeaths):,d}" + " in the " + north + ".", in_reply_to_status_id=hospitalUpdate.id)

    deathUpdate

    moreInfo = covidAlberta.update_status(lastUpdated + "\n\nFor more detailed information, please visit:\n\nhttps://www.alberta.ca/covid-19-alberta-data.aspx", in_reply_to_status_id=deathUpdate.id)
    
    moreInfo
authenticateTwitter()
tweet()