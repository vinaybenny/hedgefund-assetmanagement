
$(document).ready(function () {

    // This function corrects the default behavior of ignoring the form fields on inactive tabs.
    /*$("#simparams").validate({
        ignore: ""
    });*/

    /* This function shows and hides sections for range parameter entry in SubmitParamsPage.html,
    based on the checkbox selection.*/
    $('[id^=fig_]').click(function showGraphRangeSection() {
        var pClass = '.' + $(this).val();
        if ($(this).is(':checked')) {
            $(pClass).show();
        } else {
            $(pClass).hide();
        }
    });
    

})

// This function returns fires a JSON POST request for running a fig_2 class simulation
function fig_2_jsonPost(simParams) {
    jsonObj = {
        "simType": 2,
        "initWealth": simParams.initWealth,
        "relriskAversion": simParams.relriskAversion,
        "timeHorizon": simParams.timeHorizon,
        "riskfreeRate": simParams.riskfreeRate,
        "mktriskPrice": simParams.mktriskPrice,
        "liquidPercent": simParams.liquidPercent,
        "maxLeverage": simParams.maxLeverage,

        "fundManagefee_hf": simParams.fundManagefee_hf,
        "performFee_hf": simParams.performFee_hf,

        "fundManagefee_mf": simParams.fundManagefee_mf,
        "interval": simParams.interval,
        "simSize": simParams.simSize,

        "alpha_hf_min": simParams.alpha_hf_min_fig_2,
        "alpha_hf_max": simParams.alpha_hf_max_fig_2,
        "leverage_hf_min": simParams.leverage_hf_min_fig_2,
        "leverage_hf_max": simParams.leverage_hf_max_fig_2,

        // Hard Coding the user- CHANGE LATER DURING AUTHENTICATION/AUTHORIZATION
        "user": "/api/v1/user/1/"
    };
    
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/api/v1/simulationmodel/",
        data: JSON.stringify(jsonObj),
        contentType: "application/json",
        dataType: "json",
        success: function (data) {
            var newGraphcount = document.getElementById("StatsPage_badge").innerHTML
            if (newGraphcount === "")
            { newGraphcount = 1; }
            else
            { newGraphcount = parseInt(newGraphcount) + 1; }
            document.getElementById("StatsPage_badge").innerHTML = newGraphcount;

        }
    });
    alert("Parameters Submitted!");
}

