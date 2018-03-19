import React, {Component} from 'react';
import {RadioGroup, Radio} from 'react-radio-group'
import './App.css';


// TODO: these need to come from an AJAX call to the server
const charities = [
  {
    name: "Schistosomiasis Control Initiative",
    blurb: "Schistosomiasis Control Initiative supports programs that work to eliminate debilitating neglected tropical diseases in Africa",
    logo: "//donations.effectivealtruism.org.au/static/thumbnails/logo_sci.jpg",
  },
  {
    name: "Deworm the World",
    blurb: <span><b>Deworm the World</b> supports programs that work to eliminate debilitating neglected
      tropical diseases in Africa</span>,
    logo: "//donations.effectivealtruism.org.au/static/thumbnails/logo_evidenceaction.gif",
  },
  {
    name: "Against Malaria Foundation",
    blurb: <span><b>Against Malaria Foundation</b> provides long-lasting insecticidal nets to populations
      at high risk of malaria, primarily in Africa.</span>,
    logo: "//donations.effectivealtruism.org.au/static/thumbnails/logo_amf.jpg",
  },
];


// TODO: Some charities are listed as choices but the portal can't donate to them.
// TODO: This should probably be a flag on the above `charities` data, and the text can
// TODO: be generated rather than listed like this.
const charityOverrides = {
  "Against Malaria Foundation": {
    directDonationOnly: <p className="donation-info">
      Donations to the Against Malaria Foundation are tax deductible in Australia.
      We prefer that you donate to the Against Malaria Foundation directly at&nbsp;
      <a href='//www.againstmalaria.com/Donation.aspx?GroupID=86' target="_blank" rel="noopener noreferrer">
        https://www.againstmalaria.com/Donation.aspx?GroupID=86
      </a>.
    </p>
  }
};


// TODO: these should be the real referral sources, and probably should come
// TODO: from an AJAX call to the server. At the time of writing, the real
// TODO: referrals are:
//   The Life You Can Save / News / Advertising / GiveWell / From the charity (SCI, Evidence Action, GiveDirectly)
//   Search engine (Google etc.) / Friend / Giving What We Can / Anushka &amp; David's Wedding

const referralSources = [
  {value: "refone", label: "RefOne"},
  {value: "reftwo", label: "RefTwo"},
];


function Error(props) {
  return props.visible ? <div className="error-text">{props.children}</div> : null;
}


class CharityChoice extends Component {
  render() {
    return (
        <div className="charity">
          <div className="charity-info">
            <img className="charity-img" src={this.props.charity.logo} alt={this.props.charity.name}/>
            <span className="charity-title">{this.props.charity.name}</span>
          </div>
          <div className="hover-overlay">
            <a className="charity-details charityClick" href="" onClick={this.props.onClick}>
              {this.props.charity.blurb}
            </a>
          </div>
        </div>
    )
  }
}


class CharityChooser extends Component {
  render() {
    return (
      <div className="donation-page-header">
        <h1 className="page-title">Select a program to support</h1>
        <div className="donation-progress">
          <div className="progress-step current-step">1</div>
          <div className="progress-step">2</div>
        </div>

        <div className="donation-step" id="step-1">
          <h2>100% of your donation will be granted to the charity of your choice</h2>
          <h3>Select a charity:</h3>
          <div className="charities-container">
            {charities.map((charity) =>
              <CharityChoice
                  key={charity.name}
                  onClick={(event) => {
                    event.preventDefault();
                    this.props.setCharity(charity)
                  }}
                  charity={charity}
              />
            )}

          </div>
        </div>
      </div>
    )
  }
}


class DonationFrequency extends Component {
  render() {
    return (
      <div>
        <h3>How often will you be donating?
          <span className='todo'>{this.props.frequency}</span>
        </h3>
        <RadioGroup name="frequency" selectedValue={this.props.frequency} onChange={this.props.pushUp}>
          <Radio value="one-time" id="id-freq-one-time"/><label htmlFor="id-freq-one-time" className="btn btn-default">One-Time</label>
          <Radio value="monthly" id="id-freq-monthly"/><label htmlFor="id-freq-monthly" className="btn btn-default">Monthly</label>
        </RadioGroup>
        <Error visible={!this.props.frequency}>Please choose a donation frequency.</Error>
      </div>
    );
  }
}


