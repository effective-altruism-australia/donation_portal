import { expect, test } from "@playwright/test";

/*
Ensure that selecting/deselecting some of the communications opt-in checkboxes
works as expected.
*/

test("Communications: checkboxes work", async ({ page }) => {
  await page.goto("http://localhost:8000/donation_form.html");

  await page.locator("#custom-amount-input").fill("5");

  await page.getByLabel("First name").fill("Nathan");

  await page.getByLabel("Last name").fill("Sherburn");

  await page
    .getByLabel("Email", { exact: true })
    .fill("nathan.sherburn@eaa.org.au");

  await page.getByLabel("Postcode").fill("3000");

  await page.locator("#referral-sources").selectOption("cant-remember");

  await page
    .locator("label")
    .filter({ hasText: "Send me news and updates" })
    .locator("div")
    .click();

  await page
    .locator("label")
    .filter({ hasText: "Connect me with my local" })
    .locator("div")
    .click();

  page.on("request", (request) => {
    if (request.url().includes("pledge_new")) {
      let data = JSON.parse(request.postData() || "{}");
      expect(data["payment_method"]).toBe("credit-card!");
      expect(data["recurring_frequency"]).toBe("one-time");
      expect(data["recurring"]).toBe(false);
      expect(data["first_name"]).toBe("Nathan");
      expect(data["last_name"]).toBe("Sherburn");
      expect(data["email"]).toBe("nathan.sherburn@eaa.org.au");
      expect(data["subscribe_to_updates"]).toBe(true);
      expect(data["subscribe_to_newsletter"]).toBe(false);
      expect(data["connect_to_community"]).toBe(true);
      expect(data["how_did_you_hear_about_us_db"]).toBe("cant-remember");
      expect(data["form-TOTAL_FORMS"]).toBe(1);
      expect(data["form-INITIAL_FORMS"]).toBe(1);
      expect(data["form-0-id"]).toBeNull();
      expect(data["form-0-amount"]).toBe("5");
      expect(data["form-0-partner_charity"]).toBe("unallocated");
      expect(data["is_gift"]).toBe(undefined);
      expect(data["gift_recipient_name"]).toBe(undefined);
      expect(data["gift_recipient_email"]).toBe(undefined);
      expect(data["gift_personal_message"]).toBe(undefined);
      expect(data["form-1-id"]).toBe(undefined);
      expect(data["form-1-amount"]).toBe(undefined);
      expect(data["form-1-partner_charity"]).toBe(undefined);
    }
  });

  await page.getByRole("button", { name: "Donate" }).click();
});
