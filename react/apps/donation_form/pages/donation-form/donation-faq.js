import React, {Component} from 'react';

export default function DonationFaq(props) { return (
    <div className="details-section payment-faq">
        <h2>Donation FAQ</h2>
        <p className="payment-faq-question">
            Are donations tax-deductible in Australia?
        </p>
        <p className="payment-faq-answer">
            Yes! Effective Altruism Australia (ABN 87 608 863 467) is endorsed as a Deductible Gift Recipient (DGR)
            by the Australian Taxation Office (ATO). Donations of $2 or more are tax deductible in Australia
        </p>
        <p className="payment-faq-question">
            When will I get a receipt?
        </p>
        <p className="payment-faq-answer">
            For credit card donations, we will email you a receipt immediately after your donation. For bank transfers,
            we will email you a receipt on the day the money is received by us, which is usually one or two business
            days after you send it.
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
            What credit cards do you accept?
        </p>
        <p className="payment-faq-answer">
            We accept Visa, Mastercard and American Express.
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
            How does Effective Altruism Australia meet its operational costs?
        </p>
        <p className="payment-faq-answer">
            Running any charity has costs. To get your donation to its destination we need to meet our regulatory
            obligations and cover the costs of auditors, accountants, government registrations, banking facilities,
            websites, software and more. Like most charities, a portion of each donation goes to these kinds of
            expenses. In the last financial year (2019-2020), our operational expenses were 2.6% of the overall
            amount of donations we received. Some donors also choose to directly fund our operational costs so that a
            higher proportion of other donations can go directly to partner charities (in the 2019-2020 financial year
            70% of our operational costs were directly funded).
        </p>
        <p className="payment-faq-question">
            Has Effective Altruism Australia changed its operational expenses policy?
        </p>
        <p className="payment-faq-answer">
            Yes, in April 2020. Previously Effective Altruism Australia separately raised funds to meet its operational expenses while
            providing 100% of donations received through this website to our partner charities. Our new policy is more
            transparent, more administratively efficient and sustainable. Read more about the
            <a href={"https://blog.givewell.org/2009/12/07/robin-hood-smile-train-and-the-0-overhead-donor-illusion/"}>illusion
                of
                “0% overheads”.</a>
        </p>
        <p className="payment-faq-question">
            Can I donate directly to Effective Altruism Australia operational costs or other special projects?
            (e.g. conferences, events, advertising, community building)
        </p>
        <p className="payment-faq-answer">
            Yes! Simply select “I would like to choose how to allocate my donation” and then “Effective Altruism
            Australia Operations” in the donation form.
        </p>
    </div>
)}
