import React from "react";

export default class APIService {
    getCharities() {

        const charities = [{
            'slug_id': 'sci',
            'name': 'Schistosomiasis Control Initiative'
        }, {
            'slug_id': 'give_directly_basic',
            'name': 'GiveDirectly Basic income research'
        }, {
            'slug_id': 'give_directly',
            'name': 'GiveDirectly'
        }, {
            'slug_id': 'malaria_consortium',
            'name': 'Malaria Consortium'
        }, {
            'slug_id': 'deworm',
            'name': 'Deworm the World Initiative (led by Evidence Action)'
        }];

        return Promise.resolve(charities);
    }

    getReferralSources() {
        const referralSources = [
            {value: "life_save", label: "The Life You Can Save"},
            {value: "news", label: "News"},
            {value: "advertising", label: "Advertising"},
            {value: "givewell", label: "GiveWell"},
            {value: "from_charity", label: "From the charity (SCI, Evidence Action, GiveDirectly)"},
            {value: "search_engine", label: "Search engine (Google etc)"},
            {value: "friend", label: "Friend"},
            {value: "giving_we_can", label: "Giving What We Can"},
        ];

        return Promise.resolve(referralSources);
    }

    submit(data) {
        console.log(data);

        fetch('http://127.0.0.1:8000/pledge', {
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

