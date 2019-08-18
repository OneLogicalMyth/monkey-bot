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
        print command
        if user not in self.users:
		    return "This function is currently only avaliable to contributors to say thanks"
        if 'tv today' in command:
		    return self.getToday()
        elif 'tv latest' in command:
		    return self.getLatest()
        elif command[-1] == '?':
		    return "No."
        else:
		    return "Invalid Command"	


    def getToday(self):
        sick = sickChillAPI(self.sickURL, self.apiKey)
        tvtoday = sick.Today()
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
        showlist = []
        for show in tvtoday:
            fields = []
            fields.append({"short": False, "title": show["showname"] , "value": "*Episode:* " + show["showepisode"] + "\n*Airs:* " + show["airs"] + "\n*Quality:* " + show["quality"]})
            showlist.append({"fallback": "blah", "fields": fields})
        for show in tvlatest:
            fields = []
            fields.append({"short": False, "title": show["showname"] , "value": "*Episode:* " + show["showepisode"] + "\n*Airs:* " + show["airs"] + "\n*Quality:* " + show["quality"]})
            showlist.append({"fallback": "blah", "fields": fields})
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
                shows = []
                for show in json_data["data"]["soon"]:
                    ishow = {}
                    ishow["showname"] = show["show_name"]
                    ishow["showepisode"] = show["ep_name"]
                    ishow["quality"] = show["quality"]
                    ishow["airs"] = show["airs"]
                    shows.append(ishow)
                return shows