/* This function converts the form in the SubmitParamsPage.html into a JSON object and posts it to the web
service defined by webservicejson.*/
function postsimparams() {

    // Define variables for checkboxes
    var fig2chk, fig3chk, fig4chk, fig5chk, fig6chk, fig7chk, fig8chk, fig9chk;

    var varObj = {
        // Get fixed variable values in correct format
        "initWealth": parseFloat(document.getElementById("initWealth").value, 10),
        "relriskAversion": parseInt(document.getElementById("relriskAversion").value),
        "timeHorizon": parseInt(document.getElementById("timeHorizon").value),
        "riskfreeRate": parseFloat(document.getElementById("riskfreeRate").value, 10),
        "mktriskPrice": parseFloat(document.getElementById("mktriskPrice").value, 10),
        "liquidPercent": parseFloat(document.getElementById("liquidPercent").value, 10),
        "maxLeverage": parseFloat(document.getElementById("maxLeverage").value, 10),

        "fundManagefee_hf": parseFloat(document.getElementById("fundManagefee_hf").value, 10),
        "performFee_hf": parseFloat(document.getElementById("performFee_hf").value, 10),

        "fundManagefee_mf": parseFloat(document.getElementById("fundManagefee_mf").value, 10),
        "interval": parseInt(document.getElementById("interval").value),
        "simSize": parseInt(document.getElementById("simSize").value),

        // Get range variable values
        "alpha_hf_min_fig_2": parseFloat(document.getElementById("alpha_hf_min_fig_2").value, 10),
        "alpha_hf_max_fig_2": parseFloat(document.getElementById("alpha_hf_max_fig_2").value, 10),
        "leverage_hf_min_fig_2": parseFloat(document.getElementById("leverage_hf_min_fig_2").value, 10),
        "leverage_hf_max_fig_2": parseFloat(document.getElementById("leverage_hf_max_fig_2").value, 10),
        "alpha_hf_min_fig_3": parseFloat(document.getElementById("alpha_hf_min_fig_3").value, 10),
        "alpha_hf_max_fig_3": parseFloat(document.getElementById("alpha_hf_max_fig_3").value, 10),
        "alpha_mf_min_fig_3": parseFloat(document.getElementById("alpha_mf_min_fig_3").value, 10),
        "alpha_mf_max_fig_3": parseFloat(document.getElementById("alpha_mf_max_fig_3").value, 10),
        "alpha_hf_min_fig_4": parseFloat(document.getElementById("alpha_hf_min_fig_4").value, 10),
        "alpha_hf_max_fig_4": parseFloat(document.getElementById("alpha_hf_max_fig_4").value, 10),
        "performFee_hf_min_fig_4": parseFloat(document.getElementById("performFee_hf_min_fig_4").value, 10),
        "performFee_hf_max_fig_4": parseFloat(document.getElementById("performFee_hf_max_fig_4").value, 10),
        "volatility_hf_min_fig_5": parseFloat(document.getElementById("volatility_hf_min_fig_5").value, 10),
        "volatility_hf_max_fig_5": parseFloat(document.getElementById("volatility_hf_max_fig_5").value, 10),
        "leverage_hf_min_fig_5": parseFloat(document.getElementById("leverage_hf_min_fig_5").value, 10),
        "leverage_hf_max_fig_5": parseFloat(document.getElementById("leverage_hf_max_fig_5").value, 10),
        "alpha_hf_min_fig_6": parseFloat(document.getElementById("alpha_hf_min_fig_6").value, 10),
        "alpha_hf_max_fig_6": parseFloat(document.getElementById("alpha_hf_max_fig_6").value, 10),
        "beta_min_fig_6": parseFloat(document.getElementById("beta_min_fig_6").value, 10),
        "beta_max_fig_6": parseFloat(document.getElementById("beta_max_fig_6").value, 10),
        "volatility_ifmf_min_fig_7": parseFloat(document.getElementById("volatility_ifmf_min_fig_7").value, 10),
        "volatility_ifmf_max_fig_7": parseFloat(document.getElementById("volatility_ifmf_max_fig_7").value, 10),
        "alpha_mf_min_fig_7": parseFloat(document.getElementById("alpha_mf_min_fig_7").value, 10),
        "alpha_mf_max_fig_7": parseFloat(document.getElementById("alpha_mf_max_fig_7").value, 10),
        "alpha_hf_min_fig_9": parseFloat(document.getElementById("alpha_hf_min_fig_9").value, 10),
        "alpha_hf_max_fig_9": parseFloat(document.getElementById("alpha_hf_max_fig_9").value, 10),
        "leverage_hf_min_fig_9": parseFloat(document.getElementById("leverage_hf_min_fig_9").value, 10),
        "leverage_hf_max_fig_9": parseFloat(document.getElementById("leverage_hf_max_fig_9").value, 10),
        "jumpsize_fig_9": parseFloat(document.getElementById("jumpsize_fig_9").value, 10),
        "alpha_hf_fig_8": parseFloat(document.getElementById("alpha_hf_fig_8").value, 10),
        "leverage_hf_fig_8": parseFloat(document.getElementById("leverage_hf_fig_8").value, 10),
        "jumpsize_fig_8": parseFloat(document.getElementById("jumpsize_fig_8").value, 10)
    }


    // Check for the graphs that need to be simulated.
    if ($("#fig_2").prop("checked")) {
        fig_2_jsonPost(varObj);
        fig2chk = true;
    }
    else {
        fig2chk = false;
    }

    if ($("#fig_3").prop('checked')) {
        fig3chk = true;
    }

    else {
        fig3chk = false;
    }


    if ($("#fig_4").prop('checked'))
        fig4chk = true;
    else
        fig4chk = false;

    if ($("#fig_5").prop('checked'))
        fig5chk = true;
    else
        fig5chk = false;

    if ($("#fig_6").prop('checked'))
        fig6chk = true;
    else
        fig6chk = false;

    if ($("#fig_7").prop('checked'))
        fig7chk = true;
    else
        fig7chk = false;

    if ($("#fig_8").prop('checked'))
        fig8chk = true;
    else
        fig8chk = false;

    if ($("#fig_9").prop('checked'))
        fig9chk = true;
    else
        fig9chk = false;

    // Move code to validate function
    if (!(fig2chk || fig3chk || fig4chk || fig5chk || fig6chk || fig7chk || fig8chk || fig9chk)) {
        // Define code to validate that at least one graph has been selected.
        alert("At least one graph need to be selected before submission");
        return false;
    }
}



function validateMaxvals() {

}


