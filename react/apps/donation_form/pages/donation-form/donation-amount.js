import {connect} from "react-redux";
import {Radio, RadioGroup} from "react-radio-group";
import React, {Component} from "react";
import {Field, formValueSelector} from 'redux-form'
import classNames from 'classnames';
import {customCurrencyInput, customInput} from "../../components/custom-fields";
import {minValue1cent, required} from "../../services/validation";
import {getTotalDonation} from "../../services/utils";

class DonationAmount extends Component {
    constructor(props) {
        super(props);
        this.calculateTotal(props);
    }


    componentWillReceiveProps(nextProps) {
        this.calculateTotal(nextProps);
    }

    calculateTotal(props) {
        this.total = getTotalDonation(props.mode, props.amount, props.contribute);
    }

    render() {

        const contributeHeading = !this.props.charity ?
            <div className="form-group" style={{marginLeft: '5px'}}>
                <div>
                    <label htmlFor="id_will_contribute" style={{fontWeight: '400', paddingTop: '8px'}}>
                        <div style={{float: 'left'}}>
                            <Field id="id_will_contribute"
                                   name="will_contribute"
                                   component={customInput}
                                   type="checkbox"/>
                        </div>
                        <p style={{paddingLeft: '20px'}}>
                            I would like to contribute to covering Effective Altruism Australia's running costs
                        </p>
                    </label>
                </div>
            </div> :
            <div><br/><br/><br/></div>;

        const contributeSection = this.props.will_contribute ?
            <div>
                <div className="form-group">
                    <div className="col-sm-12">
                        Thank you! These funds will help cover our administrative and operations costs.
                        As we are not-for-profit organisation,
                        any excess donations will be granted to our partner charities.
                    </div>
                </div>
                <div className="form-group cover-amount-group">
                    <div className="col-sm-12">
                        <span className="amount-input-wrapper">
                            <div className="input-group amount-input">
                                <Field
                                    className="form-control"
                                    name="contribute.value"
                                    component={customCurrencyInput}
                                    type="number"
                                    placeholder="0.00"
                                    aria-describedby="Amount"
                                    validate={[required, minValue1cent]}
                                />
                            </div>
                        </span>
                    </div>
                </div>
            </div> : '';


        const amountRadio = (field) => (
            <RadioGroup {...field.input} className="donation-amount-group" selectedValue={field.input.value}>
                <Radio value="25" id="id-amount-25"/>
                <label htmlFor="id-amount-25" className="btn btn-default">$25</label>
                <Radio value="50" id="id-amount-50"/>
                <label htmlFor="id-amount-50" className="btn btn-default">$50</label>
                <Radio value="100" id="id-amount-100"/>
                <label htmlFor="id-amount-100" className="btn btn-default">$100</label>
                <Radio value="250" id="id-amount-250"/>
                <label htmlFor="id-amount-250" className="btn btn-default">$250</label>
                <Radio value="other" id="id-amount-other"/>
                <label htmlFor="id-amount-other" className="btn btn-default">Other</label>
            </RadioGroup>
        );

        const amountSection = <div>
            <h3>How much would you like to donate? </h3>
            <Field name="amount.preset"
                   component={amountRadio}/>
            {
                this.props.amount && this.props.amount.preset === 'other' && (
                    <span className="amount-input-wrapper">
                        <Field className="form-control"
                               name="amount.value"
                               component={customCurrencyInput}
                               type="number"
                               placeholder="0.00"
                               validate={[required, minValue1cent]}
                        />
                    </span>
                )
            }
            <br/><br/>
        </div>;


        const allocateSection = <div id="id-allocate-donation-section">
            {
                this.props.charities.filter((charity) => charity.category === "Our recommended charities").length > 0 &&
                <div>
                    <h3>Our recommended charities <a target="_blank" href="https://effectivealtruism.org.au/inclusion-criteria/">ℹ️</a></h3>
                    {
                        this.props.charities.filter((charity) => charity.category === "Our recommended charities").map(function (charity) {
                            return <div className="form-group" key={charity.slug_id}>
                                <label className="control-label col-sm-5">{charity.name}</label>
                                <div className="col-sm-7">
                                    <div className="input-group">
                                        <span className="input-group-addon">$</span>
                                        <Field className="form-control"
                                            name={"amount." + charity.slug_id}
                                            component={customInput}
                                            type="number"
                                            placeholder="0.00"
                                        />
                                    </div>
                                </div>
                            </div>;
                        })
                    }
                </div>
            }
            {
                this.props.charities.filter((charity) => charity.category === "Other charities we support").length > 0 &&
                <div>
                    <h3>Other charities we support <a target="_blank" href="https://effectivealtruism.org.au/inclusion-criteria/">ℹ️</a></h3>
                    {
                        this.props.charities.filter((charity) => charity.category === "Other charities we support").map(function (charity) {
                            return <div className="form-group" key={charity.slug_id}>
                                <label className="control-label col-sm-5">{charity.name}</label>
                                <div className="col-sm-7">
                                    <div className="input-group">
                                        <span className="input-group-addon">$</span>
                                        <Field className="form-control"
                                            name={"amount." + charity.slug_id}
                                            component={customInput}
                                            type="number"
                                            placeholder="0.00"
                                        />
                                    </div>
                                </div>
                            </div>;
                        })
                    }
                </div>
            }
            {
                this.props.charities.filter((charity) => charity.category === "Help us do more good").length > 0 &&
                <div>
                    <h3>Help us do more good</h3>
                    {
                        this.props.charities.filter((charity) => charity.category === "Help us do more good").map(function (charity) {
                            return <div className="form-group" key={charity.slug_id}>
                                <label className="control-label col-sm-5">{charity.name}</label>
                                <div className="col-sm-7">
                                    <div className="input-group">
                                        <span className="input-group-addon">$</span>
                                        <Field className="form-control"
                                            name={"amount." + charity.slug_id}
                                            component={customInput}
                                            type="number"
                                            placeholder="0.00"
                                        />
                                    </div>
                                </div>
                            </div>;
                        })
                    }
                </div>
            }
        </div>;

        const modeSwitch = this.props.mode === 'custom' ? allocateSection : amountSection;

        return (
            <div>
                {modeSwitch}
                {/*<br/><br/>*/}
                <p>Donations are inclusive of all transaction fees and operational costs.</p>
                <div className="total-amount-group">
                    <label className={classNames("control-label", {
                        "col-sm-1": this.props.mode !== 'custom',
                        "col-sm-5": this.props.mode === 'custom'
                    })}>Total</label>
                    <div className="col-sm-7">
                        <div className="input-group amount-input">
                            <span className="input-group-addon">$</span>
                            <input className="form-control" type="number"
                                   placeholder="0.00"
                                   aria-describedby="Amount"
                                   value={this.total}
                                   readOnly/>
                        </div>
                    </div>
                </div>
            </div>
        );

    }
}

// Decorate with connect to read form values
const selector = formValueSelector('donation'); // <-- same as form name
export default connect(
    state => {
        return {
            amount: selector(state, 'amount'),
            contribute: selector(state, 'contribute'),
            will_contribute: selector(state, 'will_contribute'),
            mode: selector(state, 'mode')
        }
    }
)(DonationAmount)
