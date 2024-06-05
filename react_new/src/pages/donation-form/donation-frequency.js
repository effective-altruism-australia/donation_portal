import React, {Component} from "react";
import FrequencyComponent from "./frequency-component";
import { Field } from 'redux-form'

export default class DonationFrequency extends Component {

    render() {
        return (
            <div>
                <h3>How often will you be donating?</h3>
                <Field name="frequency" component={FrequencyComponent} />
            </div>
        );
    }
}
