import React, {Component} from 'react';

export default function DonationFaq(props) { return (
    <div className="details-section payment-faq">
        <h2>Donation FAQ</h2>
        <p className="payment-faq-question">
            What credit cards do you accept?
        </p>
        <p className="payment-faq-answer">
            We accept Visa and Mastercard. Sorry, we do not accept American Express at this time.
        </p>
        <p className="payment-faq-question">
            Are credit card donations secure?
        </p>
        <p className="payment-faq-answer">
            Yes. Your credit card details are encrypted and submitted directly from your web browser to our
            payment processor, Pin Payments (ABN: 46 154 451 582). Our accounting staff only have access to
            the last 4 digits of your credit card number.
        </p>
        <p className="payment-faq-question">
            How much does it cost you to process a donation?
        </p>
        <p className="payment-faq-answer">
            Credit card donations cost us 1.4% plus 30c per donation. Bank transfers have no fees.
        </p>
        <p className="payment-faq-question">
            Which payment method do you prefer?
        </p>
        <p className="payment-faq-answer">
            We suggest that you use whichever payment method is most convenient for you.
            For major donations (over $2,000), we prefer that you donate via bank transfer to reduce fees.
        </p>
        <p className="payment-faq-question">
            When will I get a receipt?
        </p>
        <p className="payment-faq-answer">
            For credit card donations, we will email you a receipt immediately after your donation.
            For bank transfers, we will email you a receipt on the day the money is received by us,
            which is usually one or two business days after you send it.
        </p>
    </div>
)}
