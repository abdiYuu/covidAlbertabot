# %%
from modules import *

url = 'https://www.alberta.ca/covid-19-alberta-data.aspx'
r = requests.get(url)
r_html = r.text
soup = BeautifulSoup(r_html, 'html.parser') 


#new df - specific locations, cases, and hospitalizations - locations as index
table = soup.find('table')
dataframe = pd.read_html(str(table))[0]
dataframe = dataframe.iloc[[1, 2, 3, 4, 5, 6]]
data = dataframe[['Location', 'Active  cases*', 'In  hospital**', 'In intensive  care***']].copy()
data = data.set_index('Location')
time = datetime.datetime.now().strftime("%B %d")

#when was the table last updated
table_comments = soup.find('em')
text = table_comments.get_text()
lines = text.split('*')
latest_update = lines[0]

#create region object class to easily identify and obtain regional data
class Region:
    def __init__(self, location, data_table):
        self.location = location
        self.data = data_table

    def cases(self):
        #the ab health website has two spaces between 'Active' and 'Cases' on their column name
        return self.data.loc[self.location]['Active  cases*']

    def hospital(self):
        return self.data.loc[self.location]['In  hospital**']
        
    def icu(self):
        return self.data.loc[self.location]['In intensive  care***']

#create the region object instances
alberta = Region('In Alberta', data)
calgary = Region('Calgary zone', data)
edmonton = Region('Edmonton zone', data)
central = Region('Central zone', data)
north = Region('North zone', data)
south = Region('South zone', data)

#Authenticate to Twitter using the API keys you obtained from your developer account - should be stored in environment variables
auth = tweepy.OAuthHandler(os.environ.get("CONSUMER_KEY"), 
os.environ.get("CONSUMER_SECRET"))
auth.set_access_token(os.environ.get("ACCESS_TOKEN"), 
os.environ.get("ACCESS_TOKEN_SECRET"))

#create an authenticated object to interact with twitter's API
covid_twt = tweepy.API(auth)


#tweet cases
cases = covid_twt.update_status('''%s - Update
                         Active Cases:

Alberta: %s

Calgary: %s

Edmonton: %s

Central AB: %s

North AB: %s

South AB: %s'''%(time, alberta.cases(), calgary.cases(), edmonton.cases(), central.cases(), north.cases(), south.cases()))

#tweet hospitalizations
hospitalizations = covid_twt.update_status(status='''%s - Update
                         In Hospital:

Alberta: %s

Calgary: %s

Edmonton: %s

Central AB: %s

North AB: %s

South AB: %s'''%(time, alberta.hospital(), calgary.hospital(), edmonton.hospital(), central.hospital(), north.hospital(), south.hospital()), in_reply_to_status_id=cases.id)

#tweet deaths
deaths = covid_twt.update_status('''%s - Update
                         In ICU:

Alberta: %s

Calgary: %s

Edmonton: %s

Central AB: %s

North AB: %s

South AB: %s'''%(time, alberta.icu(), calgary.icu(), edmonton.icu(), central.icu(), north.icu(), south.icu()), in_reply_to_status_id=hospitalizations.id)


update_info = covid_twt.update_status(status=(latest_update + '\nPlease visit the Alberta Health website for more information\n' + url), in_reply_to_status_id=deaths.id)

# %%
