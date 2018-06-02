import { Radio, RadioGroup } from "react-radio-group";
import React, {Component} from "react";
import {connect} from "react-redux";
import Select from 'react-select';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import timezones from '../../services/timezones';
import moment from 'moment';
import { Field, formValueSelector} from 'redux-form'

class DonationAsGift extends Component {
    constructor() {
        super();
    }

    render() {

        return (
            <div>
                <h3>Finally, are you making this donation as a gift to someone?</h3>
                <div className="form-group">
                    <div className="col-sm-12">
                        <div className="checkbox">
                            <label htmlFor="id_donation_is_gift">
                                <Field
                                    id="id_donation_is_gift"
                                    name="is_gift"
                                    component="input"
                                    type="checkbox" />
                                Yes</label>
                        </div>
                    </div>
                </div>
                {
                    this.props.is_gift && (
                    <div>
                        <div className="form-group">
                            <label className="control-label labels col-sm-3" htmlFor="id_gift_recipient_name">
                                Recipient name
                            </label>
                            <div className="col-sm-9">
                                <Field className="form-control"
                                       type="text"
                                       name="gift.recipient_name"
                                       component="input"
                                       placeholder="Name"
                                />
                            </div>
                        </div>
                        <div className="form-group">
                            <label className="control-label labels col-sm-3" htmlFor="id_gift_recipient_email">
                                Recipient email
                            </label>
                            <div className="col-sm-9">
                                <Field className="form-control"
                                       type="email"
                                       name="gift.recipient_email"
                                       component="input"
                                       placeholder="Email"
                                />
                            </div>
                        </div>
                        <div className="form-group">
                            <label className="control-label labels col-sm-3" htmlFor="id_gift_personal_message">
                                Include a personal message?
                            </label>
                            <div className="col-sm-9">
                                <Field className="form-control"
                                       component="textarea"
                                       name="gift.personal_message"
                                       placeholder="Optional"
                                />
                            </div>
                        </div>
                        <div className="form-group">
                            <div className="col-sm-12">
                                <Field name="gift.send_when" component={
                                    (field) => (
                                        <RadioGroup
                                            className="raw-options" selectedValue={field.input.value}
                                            onChange={field.input.onChange}>
                                            <div>
                                                <Radio value="auto" id="id-gift-email-option-1"/>
                                                <label htmlFor="id-gift-email-option-1">
                                                    Send email as soon as payment received
                                                </label>
                                            </div>
                                            <div>
                                                <Radio value="custom" id="id-gift-email-option-2"/>
                                                <label htmlFor="id-gift-email-option-2">
                                                    Choose when to send email
                                                </label>
                                            </div>
                                        </RadioGroup>
                                    )}/>
                            </div>
                        </div>
                        { /* Send email time section */
                            this.props.send_when === 'custom' && (
                                <div className="form-group gift-date-form">
                                    <div className="col-sm-4 text-center">
                                        <label>Date</label>
                                        <Field name="gift.date" component={
                                            (field) => (
                                                <DatePicker placeholderText="DD/MM/YYYY" className="text-center form-control"
                                                            dateFormat="DD/MM/YYYY"
                                                            value={field.input.value}
                                                            onChange={ (date, event) => {
                                                                if (event && event.type === 'change') {
                                                                    field.input.onChange(event.target.value);
                                                                }
                                                                const strDate = date && date.isValid() ? date.format('DD/MM/YYYY') : '';
                                                                field.input.onChange(strDate);
                                                            }}/>
                                            )}/>

                                    </div>
                                    <div className="col-sm-2 text-center">
                                        <label>Hour</label>
                                        <Field className="form-control"
                                               component="input"
                                               type="number"
                                               name="gift.hour"
                                               placeholder="HH"
                                               min="0"
                                               max="23"
                                        />
                                    </div>
                                    <div className="col-sm-2 text-center">
                                        <label>Minute</label>
                                        <Field className="form-control"
                                               component="input"
                                               type="number"
                                               name="gift.minute"
                                               placeholder="MM"
                                               min="0"
                                               max="59"
                                        />
                                    </div>
                                    <div className="col-sm-4 text-center">
                                        <label>Time zone</label>
                                        <Field name="gift.timezone" component={
                                            (field) => (
                                                <Select id="id_gift_timezone"
                                                        className="form-control"
                                                        name="timezone"
                                                        onChange={field.input.onChange}
                                                        value={field.input.value}
                                                        searchable={false}
                                                        options={
                                                            timezones
                                                        } clearable={false}>
                                                </Select>
                                            )}/>

                                    </div>
                                </div>
                            )
                        }
                    </div>
                    )
                }
            </div>

        )
    }
}

// Decorate with connect to read form values
const selector = formValueSelector('donation'); // <-- same as form name
export default connect(
    state => {
        return {
            is_gift: selector(state, 'is_gift'),
            send_when: selector(state, 'gift.send_when')
        }
    }
)(DonationAsGift)

