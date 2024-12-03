import { expect, test } from "@playwright/test";

/*
Ensure that the form submits the correct data when a "bank transactions" is
selected for a specific charity.
*/

test("Payment method: submit a bank transaction donation for a specific selection of charities", async ({
  page,
}) => {
  await page.goto("http://localhost:8000/pledge_new/");

  await page.getByText("These specific charities").click();

  await page.locator("#malaria-consortium-amount").fill("33");

  await page.locator("#give-directly-amount").fill("66");

  await page.getByLabel("First name", { exact: true }).fill("Nathan");

  await page.getByLabel("Last name").fill("Sherburn");

  await page.getByLabel("Email", { exact: true }).fill("testing@eaa.org.au");

  await page.getByLabel("Postcode").fill("3000");

  await page.getByText("Bank Transfer", { exact: true }).click();

  page.on("request", (request) => {
    if (request.url().includes("pledge_new")) {
      let data = JSON.parse(request.postData() || "{}");
      expect(data["payment_method"]).toBe("bank-transfer");
      expect(data["recurring_frequency"]).toBe("one-time");
      expect(data["recurring"]).toBe(false);
      expect(data["first_name"]).toBe("Nathan");
      expect(data["last_name"]).toBe("Sherburn");
      expect(data["email"]).toBe("testing@eaa.org.au");
      expect(data["subscribe_to_updates"]).toBe(true);
      expect(data["subscribe_to_newsletter"]).toBe(false);
      expect(data["connect_to_community"]).toBe(false);
      expect(data["how_did_you_hear_about_us_db"]).toBe("");
      expect(data["form-TOTAL_FORMS"]).toBe(3);
      expect(data["form-INITIAL_FORMS"]).toBe(3);
      expect(data["form-0-id"]).toBe(null);
      expect(data["form-0-partner_charity"]).toBe("malaria-consortium");
      expect(data["form-0-amount"]).toBe("33");
      expect(data["form-1-id"]).toBe(null);
      expect(data["form-1-partner_charity"]).toBe("give-directly");
      expect(data["form-1-amount"]).toBe("66");
      expect(data["form-2-id"]).toBe(null);
      expect(data["form-2-partner_charity"]).toBe("eaa-amplify");
      expect(data["form-2-amount"]).toBe("9.90");

      // Make sure things that shouldn't be sent are not sent
      expect(data["is_gift"]).toBe(undefined);
      expect(data["gift_recipient_name"]).toBe(undefined);
      expect(data["gift_recipient_email"]).toBe(undefined);
      expect(data["gift_personal_message"]).toBe(undefined);
      expect(data["form-3-id"]).toBe(undefined);
      expect(data["form-3-partner_charity"]).toBe(undefined);
      expect(data["form-3-amount"]).toBe(undefined);
    }
  });

  let testFinished = new Promise((resolve) => {
    page.on("response", async (response) => {
      if (response.url().includes("pledge_new")) {
        expect(response.status()).toBe(200);
        await expect(page.getByText("Thank you, Nathan!")).toBeVisible();
        await expect(page.getByText("$108.90 to:")).toBeVisible({
          timeout: 10000,
        });
        await expect(
          page.getByText(
            "Your donation will be allocated to your chosen partner charity (or charities)."
          )
        ).toBeVisible();
        await page
          .locator("#bank-instructions-section--reference")
          .textContent()
          .then((text) => {
            expect(text).toMatch(/^[0-9A-F]{12}$/);
          });
        resolve(true);
      }
    });
  });

  await page.getByRole("button", { name: "Donate" }).click();

  await testFinished;
});
