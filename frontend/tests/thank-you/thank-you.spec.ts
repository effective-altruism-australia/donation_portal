import { expect, test } from "@playwright/test";

/*
Ensure thankyou page works
*/

test("Thank you: ensure thankyou page works", async ({ page }) => {

  await page.goto(
    "http://localhost:8000/pledge_new/?thankyou"
  );

  // Check that the "thank you" text is visible on the page
  await expect(
    page.getByText("Thank you", { exact: true })
  ).toBeVisible();

});
