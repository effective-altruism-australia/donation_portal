// Set up shadow DOM to protect donation form from WordPress CSS
const host = document.querySelector("#donation-form-host");
const shadow = host.attachShadow({ mode: "open" });
const template = document.getElementById("donation-form");
shadow.appendChild(template.content);

// Initialise Stripe
let stripe;
if (window.location.search.includes("eaae")) {
  stripe = window.Stripe(STRIPE_API_KEY_EAAE);
} else {
  stripe = window.Stripe(STRIPE_API_KEY_EAA);
}

// Show and hide sections based on the url
if (window.location.search.includes("thankyou")) {
  showBlock("thank-you-message");
} else {
  showBlock("donation-form");
}

// Initialise form state based on what's checked
if ($("custom-allocation").checked) {
  showBlock("custom-allocation-section");
  hide("default-allocation-section");
} else {
  hide("custom-allocation-section");
  showBlock("default-allocation-section");
}

if ($("gift").checked) {
  showFlex("gift-section");
} else {
  hide("gift-section");
}

if ($("bank-transfer").checked) {
  showBlock("bank-details-section");
} else {
  hide("bank-details-section");
}

function showGiftSection() {
  showFlex("gift-section");
  $("gift-section").disabled = false;
  $("recipient-name").setAttribute("required", "true");
  $("recipient-email").setAttribute("required", "true");
}

function hideGiftSection() {
  hide("gift-section");
  $("gift-section").disabled = true;
  $("recipient-name").setAttribute("required", "false");
  $("recipient-email").setAttribute("required", "false");
}

// Fetch partner charities and referral sources lists
fetch(ORIGIN + "/partner_charities")
  .then((response) => response.json())
  .then((data) => buildCustomAllocationSection(data));
fetch(ORIGIN + "/referral_sources")
  .then((response) => response.json())
  .then((data) => buildReferralSourcesList(data));

function buildCustomAllocationSection(partnerCharities) {
  let customAllocationSectionHTML = `<h2 class="text-lg mt-8">How would you like to allocate your donation?</h2>`;

  partnerCharities.forEach((charity) => {
    customAllocationSectionHTML += `
    <div class="flex" style="justify-content: space-between;">
      <label for="${charity.id}">${charity.name}</label>
      <input
        type="text"
        inputmode="numeric"
        id="${charity.id}-amount"
        name="${charity.id}-amount"
        class="block"
      />
    </div>
    `;
  });
  customAllocationSectionHTML += "<div id='total'></div>";
  $("custom-allocation-section").innerHTML = customAllocationSectionHTML;
}

function buildReferralSourcesList(referralSources) {
  console.log(referralSources);
  let referralSourcesListHTML = "";

  referralSources.forEach((referralSource) => {
    referralSourcesListHTML += `<option value="${referralSource.value}">${referralSource.label}</option>`;
  });

  $("referral-sources").innerHTML = referralSourcesListHTML;
}

function handleFormSubmit() {
  $("donation-form").style.opacity = 0.5;
  $("donation-form")
    .querySelectorAll("*")
    .forEach((element) => {
      element.disabled = true;
    });
  let formData = {
    payment_method: $("credit-card").checked ? "credit-card" : "bank-transfer",
    recurring_frequency: $("monthly").checked ? "monthly" : "one-time",
    recurring: $("monthly").checked ? true : false,
    first_name: $("first-name").value,
    last_name: $("last-name").value,
    email: $("email").value,
    subscribe_to_updates: $("subscribe-to-updates").checked,
    subscribe_to_newsletter: $("subscribe-to-newsletter").checked,
    connect_to_community: $("connect-to-community").checked,
    how_did_you_hear_about_us_db: $("referral-sources").value,
    "form-TOTAL_FORMS": 1,
    "form-INITIAL_FORMS": 1,
    "form-0-id": null, // dynamically add charities in this format
    "form-0-partner_charity": "unallocated",
    "form-0-amount": "25",
  };
  fetch(ORIGIN + "/pledge_new/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  })
    .then((response) => response.json())
    .then((data) => {
      stripe.redirectToCheckout({ sessionId: data.id });
    });
  return false;
}
