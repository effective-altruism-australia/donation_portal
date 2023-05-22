import React, {Component} from "react";
import Select from 'react-select';
// import 'react-select/dist/react-select.css';
import APIService from "../../services/api";
import {Field} from 'redux-form'
import {required, maxLength100, email} from "../../services/validation";

import {customInput} from "../../components/custom-fields";

export default class DonorDetails extends Component {

    constructor() {
        super();
        this.state = this.getInitialState();
        this.apiService = new APIService();
    }

    componentDidMount() {
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
                            component={customInput}
                            validate={[required, maxLength100]}
                        />
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
                            component={customInput}
                            validate={[required, email]}

                        />
                    </div>
                </div>

                <div className="form-group">
                    <label className="control-label col-sm-3 long-control-label"
                           htmlFor="id_how_did_you_hear_about_us_db">
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
                                        {value: '', label: '---------'}
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
                                component="input"/>

                            Send me news and updates
                        </label>
                    </div>
                </div>

                <div className="form-group" id="id_formgroup_subscribe_to_newsletter">
                    <div className="checkbox col-sm-offset-3">
                        <label htmlFor="id_subscribe_to_newsletter">
                            <Field
                                id="id_subscribe_to_newsletter"
                                name="subscribe_to_newsletter"
                                type="checkbox"
                                maxLength="254"
                                component="input"/>
                            Subscribe me to the <a target={"_blank"} href={"https://www.effectivealtruism.org/ea-newsletter-archives/"}>global Effective Altruism newsletter</a>
                        </label>
                    </div>
                </div>

                <div className="form-group" id="id_formgroup_sconnect_to_community">
                    <div className="checkbox col-sm-offset-3">
                        <label htmlFor="id_connect_to_community">
                            <Field
                                id="id_connect_to_community"
                                name="connect_to_community"
                                type="checkbox"
                                maxLength="254"
                                component="input"/>
                            Connect me with my <a target={"_blank"} href={"https://eahub.org/groups/"}>local Effective Altruism community</a>
                        </label>
                    </div>
                </div>
            </div>
        )
    }
}