class DonationAmount extends Component {
  constructor(props) {
    super(props);
    this.isValidAmount = this.isValidAmount.bind(this);
    this.otherChange = this.otherChange.bind(this);
    this.showOther = this.showOther.bind(this);
  }

  isValidAmount() {
    return this.props.amount && this.props.amount.value && !isNaN(parseFloat(this.props.amount.value));
  }

  otherChange(event) {
    const value = parseFloat(event.target.value);
    this.props.useOtherAmount(value);
    event.preventDefault();
  }

  showOther() {
    return this.props.amount.preset === 'other';
  }

  render() {
    let error = <Error visible={!this.isValidAmount()}>Please choose a donation amount.</Error>
    let other = this.showOther() ?
      <input type="number"
             value={isNaN(this.props.amount.value) ? '' : this.props.amount.value}
             onChange={this.otherChange}
      /> : null;

    return (
      <div>
        <h3>How much would you like to donate? <span className='todo'>{JSON.stringify(this.props.amount)}</span></h3>
        <RadioGroup name="amount"
                    selectedValue={this.props.amount.preset}
                    onChange={this.props.usePresetAmount}>
          <Radio value="25"    id="id-amount-25" /><label htmlFor="id-amount-25" className="btn btn-default">$25</label>
          <Radio value="50"    id="id-amount-50" /><label htmlFor="id-amount-50" className="btn btn-default">$50</label>
          <Radio value="100"   id="id-amount-100" /><label htmlFor="id-amount-100" className="btn btn-default">$100</label>
          <Radio value="250"   id="id-amount-250" /><label htmlFor="id-amount-250" className="btn btn-default">$250</label>
          <Radio value="other" id="id-amount-other" /><label htmlFor="id-amount-other" className="btn btn-default">Other</label>
          {other}
        </RadioGroup>
        {error}
      </div>
    );
  }
}

class DonorDetails extends Component {

  render() {
    return (
      <div className="panel panel-default form-container details-section donor-details-section">
        <div className="panel-body form-horizontal">
          <legend>Donor Details</legend>
          <div className="form-group" id="form_first_name">
            <label className="control-label col-sm-3" htmlFor="id_first_name">Name</label>
            <div className="col-sm-9">
              <input className="form-control" type="text" id="id_first_name" maxLength="1024" name="first_name"
                     placeholder="Name"
                     value={this.props.details.first_name}
                     onChange={this.props.handleInputChange}/>
            </div>
          </div>

          <div className="form-group" id="form_email">
            <label className="control-label col-sm-3" htmlFor="id_email">Email</label>
            <div className="col-sm-9">
              <input className="form-control" type="email" id="id_email" maxLength="254" name="email"
                     placeholder="Email"
                     value={this.props.details.email}
                     onChange={this.props.handleInputChange}/>
            </div>
          </div>

          <div className="form-group">
            <label className="control-label col-sm-3 long-control-label" htmlFor="id_how_did_you_hear_about_us_db">
              How did you hear about us?</label>
            <div className="col-sm-9">
              <select className="form-control" id="id_how_did_you_hear_about_us_db"
                      name="how_did_you_hear_about_us_db"
                      value={this.props.details.how_did_you_hear_about_us_db}
                      onChange={this.props.handleInputChange}>
                <option value="" disabled>---------</option>
                { referralSources.map(source =>
                    <option key={source.label} value={source.value}>{source.label}</option>
                )}
              </select>
            </div>
          </div>

          <div className="form-group" id="id_formgroup_subscribe">
            <div className="checkbox col-sm-offset-3">
              <label htmlFor="id_subscribe">
                <input type="checkbox"
                       id="id_subscribe"
                       name="subscribe_to_updates"
                       checked={this.props.details.subscribe_to_updates}
                       onChange={this.props.handleInputChange}
                />
                Send me news and updates</label>
            </div>
          </div>
        </div>
        {/*<div><pre>{JSON.stringify(this.props.details, null, 2)}</pre></div>*/}
      </div>
    )
  }
}

