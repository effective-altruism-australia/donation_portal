import { expect, test } from "@playwright/test";

/*
Ensure that the form submits the correct data when a Specific allocation is filled
out correctly
*/

test("Custom allocation: submit with standard data", async ({ page }) => {
  await page.goto("http://localhost:8001");

  await page.getByText("These specific charities").click();

  await page.locator("#give-directly-amount").fill("5");

  await page.getByText("Skip", { exact: true }).click();

  await page.getByLabel("First name", { exact: true }).fill("Nathan");

  await page.getByLabel("Last name").fill("Sherburn");

  await page
    .getByLabel("Email", { exact: true })
    .fill("nathan.sherburn@eaa.org.au");

  await page.getByLabel("Postcode").fill("3000");

  await page
    .locator("#communications-section--referral-sources")
    .selectOption("cant-remember");

  await page
    .locator("label")
    .filter({ hasText: "Yes, this is a gift for the festive season" })
    .locator("div")
    .click();

  await page
    .locator("#festive-gift-section--recipient-email")
    .fill("nathan.sherburn@eaa.org.au");

  await page.locator("#festive-gift-section--recipient-name").fill("Test");

  await page.locator("#festive-gift-section--message").fill("Test message!");

  const testFinished = new Promise<void>((resolve) => {
    page.on("request", (request) => {
      if (request.url().includes("eaa-festiveseasoncards.deno.dev")) {
        let data = JSON.parse(request.postData() || "{}");
        expect(data["paymentReference"]).toMatch(
          /^[0-9A-F]{12}$|^cs_test_[A-Za-z0-9]{58}$/
        );
        expect(data["charity"]).toBe("give-directly");
        expect(data["donorName"]).toBe("Nathan");
        expect(data["donorEmail"]).toBe("nathan.sherburn@eaa.org.au");
        expect(data["recipientName"]).toBe("Test");
        expect(data["recipientEmail"]).toBe("nathan.sherburn@eaa.org.au");
        expect(data["amount"]).toBe("5");
        expect(data["message"]).toBe("Test message!");
        resolve();
      }
    });
  });

  await page.getByRole("button", { name: "Donate" }).click();

  await testFinished;
});
