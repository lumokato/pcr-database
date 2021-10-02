import requests
from PCRPack import *
import ast
import hashlib
import base64
import random
class PCRClient:
    def __init__(self, viewer_id):
        self.viewer_id = viewer_id
        self.request_id = ""
        self.session_id = ""
        self.urlroot = "https://l3-prod-uo-gs-gzlj.bilibiligame.net/"
        self.default_headers={
            "EXCEL-VER": "1.0.0",
            "SHORT-UDID": "000a67;666:366:153;811:356<465C755=844=162;435141553828347141745637252372331",
            "BATTLE-LOGIC-VERSION": "4",
            "IP-ADDRESS": "10.0.2.15",
            "DEVICE-ID": "febf37270db0254b8d1f76af92f0419f",
            "DEVICE-NAME": "Google PIXEL 2 XL",
            "GRAPHICS-DEVICE-NAME": "Adreno (TM) 540",
            "APP-VER": "3.4.8",
            "RES-KEY": "d145b29050641dac2f8b19df0afe0e59",
            "RES-VER": "10002200",
            "KEYCHAIN": "",
            "CHANNEL-ID": "4",
            "PLATFORM-ID": "4", 
            "REGION-CODE": "",
            "PLATFORM": "2",
            "PLATFORM-OS-VERSION": "Android OS 7.1.2 / API-25 (NOF26V/4565141)",
            "LOCALE": "Jpn",
            "X-Unity-Version": "2018.4.30f1",
            "BUNDLE_VER" : "",
            "DEVICE": "2",            
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; PIXEL 2 XL Build/NOF26V)",
            "Accept-Encoding": "gzip, deflate",           
            "Connection": "close"}
        self.conn = requests.session()
    def Callapi(self, apiurl, request, crypted = True):
        key = CreateKey()
        if crypted:
            request['viewer_id'] = encrypt(str(self.viewer_id), key).decode()
        else:
            request['viewer_id'] = str(self.viewer_id)
        req = Pack(request, key)
        flag = self.request_id != None and self.request_id != ''
        flag2 = self.session_id != None and self.session_id != ''
        headers = self.default_headers
        if flag: headers["REQUEST-ID"] = self.request_id
        if flag2: headers["SID"] = self.session_id
        resp = self.conn.post(url= self.urlroot + apiurl,
                        headers = headers, data = req)
        null = None
        if crypted:
            ret = decrypt(resp.content)
        else: ret = eval(resp.content.decode())
        ret_header = ret["data_headers"]
        if "sid" in ret_header:
            if ret_header["sid"] != None and ret_header["sid"] != "":
                self.session_id = hashlib.md5((ret_header["sid"] + "c!SID!n").encode()).hexdigest()
        if "request_id" in ret_header:
            if ret_header["request_id"] != None and ret_header["request_id"] != "" and ret_header["request_id"] != self.request_id:
                self.request_id = ret_header["request_id"]
        if "viewer_id" in ret_header:
            if ret_header["viewer_id"] != None and ret_header["viewer_id"] != 0 and ret_header["viewer_id"] != self.viewer_id:
                self.viewer_id = int(ret_header["viewer_id"])
        return ret["data"]
    def login(self, uid, access_key):
        self.manifest = self.Callapi('source_ini/get_maintenance_status', {}, False)
        ver = self.manifest["required_manifest_ver"]
        self.default_headers["MANIFEST-VER"] = ver
        self.Callapi('tool/sdk_login', {"uid": uid, "access_key" : access_key, "platform" : self.default_headers["PLATFORM-ID"], "channel_id" : self.default_headers["CHANNEL-ID"]})
        self.Callapi('check/game_start', {"app_type": 0, "campaign_data" : "", "campaign_user": random.randint(1, 1000000)})
        self.Callapi("check/check_agreement", {})
        self.Callapi("load/index", {"carrier": "google"})
        self.Home = self.Callapi("home/index", {'message_id': random.randint(1, 5000), 'tips_id_list': [], 'is_first': 1, 'gold_history': 0})
        return self.Home
class ApiException(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code
        

    
    
