import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.playwright
async def test_thank_you_ensure_thankyou_page_works():
    """
    Ensure thankyou page works
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        await page.goto("http://localhost:8001?thankyou")

        # Check that the "thank you" text is visible on the page
        await expect(page.get_by_text("Thank you!", exact=True)).to_be_visible()
        
        await browser.close()