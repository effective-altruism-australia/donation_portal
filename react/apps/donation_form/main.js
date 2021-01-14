import './main.css';
import React, {Component} from "react";
import DonationForm from "./pages/donation-form/index";
import DonationResult from "./pages/donation-result/index";
import DonationAdvice from "./pages/donation-advice";
import {formValueSelector} from 'redux-form'
import {connect} from "react-redux";
import {getAllUrlParams} from "./services/utils";

export class Main extends Component {
    constructor(props) {
        super(props);
        this.pages = {
            "paymentForm": {
                title: "Donate",
                step: 1,
                component: DonationForm
            },
            "paymentAdvice": {
                title: "Donate",
                step: 1,
                component: DonationAdvice
            },
            "donationResult": {
                step: 2,
                component: DonationResult
            }
        };

        this.state = this.getInitialState();

        this.handleClickStep = this.handleClickStep.bind(this);
    }

    onUpdatePageQueue(pageQueue) {

        this.setState({
            "pageQueue": pageQueue
        });
    }

    switchPage(pageId) {
        let pageQueue = this.state.pageQueue;

        if (pageQueue.length > 0) {
            pageQueue[pageQueue.length - 1] = pageId;
        } else {
            pageQueue.push(pageId);
        }

        this.onUpdatePageQueue(pageQueue);
    }

    pushPage(pageId) {
        let pageQueue = this.state.pageQueue;
        pageQueue.push(pageId);
        this.onUpdatePageQueue(pageQueue);
    }

    popPage() {
        let pageQueue = this.state.pageQueue;

        if (pageQueue.length > 1) {
            pageQueue.pop();
            this.onUpdatePageQueue(pageQueue);
        }
    }

    popToRoot() {
        let pageQueue = this.state.pageQueue;

        if (pageQueue.length > 0)
            pageQueue.length = 1;
        this.onUpdatePageQueue(pageQueue);
    }

    handleClickStep() {
        this.popToRoot();
    }

    getInitialState() {
        if (getAllUrlParams().thankyou) {
            console.log(this.state)
            return {
                'mode': 'credit-card',
                'pageQueue': ['donationResult']
            }
        }
        return {
            'pageQueue': ['paymentForm'] // TODO: remove charity list
        }
    }


    render() {
        let pageId = this.state.pageQueue[this.state.pageQueue.length - 1];
        let PageComponent = this.pages[pageId].component;
        let step = this.pages[pageId].step;
        let pageTitle = step !== 3 ? this.pages[pageId].title : this.props.method === 'credit-card' ? 'Success' : 'Complete payment';

        return (
            <div className="container">
                <div className="donation-page-header">
                    <h1 className="page-title">{pageTitle}</h1>
                </div>
                <PageComponent router={this}/>
            </div>
        );
    }
}

const selector = formValueSelector('donation'); // <-- same as form name
export default connect(
    state => {
        return {
            method: selector(state, 'payment.method')
        }
    }
)(Main)
