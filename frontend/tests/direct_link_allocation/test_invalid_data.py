import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.playwright
async def test_direct_linked_allocation_unknown_charity():
    """
    Ensure that the error page shows when an invalid direct-linked charity
    is chosen through the url params. e.g. <baseurl>/pledge_new/?charity=charity-that-doesnt-exist
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()

        await page.goto("http://localhost:8001?charity=charity-that-doesnt-exist")

        # Check that the error message is displayed
        error_message = page.get_by_text("Something's gone wrong", exact=True)
        await expect(error_message).to_be_visible()

        await browser.close()
