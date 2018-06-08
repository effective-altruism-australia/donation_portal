import React, { Component } from "react";
import { Field, reduxForm } from 'redux-form'
import {required, minValue2, cardNumber, expirationDate, cvv} from "../../services/validation";
import {customInput, cardNumberInput} from "../../components/custom-fields";

class CardPaymentDetails extends Component {
    constructor(props) {
        super(props);
    }


    render() {
        const normalizeCardNumber = (value) => {
            return value.replace(/\s/g, '');
        };
        const normalizeExpiry = (value) => {
            return value.replace(/[a-zA-Z ]/g, '');
        };

        return (
            <div className="payment-subsection" id="id_credit_card">
                <fieldset id="pin_credit_card_details">
                    <div className="form-group">
                        <label className="control-label labels col-sm-3" htmlFor="cc-name">Name on card</label>
                        <div className="col-sm-9">
                            <Field className="form-control cc-form"
                                   name="payment.cardName"
                                   component={customInput}
                                   type="text" placeholder="Full name"
                                   validate={[required]}/>
                        </div>
                    </div>
                    <div className="form-group DEL-TODO-has-error">
                        <label className="control-label labels col-sm-3" htmlFor="cc-number">Card number</label>
                        <div className="col-sm-9">
                            <Field className="form-control cc-form unknown"
                                   name="payment.cardNumber"
                                   component={cardNumberInput}
                                   type="tel" placeholder="Card Number"
                                   normalize={normalizeCardNumber}
                                   validate={[cardNumber, required]}
                            />
                        </div>
                    </div>
                    <div className="multi-form-group">
                        <div className="form-group col-sm-7">
                            <label className="control-label labels col-sm-3" htmlFor="cc-expiry">
                                <span className="hidden-xs">Expiration</span>
                                <span className="visible-xs-inline">Exp</span> date
                            </label>
                            <div className="col-sm-4">
                                <Field className="form-control cc-form"
                                       name="payment.cardExpiry"
                                       component={customInput}
                                       type="tel" placeholder="MM / YY"
                                       normalize={normalizeExpiry}
                                       validate={[expirationDate, required]}
                                />
                            </div>
                        </div>
                        <div className="form-group col-sm-5">
                            <label className="control-label labels col-sm-3" htmlFor="cc-cvc">CV code</label>
                            <div className="col-sm-2">
                                <Field className="form-control cc-form"
                                       name="payment.cardCVC"
                                       component={customInput}
                                       type="text" placeholder="CVC"
                                       validate={[cvv, required]} />
                            </div>
                        </div>
                    </div>
                    <div className="form-group">
                        <label className="control-label labels col-sm-3" htmlFor="address-line1">Billing Address</label>
                        <div className="col-sm-9">
                            <Field className="form-control cc-form"
                                   name="payment.cardAddress"
                                   component={customInput}
                                   type="text"
                                   placeholder="Address Line 1"
                                   required=""
                                   aria-required="true"
                                   validate={[required]}/>
                        </div>
                    </div>
                    <div className="form-group">
                        <label className="control-label sr-only labels" hidden="" aria-hidden="true" htmlFor="address-line2">Billing Address line 2</label>
                        <div className="col-sm-9 col-sm-offset-3">
                            <Field className="form-control cc-form"
                                   name="payment.cardAddress2"
                                   component={customInput}
                                   type="text"
                                   placeholder="Address Line 2"/>
                        </div>
                    </div>
                    <div className="multi-form-group">
                        <div className="form-group col-sm-6">
                            <label className="control-label labels col-sm-3 visible-xs" htmlFor="address-city">City</label>
                            <div className="col-sm-3 col-sm-offset-3">
                                <Field className="form-control cc-form"
                                       name="payment.cardCity"
                                       component={customInput}
                                       type="text"
                                       placeholder="City"
                                       validate={[required]}/>
                            </div>
                        </div>
                        <div className="form-group col-sm-3">
                            <label className="control-label labels col-sm-3 visible-xs" htmlFor="address-state">State</label>
                            <div className="col-sm-3">
                                <Field className="form-control cc-form"
                                       name="payment.cardState"
                                       component={customInput}
                                       type="text"
                                       placeholder="State"
                                       validate={[required]}/>
                             </div>
                        </div>
                        <div className="form-group col-sm-3">
                            <label className="control-label labels col-sm-3 visible-xs" htmlFor="address-postcode">Postcode</label>
                            <div className="col-sm-3">
                                <Field className="form-control cc-form"
                                       name="payment.cardPostcode"
                                       component={customInput}
                                       type="text"
                                       placeholder="Postal Code"
                                       validate={[required]}/>
                            </div>
                        </div>
                    </div>
                    <div className="form-group">
                        <label className="control-label labels col-sm-3" htmlFor="address-country">Country</label>
                        <div className="col-sm-9">
                            <Field className="form-control cc-form"
                                   name="payment.cardCountry"
                                   component={customInput}
                                   type="text"
                                   placeholder="Country"
                                   required=""
                                   aria-required="true"
                                   validate={[required]}/>
                        </div>
                    </div>
                </fieldset>
            </div>
        )}
}

export default CardPaymentDetails;
