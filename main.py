import asyncio
import json
import os

PYPPETEER_CHROMIUM_REVISION = '1263111'

os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION

from pyppeteer import launch
from telethon import TelegramClient

from ApiInstagrapiRequests.instagrapiUtils import cachedInstagramLoginPath, requestLoginAttemptInstagram
from ApiTelethonRequests.telethonUtils import requestLoginAttemptTelegram
from pyppeteerClient.pyppeteerUtils import goToPageAndClick

telegramApiCredentialsPath = "telegramApiCredentials.json"
instagramApiCredentialsPath = "instagramApiCredentials.json"
settingsPath = "settings.json"

client: TelegramClient = None
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

async def main():
    clientInstagram = requestLoginAttemptInstagram(
        accountInstagramInfo["accountName"],
        accountInstagramInfo["accountPassword"]
    )
    clientTelegram = requestLoginAttemptTelegram(
        accountTelegramInfo["accountName"],
        accountTelegramInfo["apiId"],
        accountTelegramInfo["apiHash"]
    )
    browserPyppeteer = await launch(
        headless=False,
        args=['--no-sandbox'],
        autoClose=False
    )
    await goToPageAndClick(browserPyppeteer, "www.google.com")
    print(clientInstagram)
    print(clientTelegram)


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

asyncio.run(main())

# TODO Add instagram client connection
