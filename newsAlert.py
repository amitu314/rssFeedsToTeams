from pip._vendor import requests
from bs4 import BeautifulSoup 
from datetime import datetime, timedelta,timezone
import json
import time

def rssFeed():
    global consolidatedTitle 
    #print(f"Consolidated Title: {consolidatedTitle}")
    rssUrls = ['https://feeds.feedburner.com/TheHackersNews']
    topicOfInterest = ['linux','kernel', 'npm', 'pypi', 'malicious','package', 'exploit','patches','vulnerability','patch','packages','exploits','chrome','firefox','microsoft','windows','github','gitlab','gnome','fedora','ubuntu','debian','cisa','apache']
    consolidatedSet = set()
    #print(f"Consolidated Set: {consolidatedSet}")
    
    for item in topicOfInterest:
        lowerTopicOfInterest = item.lower()
    now = datetime.now()
    one_day_ago = now - timedelta(days=1)
    try:
        with open('title.csv', 'r') as file:
            consolidatedTitle = set(line.strip().lower() for line in file.readlines())
    except FileNotFoundError:
        print("File not found.") 
    for rssUrl in rssUrls:
        response = requests.get(rssUrl)
        response.raise_for_status() 
        print(f"Successfully fetched {rssUrl}")
        soup = BeautifulSoup(response.content, 'xml')  
        items = soup.find_all('item')
        
        for item in items:
            try:
                titleText = item.find('title').text            
                publishdDate = item.find('pubDate').text
                formattedDate = datetime.strptime(publishdDate, '%a, %d %b %Y %H:%M:%S %z').strftime('%m/%d/%Y ')
                #print(f"Formatted Date: {formattedDate}")
                #print(f"One day ago: {one_day_ago.strftime('%m/%d/%Y')}")
                #print(f"Lookig at {titleText}")
                link = item.find('link').text
                #print( f"{titleText.strip().lower()}")
                normalized_title = normalize_title(titleText)
                #if formattedDate >= one_day_ago.strftime('%m/%d/%Y') and any(topic.lower() in titleText.lower() for topic in topicOfInterest):
                if formattedDate >= one_day_ago.strftime('%m/%d/%Y') and normalized_title not in consolidatedTitle and any(topic.lower() in titleText.lower() for topic in topicOfInterest)  and "weekly recap" not in titleText.lower():
                    #print(titleText.strip().lower() not in consolidatedTitle, formattedDate >= one_day_ago.strftime('%m/%d/%Y'))
                    consolidatedSet.add(f"Title: {titleText};| Link: {link}")
                    consolidatedTitle.add(titleText.strip().lower().replace("$","_").replace("-","_").replace("#","_").replace("%","_").replace("€","_").replace("'","_").replace("â€”", "_").replace("â‚¬", "_"))
                    #print( f"Title: {titleText}\nPublished Date: {formattedDate}\nLink: {link}\n")
                    #print(f"Consolidated title: {consolidatedTitle}")
            except Exception as e:
                print(f"Error for {rssUrl}: {e}")
    if consolidatedSet:
        logicApp(consolidatedSet)
        writeTitleToFile(consolidatedSet)

def rssFeedBC():
    global consolidatedTitle 
    #print(f"Consolidated Title: {consolidatedTitle}")
    rssUrls = ['https://www.bleepingcomputer.com/feed/']
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
    topicOfInterest = ['linux','kernel', 'npm', 'pypi', 'malicious','package', 'exploit','patches','vulnerability','patch','packages','exploits','chrome','firefox','microsoft','windows','github','gitlab','gnome','fedora','ubuntu','debian','cisa','apache']
    consolidatedSet = set()
    #print(f"Consolidated Set: {consolidatedSet}")
    
    for item in topicOfInterest:
        lowerTopicOfInterest = item.lower()
    now = datetime.now()
    one_day_ago = now - timedelta(days=1)
    try:
        with open('title.csv', 'r') as file:
            consolidatedTitle = set(line.strip().lower() for line in file.readlines())
    except FileNotFoundError:
        print("File not found.") 
    for rssUrl in rssUrls:
        response = requests.get(rssUrl, headers=headers)
        response.raise_for_status() 
        print(f"Successfully fetched {rssUrl}")
        soup = BeautifulSoup(response.content, 'xml')  
        items = soup.find_all('item')
        
        for item in items:
            try:
                titleText = item.find('title').text            
                publishdDate = item.find('pubDate').text
                formattedDate = datetime.strptime(publishdDate, '%a, %d %b %Y %H:%M:%S %z').strftime('%m/%d/%Y ')
                #print(f"Formatted Date: {formattedDate}")
                #print(f"One day ago: {one_day_ago.strftime('%m/%d/%Y')}")
                #print(f"Lookig at {titleText}")
                link = item.find('link').text
                #print( f"{titleText.strip().lower()}")
                normalized_title = normalize_title(titleText)
                #if formattedDate >= one_day_ago.strftime('%m/%d/%Y') and any(topic.lower() in titleText.lower() for topic in topicOfInterest):
                if formattedDate >= one_day_ago.strftime('%m/%d/%Y') and normalized_title not in consolidatedTitle and any(topic.lower() in titleText.lower() for topic in topicOfInterest)  and "weekly recap" not in titleText.lower():
                    #print(titleText.strip().lower() not in consolidatedTitle, formattedDate >= one_day_ago.strftime('%m/%d/%Y'))
                    consolidatedSet.add(f"Title: {titleText};| Link: {link}")
                    consolidatedTitle.add(titleText.strip().lower().replace("$","_").replace("-","_").replace("#","_").replace("%","_").replace("€","_").replace("'","_").replace("â€”", "_").replace("â‚¬", "_"))
                    #print( f"Title: {titleText}\nPublished Date: {formattedDate}\nLink: {link}\n")
                    #print(f"Consolidated title: {consolidatedTitle}")
            except Exception as e:
                print(f"Error for {rssUrl}: {e}")
    if consolidatedSet:
        logicApp(consolidatedSet)
        writeTitleToFile(consolidatedSet)

def writeTitleToFile(consolidatedSet):
    try:
        with open('title.csv', 'r',encoding='utf-8') as file:
            existing_titles = set(line.strip().lower() for line in file.readlines())
            #print(f"Existing Titles from File: {existing_titles}")
    except FileNotFoundError:
        existing_titles = set()

    with open('title.csv', 'a',encoding='utf-8') as file:
        for entry in consolidatedSet:
            title = normalize_title(entry.split(";|")[0].replace("Title: ", ""))
            print(f"Normalized Title: {title}")
            if title not in existing_titles:
                file.write(title + '\n')
    
def logicApp(consolidatedSet):
    logicAppURL = "AddYourLogicAPPURL here"
    
    payloadv1 = {
        "requestbody": list(consolidatedSet)
    }

    response1 = requests.post(logicAppURL, json=payloadv1, headers={"Content-Type": "application/json"})
    
    if response1.status_code == 200:
        print("Logic App triggered successfully.")

def normalize_title(title):
    return title.strip().lower().replace("$", "_").replace("-", "_").replace("#", "_").replace("%", "_").replace("€", "_").replace("â€”", "_").replace("â‚¬", "_").replace("—", "_").replace("’", "_").replace(";", "_")

if __name__ == "__main__":
    consolidatedTitle = set()
    #rssFeed()
    while True:
        rssFeed()
        rssFeedBC()
        print("Sleeping for 1 hour...")
        time.sleep(60*60) 
