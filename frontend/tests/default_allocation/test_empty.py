import pytest
from playwright.async_api import async_playwright


@pytest.mark.playwright
async def test_default_allocation_submit_with_empty_data():
    """
    Ensure that the form prompts donors to complete form when their default
    allocation section is empty.
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()

        await page.goto("http://localhost:8001")

        await page.get_by_label("First name", exact=True).fill("Nathan")

        await page.get_by_label("Last name").fill("Sherburn")

        await page.get_by_label("Email", exact=True).fill("testing@eaa.org.au")

        await page.get_by_label("Postcode").fill("3000")

        await page.locator("#communications-section--referral-sources").select_option(
            "cant-remember"
        )

        # Set up dialog handler to check the alert message
        dialog_message = None

        async def handle_dialog(dialog):
            nonlocal dialog_message
            dialog_message = dialog.message
            assert dialog.message == "Please select an amount of at least $2."
            await dialog.dismiss()

        page.on("dialog", handle_dialog)

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

        # Verify that the dialog was shown and no request was sent
        assert dialog_message == "Please select an amount of at least $2."
        assert not request_sent, "No request should be sent with invalid data"

        await browser.close()
