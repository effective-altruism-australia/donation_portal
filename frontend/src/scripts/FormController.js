// We're using Shadow DOM to isolate this donation form's design from WordPress's CSS
const host = document.querySelector("#donation-form-host");
const shadow = host.attachShadow({ mode: "open" });
const template = document.getElementById("donation-form");
shadow.appendChild(template.content);

class FormController {
  #allocationType = "default"; // default, specific, direct-link
  #directLinkCharity;
  #directLinkCharityDetails;
  #donationFrequency = "one-time";
  #donorCountry;
  #donorEmail;
  #donorFirstName;
  #donorLastName;
  #donorPostcode;
  #isFestiveGift = false;
  #partnerCharities = [];
  #paymentMethod = "credit-card";
  #showThankYouMessage;
  #subscribeToCommunity = false;
  #subscribeToNewsletter = false;
  #subscribeToUpdates = true;
  #tipSize = 10;
  #tipType = "percentage";
  #tipDollarAmount = 0;
  #stripe;
  #howDidYouHearAboutUs = "";
  #basicDonationAmount = 0;
  #specificAllocations = {};

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
      new ThankyouSection();
    } else if (this.#directLinkCharity === "eaae") {
      this.#renderEaaeForm();
    } else if (this.#directLinkCharity) {
      this.#allocationType = "direct-link";
      this.#renderDirectLinkCharityForm();
    } else {
      this.#renderStandardForm();
    }
  }

  #renderEaaeForm() {
    $("form").innerText = "EAAE Not yet implemented";
  }

  async #renderDirectLinkCharityForm() {
    new AmountSection();
    new AmplifyImpactSection();
    new TotalAmountSection();
    new PersonalDetailsSection();
    new CommunicationsSection();
    new PaymentMethodSection();
    new FestiveGiftSection();
    new DonateButtonSection();
    new DonationFrequencySection();

    const response = await fetch(ORIGIN + "/partner_charities");
    this.#partnerCharities = await response.json();
    this.#partnerCharities.forEach((charity) => {
      this.#specificAllocations[charity.slug_id] = 0;
    });
    this.#directLinkCharityDetails = this.#partnerCharities.find(
      (charity) => charity.slug_id === this.#directLinkCharity
    );
    if (!this.#directLinkCharityDetails) {
      new ErrorSection();
      return;
    }
    new DirectLinkCharitySection(this.#directLinkCharityDetails);
  }

  async #renderStandardForm() {
    new DonationFrequencySection();
    new AllocationSection();
    new AmountSection();
    new AmplifyImpactSection();
    new TotalAmountSection();
    new PersonalDetailsSection();
    new CommunicationsSection();
    new PaymentMethodSection();
    new FestiveGiftSection();
    new DonateButtonSection();

    const response = await fetch(ORIGIN + "/partner_charities");
    this.#partnerCharities = await response.json();
    this.#partnerCharities = this.#partnerCharities.filter(
      (charity) => charity.slug_id !== "eaa-amplify"
    );
    this.#partnerCharities.forEach((charity) => {
      this.#specificAllocations[charity.slug_id] = 0;
    });

    new SpecificAllocationSection(this.#partnerCharities);
  }

  setDonationFrequency(frequency) {
    this.#donationFrequency = frequency;
    this.updateTotalAmountSection();
  }

  getDonationFrequency() {
    return this.#donationFrequency;
  }

  setAllocationType(type) {
    this.#allocationType = type;
    if (this.#allocationType === "specific") {
      AmountSection.hide();
      SpecificAllocationSection.show();
    } else {
      SpecificAllocationSection.hide();
      AmountSection.show();
    }
    this.updateTipDollarAmount();
    this.updateTotalAmountSection();
  }

  setBasicDonationAmount(amount) {
    this.#basicDonationAmount = +amount;
    this.updateTipDollarAmount();
    this.updateTotalAmountSection();
  }

  setCharityAllocation(charity, amount) {
    this.#specificAllocations[charity] = amount;
    this.updateTipDollarAmount();
    this.updateTotalAmountSection();
  }

  setTipValues(amount, type) {
    this.#tipType = type;
    this.#tipSize = +amount;
    this.updateTipDollarAmount();
    this.updateTotalAmountSection();
  }

  #getSpecificAllocationsTotal() {
    let total = 0;
    Object.values(this.#specificAllocations).forEach((amount) => {
      total += +amount;
    });
    return total;
  }

  updateTipDollarAmount() {
    const totalDonationAmount =
      this.#allocationType === "specific"
        ? this.#getSpecificAllocationsTotal()
        : this.#basicDonationAmount;
    if (this.#tipType === "percentage") {
      this.#tipDollarAmount = +totalDonationAmount * (this.#tipSize / 100);
    } else if (this.#tipType === "dollar") {
      this.#tipDollarAmount = this.#tipSize;
    }
  }

  updateTotalAmountSection() {
    TotalAmountSection.render({
      allocationType: this.#allocationType,
      basicDonationAmount: this.#basicDonationAmount,
      specificAllocations: this.#specificAllocations,
      tipType: this.#tipType,
      tipSize: this.#tipSize,
      tipDollarAmount: this.#tipDollarAmount,
    });
  }

  setPaymentMethod(method) {
    this.#paymentMethod = method;
  }

  getPartnerCharities() {
    return this.#partnerCharities;
  }

  setIsFestiveGift(isFestiveGift) {
    this.#isFestiveGift = isFestiveGift;
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
    if (
      this.#allocationType === "specific" &&
      this.#getSpecificAllocationsTotal() + this.#tipDollarAmount < 2
    ) {
      alert("Please allocate at least $2 across your preferred charities.");
      $("#allocation-section--specific-allocation").focus();
      return false;
    }

    if (
      (this.#allocationType === "direct-link" ||
        this.#allocationType === "default") &&
      this.#basicDonationAmount + this.#tipDollarAmount < 2
    ) {
      alert("Please select an amount of at least $2.");
      $("#amount-section--custom-amount-input").focus();
      return false;
    }

    $("#loader").style.display = "block";

    let formData = this.#buildFormData();
    fetch(ORIGIN + "/pledge_new/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then(async (data) => {
        const result = await FestiveGiftSection.generateAndSendCard({
          paymentReference: data,
          isFestiveGift: this.#isFestiveGift,
          donorName: this.#donorFirstName,
          donorEmail: this.#donorEmail,
          allocationType: this.#allocationType,
          basicDonationAmount: this.#basicDonationAmount,
          specificAllocations: this.#specificAllocations,
          directLinkCharity: this.#directLinkCharity,
        });
        $("#loader").style.display = "none";
        if (result === "error") {
          return;
        } else {
          this.#handleFormSubmitResponse(data, formData);
        }
      });
    return false;
  }

  #handleFormSubmitResponse(data, formData) {
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
      allocationType: this.#allocationType,
      firstName: formData.first_name,
      bankReference: data.bank_reference,
      recurring: formData.recurring,
      basicDonationAmount: this.#basicDonationAmount,
      tipDollarAmount: this.#tipDollarAmount,
      specificAllocationsTotal: this.#getSpecificAllocationsTotal(),
      directLinkCharityDetails: this.#directLinkCharityDetails,
    });
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
      how_did_you_hear_about_us_db: this.#howDidYouHearAboutUs,
      postcode: this.#donorPostcode,
      country: this.#donorCountry,
    };

    if (this.#allocationType === "specific") {
      formData = this.#addSpecificAllocationFormData(formData);
    } else {
      formData = this.#addStandardAllocationFormData(formData);
    }
    return formData;
  }

  #addStandardAllocationFormData(formData) {
    let totalForms = 0;
    if (this.#basicDonationAmount > 0) {
      formData[`form-${totalForms}-id`] = null;
      formData[`form-${totalForms}-amount`] =
        this.#basicDonationAmount.toString();
      formData[`form-${totalForms}-partner_charity`] =
        this.#directLinkCharity || "unallocated";
      totalForms++;
    }
    if (this.#tipDollarAmount > 0) {
      formData[`form-${totalForms}-id`] = null;
      formData[`form-${totalForms}-amount`] = this.#tipDollarAmount
        .toFixed(2)
        .toString();
      formData[`form-${totalForms}-partner_charity`] = "eaa-amplify";
      totalForms++;
    }
    formData["form-TOTAL_FORMS"] = totalForms;
    formData["form-INITIAL_FORMS"] = totalForms;
    return formData;
  }

  #addSpecificAllocationFormData(formData) {
    let totalForms = 0;
    this.#partnerCharities.forEach((charity) => {
      let amount = $(`#${charity.slug_id}-amount`).value;
      if (amount > 0) {
        formData[`form-${totalForms}-id`] = null;
        formData[`form-${totalForms}-amount`] = amount;
        formData[`form-${totalForms}-partner_charity`] = charity.slug_id;
        totalForms++;
      }
    });
    if (this.#tipDollarAmount > 0) {
      formData[`form-${totalForms}-id`] = null;
      formData[`form-${totalForms}-amount`] = this.#tipDollarAmount
        .toFixed(2)
        .toString();
      formData[`form-${totalForms}-partner_charity`] = "eaa-amplify";
      totalForms++;
    }
    formData["form-TOTAL_FORMS"] = totalForms;
    formData["form-INITIAL_FORMS"] = totalForms;
    return formData;
  }
}

const formController = new FormController();
