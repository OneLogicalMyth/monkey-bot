import requests
from re import findall
from argparse import ArgumentParser
import datetime, json, urllib3

class myzone(object):

    def __init__(self,username,password,nicknames):
        self.username = username
        self.password = password
        self.nicknames = nicknames
        self.login()

    def login(self):
        logindata = {'e':self.username,'p':self.password,'r':'0'}
        response = requests.post('https://www.myzonemoves.com/calls/login/', data=logindata)
        if response.text == 0:
            return False
        else:
            self.phpsession = {'PHPSESSID': response.text}
            return True

    def logout(self):
        response = requests.get('https://www.myzonemoves.com/sessioncalls/logout/', cookies=self.phpsession)

    def leaderboard(self,nicknames=None):
        # nicknames should be in the format of ["nick1","nick2","nick3"]
        response = requests.get('https://www.myzonemoves.com/sessioncalls/leaderboard/', cookies=self.phpsession)
        leaderboard = response.json()                                                                                                                                                                                                                
        if 'error' in leaderboard:
            return False
        else:
            board = [obj for obj in leaderboard["data"] if(obj['nickname'] in self.nicknames)]
            output = "*My Zone Leaderboard*\n"
            for person in board:
                output += person["name"] + " - MEPS " + person["score"]
            return output
            self.logout()
