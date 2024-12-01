// We're using Shadow DOM to isolate this donation form's design from WordPress's CSS
const host = document.querySelector("#donation-form-host");
const shadow = host.attachShadow({ mode: "open" });
const template = document.getElementById("donation-form");
shadow.appendChild(template.content);

class FormController {
  #allocationType = "default";
  #directLinkCharity;
  #directLinkCharityDetails;
  #donationFrequency = "one-time";
  #donorCountry;
  #donorEmail;
  #donorFirstName;
  #donorLastName;
  #donorPostcode;
  #howDidYouHearAboutUs;
  #isFestiveGift = false;
  #partnerCharities = [];
  #paymentMethod;
  #showThankYouMessage;
  #subscribeToCommunity;
  #subscribeToNewsletter;
  #subscribeToUpdates;
  #tipSize = 10;
  #tipType = "percentage";
  #tipDollarAmount;
  #donationAmount = 0;
  #combinedAmount;
  #stripe;

  constructor() {
    // Get url parameters
    const urlParams = new URLSearchParams(window.location.search);
    this.#showThankYouMessage = urlParams.get("thankyou") === "";
    this.#directLinkCharity = urlParams.get("charity");

    // Initialise Stripe
    if (this.#directLinkCharity === "eaae") {
      this.#stripe = window.Stripe(STRIPE_API_KEY_EAAE);
    } else {
      this.#stripe = window.Stripe(STRIPE_API_KEY_EAA);
    }

    // Decide which form to build based on the url params
    if (this.#showThankYouMessage) {
      new ThankYouMessage();
    } else if (this.#directLinkCharity === "eaae") {
      this.#renderEaaeForm();
    } else if (this.#directLinkCharity) {
      this.#renderDirectLinkCharityForm();
    } else {
      this.#renderStandardForm();
    }
  }

