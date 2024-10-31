import { expect, test } from "@playwright/test";

/*
Ensure that the form prompts donors to complete the custom allocation section
when their data is invalid.
*/

test("Custom allocation: submit with invalid data", async ({ page }) => {

  await page.goto("http://localhost:8000/pledge_new/");

  await page.getByText("These specific charities").click();

  await page.locator("#malaria-consortium-amount").fill("10");

  await page.locator("#give-directly-amount").fill("-5");

  await page.getByLabel("First name").fill("Nathan");

  await page.getByLabel("Last name").fill("Sherburn");

  await page.getByLabel("Email", { exact: true }).fill("testing@eaa.org.au");

  await page.getByLabel("Postcode").fill("3000");

  await page.locator("#referral-sources").selectOption("cant-remember");

  const testFinished = new Promise<void>((resolve) => {
    page.on("request", (request) => {
      // The request should never be sent with invalid data
      if (request.url().includes("pledge_new")) {
        expect(true).toBe(false);
      }
      resolve();
    });
  });

  await page.getByRole("button", { name: "Donate" }).click();
  
  await testFinished;
});
