import { expect, test } from "@playwright/test";

/*
Ensure that a Christmas card is generated with default allocation and no tip
when the festive gift option is checked.
*/

test("Christmas gift: default allocation with no tip", async ({ page }) => {
  await page.goto("http://localhost:8001");

  await page.locator("#amount-section--custom-amount-input").fill("1000");

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

  await page.locator("#festive-gift-section--recipient-name").fill("Test");

  await page
    .locator("#festive-gift-section--recipient-email")
    .fill("nathan.sherburn@eaa.org.au");

  await page.getByLabel("Personal message (optional,").fill("Test message!");

  const testFinished = new Promise<void>((resolve) => {
    page.on("request", (request) => {
      if (request.url().includes("eaa-festiveseasoncards.deno.dev")) {
        let data = JSON.parse(request.postData() || "{}");
        expect(data["paymentReference"]).toMatch(
          /^[0-9A-F]{12}$|^cs_test_[A-Za-z0-9]{58}$/
        );
        expect(data["charity"]).toBe("unallocated");
        expect(data["donorName"]).toBe("Nathan");
        expect(data["donorEmail"]).toBe("nathan.sherburn@eaa.org.au");
        expect(data["recipientName"]).toBe("Test");
        expect(data["recipientEmail"]).toBe("nathan.sherburn@eaa.org.au");
        expect(data["amount"]).toBe("1000");
        expect(data["message"]).toBe("Test message!");
        resolve();
      }
    });
  });

  await page.getByRole("button", { name: "Donate" }).click();

  await testFinished;
});
