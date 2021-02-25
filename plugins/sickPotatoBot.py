import requests
import json
import urllib

class sickChill(object):
    
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
        sick = sickChillAPI(self.sickURL, self.apiKey)
        download = sick.downloadTvShow(searchstr)
        if download == "An existing indexerid already exists in database":
            return "Tv Show allready added", False
        elif "could not be parsed into" in download:
            return "Tv Show ID invalid, Full Error: " + download, False
        elif "queued to be added" in download:
            return "Success: " + download + "\n *WARNING: This will only add future episodes, contact steve to add past episodes*", False
        return download, False

    def getSearch(self,seachstr):
        sick = sickChillAPI(self.sickURL, self.apiKey)
        tvshows = sick.searchTvShows(seachstr)
        if tvshows == "Empty":
            return "No tvshows found", False
        showlist =[]
        for show in tvshows:
            fields = []
            fields.append({"short": False, "title": show["name"] , "value": "*First Aired:* " + show["first_aired"] + "\n*Allready added:* " + show["in_show_list"] + "\n*ShowID:* " + str(show["id"])})
            showlist.append({"fallback": "blah", "fields": fields})
        #message = [{"fallback": "blah", "pretext": "The following shows will download today:", "fields": showlist}]
        message = showlist
        return message, True

    def getToday(self):
        sick = sickChillAPI(self.sickURL, self.apiKey)
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
        sick = sickChillAPI(self.sickURL, self.apiKey)
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




class sickChillAPI:


        def __init__(self, url, apikey):
            self.rooturl = url
            self.apikey = apikey

        def Today(self):
            url = self.rooturl + '/api/' + self.apikey + '/?cmd=future&type=today'
            request = requests.get(url)
            json_data = json.loads(request.text)
            if json_data["result"] !="success":
                return False
            elif json_data["result"] == "success":
                if len(json_data["data"]["today"]) == 0:
                    return "Empty"
                shows = []
                for show in json_data["data"]["today"]:
                    ishow = {}
                    ishow["showname"] = show["show_name"]
                    ishow["showepisode"] = show["ep_name"]
                    ishow["quality"] = show["quality"]
                    ishow["airs"] = show["airs"]
                    shows.append(ishow)
                return shows

        def Latest(self):
            url = self.rooturl + '/api/' + self.apikey + '/?cmd=future&type=soon'
            request = requests.get(url)
            json_data = json.loads(request.text)
            if json_data["result"] !="success":
                return False
            elif json_data["result"] == "success":
                if len(json_data["data"]["soon"]) == 0:
                    return "Empty"
                shows = []
                for show in json_data["data"]["soon"]:
                    ishow = {}
                    ishow["showname"] = show["show_name"]
                    ishow["showepisode"] = show["ep_name"]
                    ishow["quality"] = show["quality"]
                    ishow["airs"] = show["airs"]
                    shows.append(ishow)
                return shows


        def searchTvShows(self, search):
            url = self.rooturl + '/api/' + self.apikey + '/?cmd=sb.searchindexers&only_new=0&name=' + search
            request = requests.get(url)
            json_data = json.loads(request.text)
            if json_data["result"] !="success":
                return False
            elif json_data["result"] == "success":
                if len(json_data["data"]["results"]) == 0:
                    return "Empty"
                shows = []
                for show in json_data["data"]["results"]:
                    ishow = {}
                    ishow["first_aired"] = show["first_aired"]
                    if show["in_show_list"] == True:
                        ishow["in_show_list"] = "Yes"
                    else:
                        ishow["in_show_list"] = "No"
                    ishow["name"] = show["name"]
                    ishow["id"] = show["tvdbid"]
                    shows.append(ishow)
                return shows


        def downloadTvShow(self, id):
            url = self.rooturl + '/api/' + self.apikey + "?cmd=show.addnew&indexerid=268592&status=ignored&tvdbid=" + id
            request = requests.get(url)
            json_data = json.loads(request.text)
            if json_data["result"] !="success":
                return json_data["message"]
            elif json_data["result"] == "success":
                return json_data["message"]
        





