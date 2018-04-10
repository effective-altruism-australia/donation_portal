// This provides the data that will be supplied by the back-end, either by fetching it via API or by including it in
// the script at compile time (for data that is unlikely to change).

// Please just use the example data below for now.
// You are welcome to change the schema -- the API functions haven't been written yet.

const data = {
    charity_database_ids:  // TODO better to use slugs
        {
            "GiveDirectly": 2,
            "Schistosomiasis Control Initiative": 1,
            "Malaria Consortium": 5,
            "Deworm the World Initiative (led by Evidence Action)": 4,
            "GiveDirectly Basic income research": 3
        },
    donation_amounts: [25, 50, 100, 250],  // dollars
    referral_sources: [
        {id: 4, reason: 'The Life You Can Save'},
        {id: 1, reason: 'News'},
        {id: 6, reason: 'Advertising'},
        {id: 9, reason: 'GiveWell'},
        {id: 3, reason: 'From the charity (SCI, Evidence Action, GiveDirectly)'},
        {id: 8, reason: 'Friend'}
        ],
    csrf_token: '0CKtGyB07MgcoLd3TiD2YBDo9QlozVSV'
};

export default data;