import asyncio
import json
import os
import random
import sys
import time
from time import sleep

from telethon import TelegramClient, events
from telethon.tl.types import MessageEntityUrl

import campaignEnum
from ApiTelethonRequests.telethonUtils import requestLoginAttemptTelegram

# PYPPETEER MUST BE ABOVE FROM IMPORT #
PYPPETEER_CHROMIUM_REVISION = '1263111'

os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION

from pyppeteerClient.pyppeteerUtils import goToPageAndClick, pyppeteerBrowser

telegramApiCredentialsPath = "telegramApiCredentials.json"
instagramApiCredentialsPath = "instagramApiCredentials.json"
settingsPath = "settings.json"

campaignEnumObject = campaignEnum.Campaign

clientTelegram: TelegramClient = None

sleeptime = random.uniform(2, 4)

# TODO need Instagram Client

accountInstagramInfo = {}
accountTelegramInfo = {}
settings = {}


# Api Information region #
def telegramApiCredentialsFileRead():
    global accountTelegramInfo
    try:
        assert os.path.isfile(telegramApiCredentialsPath)
        with open(telegramApiCredentialsPath, "r") as apiInfo:
            accountData = json.load(apiInfo)
            apiInfo.close()
            accountTelegramInfo = accountData
            print("Account data for telegram loaded correctly!")
            return True
    except Exception as e:
        print("Error! Account credentials not found for telegram, file is not found, a new one will be created now.")
        return False


def telegramApiCredentialsFileWrite():
    global accountTelegramInfo
    try:
        accountData = {
            'accountName': input('Enter account name: '),
            'apiId': input('Enter api_id: '),
            'apiHash': input('Enter api_hash: '),
            'accountNumber': input('Enter account number (used only for first login): '),
            'accountPassword': input(
                'Enter account password (used only for first login if two factor auth is enabled): '),
        }
        with open(telegramApiCredentialsPath, "w") as apiInfo:
            json.dump(accountData, apiInfo, indent=4)
            apiInfo.close()
            accountTelegramInfo = accountData
            print("Account data for telegram saved correctly!")
            return True
    except Exception as e:
        print("Error! Account credentials not found for telegram, could not create account data file.")
        print("Code error: " + str(e))
        return False


def instagramApiCredentialsFileRead():
    global accountInstagramInfo
    try:
        assert os.path.isfile(telegramApiCredentialsPath)
        with open(instagramApiCredentialsPath, "r") as apiInfo:
            accountData = json.load(apiInfo)
            apiInfo.close()
            accountInstagramInfo = accountData
            print("Account data for instagram loaded correctly!")
            return True
    except Exception as e:
        print("Error! Account credentials not found for instagram, file is not found, a new one will be created now.")
        return False


def instagramApiCredentialsFileWrite():
    global accountInstagramInfo
    try:
        accountData = {
            'accountName': input('Enter account username: '),
            'accountPassword': input('Enter account password: '),
        }
        with open(instagramApiCredentialsPath, "w") as apiInfo:
            json.dump(accountData, apiInfo, indent=4)
            apiInfo.close()
            accountInstagramInfo = accountData
            print("Account data for instagram saved correctly!")
            return True
    except Exception as e:
        print("Error! Account credentials not found for instagram, could not create account data file.")
        print("Code error: " + str(e))
        return False


# Api Information END region #

# Settings region #
def settingsFileRead():
    global settings
    try:
        assert os.path.isfile(settingsPath)
        with open(settingsPath, "r") as settingsInfo:
            settings = json.load(settingsInfo)
            settingsInfo.close()
            print("Settings data loaded correctly!")
            return True
    except Exception as e:
        print("Error! Settings file not found, you will create one now.")
        return False


def settingsFileWrite():
    global settings
    try:
        settings = {
            'pauseTimeBetweenEachChallenge': int(input('Enter pause time (seconds) before starting a new challenge: ')),
            'retryCampaign': input('Enter amount of tries before skipping a campaign: '),
        }
        with open(settingsPath, "w") as settingsInfo:
            json.dump(settings, settingsInfo, indent=4)
            settingsInfo.close()
            print("Settings data saved correctly!")
            return True
    except Exception as e:
        print("Error! Settings file could not be created.")
        print("Code error: " + str(e))
        return False


# Settings END region #


def waitTimeBeforeContinue(totalTimeToWait):
    for i in reversed(range(1, totalTimeToWait)):
        time.sleep(1 - time.time() % 1)
        sys.stderr.write('\r%4d' % i)


def scrapeLinkFromTelegramMessage(event):
    msg = event.message
    for _, inner_text in msg.get_entities_text(MessageEntityUrl):
        url = inner_text
        return url


async def evaluateAndCompleteCampaign(message, filteredUrl):
    campaignCompleted = False
    retryCount = 0
    if message.find(campaignEnumObject.IGTV.value['textMessageToEvaluate']) != -1:
        while not campaignCompleted:
            print("Campaign evaluated: IGTV")
            print("Opening website and clicking button...")
            didClickHappenSuccessfully = await goToPageAndClick(filteredUrl)
            if didClickHappenSuccessfully:
                print("Button click worked successfully!")
                campaignCompleted = True
                print("Waiting before confirming the campaign...")
                waitTimeBeforeContinue(45)
                print("Campaign completed")
            else:
                retryCount = retryCount + 1
                sleep(sleeptime)
                print("Error occurred with pyppeteer browser while clicking button, retry number: ", retryCount)
    else:
        print("No campaign have been found from message")
    return campaignCompleted


try:
    import progressbar
except ModuleNotFoundError:
    print("please run > pip install progressbar2")

if not telegramApiCredentialsFileRead():
    if not telegramApiCredentialsFileWrite():
        print('Could not read or create new login file data, please check Github and follow the steps')
        exit(0)

if not instagramApiCredentialsFileRead():
    if not instagramApiCredentialsFileWrite():
        print('Could not read or create new login file data, please check Github and follow the steps')
        exit(0)

if not settingsFileRead():
    if not settingsFileWrite():
        print('Could not read or create new settings file, please check Github and follow the steps')
        exit(0)

#clientInstagram = requestLoginAttemptInstagram(
    #accountInstagramInfo["accountName"],
    #accountInstagramInfo["accountPassword"]
#)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(pyppeteerBrowser())

with requestLoginAttemptTelegram(
        accountTelegramInfo["accountName"],
        accountTelegramInfo["apiId"],
        accountTelegramInfo["apiHash"]
) as clientTelegram:
    client = clientTelegram
    client.connect()


    @client.on(events.NewMessage(chats='@socialgiftbot', incoming=True, outgoing=False))
    async def handler(event):
        eventRawText = event.raw_text

        print("Incoming message from @socialgiftbot")
        print("message received: ", event.message)
        print("raw message received: ", event.raw_text)
        filteredUrl = scrapeLinkFromTelegramMessage(event)
        campaignResult = await evaluateAndCompleteCampaign(eventRawText, filteredUrl)
        if campaignResult:
            await event.message.click(1)
            print("Confirm button clicked! Campaign is completed")
        else:
            await event.message.click(0)
            print("Skip button clicked! Campaign is NOT completed")


    client.start()

    client.run_until_disconnected()
