import json
import pytest
from playwright.async_api import async_playwright


@pytest.mark.playwright
async def test_tipping_submit_basic_donation_with_30_percent_tip():
    """
    Ensure that the form sends the right data when a basic donation with a 30% tip is submitted.
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        await page.goto("http://localhost:8001")

        await page.get_by_text("$50", exact=True).click()

        await page.get_by_text("30%").click()

        await page.get_by_label("First name", exact=True).fill("Nathan")

        await page.get_by_label("Last name").fill("Sherburn")

        await page.get_by_label("Email", exact=True).fill("testing@eaa.org.au")

        await page.get_by_label("Postcode").fill("3000")

        await page.locator("#communications-section--referral-sources").select_option("cant-remember")

        # Set up request interception to capture the pledge_new request
        request_data = {}
        
        def handle_request(request):
            if "pledge_new" in request.url:
                if request.post_data:
                    request_data.update(json.loads(request.post_data))

        page.on("request", handle_request)

        await page.get_by_role("button", name="Donate").click()

        # Wait for the request to be captured
        await page.wait_for_timeout(1000)

        # Verify the request data
        assert request_data["payment_method"] == "credit-card"
        assert request_data["recurring_frequency"] == "one-time"
        assert request_data["recurring"] is False
        assert request_data["first_name"] == "Nathan"
        assert request_data["last_name"] == "Sherburn"
        assert request_data["email"] == "testing@eaa.org.au"
        assert request_data["subscribe_to_updates"] is True
        assert request_data["subscribe_to_newsletter"] is False
        assert request_data["connect_to_community"] is False
        assert request_data["how_did_you_hear_about_us_db"] == "cant-remember"
        assert request_data["form-TOTAL_FORMS"] == 2
        assert request_data["form-INITIAL_FORMS"] == 0
        assert request_data["form-0-id"] is None
        assert request_data["form-0-partner_charity"] == "unallocated"
        assert request_data["form-0-amount"] == "50"
        assert request_data["form-1-id"] is None
        assert request_data["form-1-partner_charity"] == "eaa-amplify"
        assert request_data["form-1-amount"] == "15.00"

        # Make sure things that shouldn't be sent are not sent
        assert "is_gift" not in request_data
        assert "gift_recipient_name" not in request_data
        assert "gift_recipient_email" not in request_data
        assert "gift_personal_message" not in request_data
        assert "form-2-id" not in request_data
        assert "form-2-partner_charity" not in request_data
        assert "form-2-amount" not in request_data
        
        await browser.close()