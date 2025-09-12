import os
import pathlib
from dotenv import load_dotenv


# Get the directory where the script is located
script_dir = pathlib.Path(__file__).parent.absolute()

# Construct the absolute path to the .env file
dotenv_path = os.path.join(script_dir, "../.env")

# Load the .env file
load_dotenv(dotenv_path=dotenv_path)

# Note: The "Paste this into WordPress" instructions below are for the final
# output. Do not copy and paste any of the code in this file into WordPress.
donation_form_html = f"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>EAA Donation Form</title>
    <!-- These styles are just for local development (i.e. when viewing outside of WordPress) -->
    <style>
      #donation-form-host {{
        max-width: 720px;
        margin: 0 auto;
        padding: 32px;
        border: 1px solid #ccc;
        border-radius: 4px;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif
      }}
    </style>
  </head>
  <body>

    <!-- Paste this into WordPress: START -->

    <!-- WARNING: If you're looking at this from within WordPress, please note that any changes you make here will be lost! Please submit changes as pull requests to: https://github.com/effective-altruism-australia/donation_portal -->

    <script
      src="https://js.sentry-cdn.com/d205ff693a7fc76ead4d172e310f66ff.min.js"
      crossorigin="anonymous"
    ></script>

    <template id="donation-form">
      <style>
        {open(script_dir / 'src/styles/main.css', 'r').read()}
        {open(script_dir / 'src/styles/utilities.css', 'r').read()}
        {open(script_dir / 'src/styles/custom-inputs.css', 'r').read()}
      </style>

      <form onsubmit="return formController.handleFormSubmit();">
        {open(script_dir / 'src/donation-frequency-section.html', 'r').read()}
        {open(script_dir / 'src/allocation-section.html', 'r').read()}
        {open(script_dir / 'src/direct-link-charity-section.html', 'r').read()}
        {open(script_dir / 'src/amount-section.html', 'r').read()}
        {open(script_dir / 'src/specific-allocation-section.html', 'r').read()}
        {open(script_dir / 'src/amplify-impact-section.html', 'r').read()}
        {open(script_dir / 'src/total-amount-section.html', 'r').read()}
        {open(script_dir / 'src/personal-details-section.html', 'r').read()}
        {open(script_dir / 'src/communications-section.html', 'r').read()}
        {open(script_dir / 'src/payment-method-section.html', 'r').read()}
        {open(script_dir / 'src/donate-button-section.html', 'r').read()}
        {open(script_dir / 'src/bank-instructions-section.html', 'r').read()}
        {open(script_dir / 'src/thankyou-section.html', 'r').read()}
        {open(script_dir / 'src/error-section.html', 'r').read()}
        {open(script_dir / 'src/loader.html', 'r').read()}
      </form>
    </template>

    <div id="donation-form-host"></div>

    <script src="https://js.stripe.com/v3/"></script>
    <script>
      const STRIPE_API_KEY_EAAE = "{os.environ.get('STRIPE_PUBLIC_KEY_EAAE')}";
      const STRIPE_API_KEY_EAA = "{os.environ.get('STRIPE_PUBLIC_KEY_EAA')}";
      const ORIGIN = "{os.environ.get('ORIGIN')}";
      {open(script_dir / 'src/scripts/utilities.js', 'r').read()}
      {open(script_dir / 'src/scripts/FormController.js', 'r').read()}
    </script>

    <!-- Paste this into WordPress: END -->
  
  </body>
</html>"""

# Create dist directory relative to script location
dist_dir = script_dir / "dist"
os.makedirs(dist_dir, exist_ok=True)

with open(dist_dir / "index.html", "w") as f:
    f.write(donation_form_html)

origin = os.environ.get('ORIGIN', '')
if 'localhost' in origin:
    print("DEVELOPMENT build complete")
else:
    print("PRODUCTION build complete")
