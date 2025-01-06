import { expect, test } from "@playwright/test";

/*
Ensure that not selecting any of the communications opt-in checkboxes
works as expected.
*/

test("Communications: no checkboxes selected", async ({ page }) => {
  await page.goto("http://localhost:8000/pledge_new/");

  await page.locator("#amount-section--custom-amount-input").fill("5");

  await page.getByLabel("First name", { exact: true }).fill("Nathan");

  await page.getByLabel("Last name").fill("Sherburn");

  await page.getByLabel("Email", { exact: true }).fill("testing@eaa.org.au");

  await page.getByLabel("Postcode").fill("3000");

  await page.locator("#communications-section--referral-sources").selectOption("cant-remember");

  await page
    .locator("label")
    .filter({ hasText: "Send me news and updates" })
    .locator("div")
    .click();

  const testFinished = new Promise<void>((resolve) => {
    page.on("request", (request) => {
      if (request.url().includes("pledge_new")) {
        let data = JSON.parse(request.postData() || "{}");
        expect(data["payment_method"]).toBe("credit-card");
        expect(data["recurring_frequency"]).toBe("one-time");
        expect(data["recurring"]).toBe(false);
        expect(data["first_name"]).toBe("Nathan");
        expect(data["last_name"]).toBe("Sherburn");
        expect(data["email"]).toBe("testing@eaa.org.au");
        expect(data["subscribe_to_updates"]).toBe(false);
        expect(data["subscribe_to_newsletter"]).toBe(false);
        expect(data["connect_to_community"]).toBe(false);
        expect(data["how_did_you_hear_about_us_db"]).toBe("cant-remember");
        expect(data["form-TOTAL_FORMS"]).toBe(2);
        expect(data["form-INITIAL_FORMS"]).toBe(2);
        expect(data["form-0-id"]).toBeNull();
        expect(data["form-0-amount"]).toBe("5");
        expect(data["form-0-partner_charity"]).toBe("unallocated");
        expect(data["form-1-id"]).toBeNull();
        expect(data["form-1-amount"]).toBe("0.50");
        expect(data["form-1-partner_charity"]).toBe("eaa-amplify");
        
        // Make sure things that shouldn't be sent are not sent
        expect(data["is_gift"]).toBe(undefined);
        expect(data["gift_recipient_name"]).toBe(undefined);
        expect(data["gift_recipient_email"]).toBe(undefined);
        expect(data["gift_personal_message"]).toBe(undefined);
        expect(data["form-2-id"]).toBe(undefined);
        expect(data["form-2-amount"]).toBe(undefined);
        expect(data["form-2-partner_charity"]).toBe(undefined);
        resolve();
      }
    });
  });

  await page.getByRole("button", { name: "Donate" }).click();
  
  await testFinished;
});
