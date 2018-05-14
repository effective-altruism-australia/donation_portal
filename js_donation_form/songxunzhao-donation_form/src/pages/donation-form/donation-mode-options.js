import React, { Component } from 'react';
import { Radio, RadioGroup } from "react-radio-group";
import { Field, reduxForm } from 'redux-form'

export default class DonationModeOption extends Component {
    constructor() {
        super();
    }


    render() {
        const radioGroup = (field) => (

            <RadioGroup
                className="raw-options" selectedValue={field.input.value} onChange={value => {field.input.onChange(value);}}>
                <div>
                    <Radio value="auto" id="id-donate-option-1"/>
                    <label htmlFor="id-donate-option-1">
                        Please distribute my donation to the most effective charities, based on evidence and need.
                    </label>
                </div>
                <div>
                    <Radio value="custom" id="id-donate-option-2"/>
                    <label htmlFor="id-donate-option-2">
                        I would like to choose how to allocate my donation
                    </label>
                </div>
            </RadioGroup>
        );

        return (<div className="panel panel-default">
            <div className="panel-body">
                <Field name="mode" component={radioGroup}/>
            </div>
        </div>)
    }
}
