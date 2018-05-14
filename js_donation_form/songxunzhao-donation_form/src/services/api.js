import React from "react";

export default class APIService {
    getCharities() {
        const charities = [
            {
                name: "Schistosomiasis Control Initiative",
                blurb: <span><b>Schistosomiasis Control Initiative</b> supports programs that work
                    to eliminate debilitating neglected tropical diseases in Africa</span>,
                logo: "//donations.effectivealtruism.org.au/static/thumbnails/logo_sci.jpg",
            },
            {
                name: "Deworm the World",
                blurb: <span><b>Deworm the World</b> supports programs that work to eliminate debilitating neglected
                    tropical diseases in Africa</span>,
                logo: "//donations.effectivealtruism.org.au/static/thumbnails/logo_evidenceaction.gif",
            },
            {
                name: "Against Malaria Foundation",
                blurb: <span><b>Against Malaria Foundation</b> provides long-lasting insecticidal nets to populations
                    at high risk of malaria, primarily in Africa.</span>,
                logo: "//donations.effectivealtruism.org.au/static/thumbnails/logo_amf.jpg",
                directDonationOnly: true,
                advice: <p className="donation-info">
                    Donations to the Against Malaria Foundation are tax deductible in Australia.
                    We prefer that you donate to the Against Malaria Foundation directly at&nbsp;
                    <a href='//www.againstmalaria.com/Donation.aspx?GroupID=86' target="_blank" rel="noopener noreferrer">
                        https://www.againstmalaria.com/Donation.aspx?GroupID=86
                    </a>.
                </p>
            },
            {
                name: "GiveDirectly",
                blurb: <span><b>GiveDirectly</b> makes direct, unconditional cash transfers to
                    the world's poorest people</span>,
                logo: "//donations.effectivealtruism.org.au/static/thumbnails/logo_givedirectly.png"
            },
            {
                name: "Basic Income (GD)",
                blurb: <span><b>Basic Income (GD)</b> measures the impact of providing direct cash transfers to the world's
                    poorest people over an extended period</span>,
                logo: "//donations.effectivealtruism.org.au/static/thumbnails/logo_gdbi.png"
            },
            {
                name: "Malaria Consortium",
                blurb: <span><b>Malaria Consortium</b> supports programs that
                    provide malaria prevention medication to children in sub-Saharan Africa</span>,
                logo: "//donations.effectivealtruism.org.au/static/thumbnails/logo_mc.jpg",
            }
        ];
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
        return Promise.resolve({
            'bank_reference': 'xxxx',
            'receipt_url': 'xxxx'
        });
    }
}

