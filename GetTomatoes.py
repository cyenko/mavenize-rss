import urllib2, json, AlchemyAPI
import urllib as urllib
class GetTomatoes:
    print('Imported GetTomatoes successfully.')
    def __init__(self,apikey=''):
        if apikey == '':
            self.KEY='mz7z7f9zm79tc3hcaw3xb85w'
        else:
            self.KEY=apikey
        BASE='http://api.rottentomatoes.com/api/public/v1.0/'
        self.BASE = BASE
        self.movieURL=BASE+'movies.json'
        self.listsURL=BASE+'lists.json'
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
        print(movieSearchURL)
        reviewSearchURL=self.BASE+'movies/'+correctMovieID+'/reviews.json?'
        reviewSearchURL = reviewSearchURL +urllib.urlencode({'apikey':self.KEY})
        print(reviewSearchURL)
        reviewData=json.loads(urllib2.urlopen(reviewSearchURL).read())
        reviewData = reviewData['reviews']
        return reviewData
        #Create the dictionary of each review with the following properties
        #reviewer name, rating, text (Get first paragraph, url, date

        # returns an array of dictionaries, where each dictionary is one review
        # have done by wednesday meeting
