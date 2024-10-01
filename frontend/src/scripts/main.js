// Use Shadow DOM to isolate this donation form's design from WordPress's CSS
const host = document.querySelector("#donation-form-host");
const shadow = host.attachShadow({ mode: "open" });
const template = document.getElementById("donation-form");
shadow.appendChild(template.content);

// Get url parameters
const urlParams = new URLSearchParams(window.location.search);
const thankyou = urlParams.get("thankyou") === "";
const specificCharity = urlParams.get("charity");

// Initialise Stripe
let stripe;
if (specificCharity === "eaae") {
  stripe = window.Stripe(STRIPE_API_KEY_EAAE);
} else {
  stripe = window.Stripe(STRIPE_API_KEY_EAA);
}

// Decide which form to build based on the url params
if (thankyou) {
  showBlock("#thank-you-message");
} else if (specificCharity === "eaae") {
  renderEaaeForm();
} else if (specificCharity) {
  renderSpecificCharityForm();
} else {
  renderStandardForm();
}

function renderEaaeForm() {
  fetch(ORIGIN + "/partner_charities")
    .then((response) => response.json())
    .then((data) => buildSpecificCharitySection(data));
  showBlock("#donation-frequency-section");
  showBlock("#specific-charity-section");
  showBlock("#amount-section");
  showBlock("#personal-details-section");
  showBlock("#communications-section");
  showBlock("#payment-method-section");
  showBlock("#gift-section");
  showBlock("#donate-button-section");
}

function renderSpecificCharityForm() {
  fetch(ORIGIN + "/partner_charities")
    .then((response) => response.json())
    .then((data) => buildSpecificCharitySection(data));
  showBlock("#donation-frequency-section");
  showBlock("#specific-charity-section");
  showBlock("#amount-section");
  showBlock("#personal-details-section");
  showBlock("#communications-section");
  showBlock("#payment-method-section");
  showBlock("#gift-section");
  showBlock("#donate-button-section");
}

function renderStandardForm() {
  fetch(ORIGIN + "/partner_charities")
    .then((response) => response.json())
    .then((data) => buildCustomAllocationSection(data));
  showBlock("#donation-frequency-section");
  showBlock("#allocation-section");
  showBlock("#amount-section");
  showBlock("#personal-details-section");
  showBlock("#communications-section");
  showBlock("#payment-method-section");
  showBlock("#gift-section");
  showBlock("#donate-button-section");
}

// function handleFormSubmit() {
//   $("form").style.opacity = 0.5;
//   $("form")
//     .querySelectorAll("*")
//     .forEach((element) => {
//       element.disabled = true;
//     });
//   let formData = {
//     payment_method: $("#credit-card").checked ? "credit-card" : "bank-transfer",
//     recurring_frequency: $("#monthly").checked ? "monthly" : "one-time",
//     recurring: $("#monthly").checked ? true : false,
//     first_name: $("#first-name").value,
//     last_name: $("#last-name").value,
//     email: $("#email").value,
//     subscribe_to_updates: $("#subscribe-to-updates").checked,
//     subscribe_to_newsletter: $("#subscribe-to-newsletter").checked,
//     connect_to_community: $("#connect-to-community").checked,
//     how_did_you_hear_about_us_db: $("#referral-sources").value,
//     "form-TOTAL_FORMS": 1,
//     "form-INITIAL_FORMS": 1,
//     "form-0-id": null, // dynamically add charities in this format
//     "form-0-partner_charity": "unallocated",
//     "form-0-amount": "25",
//   };
//   fetch(ORIGIN + "/pledge_new/", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify(formData),
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       stripe.redirectToCheckout({ sessionId: data.id });
//     });
//   return false;
// }
