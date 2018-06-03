import React from "react";
import {charities, referralSources} from "./data_dump";

export default class APIService {
    getCharities() {
        return Promise.resolve(charities);
    }

    getReferralSources() {
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

