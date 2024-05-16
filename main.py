import asyncio
import json
import os
import random
import sys
import time
from time import sleep

from telethon import TelegramClient, events
from telethon.tl.types import MessageEntityUrl, MessageEntityTextUrl

import campaignEnum
from ApiInstagrapiRequests.instagrapiUtils import likeInstagramPost, requestLoginAttemptInstagram, \
    followInstagramProfile
from ApiTelethonRequests.telethonUtils import requestLoginAttemptTelegram, sendEarnMoneyMessageChoice

# PYPPETEER MUST BE ABOVE FROM IMPORT #
PYPPETEER_CHROMIUM_REVISION = '1263111'

os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION

from pyppeteerClient.pyppeteerUtils import goToPageAndClick, pyppeteerBrowser, goToRulesPageAndCompileInformations, \
    closePyppeteerBrowser

telegramApiCredentialsPath = "telegramApiCredentials.json"
clientTelegram: TelegramClient = None
accountTelegramInfo = {}

instagramApiCredentialsPath = "instagramApiCredentials.json"
accountInstagramInfo = {}

socialGiftInfoPath = "socialGiftInfo.json"
accountSocialGiftInfo = {}

settingsPath = "settings.json"
settings = {}

campaignEnumObject = campaignEnum.Campaign

sleeptime = random.uniform(2, 4)


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


def socialGiftInfoFileRead():
    global accountSocialGiftInfo
    try:
        assert os.path.isfile(socialGiftInfoPath)
        with open(socialGiftInfoPath, "r") as apiInfo:
            accountData = json.load(apiInfo)
            apiInfo.close()
            accountSocialGiftInfo = accountData
            print("Account info for social gift loaded correctly!")
            return True
    except Exception as e:
        print("Error! Account info for social gift not found, file is not found, a new one will be created now.")
        return False


def socialGiftInfoFileWrite():
    global accountSocialGiftInfo
    try:
        accountData = {
            'personalName': input('Enter your name (used for rules auto-compilation if not already done): '),
            'personalSurname': input('Enter your surname (used for rules auto-compilation if not already done): '),
            'personalEmail': input('Enter your email (used for rules auto-compilation if not already done): '),
        }
        with open(socialGiftInfoPath, "w") as apiInfo:
            json.dump(accountData, apiInfo, indent=4)
            apiInfo.close()
            accountSocialGiftInfo = accountData
            print("Account info for social gift saved correctly!")
            return True
    except Exception as e:
        print("Error! Account info for social gift not found, could not create account data file.")
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
            'autocompleteRulesScenario': str(
                input('Do you want to auto-complete Rules request? (y/n): ')).lower().strip() == 'y',
            'debugMode': str(
                input('Do you want to auto debug mode? (y/n): ')).lower().strip() == 'y',
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


def scrapeLinkFromInnerTextTelegramMessage(event):
    msg = event.message
    for _, inner_text in msg.get_entities_text(MessageEntityUrl):
        print("Link found in message: ", inner_text)
        url = inner_text
        return url


def scrapeLinkFromUrlEntityTelegramMessage(event):
    msg = event.message
    for url_entity in msg.get_entities_text(MessageEntityTextUrl):
        print("Link found in message: ", url_entity)
        url = url_entity
        return url


