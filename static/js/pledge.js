/**
 * Created by andrew on 1/8/17.
 */
jQuery(function ($) {

    // Actions to change button colours within a group when clicked
    function toggle(e) {
        $(this).addClass('btn-primary');
        $(this).siblings().removeClass('btn-primary');
    }

    // Actions to trigger when the "other" donation amount is selected
    function toggle_amount(e) {

        if ($("#id_other").hasClass('btn-primary')) {
            $("#id_formgroup_amount").addClass('in');
            document.getElementById("id_amount").value = "";
        } else {
            $("#id_formgroup_amount").removeClass('in');
            console.log(this.value)
            document.getElementById("id_amount").value = this.value;
        }
    }

    // Actions to trigger when the second form page is shown
    function charity_select(e) {
        $("#id_formgroup_amount").addClass('collapse');
        $("#id_bank_transfer").addClass('collapse');
        $("#id_recipient_org").hide();
        $("#id_payment_method").hide();
        $("#id_recurring").parent().hide();
        console.log(this, this.value)
        $("#id_recipient_org")[0].value = this.children[0].value;

    }


    // Actions to trigger when the payment type buttons are selected
    function toggle_pmt_method(e) {

        $("#id_payment_method")[0].value = this.value;
        console.log($("#id_payment_method")[0].value, this.value)

        if ($("#id_btn_bank_transfer").hasClass('btn-primary')) {
            $("#id_bank_transfer").addClass('in');
        } else {
            $("#id_bank_transfer").removeClass('in');
        }
    }

    // Actions to trigger when pledge recurring buttons are clicked
    function toggle_recurring(e) {
        $("#id_recurring")[0].checked = parseInt(this.children[0].value); // This could be done better I'm sure!
    }

    // Setup listeners to trigger the functions above
    $('body').on('click', '.btn-toggle', toggle);
    $('body').on('click', '.btn-amt', toggle_amount);
    $('body').on('click', '.charityClick', charity_select);
    $('body').on('click', '.btn-pmt-method', toggle_pmt_method);
    $('body').on('click', '.btn-recurring', toggle_recurring);


});
