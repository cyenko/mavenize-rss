import urllib2, json, AlchemyAPI
import urllib as urllib
import GetRSS
class GetTomatoes:
    print('Imported GetTomatoes successfully.')
    debugReviewList = [];
    def __init__(self,apikey=''):
        if apikey == '':
            self.KEY='mz7z7f9zm79tc3hcaw3xb85w'
        else:
            self.KEY=apikey
        BASE='http://api.rottentomatoes.com/api/public/v1.0/'
        self.BASE = BASE
        self.movieURL=BASE+'movies.json'
        self.listsURL=BASE+'lists.json'
        self.GetRSS = GetRSS.GetRSS()

    def debugGetMovieList(self,movieName,movieYear):#Will remove before final version
        movieSearchURL=self.movieURL+'?'+urllib.urlencode({'apikey':self.KEY, 'q': movieName})
        movieData = json.loads(urllib2.urlopen(movieSearchURL).read())
        movieData = movieData['movies']
        return movieData

    def getReviews(self, movieName, movieYear):
        movieSearchURL=self.movieURL+'?'+urllib.urlencode({'apikey':self.KEY, 'q': movieName})
        movieData = json.loads(urllib2.urlopen(movieSearchURL).read())
        movieData = movieData['movies']
        
        #We need to find the right movie now, because we don't want to just take the 1st result
        #  Filter by year.
        correctMovieID=-1
        correctMovie={}#REMOVE LATER, FOR DEBUGGING PURPOSES
        for movie in movieData:
            if movie['year'] == movieYear:
                correctMovieID=movie['id']
                correctMovie=movie
                break
        if correctMovieID==-1:
            print('error - cannot find movie')
            #throw exception here
        #Get IMDB id - ask sameen what this is for again
        movieIMDBNum=correctMovie['alternate_ids']['imdb']
        print('IMDB ID is '+ movieIMDBNum)
        print(movieSearchURL)
        #This part is also prone to errors.  How can we catch errors where the user's request
        #times out?
        reviewSearchURL=self.BASE+'movies/'+correctMovieID+'/reviews.json?'
        reviewSearchURL = reviewSearchURL +urllib.urlencode({'apikey':self.KEY})
        print(reviewSearchURL)
        reviewData=json.loads(urllib2.urlopen(reviewSearchURL).read())
        reviewData = reviewData['reviews']
        self.debugReviewList = reviewData
        returnList=[]
        for review in reviewData:
            #Introduce error catching later
            author=review['critic']
            date=review['date']
            link=review['links']['review']
            try:
                text=self.GetRSS.getFirstParagraph(link) #Once tihs is fixed, it will work
            except: #Comment this out to see the error from AlchemyAPI
                text='N/A'
            try:
                score=review['original_score']
                #This score is either in number format
                # or a letter grade with + or - (i.e. A-)
                #
            except:
               # score=-1 #If there is no original score, we take the sentiment and assign a score
                if not text=='N/A':
                    sentiment=self.GetRSS.getSentimentFromText(text)
                    if sentiment < -.2:
                        score = 1 #Arbitrary score assignments - will have to test for accuracy later
                    elif sentiment < 0:
                        score = 2
                    elif sentiment < .1:
                        score = 3
                    else:
                        score = 4
                    if sentiment == -1:
                        score= -1 #what to do when the sentiment is neutral
                else:
                    score=-1

            reviewDictionary={'name':author,'rating':score,'text':text,'url':link,'date':date}
            returnList.append(reviewDictionary)

        return returnList
        #Create the dictionary of each review with the following properties
        #reviewer name, rating, text (Get first paragraph, url, date

        # returns an array of dictionaries, where each dictionary is one review
        # have done by wednesday meeting
