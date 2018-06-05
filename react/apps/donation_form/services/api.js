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

        let donation = data.donation;

        if (donation.mode === 'auto') {
            console.log('hi');
            let amount = null;
            if (donation.amount.preset === 'other') {
                amount = donation.amount.value;
            } else {
                amount = donation.amount.preset;
            }

            let charity = 'unallocated';
            if (data.charity) {
                charity = data.charity.slug_id
            }
            donation.components = [{'charity': charity, 'amount': amount}];
        } else if (donation.mode === 'custom') {
            donation.components = [];
            for (let charity in donation.amount) {
                if (charity === 'preset') {
                    continue;
                }
                donation.components.push({'charity': charity, 'amount': donation.amount[charity]});
            }
        }

        if (donation.will_contribute){
            donation.components.push({'charity': 'eaa', 'amount': donation.contribute.value});
            delete donation.will_contribute;
            delete donation.contribute;
        }
        delete donation.amount;

        console.log(donation);

        fetch('/pledge_new/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(donation)
        });

        return Promise.resolve({
            'bank_reference': 'xxxx',
            'receipt_url': 'xxxx'
        });
    }
}

