import React, {Component} from "react";
import {connect} from "react-redux";
import {Radio, RadioGroup} from "../../components/radio-group";
import {Field, formValueSelector} from 'redux-form'
import CardPaymentDetails from "./card-payment";
import {customInput} from "../../components/custom-fields";
import {required} from "../../services/validation";

class PaymentDetail extends Component {
    render() {
        const detailSection = (this.props.method === 'credit-card') ?
            <CardPaymentDetails/>
            :
            <div className="payment-subsection" id="bank-transfer-instructions">
                <div className="form-group">
                    <label className="control-label labels col-sm-3"
                           htmlFor="address-postcode">Postcode</label>
                    <div className="col-sm-3">
                        <Field className="form-control cc-form"
                               name="postcode"
                               component={customInput}
                               type="text"
                               placeholder="Postal Code"
                               validate={[required]}/>
                    </div>
                </div>
                <div className="form-group">
                    <label className="control-label labels col-sm-3" htmlFor="address-country">Country</label>
                    <div className="col-sm-9">
                        <Field className="form-control cc-form"
                               name="country"
                               component={customInput}
                               type="text"
                               placeholder="Country"
                               required=""
                               aria-required="true"
                               validate={[required]}/>
                    </div>
                </div>
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
                                       <Radio value="credit-card" id="id-credit-card"
                                              />
                                       <label htmlFor="id-credit-card" className="btn btn-default"
                                              >Credit Card</label>
                                       <Radio value="bank-transfer" id="id-bank-transfer"/>
                                       <label htmlFor="id-bank-transfer" className="btn btn-default">Bank
                                           Transfer</label>
                                   </RadioGroup>
                               )}/>
                    </div>
                </div>
                <div className="payment-subsections" id="id_payment_options">
                    {detailSection}
                </div>
            </div>
        )
    }
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