class PaymentMethod extends Component {

  render() { return (
    <div className="payment-type form-group">
      <label className="control-label col-sm-3">Payment Method</label>
      <div className="col-sm-9">
        <RadioGroup name="paymentMethod"
                    selectedValue={this.props.paymentMethod}
                    onChange={this.props.setPaymentMethod}>
          <Radio value="credit-card" id="id-credit-card"/><label htmlFor="id-credit-card" className="btn btn-default">Credit Card</label>
          <Radio value="bank-transfer" id="id-bank-transfer"/><label htmlFor="id-bank-transfer" className="btn btn-default">Bank Transfer</label>
        </RadioGroup>
      </div>
    </div>
  )}
}


/*
 * TODO: Card payment is NOT implemented fully.
 * TODO: Recommend NOT building this out until using a pre-built Stripe form is
 * TODO: considered in detail. No point building this if Stripe does it all already.
 */
class CardPaymentDetails extends Component {
  constructor(props) {
    super(props);
    this.state = {
      focused: '',
      cardName: '',
      cardNumber: '',
      cardExpiry: '',
      cardCVC: '',
      cardAddress: '',
      cardAddress2: '',
      cardCity: '',
      cardState: '',
      cardPostcode: '',
      cardCountry: '',
    }
  }

  // with thanks to https://github.com/amarofashion/react-credit-cards/blob/master/demo/component.jsx

  componentDidMount() {
    // Payment.formatCardNumber(document.querySelector('[name="number"]'));
    // Payment.formatCardExpiry(document.querySelector('[name="expiry"]'));
    // Payment.formatCardCVC(document.querySelector('[name="cvc"]'));
  }

  handleInputFocus = ({ target }) => {
    this.setState({
      focused: target.name,
    });
  };

