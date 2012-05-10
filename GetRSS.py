import AlchemyAPI,re,urllib2
from bs4 import BeautifulSoup as soup
class GetRSS:
    print('tes');
    def __init__(self):
        self.alchemyObject = AlchemyAPI.AlchemyAPI();
        self.alchemyObject.loadAPIKey("api_key.txt");
        print('This script retrieves a list of permalinks, given an RSS URL');
        #self.url=raw_input('Enter URL: ');
        #print('You entered ' + self.url);
        #Change the below to whatever URL we need.  Can be interfaced with a get method
        self.url = 'http://www.rottentomatoes.com/syndication/rss/top_news.xml'
        #self.urllist = self.getPermaLinks(self.url);
        #result = alchemyObject.URLGetRawText(url);
        #print(result);
        #print('done');
	    
    def getPermaLinks(self,url):
        print('called helper method')
        req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
        page = urllib2.urlopen(req) #We are blocked from accessing feeds (detected as bot
        soupPage = soup(page)
        returnList = []
        stringList = []
        unparsedList = soupPage.findAll('guid')
        for listelement in unparsedList:
	        returnList.append(listelement.findAll(text=True))
        return returnList

    def getLumpText(self,url):
        print('Getting Lump Text');
        returnText = self.alchemyObject.URLGetRawText(url)
        return returnText
