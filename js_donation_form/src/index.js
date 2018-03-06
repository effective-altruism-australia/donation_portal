import charities from './charities.js';
import from_server from './from_server.js';
import './css/credit_card.css';
import './css/pledge.css';
import './css/process_steps.css';


Ractive.DEBUG = false;
$(function() {
    if (Pin === undefined) {
        Raven.captureMessage("Pin not defined");
    }

    var charity_database_ids = from_server.charity_database_ids;

    var ractive = new Ractive({
        el: '#ractive_base',
        template: '#ractive_template',
        data: {
            step: 1,
            recurring: null,
            donation_amount: null,
            from_server: from_server,
            is_custom_amount: false,
            pmt_method: '3',
            selected_charity_id: null,
            selected_charity: null,
            charities: charities,
            has_pin_errors: false,
            pin_error_description: null,
            pin_error_messages: null,
            submit_enabled: true,
            bank_reference: null,
            receipt_url: null,
            name: null
        },
        delimiters: ['[[', ']]'],

        set_step: function (step) {
            ractive.set({step: step});
        },

        restart_donation: function () {
            ractive.set({step: 1})
        },

        charity_click: function (name) {
            var id = charity_database_ids[name];

            var selected_charity = _.find(charities, function (x) {
                return x.name === name;
            });
            ractive.set({
                            step: 2,
                            selected_charity_id: id,
                            selected_charity: selected_charity
                        });
            // For paypal
            // document.getElementById('id_item_name').value = 'Donation: '.concat(selected_charity.website_label);
        },

        set_recurring: function (is_recurring) {
            ractive.set({recurring: is_recurring});
            if (is_recurring) {
                ractive.set_pmt_method('1');
            }
            // Clear validation errors, if any
            $('#donation-frequency-error').html("");
        },

        set_donation_amount: function (amount) {
            this.hide_other_donation_amount();
            ractive.set({donation_amount: amount});
            // Clear validation errors, if any
            $('#donation-amount-error').html("");
        },

        show_other_donation_amount: function () {
            ractive.set({donation_amount: ""});
            ractive.set({is_custom_amount: true});
        },

        hide_other_donation_amount: function () {
            ractive.set({is_custom_amount: false});
        },

        set_pmt_method: function (pmt_method) {
            ractive.set({pmt_method: pmt_method});
        },

        clear_pin_errors: function () {
            ractive.set({has_pin_errors: false});
        },

        set_pin_errors: function (error_description, messages) {
            ractive.set({has_pin_errors: true, pin_error_description: error_description, pin_error_messages: messages});
        },

        set_submit_disabled: function () {
            ractive.set({submit_enabled: false});
        },

        set_submit_enabled: function () {
            ractive.set({submit_enabled: true});
        }
    });

    // Ractive has rendered by now, so we can set up our validation.
    // (Because all the relevant elements are hidden and waiting.)
    var $form = $('#pledge-form');

    // We set up restrictions on credit card fields with jQuery.payment calls.
    $form.find('#cc-number').payment('formatCardNumber');
    $form.find('#cc-expiry').payment('formatCardExpiry');
    $form.find('#cc-cvc').payment('formatCardCVC');

    // Add custom validation methods to verify expiry and AMEX-ness of the credit card.
    $.validator.addMethod("cardNumber", function (value, element) {
        return $.payment.validateCardNumber(value);
    }, "Please enter a valid credit card number.");
    $.validator.addMethod("cardExpiry", function (value, element) {
        var expiry = $.payment.cardExpiryVal(value);
        return $.payment.validateCardExpiry(expiry);
    }, "Invalid card expiry.");
    $.validator.addMethod("cardCVC", function (value, element) {
        return $.payment.validateCardCVC(value);
    }, "Invalid CVC.");
    $.validator.addMethod("notAMEX", function (value, element) {
        return $.payment.cardType(value) !== 'amex';
    }, "Sorry, we do not accept American Express.");

    var validator = $form.validate({
        rules: {
            // Validators for cardName:
            cardName: {
                // Since we don't have a custom validator ("yet! growth mindset!"), we at least make it required:
                required: true
            },
            // This gives the validators to apply to the field with name "cardNumber":
            cardNumber: {
                cardNumber: true,
                notAMEX: true
            },
            // Again, validators to apply to the field with name "cardExpiry":
            cardExpiry: {
                cardExpiry: true
            },
            // Validators for CVC:
            cardCVC: {
                cardCVC: true
            }
        },
        highlight: function (element) {
            $(element).closest('.form-group').addClass('has-error');
        },
        unhighlight: function (element) {
            $(element).closest('.form-group').removeClass('has-error');
        }
    });


    function callPinAPI(callBack) {
        // Disable the submit button to prevent multiple clicks
        ractive.set_submit_disabled();

        // Clear prior errors.
        ractive.clear_pin_errors();

        // Convert expiry string into year and month values for Pin
        var expiry = $.payment.cardExpiryVal($('#cc-expiry').val());

        // Fetch details required for the createToken call to Pin
        var card = {
            // Removing spaces from cc-number is necessary for the Pin test cards to work
            number: $('#cc-number').val().replace(/\s/g, ''),
            name: $('#cc-name').val(),
            expiry_month: expiry.month,
            expiry_year: expiry.year,
            cvc: $('#cc-cvc').val(),
            address_line1: $('#address-line1').val(),
            address_line2: $('#address-line2').val(),
            address_city: $('#address-city').val(),
            address_state: $('#address-state').val(),
            address_postcode: $('#address-postcode').val(),
            address_country: $('#address-country').val()
        };

        Pin.createToken(card, handlePinResponse);

        function handlePinResponse(response) {
            if (response.response) {
                // Add the card token and ip address of the customer to the form
                // You will need to post these to Pin when creating the charge.
                callBack({card_token: response.response.token, ip_address: response.ip_address})
            } else {
                ractive.set_pin_errors(response.error_description, response.messages);
                // Re-enable the button.
                ractive.set_submit_enabled();
            }
        }
    }

    function submitForm(data) {
        // Disable the submit button to prevent multiple clicks
        ractive.set_submit_disabled();

        if (!data) {
            data = {}
        }
        // Extra fields that Django wants, that aren't in the form data:
        data['payment_method'] = ractive.get('pmt_method');
        data['recipient_org'] = ractive.get('selected_charity_id');
        data['recurring'] = ractive.get('recurring');

        // We needed to name the credit card fields for jQuery.validator to work
        // but we don't want to submit them, so we need to remove the fields here.
        var card_fields = $('fieldset#pin_credit_card_details input').map(function(_, elt) {return elt.name;});
        // Now we add all the data from the form:
        var formData = $('#pledge-form').serializeArray();
        for (var i = 0; i < formData.length; ++i) {
            var field_name = formData[i].name;
            if ($.inArray(field_name, card_fields) == -1) {
                data[field_name] = formData[i].value;
            }
        }

        $.ajax({
            url : "", // the endpoint
            type : "POST", // http method
            data : data,

            // handle a successful response
            success : function(json) {
                if (json['payment_method']==='1') {
                    ractive.set({
                        step: 3,
                        bank_reference: json['bank_reference']
                    });
                }
                else if (json['payment_method']==='3') {
                    ractive.set({
                        step: 3,
                        receipt_url: json['receipt_url']
                    });
                }

            },

            // handle a non-successful response
            error : function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
                var message = "Sorry, an unknown error occurred. Please check the data you entered, or try again."
                // Parse the errors
                if (xhr.status == 400) {
                    var response_data = JSON.parse(xhr.responseText);
                    if (response_data['error'] == 'form-error') {
                        var errors = response_data['form_errors']
                        message = Object.keys(errors).map(function (key) {
                           return errors[key].join(' ');
                        }).join(' ');
                    } else if (response_data['error'] == 'pin-error') {
                        message = response_data['pin_response']
                    }
                }
                // add the error to the dom
                $('#other-errors').html("<div class='error-text'>" + message + "</div>");
                // re-enable the button
                ractive.set_submit_enabled();
            }
        });


    }

    ractive.on('submit', function(event) {
        event.original.preventDefault();

        var validationFailed = false;

        if (!validator.checkForm()) {
            validator.showErrors();
            validationFailed = true;
        }

        if (ractive.get('recurring')==null) {
            $('#donation-frequency-error').html("<div class='error-text'>Please choose a donation frequency.</div>");
            validationFailed = true;
        }
        if (!ractive.get('donation_amount')) {
            $('#donation-amount-error').html("<div class='error-text'>Please choose a donation amount.</div>");
            validationFailed = true;
        }

        if (validationFailed) {
            // provide a generic message near the submit button that something has gone wrong.
            $('#other-errors').html("<div class='error-text'>Cannot submit incomplete form: Please see error message(s) in red above.</div>");
            return;
        }

        if (ractive.get('pmt_method') === "3") {
            callPinAPI(submitForm);
        } else {
            submitForm()
        }
    });
});