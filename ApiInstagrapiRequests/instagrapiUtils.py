import os

from instagrapi import Client

cachedInstagramLoginPath = "dumps.json"


def requestLoginAttemptInstagram(username, password):
    cl = Client()

    if (os.path.exists(cachedInstagramLoginPath)):
        cl.load_settings(cachedInstagramLoginPath)
        cl.login(username, password)
        cl.get_timeline_feed()
    else:
        cl.login(username, password)
        cl.dump_settings(cachedInstagramLoginPath)
        print("dump file not found, i have created one for you.")

    return cl
