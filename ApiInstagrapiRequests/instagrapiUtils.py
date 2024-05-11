import os

from instagrapi import Client
from instagrapi.exceptions import LoginRequired

cachedInstagramLoginPath = "dumps.json"


def requestLoginAttemptInstagram(username, password):
    cl = Client()
    try:
        if os.path.exists(cachedInstagramLoginPath):
            cl.load_settings(cachedInstagramLoginPath)
            cl.login(username, password)
            cl.get_timeline_feed()
        else:
            cl.login(username, password)
            cl.dump_settings(cachedInstagramLoginPath)
            print("dump file not found, i have created one for you.")
    except LoginRequired:
        cl.relogin()
        cl.dump_settings(cachedInstagramLoginPath)

    return cl
