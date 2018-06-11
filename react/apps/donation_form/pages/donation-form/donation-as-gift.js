import React, {Component} from "react";
import {connect} from "react-redux";
import 'react-datepicker/dist/react-datepicker.css';
import {Field, formValueSelector} from 'redux-form'

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
                                    type="checkbox"/>
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

