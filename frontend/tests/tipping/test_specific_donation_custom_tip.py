import json
import re
import pytest
from playwright.async_api import async_playwright


@pytest.mark.playwright
async def test_tipping_submit_specific_donation_with_custom_tip():
    """
    Ensure that the form submits the correct data when a specific donation is made with a custom tip
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()

        await page.goto("http://localhost:8001")

        await page.get_by_text("These specific charities").click()

        await page.locator("#malaria-consortium-amount").fill("50")

        await page.locator("#give-directly-amount").fill("50")

        await page.locator("#amplify-impact-section--custom-amount-input").fill("20")

        await page.get_by_label("First name", exact=True).fill("Nathan")

        await page.get_by_label("Last name").fill("Sherburn")

        await page.get_by_label("Email", exact=True).fill("testing@eaa.org.au")

        await page.get_by_label("Postcode").fill("3000")

        await page.locator("#communications-section--referral-sources").select_option(
            "cant-remember"
        )

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
        assert request_data["form-TOTAL_FORMS"] == 3
        assert request_data["form-INITIAL_FORMS"] == 0
        assert request_data["form-0-id"] is None
        assert re.match(
            r"^(malaria-consortium|give-directly)$",
            request_data["form-0-partner_charity"],
        )
        assert request_data["form-0-amount"] == "50"
        assert request_data["form-1-id"] is None
        assert re.match(
            r"^(malaria-consortium|give-directly)$",
            request_data["form-1-partner_charity"],
        )
        assert request_data["form-1-amount"] == "50"
        assert request_data["form-2-id"] is None
        assert request_data["form-2-partner_charity"] == "eaa-amplify"
        assert request_data["form-2-amount"] == "20.00"

        # Make sure things that shouldn't be sent are not sent
        assert "is_gift" not in request_data
        assert "gift_recipient_name" not in request_data
        assert "gift_recipient_email" not in request_data
        assert "gift_personal_message" not in request_data
        assert "form-3-id" not in request_data
        assert "form-3-partner_charity" not in request_data
        assert "form-3-amount" not in request_data

        await browser.close()
