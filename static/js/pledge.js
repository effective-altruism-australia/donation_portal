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
            document.getElementById("id_amount").value = this.value;
        }
    }

    // Actions to trigger when the second form page is shown
    function charity_select(e) {
        $("#id_formgroup_amount").addClass('collapse');
        $("#id_bank_transfer").addClass('collapse');
        $("#id_credit_card").addClass('collapse');
        $("#id_recipient_org").hide();
        $("#id_payment_method").hide();
        $("#id_recurring").parent().hide();
        $("#id_recipient_org")[0].value = this.children[0].value;

    }


    // Actions to trigger when the payment type buttons are selected
    function toggle_pmt_method(e) {
        $("#id_payment_method")[0].value = this.value;
        $(".payment_option").collapse('hide')
        $(this.getAttribute('data-target')).collapse('show')

        if ($("#id_btn_cc").hasClass('btn-primary')) {
            $(".cc-form").prop('required',true);
        } else {
            $(".cc-form").prop('required',false);
            $("#id_pledge_form").validate({
               ignore: ".ignore, :hidden"
            })
        }

    }

    // Actions to trigger when pledge recurring buttons are clicked
    function toggle_recurring(e) {

        if ($("#id_btn_recurring").hasClass('btn-primary')) {
            $("#id_recurring")[0].checked = true;
        } else {
            $("#id_recurring")[0].checked = false;
        }
    }

    // Setup listeners to trigger the functions above
    $('body').on('click', '.btn-toggle', toggle);
    $('body').on('click', '.btn-amt', toggle_amount);
    $('body').on('click', '.charityClick', charity_select);
    $('body').on('click', '.btn-pmt-method', toggle_pmt_method);
    $('body').on('click', '.btn-recurring', toggle_recurring);


});
