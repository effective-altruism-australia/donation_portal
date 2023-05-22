import React, {Component} from 'react';
import {connect} from "react-redux";
import { Field, getFormValues} from 'redux-form'
import {setDonationResult} from "../../services/reduxStorage/actions";

class DonationSubmit extends Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (
        <div className="form-actions">
            <button type="submit" className="btn btn-success btn-lg"
                    disabled={
                        this.props.submitting
                    }>Donate</button>
        </div>
    )}
}

const mapStateToProps = (state) => {
    return {
        charity: state.charity.currentCharity,
        donation: getFormValues('donation')(state)
    }
};

const mapDispatchToProps = (dispatch) => ({
        onSubmit: (response) => {
            dispatch(setDonationResult(response))
        }
    });
export default connect(mapStateToProps, mapDispatchToProps)(DonationSubmit);

