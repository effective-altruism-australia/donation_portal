// We're using Shadow DOM to isolate this donation form's design from WordPress's CSS
const host = document.querySelector("#donation-form-host");
const shadow = host.attachShadow({ mode: "open" });
const template = document.getElementById("donation-form");
shadow.appendChild(template.content);

class FormController {
  #donationFrequency = "one-time";
  #donorCountry = "Australia";
  #donorEmail;
  #donorFirstName;
  #donorLastName;
  #donorPostcode;
  #paymentMethod = "credit-card";
  #showThankYouMessage;
  #subscribeToCommunity = false;
  #subscribeToNewsletter = false;
  #subscribeToUpdates = true;
  #stripe;
  #howDidYouHearAboutUs = "";
  #eaaeAmount = 0;
  #eaaeOpsAmount = 0;

  constructor() {
    // Get url parameters
    const urlParams = new URLSearchParams(window.location.search);
    this.#showThankYouMessage = urlParams.get("thankyou") === "";

    // Initialise Stripe
    this.#stripe = window.Stripe(STRIPE_API_KEY_EAAE);

    // Decide which form to build based on the url params
    if (this.#showThankYouMessage) {
      new ThankyouSection();
    } else {
      this.#renderEaaeForm();
    }
  }

  async #renderEaaeForm() {
    new DonationFrequencySection();
    new TotalAmountSection();
    new PersonalDetailsSection();
    new CommunicationsSection();
    new PaymentMethodSection();
    new DonateButtonSection();
    new SpecificAllocationSection();
  }

  setDonationFrequency(frequency) {
    this.#donationFrequency = frequency;
    this.updateTotalAmountSection();
  }

  getDonationFrequency() {
    return this.#donationFrequency;
  }

  setEaaeAmount(amount) {
    this.#eaaeAmount = +amount;
    this.updateTotalAmountSection();
  }

  setEaaeOpsAmount(amount) {
    this.#eaaeOpsAmount = +amount;
    this.updateTotalAmountSection();
  }

  updateTotalAmountSection() {
    TotalAmountSection.render({
      eaaeAmount: this.#eaaeAmount,
      eaaeOpsAmount: this.#eaaeOpsAmount,
    });
  }

  setPaymentMethod(method) {
    this.#paymentMethod = method;
  }

  setDonorFirstName(firstName) {
    this.#donorFirstName = firstName;
  }

  setDonorLastName(lastName) {
    this.#donorLastName = lastName;
  }

  setDonorEmail(email) {
    this.#donorEmail = email;
  }

  setDonorPostcode(postcode) {
    this.#donorPostcode = postcode;
  }

  setDonorCountry(country) {
    this.#donorCountry = country;
  }

  setSubscribeToUpdates(subscribe) {
    this.#subscribeToUpdates = subscribe;
  }

  setSubscribeToNewsletter(subscribe) {
    this.#subscribeToNewsletter = subscribe;
  }

  setSubscribeToCommunity(subscribe) {
    this.#subscribeToCommunity = subscribe;
  }

  setHowDidYouHearAboutUs(howDidYouHearAboutUs) {
    this.#howDidYouHearAboutUs = howDidYouHearAboutUs;
  }

  handleFormSubmit() {
    if (this.#eaaeAmount + this.#eaaeOpsAmount < 2) {
      alert("Please allocate at least $2 across the options provided.");
      $("#specific-allocation-section").focus();
      return false;
    }

    $("#loader").style.display = "block";

    let formData = this.#buildFormData();
    console.log(formData);
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    };
    fetch(ORIGIN + "/pledge_new/", requestOptions)
      .then((response) => response.json())
      .then(async (data) => {
        this.#handleFormSubmitResponse(data, formData);
      });
    return false;
  }

  #handleFormSubmitResponse(data, formData) {
    $("#loader").style.display = "none";
    if (data.bank_reference) {
      this.#renderBankTransferInstructions(formData, data);
    } else if (data.id) {
      this.#stripe.redirectToCheckout({ sessionId: data.id });
    } else {
      $("form").innerText =
        "Error submitting form. Please try again. If this problem persists, please email info@eaa.org.au.";
    }
  }

  #renderBankTransferInstructions(formData, data) {
    new BankInstructionsSection({
      firstName: formData.first_name,
      bankReference: data.bank_reference,
      recurring: formData.recurring,
      eaaeAmount: this.#eaaeAmount,
      eaaeOpsAmount: this.#eaaeOpsAmount,
    });
    hide("#payment-method-section");
    hide("#specific-allocation-section");
    hide("#total-amount-section");
    hide("#communications-section");
    hide("#personal-details-section");
    hide("#donation-frequency-section");
    hide("#thankyou-section");
    hide("#donate-button-section");
  }

  #buildFormData() {
    let formData = {
      payment_method: this.#paymentMethod,
      recurring_frequency: this.#donationFrequency,
      recurring: this.#donationFrequency === "monthly" ? true : false,
      first_name: this.#donorFirstName,
      last_name: this.#donorLastName,
      email: this.#donorEmail,
      subscribe_to_updates: this.#subscribeToUpdates,
      subscribe_to_newsletter: this.#subscribeToNewsletter,
      connect_to_community: this.#subscribeToCommunity,
      how_did_you_hear_about_us_db:
        this.#howDidYouHearAboutUs === ""
          ? undefined
          : this.#howDidYouHearAboutUs,
      postcode: this.#donorPostcode,
      country: this.#donorCountry,
      is_gift: undefined,
    };
    formData = this.#addSpecificAllocationFormData(formData);
    return formData;
  }

  #addSpecificAllocationFormData(formData) {
    let totalForms = 0;
    if (this.#eaaeAmount > 0) {
      formData[`form-${totalForms}-id`] = null;
      formData[`form-${totalForms}-amount`] = this.#eaaeAmount;
      formData[`form-${totalForms}-partner_charity`] = "eaae";
      totalForms++;
    }
    if (this.#eaaeOpsAmount > 0) {
      formData[`form-${totalForms}-id`] = null;
      formData[`form-${totalForms}-amount`] = this.#eaaeOpsAmount;
      formData[`form-${totalForms}-partner_charity`] = "eaae-operations";
      totalForms++;
    }
    formData["form-TOTAL_FORMS"] = totalForms;
    formData["form-INITIAL_FORMS"] = 0;
    return formData;
  }
}

const formController = new FormController();