  handleInputChange = ({ target }) => {
    if (target.name === 'number') {
      this.setState({
        [target.name]: target.value.replace(/ /g, ''),
      });
    }
    else if (target.name === 'expiry') {
      this.setState({
        [target.name]: target.value.replace(/ |\//g, ''),
      });
    }
    else {
      this.setState({
        [target.name]: target.value,
      });
    }
  };

  handleCallback(type, isValid) {
    console.log(type, isValid); //eslint-disable-line no-console
  }

  render() {
    const { focused, name, number, expiry, cvc, address, address2, city, state, postcode, country } = this.state;
    return (
    <div className="payment-subsection" id="id_credit_card">
      <fieldset id="pin_credit_card_details">
        <div className="form-group">
          <label className="control-label labels col-sm-3" htmlFor="cc-name">Name on card</label>
          <div className="col-sm-9">
            <input className="form-control cc-form"
                   type="text" name="cardName"
                   id="cc-name"
                   placeholder="Full name"
                   value={name}
                   onKeyUp={this.handleInputChange}
                   onFocus={this.handleInputFocus}
            />
          </div>
        </div>
        <div className="form-group DEL-TODO-has-error">
          <label className="control-label labels col-sm-3" htmlFor="cc-number">Card number</label>
          <div className="col-sm-9">
            <div className="input-group">
              <input className="form-control cc-form unknown"
                     name="cardNumber"
                     type="tel"
                     id="cc-number"
                     placeholder="Card Number"
                     autoComplete="cc-number"
                     value=""
              />
              <span className="input-group-addon"><span className="glyphicon glyphicon-lock"></span></span>
            </div>
            {/*<label className="error" htmlFor="cc-number">Please enter a valid credit card number.</label>*/}
          </div>
        </div>
        <div className="multi-form-group">
          <div className="form-group col-sm-7">
            <label className="control-label labels col-sm-3" htmlFor="cc-expiry">
              <span className="hidden-xs">Expiration</span>
              <span className="visible-xs-inline">Exp</span> date
            </label>
            <div className="col-sm-4">
              <input className="form-control cc-form" name="cardExpiry" type="tel" id="cc-expiry" placeholder="MM / YY" autoComplete="cc-exp" value=""/>
            </div>
          </div>
          <div className="form-group col-sm-5">
            <label className="control-label labels col-sm-3" htmlFor="cc-cvc">CV code</label>
            <div className="col-sm-2">
              <input className="form-control cc-form" name="cardCVC" type="text" id="cc-cvc" placeholder="CVC" autoComplete="cc-csc" value=""/>
            </div>
          </div>
        </div>
        <div className="form-group">
          <label className="control-label labels col-sm-3" htmlFor="address-line1">Billing Address</label>
          <div className="col-sm-9">
            <input className="form-control cc-form" type="text" id="address-line1" name="cardAddress" placeholder="Address Line 1" required="" aria-required="true" value=""/>
          </div>
        </div>
        <div className="form-group">
          <label className="control-label sr-only labels" hidden="" aria-hidden="true" htmlFor="address-line2">Billing Address line 2</label>
          <div className="col-sm-9 col-sm-offset-3">
            <input className="form-control cc-form" type="text" id="address-line2" name="cardAddress2" placeholder="Address Line 2" value=""/>
          </div>
        </div>
        <div className="multi-form-group">
          <div className="form-group col-sm-6">
            <label className="control-label labels col-sm-3 visible-xs" htmlFor="address-city">City</label>
            <div className="col-sm-3 col-sm-offset-3">
              <input className="form-control cc-form" type="text" id="address-city" name="cardCity" placeholder="City" required="" aria-required="true" value=""/>
            </div>
          </div>
          <div className="form-group col-sm-3">
            <label className="control-label labels col-sm-3 visible-xs" htmlFor="address-state">State</label>
            <div className="col-sm-3">
              <input className="form-control cc-form" type="text" id="address-state" name="cardState" placeholder="State" value=""/>
            </div>
          </div>
          <div className="form-group col-sm-3">
            <label className="control-label labels col-sm-3 visible-xs" htmlFor="address-postcode">Postcode</label>
            <div className="col-sm-3">
              <input className="form-control cc-form" type="text" id="address-postcode" name="cardPostcode" placeholder="Postal Code" value=""/>
            </div>
          </div>
        </div>
        <div className="form-group">
          <label className="control-label labels col-sm-3" htmlFor="address-country">Country</label>
          <div className="col-sm-9">
            <input className="form-control cc-form" type="text" id="address-country" name="cardCountry" placeholder="Country" required="" aria-required="true" value=""/>
          </div>
        </div>
      </fieldset>
    </div>
  )}
}

class DonationSubmit extends Component {
  render() { return (
    <div className="form-actions">
      <button type="submit" className="btn btn-success btn-lg" onClick={this.onSubmit}>Donate</button>
    </div>
  )}
}

function DonationFaq(props) { return (
  <div className="details-section payment-faq">
    <h2>Donation FAQ</h2>
    <p className="payment-faq-question">
      What credit cards do you accept?
    </p>
    <p className="payment-faq-answer">
      We accept Visa and Mastercard. Sorry, we do not accept American Express at this time.
    </p>
    <p className="payment-faq-question">
      Are credit card donations secure?
    </p>
    <p className="payment-faq-answer">
      Yes. Your credit card details are encrypted and submitted directly from your web browser to our
      payment processor, Pin Payments (ABN: 46 154 451 582). Our accounting staff only have access to
      the last 4 digits of your credit card number.
    </p>
    <p className="payment-faq-question">
      How much does it cost you to process a donation?
    </p>
    <p className="payment-faq-answer">
      Credit card donations cost us 1.4% plus 30c per donation. Bank transfers have no fees.
    </p>
    <p className="payment-faq-question">
      Which payment method do you prefer?
    </p>
    <p className="payment-faq-answer">
      We suggest that you use whichever payment method is most convenient for you.
      For major donations (over $2,000), we prefer that you donate via bank transfer to reduce fees.
    </p>
    <p className="payment-faq-question">
      When will I get a receipt?
    </p>
    <p className="payment-faq-answer">
      For credit card donations, we will email you a receipt immediately after your donation.
      For bank transfers, we will email you a receipt on the day the money is received by us,
      which is usually one or two business days after you send it.
    </p>
  </div>
)}


class PaymentWizard extends Component {
  constructor(props) {
    super(props);
    this.usePresetAmount = this.usePresetAmount.bind(this);
    this.useOtherAmount = this.useOtherAmount.bind(this);
    this.chooseDifferentCharity = this.chooseDifferentCharity.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
  }

