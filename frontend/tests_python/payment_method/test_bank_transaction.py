import json
import re
import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.playwright
async def test_payment_method_submit_bank_transaction_donation():
    """
    Ensure that the form submits the correct data when a "bank transactions" is
    selected.
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        await page.goto("http://localhost:8001")

        await page.locator("#amount-section--custom-amount-input").fill("2222")

        await page.get_by_label("First name", exact=True).fill("Nathan")

        await page.get_by_label("Last name").fill("Sherburn")

        await page.get_by_label("Email", exact=True).fill("testing@eaa.org.au")

        await page.get_by_label("Postcode").fill("3000")

        await page.locator("#communications-section--referral-sources").select_option("cant-remember")

        await page.get_by_text("Bank Transfer", exact=True).click()

        # Set up request interception to capture the pledge_new request
        request_data = {}
        
        def handle_request(request):
            if "pledge_new" in request.url:
                if request.post_data:
                    request_data.update(json.loads(request.post_data))

        page.on("request", handle_request)

        # Set up response handler to check the UI after submission
        response_received = False
        
        async def handle_response(response):
            nonlocal response_received
            if "pledge_new" in response.url:
                assert response.status == 200
                await expect(page.get_by_text("Thank you, Nathan!")).to_be_visible()
                await expect(page.get_by_text("$2444.20 to:")).to_be_visible()
                await expect(
                    page.get_by_text("Your donation will be allocated to our partner charities.")
                ).to_be_visible()
                
                # Check that the reference follows the expected pattern
                reference_text = await page.locator("#bank-instructions-section--reference").text_content()
                assert re.match(r"^[0-9A-F]{12}$", reference_text)
                response_received = True

        page.on("response", handle_response)

        await page.get_by_role("button", name="Donate").click()

        # Wait for both request and response to be processed
        await page.wait_for_timeout(2000)

        # Verify the request data
        assert request_data["payment_method"] == "bank-transfer"
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
        assert request_data["form-0-amount"] == "2222"
        assert request_data["form-1-id"] is None
        assert request_data["form-1-partner_charity"] == "eaa-amplify"
        assert request_data["form-1-amount"] == "222.20"

        # Make sure things that shouldn't be sent are not sent
        assert "is_gift" not in request_data
        assert "gift_recipient_name" not in request_data
        assert "gift_recipient_email" not in request_data
        assert "gift_personal_message" not in request_data
        assert "form-2-id" not in request_data
        assert "form-2-partner_charity" not in request_data
        assert "form-2-amount" not in request_data

        # Ensure response was processed
        assert response_received
        
        await browser.close()