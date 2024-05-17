from time import sleep

from pyppeteer import launch
from pyppeteer.browser import Browser

browserPyppeteer: Browser = None


async def goToPageAndClick(link):
    try:
        page = await browserPyppeteer.newPage()
        await page.goto(link)
        element = await page.querySelector('a.w3-button')
        await element.click()
        sleep(3)
        await page.close()
        return True
    except Exception as e:
        print('Exception found for goToPageAndClick: ', e)
        return False


async def goToRulesPageAndCompileInformations(link, name, surname, email):
    try:
        page = await browserPyppeteer.newPage()
        await page.goto(link)
        await page.type('#name', name)
        await page.type('#surname', surname)
        await page.type('#email', email)
        await page.click('#privacy-acceptance')
        await page.click('#service-acceptance')
        await page.click('#accept')
        sleep(30)
        await page.close()
        return True
    except Exception as e:
        print('Exception found for goToPageAndClick: ', e)
        return False


async def pyppeteerBrowser():
    global browserPyppeteer
    browserPyppeteer = await launch(
        headless=False,
        args=['--no-sandbox'],
        autoClose=False
    )


async def closePyppeteerBrowser():
    await browserPyppeteer.disconnect()
    await browserPyppeteer.close()
