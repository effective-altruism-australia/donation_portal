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
        ${fs.readFileSync("./src/theme.css", "utf8")}
        ${fs.readFileSync("./src/utilities.css", "utf8")}
        ${fs.readFileSync("./src/radios.css", "utf8")}
        ${fs.readFileSync("./src/checkboxes.css", "utf8")}
        ${fs.readFileSync("./src/select.css", "utf8")}
        ${fs.readFileSync("./src/buttons.css", "utf8")}
        ${fs.readFileSync("./src/fieldsets.css", "utf8")}
        ${fs.readFileSync("./src/inputs.css", "utf8")}
      </style>
      ${fs.readFileSync("./src/form.html", "utf8")}
    </template>

    <div id="donation-form-host"></div>

    <script src="https://js.stripe.com/v3/"></script>
    <script>
      const STRIPE_API_KEY_EAAE = "${process.env.STRIPE_API_KEY_EAAE}";
      const STRIPE_API_KEY_EAA = "${process.env.STRIPE_API_KEY_EAA}";
      const ORIGIN = "${process.env.ORIGIN}";
      ${fs.readFileSync("./src/utilities.js", "utf8")}
      ${fs.readFileSync("./src/main.js", "utf8")}
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
