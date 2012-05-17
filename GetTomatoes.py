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

    #Create the dictionary of each review with the following properties:
    #reviewer name, rating, summary text, url, date
    #(returnReviews[]) = getReviews(String movieName, int movieYear)
    def getReviews(self, movieName, movieYear):
        movieSearchURL=self.movieURL+'?'+urllib.urlencode({'apikey':self.KEY, 'q': movieName})
        movieData = json.loads(urllib2.urlopen(movieSearchURL).read())
        movieData = movieData['movies']
        
        #We need to find the right movie now, because we don't want to just take the 1st result
        #  Filter by year.
        correctMovieID=-1
        correctMovie={}
        for movie in movieData:
            if movie['year'] == movieYear:
                correctMovieID=movie['id']
                correctMovie=movie
                break
        if correctMovieID==-1:
            raise Exception('Error: Cannot find movie with that year and name.')
        
        #Get IMDB id - ask sameen what this is for again
        movieIMDBNum=correctMovie['alternate_ids']['imdb']
        print('IMDB ID is '+ movieIMDBNum)
        
        #Get all the reviews written
        reviewSearchURL=self.BASE+'movies/'+correctMovieID+'/reviews.json?'
        reviewSearchURL = reviewSearchURL +urllib.urlencode({'apikey':self.KEY})
        reviewData=json.loads(urllib2.urlopen(reviewSearchURL).read())
        reviewData = reviewData['reviews']
        #reviewData is list of reviews for the movie found


        #We need to take data from each list in put it into a format we like.
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
                try: #Score is is number format
                    score = int(round(score))
                except: #Score is in letter format
                    #Get the first letter, and assign a score based on that.
                    letter = score[0]
                    if letter == 'A':
                        score = 4
                    elif letter == 'B':
                        score = 3
                    elif letter == 'C':
                        score = 2
                    else:
                        score = 1
            except:
               # score=-1 #If there is no original score, we take the sentiment and assign a score
                if not text=='N/A':
                    print('Called sentiment analysis')
                    sentiment=self.GetRSS.getSentimentFromText(text)
                    if sentiment < -.2:
                        score = 1 #Arbitrary score assignments - will have to test for accuracy later
                    elif sentiment < 0:
                        score = 2
                    elif sentiment < .1:
                        score = 3
                    else:
                        score = 4
                    
                else:
                    score=-1 #If there is no original score and no text, we automatically assign -1
                    #This should be a red flag for the database to NOT import this review

            #Package the review in a dictionary and stick it in the return array
            reviewDictionary={'name':author,'rating':score,'text':text,'url':link,'date':date}
            returnList.append(reviewDictionary)

        return returnList
