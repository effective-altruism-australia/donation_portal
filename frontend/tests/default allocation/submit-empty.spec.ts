import { expect, test } from "@playwright/test";

/*
Ensure that the form prompts donors to complete form when their default
allocation section is empty.
*/

test("Custom allocation: submit with empty data", async ({ page }) => {
  await page.goto('http://localhost:8000/pledge_new/');
  
  await page.getByLabel('First name').fill('Nathan');

  await page.getByLabel('Last name').fill('Sherburn');

  await page.getByLabel('Email', { exact: true }).fill('testing@eaa.org.au');

  await page.getByLabel('Postcode').fill('3000');

  await page.locator('#referral-sources').selectOption('cant-remember');

  page.on('dialog', async dialog => {
    expect(dialog.message() === 'Please select an amount of at least $2.');
    await dialog.dismiss();
  });

  page.on("request", (request) => {
    // The request should never be sent with invalid data
    if (request.url().includes("pledge_new")) {
      expect(true).toBe(false);
    }
  });
  
  await page.getByRole("button", { name: "Donate" }).click();
});