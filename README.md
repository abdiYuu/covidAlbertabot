# [Alberta COVID-19 Tracker:](https://twitter.com/covidAlberta "@covidAlbertabot")

A Twitter bot that posts regularly updated COVID-19 case information from Alberta Health.

## How It Works?:

This program uses requests to grab a copy of Alberta Health's .ASPX information page, which then passes it to BeautifulSoup for parsing and obtains the COVID-19 data table. The table is then stored in a Pandas dataframe and specific datapoints for each region are tweeted. 

covidAlbertabot is hosted using a Heroku Dyno and run on a simple flask server on a timed basis to check for updates using the Heroku Scheduler.

For more detailed Alberta COVID-19 case information and data, please visit the [Alberta Health Website.](https://www.alberta.ca/covid-19-alberta-data.aspx)


### TODO:

- Find a better method to detect whether or not the page has been updated.
- Store dataframe as csv.
- Graph and display a 7-day average using matplotlib.
- Set up retweets for tweets from Alberta Health and the Chief Medical Officer.
