import React, { Component } from "react";
import {connect} from "react-redux";

class DonationAdvice extends Component {
    constructor() {
        super();
    }

    componentDidMount() {
        this.setState({
            charity: this.props.charity
        })
    }
    render() {
        return (
            <div>
                <div className="selected-charity-box">
                    <a href="https://www.againstmalaria.com/Donation.aspx?GroupID=86" target="_blank">
                        <img className="charity-img" src={this.props.charity.logo} alt={this.props.charity.name}/>
                    </a>
                    <p className="donation-info">
                        {this.props.charity.advice}
                    </p>
                </div>
            </div>
        )
    }
}

const mapStateToProps = (state) => {
    return {
        charity: state.charity.currentCharity
    }
};

export default connect(mapStateToProps)(DonationAdvice);
