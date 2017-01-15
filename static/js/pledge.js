/**
 * Created by andrew on 1/8/17.
 */
jQuery(function ($) {

    // Actions to trigger when the payment type buttons are selected
    function toggle_payment_type(e) {

        $("#id_payment_method")[0].value = this.value;

        $(this).addClass('btn-primary');
        $(this).siblings().removeClass('btn-primary');

        if ($("#id_btn_bank_transfer").hasClass('btn-primary')) {
            $("#id_bank_transfer").addClass('in');
        } else {
            $("#id_bank_transfer").removeClass('in');
        }
    }

    // Actions to trigger when the "other" donation amount is selected
    function toggle_amount(e) {

        $(this).addClass('btn-primary');
        $(this).siblings().removeClass('btn-primary');

        if ($("#id_other").hasClass('btn-primary')) {
            $("#id_formgroup_amount").addClass('in');
            document.getElementById("id_amount").value = "";
        } else {
            $("#id_formgroup_amount").removeClass('in');
            document.getElementById("id_amount").value = $(this)[0].value;
        }
    }

    // Setup listeners to trigger the functions above
    $('body').on('click', '.btn-amt', toggle_amount);
    $('body').on('click', '.btn-pmt-method', toggle_payment_type);

    // Hide fields we don't want to show
    $("#id_formgroup_amount").addClass('collapse');
    $("#id_bank_transfer").addClass('collapse');
    $("#id_recipient_org").hide();
    $("#id_payment_method").hide();

    // Temp fix, set recepient org.  This should be passed through from the previous page
    $("#id_recipient_org")[0].value = 1;

});
