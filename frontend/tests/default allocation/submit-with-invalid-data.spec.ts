import { expect, test } from "@playwright/test";

/*
Ensure that the form doesn't sent with invalid data and prompts the user to
correct the issues.
*/

test("Default allocation: submit with invalid data", async ({
  page,
}) => {
  await page.goto("http://localhost:8000/pledge_new/");

  await page.getByText("The most effective charities^").click();

  await page.locator('#custom-amount-input').fill('-30');

  await page.getByLabel("First name").fill("Nathan");

  await page.getByLabel("Last name").fill("Sherburn");

  await page.getByLabel("Email", { exact: true }).fill("testing@eaa.org.au");

  await page.getByLabel("Postcode").fill("3000");

  await page.locator("#referral-sources").selectOption("cant-remember");

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
