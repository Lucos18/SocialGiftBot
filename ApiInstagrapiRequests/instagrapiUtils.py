import os
from time import sleep

from instagrapi import Client
from instagrapi.exceptions import LoginRequired

cachedInstagramLoginPath = "dumps.json"

instagramClient: Client = None


def requestLoginAttemptInstagram(username, password):
    global instagramClient
    instagramClient = Client()
    try:
        if os.path.exists(cachedInstagramLoginPath):
            print("Cached instagram session found, trying to login in....")
            instagramClient.load_settings(cachedInstagramLoginPath)
            instagramClient.login(username, password)
            instagramClient.get_timeline_feed()
            print("Instagram login completed!")
        else:
            instagramClient.login(username, password)
            instagramClient.dump_settings(cachedInstagramLoginPath)
            print("Dump file not found, i have created one for you.")
    except LoginRequired:
        instagramClient.relogin()
        instagramClient.dump_settings(cachedInstagramLoginPath)

    return instagramClient


async def likeInstagramPost(linkInstagramPost):
    try:
        mediapk = instagramClient.media_pk_from_url(linkInstagramPost)
        mediaid = instagramClient.media_id(mediapk)

        if instagramClient.media_like(mediaid):
            try:
                print('Like done at the link: ' + linkInstagramPost)
                return True
            except Exception as e:
                print('Error while liking the instagram post, error: ' + str(e))
                return False
        else:
            print('Could not like the instagram post, no error could be resolved.')
            return False
    except Exception as e:
        print("Photo doesn't exist, i will skip to the next campaign. Error: " + str(e))
        return False


async def followInstagramProfile(linkInstagramProfile):
    try:
        usernameInstagram = linkInstagramProfile.split("/")
        #TODO when fixed from instragrapi replace username_v1 with user_id_by_username
        userid = instagramClient.user_info_by_username_v1(usernameInstagram[3])
        if instagramClient.user_follow(userid.pk):
            print("Follow done at the link: " + linkInstagramProfile)
            return True
        else:
            print("The profile doesn't exist at the link: " + linkInstagramProfile)
            return False
    except Exception as e:
        print("Follow campaign could not be completed, error: " + str(e))
        return False
