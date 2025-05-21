import { expect, test } from "@playwright/test";

/*
Ensure that the form prompts donors to complete form when their Specific
allocation section is less than 2 dollars.
*/

test("Specific allocation: submit with empty data", async ({ page }) => {
  await page.goto('http://localhost:8001');
  
  await page.getByText('These specific charities').click();

  await page.getByLabel('First name', {exact:true}).fill('Nathan');

  await page.getByLabel('Last name').fill('Sherburn');

  await page.getByLabel('Email', { exact: true }).fill('testing@eaa.org.au');

  await page.getByLabel('Postcode').fill('3000');

  await page.locator('#communications-section--referral-sources').selectOption('cant-remember');

  page.on('dialog', async dialog => {
    expect(dialog.message() === 'Please allocate at least $2 across your preferred charities.');
    await dialog.dismiss();
  });

  await page.getByRole("button", { name: "Donate" }).click();
});