import requests
import ast
import hashlib
import base64
import random
from PCRClient import PCRClient
import time

class PCRApi:
    def __init__(self, viewer_id, uid, access_key):
        self.uid = uid
        self.access_key = access_key
        self.Client = PCRClient(viewer_id)
        self.home = self.Client.login(uid, access_key)
        self.clan_id = self.home['user_clan']['clan_id']

    def query_id(self, viewer_id: int):
        res = self.Client.Callapi('/profile/get_profile', {'target_viewer_id': viewer_id})
        if ['user_info'] not in res:
            self.Client.login(self.uid, self.access_key)
            res = self.Client.Callapi('/profile/get_profile', {'target_viewer_id': viewer_id})
        return res

    def query_clan(self, clan_id: int):
        res = self.Client.Callapi('/clan/others_info', {'clan_id': clan_id})
        if 'clan' not in res:
            self.Client.login(self.uid, self.access_key)
            res = self.Client.Callapi('/clan/others_info', {'clan_id': clan_id})
        return res

    #查询会战排名页数
    def get_page_status(self,page: int):
        temp = self.Client.Callapi('clan_battle/period_ranking', {'clan_id': self.clan_id, 'clan_battle_id': -1, 'period': -1, 'month': 0, 'page': page, 'is_my_clan': 0, 'is_first': 1})
        if 'period_ranking' not in temp:
            self.Client.login(self.uid, self.access_key)
            temp = self.Client.Callapi('clan_battle/period_ranking', {'clan_id': self.clan_id, 'clan_battle_id': -1, 'period': -1, 'month': 0, 'page': page, 'is_my_clan': 0, 'is_first': 1})
        return temp['period_ranking']    