  usePresetAmount(value) {
    this.props.app.setState({
      donationAmount: {
        preset: value,
        value: parseFloat(value)
      }
    });
  }

  useOtherAmount(value) {
    value = parseFloat(value);
    if (isNaN(value)) {
      value = '';
    }

    this.props.app.setState({
      donationAmount: {
        preset: 'other',
        value: value,
      }
    });
  }

  chooseDifferentCharity(e) {
    e.preventDefault();
    this.props.app.clear();
  }

  onSubmit(e) {
    e.preventDefault();
    console.log("Pressed 'donate'", this.props.app.state)
  }

  render() {
    let paymentDetails = null;
    if (this.props.app.state.paymentMethod === 'credit-card') {
      paymentDetails = (
        <CardPaymentDetails/>
      )
    } else {
      paymentDetails = (
        <div className="payment-subsection" id="bank-transfer-instructions">
          <p>After you submit this form, we will give you our account details and a unique reference number.</p>
          <p>You then need to log in to your bank and make a bank transfer using these details.</p>
        </div>
      )
    }

    return (
      <div>
        <h1>Payment</h1>
        <h2>You have chosen {this.props.app.state.chosenCharity.name}</h2>
        <button className="btn" onClick={this.chooseDifferentCharity}>Choose a different program</button>
        <DonationFrequency
            frequency={this.props.app.state.donationFrequency}
            pushUp={(value) => this.props.app.setState({donationFrequency: value})}
        />
        <DonationAmount
            amount={this.props.app.state.donationAmount}
            usePresetAmount={this.usePresetAmount}
            useOtherAmount={this.useOtherAmount}
            // pushUp={(amount) => this.props.app.setState({donationAmount: amount})}
            //remapp={this.props.app}
        />
        <DonorDetails
            details={this.props.app.state.donorDetails}
            handleInputChange={(event) => this.props.app.donorInputChange(event)}
        />
        <div className="panel panel-default form-container details-section payment-details-section">
          <div className="panel-body form-horizontal">
            <legend>Payment Details</legend>
            <PaymentMethod paymentMethod={this.props.app.state.paymentMethod}
                           setPaymentMethod={this.props.app.setPaymentMethod}
            />
            <div className="payment-subsections" id="id_payment_options">
              {paymentDetails}
            </div>
          </div>
        </div>
        <div>
          <p className="help-text">Having a problem donating?
            Please let us know at <a href="mailto://info@eaa.org.au">info@eaa.org.au</a>.
          </p>
          <DonationSubmit/>
        </div>
        <DonationFaq/>
      </div>
    )
  }
}

class App extends Component {
  constructor(props) {
    super(props);
    this.state = this.getInitialState();
    this.setCharity = this.setCharity.bind(this);
    this.setPaymentMethod = this.setPaymentMethod.bind(this);
  }

  getInitialState() {
    return {
      chosenCharity: null,
      //chosenCharity: charities[0],
      donationFrequency: null, // null | one-time | monthly
      donationAmount: {
        preset: null, // null | 25 | 50 | 100 | 250 | other
        value: '', // must be '' not null for the 'other' input to work
      },
      donorDetails: {
        first_name: "", // TODO rename "name"?
        email: "",
        how_did_you_hear_about_us_db: "", // TODO rename "referrer" ?
        subscribe_to_updates: false, // TODO rename "subscribe" ?
      },
      paymentMethod: 'credit-card', // credit-card | bank-transfer
      paymentCard: {
        name: null,
        number: null,
        expiration: null,
        cvc: null,
        address1: null,
        address2: null,
        city: null,
        state: null,
        postalCode: null,
        country: null,
      },
      meta: {
        submitting: null, // true immediately after submit pressed and before the result is back.
        showErrors: false, // set to true after button has been pressed.
      }
    };
  }

