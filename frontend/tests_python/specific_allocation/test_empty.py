import pytest
from playwright.async_api import async_playwright


@pytest.mark.playwright
async def test_specific_allocation_submit_with_empty_data():
    """
    Ensure that the form prompts donors to complete form when their Specific
    allocation section is less than 2 dollars.
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        await page.goto("http://localhost:8001")
        
        await page.get_by_text("These specific charities").click()

        await page.get_by_label("First name", exact=True).fill("Nathan")

        await page.get_by_label("Last name").fill("Sherburn")

        await page.get_by_label("Email", exact=True).fill("testing@eaa.org.au")

        await page.get_by_label("Postcode").fill("3000")

        await page.locator("#communications-section--referral-sources").select_option("cant-remember")

        # Set up dialog handler to check the alert message
        dialog_message = None
        
        async def handle_dialog(dialog):
            nonlocal dialog_message
            dialog_message = dialog.message
            assert dialog.message == "Please allocate at least $2 across your preferred charities."
            await dialog.dismiss()

        page.on("dialog", handle_dialog)

        await page.get_by_role("button", name="Donate").click()

        # Wait a bit for the dialog
        await page.wait_for_timeout(1000)

        # Verify that the dialog was shown
        assert dialog_message == "Please allocate at least $2 across your preferred charities."
        
        await browser.close()