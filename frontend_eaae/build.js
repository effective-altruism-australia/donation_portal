const fs = require("fs");

// Note: The "Paste this into WordPress" instructions below are for the final
// output. Do not copy and paste any of the code in this file into WordPress.
const donationFormHtml = `
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>EAA Donation Form</title>
    <!-- These styles are just for local development (i.e. when viewing outside of WordPress) -->
    <style>
      #donation-form-host {
        max-width: 720px;
        margin: 0 auto;
        padding: 32px;
        border: 1px solid #ccc;
        border-radius: 4px;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif
      }
    </style>
  </head>
  <body>

    <!-- Paste this into WordPress: START -->

    <!-- WARNING: If you're looking at this from within WordPress, please note that any changes you make here will be lost! Please submit changes as pull requests to: https://github.com/effective-altruism-australia/donation_portal -->

    <template id="donation-form">
      <style>
        ${fs.readFileSync("./src/styles/main.css", "utf8")}
        ${fs.readFileSync("./src/styles/utilities.css", "utf8")}
        ${fs.readFileSync("./src/styles/custom-inputs.css", "utf8")}
      </style>

      <form onsubmit="return formController.handleFormSubmit();">
        ${fs.readFileSync("./src/donation-frequency-section.html", "utf8")}
        ${fs.readFileSync("./src/specific-allocation-section.html", "utf8")}
        ${fs.readFileSync("./src/total-amount-section.html", "utf8")}
        ${fs.readFileSync("./src/personal-details-section.html", "utf8")}
        ${fs.readFileSync("./src/communications-section.html", "utf8")}
        ${fs.readFileSync("./src/payment-method-section.html", "utf8")}
        ${fs.readFileSync("./src/donate-button-section.html", "utf8")}
        ${fs.readFileSync("./src/bank-instructions-section.html", "utf8")}
        ${fs.readFileSync("./src/thankyou-section.html", "utf8")}
        ${fs.readFileSync("./src/error-section.html", "utf8")}
        ${fs.readFileSync("./src/loader.html", "utf8")}
      </form>
    </template>

    <div id="donation-form-host"></div>

    <script src="https://js.stripe.com/v3/"></script>
    <script>
      const STRIPE_API_KEY_EAAE = "${process.env.STRIPE_API_KEY_EAAE}";
      const ORIGIN = "${process.env.ORIGIN}";
      ${fs.readFileSync("./src/scripts/utilities.js", "utf8")}
      ${fs.readFileSync("./src/scripts/FormController.js", "utf8")}
    </script>

    <!-- Paste this into WordPress: END -->
  
  </body>
</html>`;

fs.writeFileSync(
  "../donation/templates/donation_form.html",
  donationFormHtml,
  "utf8"
);

console.log("EAAE Build finished!");
