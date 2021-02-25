import requests
import json
import urllib
class couchPotato(object):

    def __init__(self, couchURL, apikey,whitelistedusers):
        self.couchURL = couchURL
        self.apiKey = apikey
        self.users = whitelistedusers
    
    def begin(self,command,user):
        # make the command lower for all functions
        command = command.lower()
        response = None
        needs_help = False
        if user not in self.users:
            return "This function is currently only avaliable to contributors to say thanks"
        if 'movies search' in command:
            return self.doSearch(command.replace("movies search", ""))
        elif 'movie search' in command:
            return self.doSearch(command.replace("movie search", ""))
        elif 'movie download' in command:
            return self.doDownload(command.replace("movie download", ""))
        elif 'movies download' in command:
                        return self.doDownload(command.replace("movies download", ""))
        elif 'movies wanted' in command:
            return self.doWanted(command.replace("movies wanted", ""))
        elif command[-1] == '?':
            return "No."
        else:
            return "Invalid Command"	


    def doSearch(self,searchstr):
        couch = couchPotatoAPI(self.couchURL, self.apiKey)
        if searchstr == "":
            return "Invalid search string please specify a search term such as 'movies search iron man'"
        searchList = couch.searchMovies(searchstr)
        if searchList == "Error":
            return "No results found for the specified search"
        message = "I found the following movies:\n"
        for movie in searchList:
            message += "<http://www.imdb.com/title/" + movie["imdb"] + "|" + movie["title"] + "(" + movie["year"]  +")" + "> Status: " + movie["status"]+ "   :id:" + movie["imdb"] + "\n"

        return message

    def doDownload(self,id):
        couch = couchPotatoAPI(self.couchURL, self.apiKey)
        if id == "":
            return "Invalid ID"
        movieDownload = couch.downloadMovie(id)
        return movieDownload

    def doWanted(self,id):
        couch = couchPotatoAPI(self.couchURL, self.apiKey)
        movieWanted = couch.getWanted()
        if movieWanted == False:
            return "Error occurred"
        message = "*Current Movies in the watch list:*\n"
        for movie in movieWanted:
            message += "* " + movie["title"] + "(" + movie["year"] +")\n"
        return message

class couchPotatoAPI:


    def __init__(self, url, apikey):
        self.rooturl = url
        self.apikey = apikey





    def printapi(self):
        return self.apikey



    def searchMovies(self,name):
        url = self.rooturl + '/api/' + self.apikey + '/search?q=' + urllib.quote_plus(name)
        request = requests.get(url)
        json_data = json.loads(request.text)
        if "movies" not in json_data:
            return "Error"
        movies = []
        for movie in json_data["movies"]:
            imovie = {}
            # print "Movie Name: " + movie["titles"][0]
            imovie["title"] = movie["titles"][0]
            if movie["in_library"]:
                #print "Already on Plex"
                imovie["status"] = "On Plex already"
            elif movie["in_wanted"]:
                #print movie["in_wanted"]["status"]
                imovie["status"] = "On Wanted List"
            else :
                imovie["status"] = "Can be Added"
            if "imdb" in movie:
                #print "ID: " + str(movie["imdb"])
                imovie["imdb"] = movie["imdb"]
            else:
                imovie["imdb"] = "unknown"
            if "year" in movie:
                imovie["year"] = str(movie["year"])
            else:
                imovie["year"] = "0000"
            movies.append(imovie)
        return movies


    def getWanted(self):
        url = self.rooturl + '/api/' + self.apikey + '/media.list?type=movie&status=active'
        request = requests.get(url)
        json_data = json.loads(request.text)
        if json_data["success"] == False:
            return False
        elif json_data["success"] == True:
            movies = []
            for movie in json_data["movies"]:
                imovie = {}
                imovie["title"] = movie["title"]
                imovie["year"] = str(movie["info"]["year"])
                movies.append(imovie)
        return movies



    def downloadMovie(self,id):
        url = self.rooturl + '/api/' + self.apikey + '/movie.add/?identifier=' + urllib.quote_plus(id)
        request = requests.get(url)
        json_data = json.loads(request.text)
        if json_data["success"] == False:
            return "Failed to download movie, is the ID valid?"
        elif json_data["success"] == True:
            return "Movie added to wanted list, it will be downloaded as soon as a release becomes avaliable"
