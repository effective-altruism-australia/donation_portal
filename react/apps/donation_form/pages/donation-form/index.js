import {connect} from "react-redux";
import React, { Component } from "react";
import {reduxForm, getFormValues} from 'redux-form';
import DonorDetails from "./donor-details"
import DonationModeOptions from "./donation-mode-options"
import DonationFrequency from "./donation-frequency"
import DonationAmount from "./donation-amount"
import PaymentMethod from "./payment-detail";
import DonationFaq from "./donation-faq";
import DonationSubmit from "./donation-submit";
import DonationAsGift from "./donation-as-gift";
import APIService from '../../services/api';
import {setDonationResult} from "../../services/reduxStorage/actions";

class DonationForm extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = props.handleSubmit;

        this.chooseDifferentCharity = this.chooseDifferentCharity.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
    }

    chooseDifferentCharity(e) {
        e.preventDefault();
        this.props.router.popToRoot();
        return false;
    }

    onSubmit(val) {
        // TODO: send http
        let service = new APIService();
        service.submit({
            charity: this.props.charity,
            donation: this.props.donation
        }).then((res) => {
            this.props.onSubmitResponse(res);
            this.props.router.pushPage('donationResult');
        });
    }

    render() {
        const donationMode = (this.props.charity) ? (
            <div>
                <h2>100% of your donation will go to support the {this.props.charity.name}</h2>
                <a href="#" onClick={this.chooseDifferentCharity}>Choose a different program to support</a>
            </div>
        ): (
            <div>
                <h2>100% of your donation will go to support our partner charities</h2>
                <DonationModeOptions/>
            </div>
        );


        return (
            <form onSubmit={this.handleSubmit(this.onSubmit.bind(this))}>
                <div className="donation-form">
                    {donationMode}

                    <div className="donation-page-header">
                        <h1 className="page-title">Payment</h1>
                    </div>
                    <div className="panel panel-default">
                        <div className="panel-body form-horizontal">
                            <DonationFrequency/>
                            <DonationAmount charity={this.props.charity}/>
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
                            <PaymentMethod change={this.props.change}/>
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
                        <DonationSubmit router={this.props.router} submitting={this.props.submitting}/>
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
            }
        }
    }
};

const mapDispatchToProps = (dispatch) => ({
    onSubmitResponse: (response) => {
        dispatch(setDonationResult(response))
    }
});
export default connect(mapStateToProps, mapDispatchToProps)(DonationForm);
