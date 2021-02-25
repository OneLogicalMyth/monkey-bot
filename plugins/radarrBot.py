import json
import requests
import urllib


class radarr(object):

    def __init__(self, couchURL, apikey, folder, whitelistedusers):
        self.couchURL = couchURL
        self.apiKey = apikey
        self.users = whitelistedusers
        self.folder = folder

    def begin(self, command, user):
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
        elif 'movie wanted' in command:
            return self.doWanted(command.replace("movie wanted", ""))
        elif command[-1] == '?':
            return "No.", False
        else:
            return "Invalid Command", False

    def doSearch(self, searchstr):
        couch = radarrAPI(self.couchURL, self.apiKey)
        if searchstr == "":
            return "Invalid search string please specify a search term such as 'movies search iron man'"
        searchList = couch.searchMovies(searchstr)
        if searchList == "Error":
            return "No results found for the specified search"
        movielist = []
        for movie in searchList:
            fields = []
            fields.append(
                {
                    "short": False,
                    "title": movie["title"],
                    "value": "*Overview:* " + movie["overview"] + "\n*Year:* " + movie["year"] + "\n*Status:* " + movie["status"] + "\n*MovieID:* " + str(movie["imdb"])
                }
            )
            movielist.append({"fallback": "blah", "fields": fields})
            # message += "<http://www.imdb.com/title/" + movie["imdb"] + "|" + movie["title"] + "(" + movie["year"] + ")" + "> Status: " + movie["status"] + "   :id:" + movie["imdb"] + "\n"
        message = movielist
        return message, True

    def doDownload(self, id):
        couch = radarrAPI(self.couchURL, self.apiKey)
        if id == "":
            return "Invalid ID"
        movieDownload = couch.downloadMovie(id, self.folder)
        return movieDownload, False

    def doWanted(self, id):
        couch = radarrAPI(self.couchURL, self.apiKey)
        movieWanted = couch.getWanted()
        if movieWanted is False:
            return "Error occurred"
        movielist = []
        for movie in movieWanted:
            fields = []
            fields.append(
                {
                    "short": False,
                    "title": movie["title"],
                    "value": "*Year:* " + movie["year"]
                }
            )
            movielist.append({"fallback": "blah", "fields": fields})
            message = movielist
        return message, True


class radarrAPI:

    def __init__(self, url, apikey):
        self.rooturl = url
        self.apikey = apikey

    def printapi(self):
        return self.apikey

    def searchMovies(self, name):
        url = self.rooturl + '/api/v3/movie/lookup?apikey=' + self.apikey + '&term=' + urllib.parse.quote_plus(name)
        request = requests.get(url)
        json_data = json.loads(request.text)
        if len(json_data) < 1:
            return "Error"
        else:
            movies = []
            for movie in json_data:
                imovie = {}
                # print "Movie Name: " + movie["titles"][0]
                imovie["title"] = movie["title"]
                if movie["folderName"] != "":
                    # print "Already on Plex"
                    imovie["status"] = "On Plex already"
                else:
                    imovie["status"] = "Can be Added"
                if "imdbId" in movie:
                    # print "ID: " + str(movie["imdb"])
                    imovie["imdb"] = movie["imdbId"]
                else:
                    imovie["imdb"] = "unknown"
                if "year" in movie:
                    imovie["year"] = str(movie["year"])
                else:
                    imovie["year"] = "0000"
                if "overview" in movie:
                    imovie["overview"] = movie["overview"]
                movies.append(imovie)
        return movies

    def getWanted(self):
        url = self.rooturl + '/api/v3/calendar?apikey=' + self.apikey + "&unmonitored=false&start=2021-02-22&end=2030-01-01"
        request = requests.get(url)
        json_data = json.loads(request.text)
        if len(json_data) < 1:
            return False
        else:
            movies = []
            for movie in json_data:
                imovie = {}
                imovie["title"] = movie["title"]
                imovie["year"] = str(movie["year"])
                movies.append(imovie)
            return movies

    def downloadMovie(self, id, folder):
        # url = self.rooturl + '/api/v3/movie/'+ urllib.quote_plus(id) + "?apikey=" + self.apikey
        url = self.rooturl + '/api/v3/movie/lookup?apikey=' + self.apikey + '&term=imdb:' + id
        request = requests.get(url)
        json_data = json.loads(request.text)
        # print(request.text)
        if len(json_data) < 1:
            return "Failed to download movie, is the ID valid?"
        else:
            postdata = {
                "title": json_data[0]["title"],
                "tmdbId": json_data[0]["tmdbId"],
                "qualityProfileId": "6",
                "monitored": "true",
                "rootFolderPath": folder,
                "apiKey": self.apikey,
                "titleSlug": json_data[0]["titleSlug"],
                "images": json_data[0]["images"]

            }
            url = self.rooturl + '/api/v3/movie?apikey=' + self.apikey
            newHeaders = {'Content-type': 'application/json'}
            bob = json.dumps(postdata)
            request2 = requests.post(url, data=bob, headers=newHeaders)
            if request2.status_code == 400:
                return "Movie already in plex library or awaiting release"
            else:
                return "Movie added to wanted list, it will be downloaded as soon as a release becomes avaliable"
