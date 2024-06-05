export default class APIService {
    getCharities() {
        return fetch(window.site_root.concat('/partner_charities')).then(function (response) {
            // TODO: COMMENT OUT LINE BELOW BEFORE PRODUCTION TO USE REAL DATA
            return [{"category": null, "is_eaae": true, "slug_id": "eaae", "name": "Effective Altruism Australia Environmentalism", "thumbnail": ""}, {"category": "Other charities we support", "is_eaae": false, "slug_id": "give-directly", "name": "GiveDirectly", "thumbnail": "thumbnails/logo_givedirectly.png"}, {"category": "Other charities we support", "is_eaae": false, "slug_id": "unlimit", "name": "Unlimit Health (formerly SCI)", "thumbnail": ""}, {"category": "Other charities we support", "is_eaae": false, "slug_id": "de-worm", "name": "Deworm the World Initiative (led by Evidence Action)", "thumbnail": "thumbnails/logo_evidenceaction.gif"}, {"category": "Other charities we support", "is_eaae": false, "slug_id": "gd-refugees", "name": "GiveDirectly Refugees", "thumbnail": ""}, {"category": "Our recommended charities", "is_eaae": false, "slug_id": "malaria-consortium", "name": "Malaria Consortium", "thumbnail": "thumbnails/logo_mc.jpg"}, {"category": "Other charities we support", "is_eaae": false, "slug_id": "gd-basic-income", "name": "GiveDirectly Basic income research", "thumbnail": "thumbnails/logo_gdbi.png"}, {"category": "Our recommended charities", "is_eaae": false, "slug_id": "new-incentives", "name": "New Incentives", "thumbnail": ""}, {"category": "Our recommended charities", "is_eaae": false, "slug_id": "hki", "name": "Helen Keller International", "thumbnail": ""}, {"category": "Our recommended charities", "is_eaae": false, "slug_id": "against-malaria", "name": "Against Malaria Foundation", "thumbnail": "thumbnails/logo_amf.gif"}, {"category": "Help us do more good", "is_eaae": false, "slug_id": "eaa", "name": "Effective Altruism Australia Operations", "thumbnail": ""}, {"category": "Help us do more good", "is_eaae": false, "slug_id": "eaa-community", "name": "Effective Altruism Australia Community Building", "thumbnail": ""}]
            // return response.json();
        });
    }

    getReferralSources() {
        return fetch(window.site_root.concat('/referral_sources')).then(function (response) {
            // TODO: COMMENT OUT LINE BELOW BEFORE PRODUCTION TO USE REAL DATA
            return [{"value": "ea-community", "label": "Effective Altruism local group"}, {"value": "ea-online", "label": "Effective Altruism online community"}, {"value": null, "label": "The Life You Can Save"}, {"value": null, "label": "News"}, {"value": null, "label": "Advertising"}, {"value": null, "label": "GiveWell"}, {"value": null, "label": "From the charity (SCI, Evidence Action, GiveDirectly)"}, {"value": null, "label": "Search engine (Google etc.)"}, {"value": null, "label": "Friend"}, {"value": null, "label": "Giving What We Can"}, {"value": "givedirectly-dinner", "label": "Give Directly Dinner"}, {"value": null, "label": "One for the World"}, {"value": "podcast", "label": "Podcast or radio"}, {"value": "cant-remember", "label": "I cannot remember"}, {"value": "other", "label": "Other"}]
            // return response.json();
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

