import { expect, test } from "@playwright/test";

/*
Ensure that the form prompts donors to complete form when their recipient name is empty.
*/

test("Christmas gift: submit with empty data", async ({ page }) => {
  await page.goto("http://localhost:8001");

  await page.locator("#amount-section--custom-amount-input").fill("1000");

  await page.getByLabel("First name", { exact: true }).fill("Nathan");

  await page.getByLabel("Last name").fill("Sherburn");

  await page.getByLabel("Email", { exact: true }).fill("testing@eaa.org.au");

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

  await page.getByLabel("Personal message (optional,").fill("Test message!");

  const testFinished = new Promise<void>((resolve) => {
    page.on("request", (request) => {
      // The request should never be sent with invalid data
      if (request.url().includes("eaa-festiveseasoncards.deno.dev")) {
        expect(true).toBe(false);
      }
      resolve();
    });
  });

  await page.getByRole("button", { name: "Donate" }).click();

  await testFinished;
});