async def evaluateAndCompleteCampaign(message, filteredUrl):
    # todo create better architecture
    campaignCompleted = False
    retryCount = 0
    if message.find(campaignEnumObject.IGTV.value['textMessageToEvaluate']) != -1:
        while not campaignCompleted:  # TODO missing retrycount check
            print("Campaign evaluated: IGTV")
            print("Opening website and clicking button...")
            didClickHappenSuccessfully = await goToPageAndClick(filteredUrl)
            if didClickHappenSuccessfully:
                print("Button click worked successfully!")
                campaignCompleted = True
                print("Waiting before confirming the campaign...")
                waitTimeBeforeContinue(
                    campaignEnumObject.IGTV.value['timeToWaitBeforeConfirmingCampaign'])  # Correct time is 15 seconds
                print("Campaign completed")
            else:
                retryCount = retryCount + 1
                sleep(sleeptime)
                print("Error occurred with pyppeteer browser while clicking button, retry number: ", retryCount)
    if message.find(campaignEnumObject.RULES.value['textMessageToEvaluate']) != -1:
        # TODO missing RULES case scenario
        if settings['autocompleteRulesScenario']:
            await goToRulesPageAndCompileInformations(
                "https://socialgift.alexdev.it/regole/?id=192481247",  # TODO ADD HERE CORRECT LINK OBTAINING
                accountSocialGiftInfo['personalName'],
                accountSocialGiftInfo['personalSurname'],
                accountSocialGiftInfo['personalEmail']
            )
    if message.find(campaignEnumObject.YOUTUBE.value['textMessageToEvaluate']) != -1:
        waitTimeBeforeContinue(campaignEnumObject.YOUTUBE.value['timeToWaitBeforeConfirmingCampaign'])
        campaignCompleted = True
    if message.find(campaignEnumObject.LIKE.value['textMessageToEvaluate']) != -1:
        resultCampaign = await likeInstagramPost(filteredUrl)
        if resultCampaign:
            print('Like campaign completed successfully! waiting some time before continuing...')
            waitTimeBeforeContinue(
                campaignEnumObject.LIKE.value['timeToWaitBeforeConfirmingCampaign'] + int(random.uniform(3, 5)))
            campaignCompleted = True
        else:
            print('Like campaign not completed, waiting some time before continuing and skip...')
            waitTimeBeforeContinue(
                campaignEnumObject.LIKE.value['timeToWaitBeforeConfirmingCampaign'] + int(random.uniform(1, 2)))
            campaignCompleted = False
    if message.find(campaignEnumObject.FOLLOW.value['textMessageToEvaluate']) != -1:
        resultCampaign = await followInstagramProfile(filteredUrl)
        if resultCampaign:
            print('Follow campaign completed successfully! waiting some time before continuing...')
            waitTimeBeforeContinue(
                campaignEnumObject.FOLLOW.value['timeToWaitBeforeConfirmingCampaign'] + int(random.uniform(5, 8)))
            campaignCompleted = True
        else:
            print('Follow campaign not completed, waiting some time before continuing and skip...')
            waitTimeBeforeContinue(
                campaignEnumObject.FOLLOW.value['timeToWaitBeforeConfirmingCampaign'] + int(random.uniform(60, 120)))
            campaignCompleted = False
    if message.find(campaignEnumObject.COMPLETED.value['textMessageToEvaluate']) != -1:
        print("All campaigns completed! Closing the script...")
        await closePyppeteerBrowser()
        exit()
    if message.find(campaignEnumObject.STORIES.value['textMessageToEvaluate']) != -1:
        # todo implement stories
        print("STORIES NOT IMPLEMENTED")
        exit()
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

if not socialGiftInfoFileRead():
    if not socialGiftInfoFileWrite():
        print('Could not read or create new social gift info file, please check Github and follow the steps')
        exit(0)

clientInstagram = requestLoginAttemptInstagram(
    accountInstagramInfo["accountName"],
    accountInstagramInfo["accountPassword"]
)

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

    loop.run_until_complete(sendEarnMoneyMessageChoice())


    @client.on(events.NewMessage(chats='@socialgiftbot', incoming=True, outgoing=False))
    async def handler(event):
        eventRawText = event.raw_text

        print("Incoming message from @socialgiftbot")
        # print("message received: ", event.message)
        print("raw message received: ", event.raw_text)
        filteredUrl = scrapeLinkFromInnerTextTelegramMessage(event)
        campaignResult = await evaluateAndCompleteCampaign(eventRawText, filteredUrl)
        if campaignResult:
            if settings['debugMode']:
                print('Debug mode: waiting before starting a new campaign. Last campaign return: ' + str(campaignResult))
                waitTimeBeforeContinue(5)
            await event.message.click(1)
            print("Confirm button clicked! Campaign is completed")
        else:
            if settings['debugMode']:
                print('Debug mode: waiting before starting a new campaign. Last campaign return: ' + str(campaignResult))
                waitTimeBeforeContinue(5)
            await event.message.click(0)
            print("Skip button clicked! Campaign is NOT completed")


    client.start()

    client.run_until_disconnected()
