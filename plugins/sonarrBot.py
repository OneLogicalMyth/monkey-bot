import requests
import json
import urllib

class sonarr(object):
    
    def __init__(self, couchURL, apikey,whitelistedusers):
        self.sickURL = couchURL
        self.apiKey = apikey
        self.users = whitelistedusers
    
    def begin(self,command,user):
        # make the command lower for all functions
        command = command.lower()
        response = None
        needs_help = False
        if user not in self.users:
            return "This function is currently only avaliable to contributors to say thanks"
        if 'tv today' in command:
            return self.getToday()
        elif 'tv latest' in command:
            return self.getLatest()
        elif 'tv search' in command:
            return self.getSearch(command.replace("tv search", ""))
        elif 'tv download' in command:
            return self.getDownload(command.replace("tv download", ""))
        elif command[-1] == '?':
            return "No.", False
        else:
            return "Invalid Command", False	

    def getDownload(self, searchstr):
        sick = sonarrAPI(self.sickURL, self.apiKey)
        download = sick.downloadTvShow(searchstr)
        if download == "An existing indexerid already exists in database":
            return "Tv Show allready added", False
        elif "could not be parsed into" in download:
            return "Tv Show ID invalid, Full Error: " + download, False
        elif "queued to be added" in download:
            return "Success: " + download + "\n *WARNING: This will only add future episodes, contact steve to add past episodes*", False
        return download, False

    def getSearch(self,seachstr):
        sick = sonarrAPI(self.sickURL, self.apiKey)
        tvshows = sick.searchTvShows(seachstr)
        if tvshows == "Empty":
            return "No tvshows found", False
        showlist =[]
        for show in tvshows:
            fields = []
            fields.append({"short": False, "title": show["name"] ,"value": "*Overview:* " + show["overview"] + "\n*First Aired:* " + show["first_aired"] + "\n*Allready added:* " + show["in_show_list"] + "\n*ShowID:* " + str(show["id"])})
            showlist.append({"fallback": "blah", "fields": fields})
        #message = [{"fallback": "blah", "pretext": "The following shows will download today:", "fields": showlist}]
        message = showlist
        return message, True

    def getToday(self):
        sick = sonarrAPI(self.sickURL, self.apiKey)
        tvtoday = sick.Today()
        if tvtoday == "Empty":
            return "No shows airing today", False
        showlist = []
        for show in tvtoday:
            fields = []
            fields.append({"short": False, "title": show["showname"] , "value": "*Episode:* " + show["showepisode"] + "\n*Airs:* " + show["airs"] + "\n*Quality:* " + show["quality"]})
            showlist.append({"fallback": "blah", "fields": fields})
        #message = [{"fallback": "blah", "pretext": "The following shows will download today:", "fields": showlist}]
        message = showlist
        return message, True

    def getLatest(self):
        sick = sonarrAPI(self.sickURL, self.apiKey)
        tvtoday = sick.Today()
        tvlatest = sick.Latest()
        if tvtoday == "Empty":
            tvtoday = []
        if tvlatest == "Empty":
            tvlatest = []
        if len(tvlatest) == 0 & len(tvtoday) == 0:
            return "Now shows in the next 7 days", False
        showlist = []
        for show in tvtoday:
            fields = []
            fields.append({"short": False, "title": show["showname"] , "value": "*Episode:* " + show["showepisode"] + "\n*Airs:* " + show["airs"] + "\n*Quality:* " + show["quality"]})
            showlist.append({"fallback": "Todays Shows", "fields": fields})
        for show in tvlatest:
            fields = []
            fields.append({"short": False, "title": show["showname"] , "value": "*Episode:* " + show["showepisode"] + "\n*Airs:* " + show["airs"] + "\n*Quality:* " + show["quality"]})
            showlist.append({"fallback": "Next 7 days shows", "fields": fields})
        #message = [{"fallback": "blah", "pretext": "The following shows will download today:", "fields": showlist}]
        message = showlist
        return message, True




class sonarrAPI:


        def __init__(self, url, apikey):
            self.rooturl = url
            self.apikey = apikey

        def Today(self):
            url = self.rooturl + '/api/calendar?apikey=' + self.apikey
            request = requests.get(url)
            json_data = json.loads(request.text)
            if len(json_data) < 1:
                return "Empty"
            else :
                shows = []
                for show in json_data:
                    ishow = {}
                    ishow["showname"] = show["series"]["title"]
                    ishow["showepisode"] = show["title"]
                    ishow["quality"] = str(show["series"]["qualityProfileId"])
                    ishow["airs"] = show["airDate"]
                    shows.append(ishow)
                return shows

        def Latest(self):
            url = self.rooturl + '/api/calendar?apikey=' + self.apikey
            request = requests.get(url)
            json_data = json.loads(request.text)
            if len(json_data) < 1:
                return "Empty"
            else :
                shows = []
                for show in json_data:
                    ishow = {}
                    ishow["showname"] = show["series"]["title"]
                    ishow["showepisode"] = show["title"]
                    ishow["quality"] = str(show["series"]["qualityProfileId"])
                    ishow["airs"] = show["airDate"]
                    shows.append(ishow)
                return shows


        def searchTvShows(self, search):
            url = self.rooturl + '/api/series/lookup?apikey=' + self.apikey + '&term=' + search
            request = requests.get(url)
            json_data = json.loads(request.text)
            if len(json_data) < 1:
                return "Empty"
            else:
                shows = []
                for show in json_data:
                    ishow = {}
                    if "firstAired" in show:
                        ishow["first_aired"] = show["firstAired"]
                    else:
                        ishow["first_aired"] = "Unknown"
                    if show["seasonFolder"] == True:
                        ishow["in_show_list"] = "Yes"
                    else:
                        ishow["in_show_list"] = "No"
                    ishow["name"] = show["title"]
                    if "overview" in show:
                        ishow["overview"] = show["overview"]
                    else:
                        ishow["overview"] = "Missing"
                    ishow["id"] = show["tvdbId"]
                    shows.append(ishow)
                return shows


        def downloadTvShow(self, id):
            url = self.rooturl + '/api/series/lookup?apikey=' + self.apikey + '&term=tvdbid:' + id
            request = requests.get(url)
            json_data = json.loads(request.text)
            if len(json_data) < 1:
                return "Failed to add Tv Show, is the ID valid?"
            else:
                postdata = {
                    "title" : json_data[0]["title"],
                    "tvdbId": json_data[0]["tvdbId"],
                    "ProfileId": "6",
                    "monitored": "true",
                    "rootFolderPath" : "/movies/",
                    "apiKey": self.apikey,
                    "titleSlug": json_data[0]["titleSlug"],
                    "images": json_data[0]["images"],
                    "seasons": json_data[0]["seasons"]
                    
                }
            url = self.rooturl + '/api/series?apikey=' + self.apikey
            newHeaders = {'Content-type': 'application/json'}
            bob = json.dumps(postdata)
            request = requests.post(url, data=bob, headers=newHeaders)
            json_data = json.loads(request.text)
            print(request.text)
            if request.status_code == 400:
                return "Tv Show already in plex library"
            else:
                return "Tv Show added to library, any future episodes will be downloaded. For past episodes contact Steve"

        





