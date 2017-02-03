
jQuery(function ($) {

    var $form = $('#payment-form');

    /* Fancy restrictive input formatting via jQuery.payment library*/
    $('input[name=cardNumber]').payment('formatCardNumber');
    $('input[name=cardCVC]').payment('formatCardCVC');
    $('input[name=cardExpiry').payment('formatCardExpiry');

    jQuery.validator.addMethod("cardExpiry", function (value, element) {
        /* Parsing month/year uses jQuery.payment library */
        console.log(value)
        // value = $.payment.cardExpiryVal(value);
        // console.log(value)
        return this.optional(element) || /(0[1-9]|1[0-2]) \/ [0-9]{2}/.test(value);
    }, "Invalid expiration date.");

    validator = $form.validate({
        rules: {
            cardNumber: {
                required: true,
                creditcard: true
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
        if ($form.find('[name=cardNumber]').hasClass("success") &&
            $form.find('[name=cardName]').val().length > 1 &&
            $form.find('[name=cardExpiry]').hasClass("success") &&
            $form.find('[name=cardCVC]').val().length > 1) {
            return true;
        } else {
            return false;
        }
    }

    $form.find('.subscribe').prop('disabled', true);
    var readyInterval = setInterval(function () {
        if (paymentFormReady()) {
            $form.find('.subscribe').prop('disabled', false);
            clearInterval(readyInterval);
        }
    }, 250)



    });