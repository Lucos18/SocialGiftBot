from telethon import TelegramClient


def requestLoginAttemptTelegram(username, apiID, apiHash):
    return TelegramClient(username, apiID, apiHash)