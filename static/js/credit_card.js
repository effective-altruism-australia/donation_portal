
validate_cc = function () {

    var $form = $('#id_pledge_form');

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
};
