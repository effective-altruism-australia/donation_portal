import React, {Component} from "react";
import {Field} from 'redux-form'
import {cardNumber, cvv, expirationDate, required} from "../../services/validation";
import {cardNumberInput, customInput} from "../../components/custom-fields";

class CardPaymentDetails extends Component {
    constructor(props) {
        super(props);
    }


    render() {
        const normalizeCardNumber = (value) => {
            var v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
            var matches = v.match(/\d{4,16}/g);
            var match = matches && matches[0] || '';
            var parts = [];

            for (let i = 0, len = match.length; i < len; i += 4) {
                parts.push(match.substring(i, i + 4))
            }

            if (parts.length) {
                return parts.join(' ')
            } else {
                return value
            }
        };
        const normalizeExpiry = (value) => {
            return value.replace(
                /^([1-9]\/|[2-9])$/g, '0$1 / ' // To handle 3/ > 03/
            ).replace(
                /^(0[1-9]{1}|1[0-2]{1})$/g, '$1 / ' // 11 > 11/
            ).replace(
                /^([0-1]{1})([3-9]{1})$/g, '0$1 / $2' // 13 > 01/3
            ).replace(
                /^(\d)\/(\d\d)$/g, '0$1 / $2' // To handle 1/11 > 01/11
            ).replace(
                /^(0?[1-9]{1}|1[0-2]{1})([0-9]{2})$/g, '$1 / $2' // 141 > 01/41
            ).replace(
                /^([0]{1,})\/|[0]{1,}$/g, '0' // To handle 0/ > 0 and 00 > 0
            ).replace(
                /\/\//g, '/' // Prevent entering more than 1 /
            );
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
                                       validate={[cvv, required]}/>
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
                        <label className="control-label sr-only labels" hidden="" aria-hidden="true"
                               htmlFor="address-line2">Billing Address line 2</label>
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
                            <label className="control-label labels col-sm-3 visible-xs"
                                   htmlFor="address-city">City</label>
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
                            <label className="control-label labels col-sm-3 visible-xs"
                                   htmlFor="address-state">State</label>
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
                            <label className="control-label labels col-sm-3 visible-xs"
                                   htmlFor="address-postcode">Postcode</label>
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
        )
    }
}

export default CardPaymentDetails;
