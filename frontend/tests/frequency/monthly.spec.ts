import { expect, test } from "@playwright/test";

/*
Ensure that the form submits the correct data when a "monthly" frequency is
selected.
*/

test("Frequency: submit a monthly donation with custom amount", async ({ page }) => {
  await page.goto('http://localhost:8001');
  
  await page.getByText('Monthly').click();

  await page.locator('#amount-section--custom-amount-input').fill('400');

  await page.getByLabel('First name', {exact:true}).fill('Nathan');

  await page.getByLabel('Last name').fill('Sherburn');

  await page.getByLabel('Email', { exact: true }).fill('testing@eaa.org.au');

  await page.getByLabel('Postcode').fill('3000');
  
  await page.locator('#communications-section--referral-sources').selectOption('cant-remember');
  
  page.on("request", (request) => {
    if (request.url().includes("pledge_new")) {
      let data = JSON.parse(request.postData() || "{}");
      expect(data["payment_method"]).toBe("credit-card");
      expect(data["recurring_frequency"]).toBe("monthly");
      expect(data["recurring"]).toBe(true);
      expect(data["first_name"]).toBe("Nathan");
      expect(data["last_name"]).toBe("Sherburn");
      expect(data["email"]).toBe("testing@eaa.org.au");
      expect(data["subscribe_to_updates"]).toBe(true);
      expect(data["subscribe_to_newsletter"]).toBe(false);
      expect(data["connect_to_community"]).toBe(false);
      expect(data["how_did_you_hear_about_us_db"]).toBe("cant-remember");
      expect(data["form-TOTAL_FORMS"]).toBe(2);
      expect(data["form-INITIAL_FORMS"]).toBe(0);
      expect(data["form-0-id"]).toBe(null);
      expect(data["form-0-partner_charity"]).toBe("unallocated");
      expect(data["form-0-amount"]).toBe("400");
      expect(data["form-1-id"]).toBe(null);
      expect(data["form-1-partner_charity"]).toBe("eaa-amplify");
      expect(data["form-1-amount"]).toBe("40.00");

      // Make sure things that shouldn't be sent are not sent
      expect(data["is_gift"]).toBe(undefined);
      expect(data["gift_recipient_name"]).toBe(undefined);
      expect(data["gift_recipient_email"]).toBe(undefined);
      expect(data["gift_personal_message"]).toBe(undefined);
      expect(data["form-2-id"]).toBe(undefined);
      expect(data["form-2-partner_charity"]).toBe(undefined);
      expect(data["form-2-amount"]).toBe(undefined);
    }
  });

  await page.getByRole("button", { name: "Donate" }).click();
});