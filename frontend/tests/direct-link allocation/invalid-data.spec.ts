import { expect, test } from "@playwright/test";

/*
Ensure that the error page shoes when an invalid direct-linked charity
is chosen through the url params. e.g. <baseurl>/pledge_new/?charity=charity-that-doesnt-exist
*/

test("Direct-linked allocation: unknown charity", async ({ page }) => {
  let testFinished = new Promise((resolve) => {
    page.on("request", async (request) => {
      if (request.url().includes("pledge_new")) {
        await expect(
          page.getByText("Something's gone wrong", { exact: true })
        ).toBeVisible();
        resolve(true);
      }
    });
  });

  await page.goto(
    "http://localhost:8000/pledge_new/?charity=charity-that-doesnt-exist"
  );

  await testFinished;
});
