import AlchemyAPI,re,urllib2
from bs4 import BeautifulSoup as soup
class GetRSS:
    print('tes');
    def __init__(self):
        self.alchemyObject = AlchemyAPI.AlchemyAPI()
        self.alchemyObject.loadAPIKey("api_key.txt")
        print('Key loaded successfully.')
        #Provided a sample URL, in case you want to test it
        self.url = 'http://www.rottentomatoes.com/syndication/rss/top_news.xml'
        print('Script loaded sucessfully.')

    def getPermaLinks(self,url):
        print('called helper method')
        req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
        page = urllib2.urlopen(req) #We are blocked from accessing feeds (detected as bot)
        #I foresee the above being large-scale inefficient.  Any ideas?
        soupPage = soup(page)
        returnList = []
        unparsedList = soupPage.findAll('guid')
        if not unparsedList: #Some RSS pages use the 'link' tag rather than the 'guid' tag
            unparsedList = soupPage.findAll('link')
        for listelement in unparsedList:
	        returnList.append(listelement.findAll(text=True))
        return returnList

    def getLumpText(self,url): #We strip the navigation links and get only content.
        #Should we leave in \n and \t marks, or no?
        print('Getting Lump Text');
        returnText = self.alchemyObject.URLGetText(url)
        return returnText 
