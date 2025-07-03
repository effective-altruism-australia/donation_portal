import pytest
from playwright.async_api import async_playwright


@pytest.mark.playwright
async def test_custom_allocation_submit_with_invalid_data():
    """
    Ensure that the form prompts donors to complete the Specific allocation section
    when their data is invalid.
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        await page.goto("http://localhost:8001")

        await page.get_by_text("These specific charities").click()

        await page.locator("#malaria-consortium-amount").fill("10")

        await page.locator("#give-directly-amount").fill("-5")

        await page.get_by_label("First name", exact=True).fill("Nathan")

        await page.get_by_label("Last name").fill("Sherburn")

        await page.get_by_label("Email", exact=True).fill("testing@eaa.org.au")

        await page.get_by_label("Postcode").fill("3000")

        await page.locator("#communications-section--referral-sources").select_option("cant-remember")

        # Set up request handler to ensure no request is sent with invalid data
        request_sent = False
        
        def handle_request(request):
            nonlocal request_sent
            if "pledge_new" in request.url:
                request_sent = True

        page.on("request", handle_request)

        await page.get_by_role("button", name="Donate").click()

        # Wait a bit to see if any requests are sent
        await page.wait_for_timeout(1000)

        # The request should never be sent with invalid data
        assert not request_sent, "No request should be sent with invalid data"
        
        await browser.close()