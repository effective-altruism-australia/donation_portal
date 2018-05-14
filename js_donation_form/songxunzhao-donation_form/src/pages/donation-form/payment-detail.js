import React, { Component } from "react";
import { connect } from "react-redux";
import { Radio, RadioGroup } from "react-radio-group";
import { Field, formValueSelector } from 'redux-form'
import CardPaymentDetails from "./card-payment";

class PaymentDetail extends Component {
    constructor(props) {
        super(props);
        if(props.frequency === 'monthly' && props.method === 'credit-card') {
            props.change('payment.method', 'bank-transfer');
        }
    }

    componentWillReceiveProps(nextProps) {
        if(nextProps.frequency === 'monthly' && nextProps.method === 'credit-card') {
            console.log(nextProps);
            nextProps.change('payment.method', 'bank-transfer');
        }
    }

    render() {
        const detailSection = (this.props.method === 'credit-card') ?
            <CardPaymentDetails/>
            :
            <div className="payment-subsection" id="bank-transfer-instructions">
                <p>After you submit this form, we will give you our account details and a unique reference number.</p>
                <p>You then need to log in to your bank and make a bank transfer using these details.</p>
            </div>;

        return (
        <div>
            <div className="payment-type form-group">
                <label className="control-label col-sm-3">Payment Method</label>
                <div className="col-sm-9">

                    <Field name="payment.method"
                           className="payment-options"
                           component={(field) => (
                               <RadioGroup name="method"
                                           className="payment-options"
                                           selectedValue={field.input.value}
                                           onChange={field.input.onChange}>
                                   <Radio value="credit-card" id="id-credit-card" disabled={this.props.frequency === 'monthly'}/>
                                   <label htmlFor="id-credit-card" className="btn btn-default" disabled={this.props.frequency === 'monthly'}>Credit Card</label>
                                   <Radio value="bank-transfer" id="id-bank-transfer"/>
                                   <label htmlFor="id-bank-transfer" className="btn btn-default">Bank Transfer</label>
                               </RadioGroup>
                           )} />
                </div>
            </div>
            {
                this.props.frequency === 'monthly' &&
                <div className="">
                    <label>Note: </label> We currently only accept monthly donations via bank transfer.
                </div>
            }
            <div className="payment-subsections" id="id_payment_options">
                {detailSection}
            </div>
        </div>
    )}
}

const selector = formValueSelector('donation'); // <-- same as form name
export default connect(
    state => {
        return {
            frequency: selector(state, 'frequency'),
            method: selector(state, 'payment.method')
        }
    }
)(PaymentDetail);
