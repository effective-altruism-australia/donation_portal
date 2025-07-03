import pytest
from playwright.async_api import async_playwright


@pytest.mark.playwright
async def test_payment_method_submit_credit_card_donation():
    """
    Placeholder test for once stripe testing is set up
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        # Placeholder test for once stripe testing is set up
        assert True
        
        await browser.close()