import smtplib, json, argparse, os, stat, time, base64, subprocess, socket, uuid, requests, urllib.request, sys, re, hashlib, hmac, shutil

class CheckForUpdate: 
    """
        this class will handle the update availability, usefull for other script that use the sendemail, or for people that wanna build theyr own update logic. Also can be used internally
    """      
    def __init__(self):  
        try:
            puo_update_available, puo_new_version = check_for_update(__version__)
            puo_response = json.dumps({"version": __version__,"latest_version": puo_new_version, "need_update": puo_update_available}, ensure_ascii=False) 
            self.puo_update_available = puo_update_available
            self.puo_new_version = puo_new_version
            self.puo_response = puo_response
        except Exception as e:
            print(f"[ERROR]: {e}")
            sys.exit(1)
            
    def parse_as_resp(self):
        return self.puo_new_version, self.puo_update_available    
    def parse_as_output(self):
        return self.puo_response