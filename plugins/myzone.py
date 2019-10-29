import requests
from re import findall
from argparse import ArgumentParser
import datetime, json, urllib3

class myzone(object):

    def __init__(self,username,password):
        self.username = username
        self.password = password
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
        response = requests.get('https://www.myzonemoves.com/sessioncalls/leaderboard/', cookies=self.phpsession)                                                                                                                                    leaderboard = response.json()                                                                                                                                                                                                                if 'error' in leaderboard:
            return False
        else:
            if nicknames == None:
                return leaderboard["data"]
            else:
                filterout = [obj for obj in leaderboard["data"] if(obj['nickname'] in nicknames)]
                return filterout
