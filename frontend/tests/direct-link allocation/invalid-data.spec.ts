import { expect, test } from "@playwright/test";

/*
Ensure that the error page shoes when an invalid direct-linked charity
is chosen through the url params. e.g. <baseurl>/pledge_new/?charity=charity-that-doesnt-exist
*/

test("Direct-linked allocation: unknown charity", async ({ page }) => {
  await page.goto(
    "http://localhost:8001?charity=charity-that-doesnt-exist"
  );

  // Check that the error message is displayed
  const errorMessage = page.getByText(
    "Something's gone wrong", { exact: true }
  );
  await expect(errorMessage).toBeVisible();

});
