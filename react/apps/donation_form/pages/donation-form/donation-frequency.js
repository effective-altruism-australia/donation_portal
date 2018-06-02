import React, {Component} from "react";
import FrequencyComponent from "./frequency-component";
import { Field, formValueSelector} from 'redux-form'
import {connect} from "react-redux";
import Error from "../../components/error";

export default class DonationFrequency extends Component {

    render() {
        return (
            <div>
                <h3>How often will you be donating?</h3>
                <Field name="frequency" component={FrequencyComponent} />
                {/*<Error visible={!this.props.frequency}>Please choose a donation frequency.</Error>*/}
            </div>
        );
    }
}
