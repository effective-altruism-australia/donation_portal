import React, {Component} from "react";
import {Radio, RadioGroup} from "../../components/radio-group";

export default class FrequencyComponent extends Component {
    constructor() {
        super();
        this.id = parseInt(Math.random() * 1000);
    }
    render() {
        const { input: { value, onChange } } = this.props;

        return (
            <span>
                <RadioGroup selectedValue={value}
                            className="frequency-options"
                            onChange={onChange}>
                    <Radio value="one-time" id={'freq-one-time' + this.id}/><label htmlFor={'freq-one-time' + this.id} className="btn btn-default">One-Time</label>
                    <Radio value="monthly" id={'freq-monthy' + this.id}/><label htmlFor={'freq-monthy' + this.id} className="btn btn-default">Monthly</label>
                </RadioGroup>
            </span>
        );
    }
}
