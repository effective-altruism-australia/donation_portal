import {connect} from "react-redux";
import React, {Component} from "react";
import {getFormValues, reduxForm} from 'redux-form';
import DonorDetails from "./donor-details"
import DonationModeOptions from "./donation-mode-options"
import DonationFrequency from "./donation-frequency"
import DonationAmount from "./donation-amount"
import PaymentMethod from "./payment-detail";
import DonationFaq from "./donation-faq";
import DonationSubmit from "./donation-submit";
import DonationAsGift from "./donation-as-gift";
import APIService from '../../services/api';
import {getAllUrlParams} from "../../services/utils";
import InitialisePin from '../../services/eaa-pin';
import {setCharity, setDonationResult} from "../../services/reduxStorage/actions";
import ReactGA from 'react-ga';

ReactGA.initialize('UA-62759567-4');

let valid = require('card-validator');


class DonationForm extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = props.handleSubmit;

        this.chooseDifferentCharity = this.chooseDifferentCharity.bind(this);
        this.onSubmit = this.onSubmit.bind(this);

        this.apiService = new APIService();
        this.state = {
            charities: [],
            submitting: false
        };

        this.getCharities();
        this.pin = InitialisePin();
    }

    getCharities() {
        this.apiService.getCharities().then((charities) => {
            this.setState({
                charities: charities
            });
        })
    }

    chooseDifferentCharity(e) {
        e.preventDefault();
        this.props.router.popToRoot();
        return false;
    }


    callPinAPI(response_data, callBack) {
        let payment = this.props.donation.payment;
        let expiry = valid.expirationDate(payment.cardExpiry);
        let donation_form = this;

        // Fetch details required for the createToken call to Pin
        let card = {
            // Removing spaces from cc-number is necessary for the Pin test cards to work
            number: payment.cardNumber.replace(/\s/g, ''),
            name: payment.cardName,
            expiry_month: expiry.month,
            expiry_year: expiry.year,
            cvc: payment.cardCVC,
            address_line1: payment.cardAddress,
            address_line2: payment.cardAddress2,
            address_city: payment.cardCity,
            address_state: payment.cardState,
            address_postcode: payment.cardPostcode,
            address_country: payment.cardCountry
        };

        this.pin.createToken(card, handlePinResponse);

        function handlePinResponse(response) {
            if (response.response) {
                // Add the card token and ip address of the customer to the form
                // You will need to post these to Pin when creating the charge.
                response_data.pin_response = response.response;
                response_data.pin_response.ip_address = response.ip_address;
                callBack(response_data, donation_form)
            } else {
                this.setState({
                    error_message: response.messages[0].message
                });
                donation_form.setState({
                    submitting: false
                });
            }
        }
    }

    submitForm(response_data, donation_form) {
        let service = new APIService();
        service.submit(response_data).then((res) => {
            if (res.error_message) {
                donation_form.setState({
                    // We shouldn't ever hit this.
                    error_message: 'There was a problem submitting your donation. Please try again later.',
                    submitting: false
                });
            } else {
                donation_form.props.onSubmitResponse(res);
                donation_form.props.router.pushPage('donationResult');
                ReactGA.event({
                    category: 'Donation',
                    action: 'Completed',
                    label: 'Donation',
                });
            }
        });
    }

    onSubmit() {
        this.setState({
            submitting: true
        });
        let response_data = {
            charity: this.props.charity,
            donation: this.props.donation
        };
        if (this.props.donation.payment.method === 'credit-card') {
            this.callPinAPI(response_data, this.submitForm);
        } else {
            this.submitForm(response_data, this)
        }
    }

    render() {
        const charity_thumbnail = (this.props.charity && this.props.charity.thumbnail) ? (
            <img src={window.site_root.concat("/static/" + this.props.charity.thumbnail)}/>) : '';
        const donationMode = (this.props.charity) ? (
            <div>
                <h2>100% of your donation will go to support {this.props.charity.name}</h2>
                {charity_thumbnail}
                <br/>
                <p>
                    <a href=".">Choose a different program to support</a>
                </p>
            </div>
        ) : (
            <div>
                <h2>100% of your donation will go to support our partner charities</h2>
                <DonationModeOptions/>
            </div>
        );
        return (
            <form onSubmit={this.handleSubmit(this.onSubmit)}>
                <div className="donation-form">
                    {donationMode}

                    <div className="donation-page-header">
                        <h1 className="page-title">Payment</h1>
                    </div>
                    <div className="panel panel-default">
                        <div className="panel-body form-horizontal">
                            <DonationFrequency/>
                            <DonationAmount charity={this.props.charity} charities={this.state.charities}/>
                        </div>
                    </div>
                    <div className="panel panel-default form-container details-section donor-details-section">
                        <div className="panel-body form-horizontal">
                            <DonorDetails/>
                        </div>
                    </div>
                    <div className="panel panel-default form-container details-section payment-details-section">
                        <div className="panel-body form-horizontal">
                            <legend>Payment Details</legend>
                            <PaymentMethod change={this.props.change} error_message={this.state.error_message}/>
                        </div>
                    </div>
                    <div className="panel panel-default">
                        <div className="panel-body form-horizontal">
                            <DonationAsGift/>
                        </div>
                    </div>
                    <div>
                        <p className="help-text">Having a problem donating?
                            Please let us know at <a href="mailto://info@eaa.org.au">info@eaa.org.au</a>.
                        </p>
                        <DonationSubmit router={this.props.router} submitting={this.state.submitting}/>
                    </div>
                    <DonationFaq/>
                </div>
            </form>
        )
    }
}


const createReduxForm = reduxForm({form: 'donation', destroyOnUnmount: false});
DonationForm = createReduxForm(DonationForm);

const mapStateToProps = (state) => {
    return {
        charity: state.charity.currentCharity,
        donation: getFormValues('donation')(state),
        initialValues: {
            payment: {
                method: 'credit-card'
            },
            mode: 'auto',
            subscribe_for_updates: true,
        }
    }
};


function set_initial_charity(dispatch) {
    let apiService = new APIService();
    return apiService.getCharities().then((charities) => {
        let charity_filtered = charities.filter(function (x) {
            if (x.slug_id === getAllUrlParams().charity) {
                return x
            }
        });
        if (charity_filtered.length === 1) {
            dispatch(setCharity(charity_filtered[0]));
        }
    })
}

const mapDispatchToProps = (dispatch) => {
    set_initial_charity(dispatch);
    return {
        onSubmitResponse: (response) => {
            dispatch(setDonationResult(response))
        }
    }
};
export default connect(mapStateToProps, mapDispatchToProps)(DonationForm);
