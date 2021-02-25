import requests
import base64
import json
import hashlib


class GitBot(object):
    def __init__(self, gitURL, username, password, toolRepoURL):
        self.gitURL = gitURL
        self.toolRepoURL = toolRepoURL
        self.username = username
        self.password = password
    
    def begin(self,command,user):
        # make the command lower for all functions
        command = command.lower()
        response = None
        needs_help = False
        if 'github.com' in command:
            gitapi = GitAPI(self.gitURL, self.username, self.password, self.toolRepoURL)
            return gitapi.star_repo(command)
        elif 'http' in command:
            gitapi = GitAPI(self.gitURL, self.username, self.password, self.toolRepoURL)
            return gitapi.add_link(command)
        elif command[-1] == '?':
            return "No."
        else:
            return "Not a valid Link"	





class GitAPI(object):
    def __init__(self, url, username, password, toolRepoURL):
        self.githuburl = url
        self.toolRepoURL = toolRepoURL
        self.username = username
        self.password = password
        self.session = requests.session()
        self.session.auth = (username, password)

    def star_repo(self, url):
        repoitems = url.replace('<','').replace('>','').split("/")[-2:]
        print(self.githuburl + "/user/starred/" + repoitems[0] + "/" + repoitems[1])
        response = self.session.put(self.githuburl + "/user/starred/" + repoitems[0] + "/" + repoitems[1])
        if response.status_code == 204:
            return "Repo has been sucessfully starred"
        else:
            return "Repo Private or Not Found"

    def add_link(self, link):
        existinglinks, sha = self.get_file()
        link = link.replace('<','').replace('>','')
        if link in existinglinks:
            return "Link exists allready"
        else:
            return self.update_file(existinglinks, link, sha)

    def update_file(self, existinglinks, link, sha):
        newlinks = existinglinks + link + "\n"
        update_payload = { "message": "New Link added", 
                            "committer" : {
                                "name" : "Monkey Bot",
                                "email" : "monkey@pentestmonkeys.tech"
                            }, 
                            "content" : base64.b64encode(newlinks),
                            "sha" : sha
                            }
        response = self.session.put(self.toolRepoURL, data=json.dumps(update_payload))
        if response.status_code == 200:
            return "Link Added successfully"
        else:
            return "An error occured :("

    def get_file(self):
        response = self.session.get(self.toolRepoURL)
        content =  response.json()
        return base64.b64decode(content["content"]), content["sha"]



