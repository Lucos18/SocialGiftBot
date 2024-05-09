from pyppeteer import launch
from pyppeteer.browser import Browser


async def goToPageAndClick(browser, link):
    try:

        page = await browser.newPage()
        await page.goto(link)
        # TODO click
        await browser.close()
        return True
    except Exception as e:
        return False


