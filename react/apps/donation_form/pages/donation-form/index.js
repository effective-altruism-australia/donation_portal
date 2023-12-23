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
    

        if (window.location.search.includes('eaae')) {
            this.stripe = window.Stripe('pk_live_51MbDLyBiXhYHr2MDTZOSex4Vvu3SQJNL4OylN4m9eg1dNXJLFOEASUUiYWASR3t075ewmrCYhqQAonqJlCv4lFVE00FgbQz9UA');
        } else {
            this.stripe = window.Stripe('pk_live_51I1Q7kEO8N9VNJdmgqN19KmuB7haiTg9A9bHfEkHlS7cxlPk0A5ejkHlWuq2sAVvE7QWQXYnTQhRbtEXAT9dSx7A00fl6fhFl5');
        }
        
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

    submitForm(response_data, donation_form) {
        if (response_data.donation.amount === undefined) {
            if (!(response_data.donation.will_contribute && response_data.donation.contribute !== undefined)) {
                window.alert('Please select a donation amount');
                donation_form.setState({
                    submitting: false
                });
                return
            }
        }
        let service = new APIService();
        service.submit(response_data).then((res) => {
                if (res.error_message) {
                    donation_form.setState({
                        error_message: res.error_message,
                        submitting: false
                    });
                } else {
                    donation_form.props.onSubmitResponse(res);
                    if (this.props.donation.payment.method === 'credit-card') {
                        this.stripe.redirectToCheckout({sessionId: res.id})
                    } else {
                        donation_form.props.router.pushPage('donationResult');
                    }
                    ReactGA.event({
                        category: 'Donation',
                        action: 'SubmitForm',
                        label: 'SubmitDonationForm'
                    });
                };
        })
    }

    onSubmit() {
        this.setState({
            submitting: true
        });
        let response_data = {
            charity: this.props.charity,
            donation: this.props.donation
        };
        this.submitForm(response_data, this)
    }

    render() {
        const charity_thumbnail = (this.props.charity && this.props.charity.thumbnail) ? (
            <img src={window.site_root.concat("/static/" + this.props.charity.thumbnail)}/>) : '';
        const donationMode = (this.props.charity) ? (
            <div>
                <h2>Your donation will go to support {this.props.charity.name}</h2>
                {charity_thumbnail}
                <br/>
            </div>
        ) : (
            <div>
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
                        {
                            this.state.error_message &&
                            <div className="text-danger" align="right">
                                {this.state.error_message}
                            </div>
                        }
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
            frequency: "one-time",
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
