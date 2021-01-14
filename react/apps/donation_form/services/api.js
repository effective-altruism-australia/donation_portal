import React from "react";

export default class APIService {
    getCharities() {
        return fetch(window.site_root.concat('/partner_charities')).then(function (response) {
            return response.json();
        });
    }

    getReferralSources() {
        return fetch(window.site_root.concat('/referral_sources')).then(function (response) {
            return response.json();
        });
    }

    submit(data) {
        let pledge_raw = data.donation;
        let pledge_clean = {};
        pledge_clean.payment_method = pledge_raw.payment.method;
        pledge_clean.recurring_frequency = pledge_raw.frequency;
        pledge_clean.recurring = pledge_raw.recurring_frequency === 'monthly';
        pledge_clean.first_name = pledge_raw.name.split(' ').slice(0, -1).join(' ');
        pledge_clean.last_name = pledge_raw.name.split(' ').slice(-1).join(' ');
        pledge_clean.email = pledge_raw.email;
        console.log(pledge_clean, pledge_raw)
    
        if (pledge_raw.amount!==undefined) {
            if (pledge_raw.mode === 'auto') {
                let amount = null;
                if (pledge_raw.amount.preset === 'other') {
                    amount = pledge_raw.amount.value;
                } else {
                    amount = pledge_raw.amount.preset;
                }

                let charity = 'unallocated';
                if (data.charity) {
                    charity = data.charity.slug_id
                }
                pledge_raw.components = [{'charity': charity, 'amount': amount}];
            } else if (pledge_raw.mode === 'custom') {
                pledge_raw.components = [];
                for (let charity in pledge_raw.amount) {
                    if (charity === 'preset' || charity === 'value') {
                        continue;
                    }
                    if (pledge_raw.amount[charity] !== "0") {
                        pledge_raw.components.push({'charity': charity, 'amount': pledge_raw.amount[charity]});
                    }
                }
            }
        } else {
            pledge_raw.components = []
        }

        if (pledge_raw.will_contribute) {
            pledge_raw.components.push({'charity': 'eaa', 'amount': pledge_raw.contribute.value});
        }

        pledge_clean.subscribe_to_updates = pledge_raw.subscribe_for_updates === true;
        pledge_clean.subscribe_to_newsletter = pledge_raw.subscribe_to_newsletter === true;
        pledge_clean.connect_to_community = pledge_raw.connect_to_community === true;

        pledge_clean.how_did_you_hear_about_us_db = pledge_raw.how_did_hear ?
            pledge_raw.how_did_hear.value : undefined;

        pledge_clean.is_gift = pledge_raw.is_gift;
        if (pledge_clean.is_gift) {
            pledge_clean.gift_recipient_name = pledge_raw.gift.recipient_name;
            pledge_clean.gift_recipient_email = pledge_raw.gift.recipient_email;
            pledge_clean.gift_personal_message = pledge_raw.gift.personal_message;
        }


        pledge_clean['form-TOTAL_FORMS'] = pledge_raw.components.length;
        pledge_clean['form-INITIAL_FORMS'] = pledge_raw.components.length;


        pledge_raw.components.forEach(function (item, i) {
            pledge_clean['form-' + i + '-id'] = null; // This tells Django that the object doesn't already exist
            pledge_clean['form-' + i + '-partner_charity'] = item.charity;
            pledge_clean['form-' + i + '-amount'] = item.amount;
        });


        if (pledge_raw.payment.method !== 'credit-card') {
            console.log(pledge_raw);
            pledge_clean.country = pledge_raw.country;
            pledge_clean.postcode = pledge_raw.postcode;
        }

        return fetch(window.site_root.concat('/pledge_new/'), {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(pledge_clean)
        }).then(function (response) {
            return response.json();
        });
    }
}

