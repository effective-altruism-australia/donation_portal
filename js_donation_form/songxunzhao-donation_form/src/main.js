import React, { Component} from "react";
import CharityList from "./pages/charity-list";
import DonationForm from "./pages/donation-form/index";
import DonationResult from "./pages/donation-result/index";
import DonationAdvice from "./pages/donation-advice";
import classNames from "classnames";
import { formValueSelector } from 'redux-form'
import './main.css';
import {connect} from "react-redux";

export class Main extends Component {
  constructor(props) {
    super(props);
    this.pages = {
        "paymentForm": {
            title: "Make a Donation",
            step: 2,
            component: DonationForm
        },
        "paymentAdvice": {
            title: "Make a Donation",
            step: 2,
            component: DonationAdvice
        },
        "donationResult": {
            step: 3,
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

      if(pageQueue.length > 0) {
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

      if(pageQueue.length > 1) {
          pageQueue.pop();
          this.onUpdatePageQueue(pageQueue);
      }
  }

  popToRoot() {
      let pageQueue = this.state.pageQueue;

      if(pageQueue.length > 0)
        pageQueue.length = 1;
      this.onUpdatePageQueue(pageQueue);
  }

  handleClickStep() {
      this.popToRoot();
  }

  getInitialState() {
      console.log(window.presetCharity);
      if(window.presetCharity && window.presetCharity === 'givedirectly') {
          return {
              'pageQueue': ['charityList', 'paymentForm']
          }
      } else {
          return {
              'pageQueue': ['charityList']
          }
      }
  }

  render() {
      let pageId = this.state.pageQueue[this.state.pageQueue.length - 1];
      console.log(pageId);
      let PageComponent = this.pages[pageId].component;
      let step = this.pages[pageId].step;
      let pageTitle = step !== 3 ? this.pages[pageId].title : this.props.method === 'credit-card' ? 'Complete payment' : 'Success';

      return (
          <div className="container">
              <div className="donation-page-header">
                  <h1 className="page-title">{pageTitle}</h1>
                  { step !== 3 &&
                      <div className="donation-progress">
                          <div className={classNames("progress-step", {"current-step": step === 1, "clickable": step !== 1})}
                               onClick={this.handleClickStep}>1</div>
                          <div className={classNames("progress-step", {"current-step": step === 2})}>2</div>
                      </div>
                  }

              </div>
              <PageComponent router={this} />
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
