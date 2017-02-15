
validate_cc = function () {

        var $form = $('#id_pledge_form');

        /* Fancy restrictive input formatting via jQuery.payment library */
        $('input[name=cardNumber]').payment('formatCardNumber');
        $('input[name=cardCVC]').payment('formatCardCVC');
        $('input[name=cardExpiry]').payment('formatCardExpiry');

        jQuery.validator.addMethod("cardExpiry", function (value, element) {
            return this.optional(element) || /(0[1-9]|1[0-2]) \/ [0-9]{2}/.test(value);
        }, "Invalid expiration date.");

        jQuery.validator.addMethod("notAMEX", function (value, element) {
            return this.optional(element) || ! /^3[47]/.test(value);
        }, "Sorry, we do not currently accept American Express");

        validator = $form.validate({
            rules: {
                cardNumber: {
                    required: true,
                    creditcard: true,
                    notAMEX: true
                },
                cardExpiry: {
                    required: true,
                    cardExpiry: true
                },
            },
            highlight: function (element) {
                $(element).closest('.form-control').removeClass('success').addClass('error');
            },
            unhighlight: function (element) {
                $(element).closest('.form-control').removeClass('error').addClass('success');
            },
            errorPlacement: function (error, element) {
                $(element).closest('.form-group').append(error);
            }
        });

        paymentFormReady = function () {
            if (($form.find('[name=cardNumber]').hasClass("success") &&
                $form.find('[name=cardName]').val().length > 1 &&
                $form.find('[name=cardExpiry]').hasClass("success") &&
                $form.find('[name=cardCVC]').val().length > 1) || ($("#id_btn_bank_transfer").hasClass('btn-primary'))) {
                return true;
            } else {
                return false;
            }
        };

        $form.find('.subscribe').prop('disabled', true);
    };
