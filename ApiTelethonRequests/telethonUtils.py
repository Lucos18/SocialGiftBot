from telethon import TelegramClient

clientTelegram: TelegramClient = None


def requestLoginAttemptTelegram(username, apiID, apiHash):
    global clientTelegram
    clientTelegram = TelegramClient(username, apiID, apiHash)
    return clientTelegram


async def sendEarnMoneyMessageChoice():
    await clientTelegram.send_message(entity='@socialgiftbot', message='🤑 GUADAGNA 🤑')


async def sendUnlockSocialCampaignsChoice():
    await clientTelegram.send_message(entity='@socialgiftbot', message='🔒 SBLOCCA CAMPAGNE SOCIAL 🔒')