  #renderEaaeForm() {
    $("form").innerText = "EAAE Not yet implemented";
  }

  #renderDirectLinkCharityForm() {
    fetch(ORIGIN + "/partner_charities")
      .then((response) => response.json())
      .then((data) => {
        this.#partnerCharities = data;
        this.#directLinkCharityDetails = partnerCharities.find(
          (charity) => charity.slug_id === directLinkCharity
        );
        buildDirectLinkCharitySection(directLinkCharityDetails);
      });
    showBlock("#donation-frequency-section");
    showBlock("#direct-link-charity-section");
    showBlock("#amount-section");
    showBlock("#amplify-impact-section");
    showBlock("#total-amount-section");
    showBlock("#personal-details-section");
    showBlock("#communications-section");
    showBlock("#payment-method-section");
    showBlock("#festive-gift-section");
    showBlock("#donate-button-section");
  }

  async #renderStandardForm() {
    const response = await fetch(ORIGIN + "/partner_charities");
    this.#partnerCharities = await response.json();

    new DonationFrequencySection();
    new AllocationSection();
    new AmountSection();
    new SpecificAllocationSection(this.#partnerCharities);
    new AmplifyImpactSection();
    new TotalAmountSection();
    new PersonalDetailsSection();
    new CommunicationsSection();
    new PaymentMethodSection();
    new FestiveGiftSection();
    new DonateButtonSection();
  }

  setAllocationType(type) {
    this.#allocationType = type;
    if (this.#allocationType === "specific") {
      SpecificAllocationSection.show();
      AmountSection.hide();
    } else {
      SpecificAllocationSection.hide();
      AmountSection.show();
    }
  }

  setDonationAmount(amount) {
    this.#donationAmount = +amount;

    if (this.#tipType === "percentage") {
      this.#tipDollarAmount = this.#donationAmount * (this.#tipSize / 100);
    } else if (this.#tipType === "dollar") {
      this.#tipDollarAmount = this.#tipSize;
    }

    this.#combinedAmount = this.#donationAmount + this.#tipDollarAmount;

    TotalAmountSection.render(
      this.#tipDollarAmount,
      this.#donationAmount,
      this.#combinedAmount
    );
  }

  setTipValues(amount, type) {
    this.#tipType = type;
    this.#tipSize = +amount;

    if (this.#tipType === "percentage") {
      this.#tipDollarAmount = this.#donationAmount * (this.#tipSize / 100);
    } else if (this.#tipType === "dollar") {
      this.#tipDollarAmount = this.#tipSize;
    }

    console.log(this.#tipSize, this.#tipType, this.#tipDollarAmount);
    this.#combinedAmount = this.#donationAmount + this.#tipDollarAmount;

    TotalAmountSection.render(
      this.#tipDollarAmount,
      this.#donationAmount,
      this.#combinedAmount
    );
  }

  setPaymentMethod(method) {
    this.#paymentMethod = method;
  }

  handleFormSubmit() {
    if (allocation === "specific") {
      if (totalAmountSpecific < 2) {
        alert("Please allocate at least $2 across your preferred charities.");
        $("#allocation-section--specific-allocation").focus();
        return false;
      }
    }

    if (allocation === "direct-link" || allocation === "default") {
      const amount = getAmount() || 0;
      if (amount < 2) {
        alert("Please select an amount of at least $2.");
        $("#custom-amount-input").focus();
        return false;
      }
    }

    $("#loader").style.display = "block";
    $("form").style.opacity = 0.5;

    let formData = buildFormData();
    fetch(ORIGIN + "/pledge_new/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then(generateAndSendFestiveCard)
      .then((data) => this.#handleFormSubmitResponse(data));
    return false;
  }

  #handleFormSubmitResponse(data) {
    $("#loader").style.display = "none";
    $("form").style.opacity = 1;

    if (data.sendCardFailed) {
      return;
    }

    if (data.bank_reference) {
      renderBankTransferInstructions(formData, data);
    } else if (data.id) {
      stripe.redirectToCheckout({ sessionId: data.id });
    } else {
      $("form").innerText =
        "Error submitting form. Please try again. If this problem persists, please email info@eaa.org.au.";
    }
  }

  #renderBankTransferInstructions(formData, data) {
    showBlock("#bank-instructions-section");
    hide("#festive-gift-section");
    hide("#payment-method-section");
    hide("#specific-allocation-section");
    hide("#amplify-impact-section");
    hide("#total-amount-section");
    hide("#communications-section");
    hide("#personal-details-section");
    hide("#amount-section");
    hide("#allocation-section");
    hide("#donation-frequency-section");
    hide("#direct-link-charity-section");
    hide("#festive-gift-section");
    hide("#thank-you-message");
    hide("#donate-button-section");
    $("#bank-instructions-name").innerText = formData.first_name;
    $("#bank-instructions-reference").innerText = data.bank_reference;

    if (formData.recurring) {
      $("#bank-instructions-frequency").innerText =
        "setting up a monthly periodic payment for";
    } else {
      $("#bank-instructions-frequency").innerText = "making a bank transfer of";
    }

    if (formData["form-0-partner_charity"] === "unallocated") {
      $("#bank-instructions-charity").innerText = "our partner charities";
      $("#bank-instructions-amount").innerText = totalAmountMostEffective;
    } else if (directLinkCharityDetails) {
      $("#bank-instructions-charity").innerText = directLinkCharityDetails.name;
      $("#bank-instructions-amount").innerText = totalAmountMostEffective;
    } else {
      $("#bank-instructions-charity").innerText =
        "your chosen partner charities";
      $("#bank-instructions-amount").innerText = totalAmountSpecific;
    }

    $("#bank-instructions-section").scrollIntoView();
  }

  #buildFormData() {
    let formData = {
      payment_method: $("#credit-card").checked
        ? "credit-card"
        : "bank-transfer",
      recurring_frequency: $("#monthly").checked ? "monthly" : "one-time",
      recurring: $("#monthly").checked ? true : false,
      first_name: $("#first-name").value,
      last_name: $("#last-name").value,
      email: $("#email").value,
      subscribe_to_updates: $("#subscribe-to-updates").checked,
      subscribe_to_newsletter: $("#subscribe-to-newsletter").checked,
      connect_to_community: $("#connect-to-community").checked,
      how_did_you_hear_about_us_db: $("#referral-sources").value,
    };

    if (directLinkCharity || $("#default-allocation").checked) {
      formData = addStandardAllocationFormData(formData);
    } else {
      formData = addSpecificAllocationFormData(formData);
    }
    return formData;
  }

  #addStandardAllocationFormData(formData) {
    const amount = getAmount();
    formData["form-0-id"] = null;
    formData["form-0-amount"] = amount.toString();
    formData["form-0-partner_charity"] = directLinkCharity || "unallocated";
    formData["form-TOTAL_FORMS"] = 1;
    formData["form-INITIAL_FORMS"] = 1;
    return formData;
  }

  #getAmount() {
    let amount = 0;
    if ($("#custom-amount-input").value !== "") {
      amount = $("#custom-amount-input").value;
    } else if ($("#donate-25").checked) {
      amount = 25;
    } else if ($("#donate-50").checked) {
      amount = 50;
    } else if ($("#donate-100").checked) {
      amount = 100;
    } else if ($("#donate-250").checked) {
      amount = 250;
    }
    totalAmountMostEffective = parseInt(amount);
    return amount;
  }

  #addSpecificAllocationFormData(formData) {
    let totalForms = 0;
    partnerCharities.forEach((charity) => {
      let amount = $(`#${charity.slug_id}-amount`).value;
      if (amount > 0) {
        formData[`form-${totalForms}-id`] = null;
        formData[`form-${totalForms}-amount`] = amount;
        formData[`form-${totalForms}-partner_charity`] = charity.slug_id;
        totalForms++;
      }
    });
    formData["form-TOTAL_FORMS"] = totalForms;
    formData["form-INITIAL_FORMS"] = totalForms;
    return formData;
  }

  async #generateAndSendFestiveCard(data) {
    if (!isFestiveGift) {
      return data;
    }

    const formData = buildFormData();

    let charity =
      formData["form-TOTAL_FORMS"] > 1
        ? "unallocated"
        : formData["form-0-partner_charity"];

    let amount = 0;
    Object.keys(formData).forEach((key) => {
      if (key.match(/form-\d+-amount/)) {
        amount += parseInt(formData[key]);
      }
    });

    const response = await fetch(
      "https://eaa-festiveseasoncards.deno.dev/api/generate-and-send-card",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          paymentReference: data.bank_reference || data.id,
          charity: charity,
          donorName: formData.first_name,
          donorEmail: formData.email,
          recipientName: $("#festive-gift-recipient-name").value,
          recipientEmail: $("#festive-gift-recipient-email").value,
          amount: String(amount),
          message: $("#festive-gift-message").value,
        }),
      }
    ).then((response) => response.json());

    if (!response.success) {
      data.sendCardFailed = true;
      alert(
        "We don't seem to be able to create a Christmas card with the details you entered. The card generator said: " +
          response.message
      );
    }

    return data;
  }
}

const formController = new FormController();
