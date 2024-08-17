const fs = require("fs");

// TODO: remove this and use built in node environment loading once we move off
// version 8 of NodeJS.
const dotenv = require("dotenv");
dotenv.config();

// Note: The "Paste this into WordPress" instructions below are for the final
// output. Do not copy-paste any of the code in this file.
const donationFormHtml = `
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>EAA Donation Form</title>
    <style>
      <!-- Read in WordPress styles so that inherited properties look like they will on the WordPress site for development -->
      ${fs.readFileSync("./src/wordpress-styles/w1.css", "utf8")}
      ${fs.readFileSync("./src/wordpress-styles/w2.css", "utf8")}
      ${fs.readFileSync("./src/wordpress-styles/w3.css", "utf8")}
      ${fs.readFileSync("./src/wordpress-styles/w4.css", "utf8")}
      ${fs.readFileSync("./src/wordpress-styles/w5.css", "utf8")}
      #donation-form-host {
        max-width: 720px;
        margin: 0 auto;
        padding: 32px;
        border: 1px solid #ccc;
        border-radius: 4px;
      }
    </style>
  </head>
  <body>

    <!-- Paste this into WordPress: START -->

    <!-- Note: If you're looking at this from within WordPress, please note that changes made here will be lost! Please make changes at: https://github.com/effective-altruism-australia/donation_portal -->

    <template id="donation-form">
      <style>
        ${fs.readFileSync("./src/style-utilities.css", "utf8")}
        ${fs.readFileSync("./src/style-radios.css", "utf8")}
        ${fs.readFileSync("./src/style-checkboxes.css", "utf8")}
      </style>
      ${fs.readFileSync("./src/form.html", "utf8")}
    </template>

    <div id="donation-form-host"></div>

    <script src="https://js.stripe.com/v3/"></script>
    <script>
      const STRIPE_API_KEY_EAAE = "${process.env.STRIPE_API_KEY_EAAE}";
      const STRIPE_API_KEY_EAA = "${process.env.STRIPE_API_KEY_EAA}";
      const ORIGIN = "${process.env.ORIGIN}";
      ${fs.readFileSync("./src/script-utilities.js", "utf8")}
      ${fs.readFileSync("./src/script-main.js", "utf8")}
    </script>

    <!-- Paste this into WordPress: END -->
  
  </body>
</html>`;

fs.writeFileSync(
  "../donation/templates/donation_form.html",
  donationFormHtml,
  "utf8"
);

console.log("Build finished!");
