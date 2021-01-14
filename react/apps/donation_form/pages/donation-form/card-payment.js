import React, {Component} from "react";
import {Field} from 'redux-form'
import {cardNumber, minLength3, expirationDate, required} from "../../services/validation";
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

            </div>
        )
    }
}

export default CardPaymentDetails;
