import React, {Component} from "react";
import APIService from '../services/api';
import {setCharity} from "../services/reduxStorage/actions";
import {connect} from 'react-redux';

class CharityChoice extends Component {
    render() {
        return (
            <div className="charity">
                <div className="charity-info">
                    <img className="charity-img" src={this.props.charity.logo} alt={this.props.charity.name}/>
                    <span className="charity-title">{this.props.charity.name}</span>
                </div>
                <div className="hover-overlay">
                    <a className="charity-details charityClick" href="" onClick={this.props.onClick}>
                        {this.props.charity.blurb}
                    </a>
                </div>
            </div>
        )
    }
}


class CharityList extends Component {
    constructor() {
        super();

        this.apiService = new APIService();
        this.state = {
            charities: []
        };

        this.getCharities();
    }

    getCharities() {
        this.apiService.getCharities().then((charities) => {
            this.setState({
                charities: charities
            });
        })
    }

    render() {
        let choices = this.state.charities.map((charity) => {
            return <CharityChoice
                key={charity.name}
                onClick={(event) => {
                    event.preventDefault();
                    this.props.onSetCharity(charity);
                    if (charity.directDonationOnly) {
                        this.props.router.pushPage('paymentAdvice');
                    } else {
                        this.props.router.pushPage('paymentForm');
                    }
                }}
                charity={charity}
            />
        });

        return (
            <div className="donation-step" id="step-1">
                <h2>100% of your donation will be granted to the charity of your choice</h2>
                <h3>Select a charity:</h3>
                <div className="charities-container">
                    {choices}
                </div>
            </div>
        )
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        onSetCharity: (charity) => {
            dispatch(setCharity(charity));
        }
    }
};

export default connect(null, mapDispatchToProps)(CharityList);
