import React from "react";

export default class APIService {
    getCharities() {
        return fetch('/partner_charities').then(function (response) {
            return response.json();
        });
    }

    getReferralSources() {
        return fetch('/referral_sources').then(function (response) {
            return response.json();
        });
    }

    submit(data) {
        console.log(data);

        fetch('/pledge_new', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        return Promise.resolve({
            'bank_reference': 'xxxx',
            'receipt_url': 'xxxx'
        });
    }
}

