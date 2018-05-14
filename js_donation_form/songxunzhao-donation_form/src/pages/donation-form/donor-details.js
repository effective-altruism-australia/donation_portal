import React, {Component} from "react";
import {connect} from "react-redux";
import Select from 'react-select';
import 'react-select/dist/react-select.css';
import APIService from "../../services/api";
import { Field, reduxForm } from 'redux-form'

export default class DonorDetails extends Component {

    constructor() {
        super();
        this.state = this.getInitialState();
        this.apiService = new APIService();
        this.apiService.getReferralSources().then((sources) => {
            this.setState({
                'sources': sources
            })
        });
    }

    getInitialState() {
        return {
            'sources': []
        }
    }

    render() {
        return (
            <div>
                <legend>Donor Details</legend>
                <div className="form-group" id="form_first_name">
                    <label className="control-label col-sm-3" htmlFor="id_first_name">Name</label>
                    <div className="col-sm-9">
                        <Field
                            className="form-control"
                            name="name"
                            placeholder="Name"
                            type="text"
                            component="input" />
                    </div>
                </div>

                <div className="form-group" id="form_email">
                    <label className="control-label col-sm-3" htmlFor="id_email">Email</label>
                    <div className="col-sm-9">
                        <Field
                            className="form-control"
                            name="email"
                            placeholder="Email"
                            type="text"
                            maxLength="254"
                            component="input" />
                    </div>
                </div>

                <div className="form-group">
                    <label className="control-label col-sm-3 long-control-label" htmlFor="id_how_did_you_hear_about_us_db">
                        How did you hear about us?</label>
                    <div className="col-sm-9">
                        <Field
                            className="form-control"
                            name="how_did_hear"
                            component={(field) => (
                                <Select
                                        value={field.input.value}
                                        onChange={field.input.onChange}
                                        searchable={false}
                                        options={[
                                            {value:'', label: '---------'}
                                        ].concat(this.state.sources)} clearable={false}>
                                </Select>
                            )}
                            />


                    </div>
                </div>

                <div className="form-group" id="id_formgroup_subscribe">
                    <div className="checkbox col-sm-offset-3">
                        <label htmlFor="id_subscribe">
                            <Field
                                id="id_subscribe"
                                name="subscribe_for_updates"
                                placeholder="Email"
                                type="checkbox"
                                maxLength="254"
                                component="input" />

                            Send me news and updates
                        </label>
                    </div>
                </div>
            </div>
        )
    }
}

