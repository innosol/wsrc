var Script = function () {

	jQuery("a[data-data='modal']").click(function(e){
		var h = jQuery(this).attr('href');
		jQuery(h).show();
        jQuery('.overlay').show();
		jQuery('.modal1-uuganaa' + h).show().siblings('.modal1-uuganaa').hide();
		e.preventDefault();
	});

    jQuery("a[data-data='modal1']").click(function(e){
        var h = jQuery(this).attr('href');
        jQuery(h).show();
        jQuery('.overlay').show();
        jQuery('.modal1-uuganaa' + h).show().siblings('.modal1-uuganaa').hide();
        e.preventDefault();
    });


	jQuery("button[data-data='modal'].btn-primary").click(function(e){
		var h = jQuery(this).attr('href');
		jQuery(h).show();
        jQuery('.overlay').show();
		jQuery('.modal1-uuganaa' + h).show().siblings('.modal1-uuganaa').hide();
		e.preventDefault();
	});

	jQuery(".modal1-uuganaa .modal1-uuganaa-header button.close").click(function(e){
        jQuery('.overlay').hide();
		jQuery(this).parents(".modal1-uuganaa").hide();
	});

    jQuery(".modal1-uuganaa .modal1-uuganaa-footer button[data-data='modal'].btn-default").click(function(e){
        jQuery('.overlay').hide();
        jQuery(this).parents(".modal1-uuganaa").hide();
    });

    jQuery(".modal1-uuganaa .modal1-uuganaa-footer a[data-data='modal'].btn-default").click(function(e){
        jQuery('.overlay').hide();
        jQuery(this).parents(".modal1-uuganaa").hide();
    });
//ehlel
    jQuery("a[data-data='gold']").click(function(e){
        var h = jQuery(this).attr('href');
        jQuery(h).show();
        jQuery('.overlay').show();
        jQuery('.gold' + h).show().siblings('.gold').hide();
        e.preventDefault();
    });


    jQuery("button[data-data='gold'].btn-primary").click(function(e){
        var h = jQuery(this).attr('href');
        jQuery(h).show();
        jQuery('.overlay').show();
        jQuery('.gold' + h).show().siblings('.gold').hide();
        e.preventDefault();
    });

    jQuery(".gold .gold-header button.close").click(function(e){
        jQuery('.overlay').hide();
        jQuery(this).parents(".gold").hide();
    });

    jQuery(".gold .gold-footer button[data-data='gold'].btn-default").click(function(e){
        jQuery('.overlay').hide();
        jQuery(this).parents(".gold").hide();
    });

    jQuery(".gold .gold-footer a[data-data='gold'].btn-default").click(function(e){
        jQuery('.overlay').hide();
        jQuery(this).parents(".gold").hide();
    });
//togsgolt

    jQuery("form input[type='radio']").click(function(e){
        var h = jQuery(this).val();
        if(h == '1'){
            jQuery("#usolborloh").slideDown(200);
            jQuery('#usolborloh input').attr('required', "True")
        }
        else{
            jQuery("#usolborloh").slideUp(200); 
            jQuery('#usolborloh input').removeAttr('required')
        }
    });

}();

function table_add_rm(tbody_id, add_button_id) {
    var $table_body_univ = $(tbody_id);
    var $tr = $('tr', tbody_id).last();
    var i = $(tbody_id).size();
    $(add_button_id).click(function() {
        $tr.clone().appendTo($(tbody_id));
        $('tr', tbody_id).each(function(j){
        $('td:first', this).text(j+1);
    });
    $("tr:last td:last", tbody_id).append("<a href='#' id='rm-row'><i class='icon-remove-sign'></i></a>");
        i++;
        return false;
    });
    $('#rm-row', tbody_id).live('click', function() { 
        $(this).parents('tr').remove();
        i--;
        $('tr', tbody_id).each(function(j){
        $('td:first', this).text(j+1);
    });
    return false;
    });
};

function update()
{ 
    var now = new Date();
    var year = now.getFullYear();
    var value = $("#id_emp_reg").val();
    var on = "19"+value.substring(2,4);
    var nas = parseInt(year) - parseInt(on)
    var birth = on + "-" + value.substring(4,6) + "-" + value.substring(6,8)
    $("#id_nas").val(nas);
    $("#id_emp_birth").val(birth);
    if(parseInt(value.substring(8,9))%2 == 1 )
    $("#id_gender").val("Эр")
    else
        $("#id_gender").val("Эм")
};

function mergejliin_unemleh_check_changed(){
    if($('#mergejliin_unemleh_checkbox').is(':checked'))
        $('#mergejliin_unemleh_list').show();
    else
        $('#mergejliin_unemleh_list').hide();
};

function zovloh_engineer_cert_check_changed(){
    if($('#zovloh_engineer_cert_checkbox').is(':checked'))
        $('#zovloh_engineer_cert_list').show();
    else
        $('#zovloh_engineer_cert_list').hide();
    };

function update_mer_zereg(){
    if($('#id_mer_zereg option:selected').text() != "---------")
        $('#university_table').show();
    else
        $('#university_table').hide();
}

var formAjaxSubmit = function(form, modal) {
    $(form).submit(function (e) {
        e.preventDefault();
        var data = new FormData($(this).get(0));
        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            success: function (xhr, ajaxOptions, thrownError) {
                if ( $(xhr).find('.errorlist').length > 0 ) {
                    $(modal).find('.modal1-uuganaa-body').html(xhr);
                    if($('#mergejliin_unemleh_checkbox').is(':checked'))
                        $('#mergejliin_unemleh_list').show();
                    else
                        $('#mergejliin_unemleh_list').hide();

                    if($('#zovloh_engineer_cert_checkbox').is(':checked'))
                        $('#zovloh_engineer_cert_list').show();
                    else
                        $('#zovloh_engineer_cert_list').hide();
                    
                    if($('#id_mer_zereg option:selected').text() != "---------")
                        $('#university_table').show();
                    else
                        $('#university_table').hide();
                }
                else {
                    location.reload();
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
            }
        });
    });
};
var AjaxSubmit = function(form, modal) {
    $(form).submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function (xhr, ajaxOptions, thrownError) {
                if ( $(xhr).find('.tze-error').length > 0 ) {
                    var x = $(xhr).find(modal+' '+'.modal1-uuganaa-body').children()
                    $(modal).find('.modal1-uuganaa-body').html(x);
                }
                else {
                    location.reload();
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
            }
        });
    });
};

var LoadAjaxSubmit = function(form, modal) {
    $(form).submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function (xhr, ajaxOptions, thrownError) {
                if ( $(xhr).find('.errorlist').length > 0 ) {
                    $(modal).find('.modal1-uuganaa-body').html(xhr);
                }
                else {
                    location.reload();
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
            }
        });
    });
};