  setCharity(which) {
    this.setState({chosenCharity: which});
  };

  clear = () => {
    // Reset only the charity choice. If a user changes their mind, when they select another charity,
    // any data they'd already entered will be intact.
    this.setState({chosenCharity: null});

    // Reset everything back to initial state
    //this.setState(this.getInitialState());
  };

  donorInputChange(event) {
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;

    // copy current state of relevant section and modify the changed value
    const updated = {...this.state.donorDetails, [name]: value};

    this.setState({donorDetails: updated})
  }

  paymentInputChange(event) {
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;

    // copy current state of relevant section and modify the changed value
    const updated = {...this.state.payment, [name]: value};

    this.setState({payment: updated})
  }

  setPaymentMethod(which) {
    //console.log("XX", which)
    this.setState({paymentMethod: which});
  }

  render() {
    let main = null;

    // The charity chosen by the user, or null if nothing chosen yet.
    const charity = this.state.chosenCharity;

    // Some charities have an "override" message, meaning it is preferred that donors
    // send their donations directly. The `charityOverride` will be null if there is no override
    // (i.e. can donate as normal) or non-null if there is an override in place.
    const charityOverride = charity && charity.name ? charityOverrides[charity.name] : null;

    if (charityOverride) {

      main = (
          <div>
            <div>
              <button className="btn" onClick={this.clear}>Choose a different program</button>
            </div>
            <div className="row">
              <div className="col-sm-3">
                <img className="img-fluid" src={charity.logo} alt={charity.name}/>
              </div>
              <div className="col-sm-9">
                {charityOverride.directDonationOnly}
              </div>
            </div>
          </div>
      )

    } else if (charity) {
      main = (
          <PaymentWizard app={this}/>
      )

    } else {
      main = (
          <CharityChooser setCharity={this.setCharity}/>
      );
    }

    return (
        <div className="container">
          {main}
          <div>
            <pre className="fwoop">{JSON.stringify(this.state, null, 2)}</pre>
          </div>
        </div>
    );
  }
}

export default App;

/* TODO: content displayed at the end, when donation succeeds:

<div class="donation-step " id="step-3">
<div class="payment_option">
<h2>Thank you !</h2>
<p>100% of your donation will be granted to Schistosomiasis Control Initiative.</p>
<div class="complete-other-info">
<p>Here is your <a href="" download="" target="_blank">receipt</a>.
We have also emailed it to you – please check your spam folder if you have not received it.</p>
</div>
<div class="complete-other-info">
<h3>Any questions?</h3>
<p>Please email us at <a href="mailto://info@eaa.org.au">info@eaa.org.au</a> or call us on +61 3 9349 4062,
if you have any questions.
</p>
</div>
<p>Best wishes and thanks,
<br> The team at Effective Altruism Australia</p>
</div>

<div class="payment_option collapse">
<h2>Thank you !</h2>
<p>100% of your donation will be granted to Schistosomiasis Control Initiative.</p>
<div class="complete-next-steps">
<h3>What to do next?</h3>
<p>Please make sure that you complete the process by making a bank transfer of $ to:</p>
<p><strong>Account Name</strong>: Effective Altruism Australia (don't worry if it doesn't fit)
<br> <strong>BSB</strong>: 083170
<br> <strong>Account No</strong>: 306556167
<br> <strong>Unique Reference Number</strong>:  (put in the transaction description)
</p>
</div>

<div class="complete-other-info">
<h3>Receipt</h3>
<p>We will send you a tax deductible receipt once we have confirmed the bank transfer.</p>
<h3>Any questions?</h3>
<p>Please email us at <a href="mailto://info@eaa.org.au">info@eaa.org.au</a> or call us on +61 3 9349 4062,
if you have any questions.</p>
</div>
<div class="complete-other-info">
<p>We have also emailed you these instructions – please check your spam folder if you have not received them.
</p></div>
<p>Best wishes and thanks,
<br> The team at Effective Altruism Australia
</p></div></div>

 */