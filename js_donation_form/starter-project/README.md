# EAA Donation Portal: reactjs proof-of-concept

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Set up

Ensure you have a recent version of Node installed. Use `nvm` if necessary to manage multiple versions.

Install the modules:

    npm install

## Run

Run the local server:

    npm run start
    

## Status

This was my first React app and is "ok" but needs work.

You may find it faster to start your own and copy parts as you see fit.

Notes:
 
- buttons for choosing one-time vs monthly work, but the logic to hide credit card details
  on the monthly choice isn't done. That's a small change.

- buttons for choosing donation amount work, including supporting the "other" field, but
  the styling on the "other amount" needs to be improved. 

- various data needs to come from AJAX calls to the server (and those calls implemented in
  the server), like referral sources and available charities. At first I thought these would
  be individual API endpoints, but it could be one endpoint, e.g.
  
```
curl https://donations.effectivealtruism.org.au/pledge-data  # or similar
{
  charities: [
    {
      name: "Schistosomiasis Control Initiative",
      blurb: "supports programs that work to eliminate debilitating neglected tropical diseases in Africa",
      logo: "/static/thumbnails/logo_sci.jpg",
    },
    {
      name: "Deworm the World",
      blurb: "supports programs that work to eliminate debilitating neglected tropical diseases in Africa",
      logo: "/static/thumbnails/logo_evidenceaction.gif",
    },
    {
      name: "Against Malaria Foundation",
      blurb: "provides long-lasting insecticidal nets to populations at high risk of malaria, primarily in Africa.",
      logo: "/static/thumbnails/logo_amf.jpg",
      directDonationSupported: false,  // <-- see note later
    },
    ...
  ],
  referrers: [
    "News", "Advertising", "GiveWell", ...    
  ]
}
```



## Tips

### JSON state

I've left code in to show the whole JSON state in the top-right corner.
It's handy during dev but, of course, remove it when ready.


### Default charity

When you're working on the main form, you don't want to select a charity each time.
This is where the charity is set:

```
  getInitialState() {
    return {
      chosenCharity: null,
      ...
```

You can fake having chosen a specific charity by modifying the initial state to
"choose" the first charity:

```
      chosenCharity: charities[0],
```


### Look for "TODO"

I've left the word "TODO" in various places. Read all of those notes before getting into it.


### Payment form

The payment form doesn't work yet. I ran out of time. I looked at various React-based credit
card forms and came back to doing it manually.

However, the better way is not to implement it at all, and instead use an off-the-shelf form
by Stripe.

It's worth thinking this through before writing any code to process card payments.
 