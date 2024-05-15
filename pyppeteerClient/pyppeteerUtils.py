from pyppeteer import launch
from pyppeteer.browser import Browser

browserPyppeteer: Browser = None


async def goToPageAndClick(link):
    try:
        page = await browserPyppeteer.newPage()
        await page.goto(link)
        element = await page.querySelector('a.w3-button')
        await element.click()
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
