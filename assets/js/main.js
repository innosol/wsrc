$(function() {

    $('a[data-ajax="ajax"]').on('click', function(event){
        event.preventDefault();
        var h = jQuery(this).attr('aid');
        var form_name = jQuery(this).attr('form-name');
        if (form_name == 'ajiltan'){
            initial_ajiltanform(h);
        }
    });

    function initial_ajiltanform(id) {
        $.ajax({
            url : "/engineering/ajiltan/"+id,
            success : function(json) {
                //alert(json.emp_name);
                $('#id_emp_name').val(json.emp_name).trigger('change');
                $('#id_emp_lname').val(json.emp_lname).trigger('change');
                $('#id_emp_reg').val(json.emp_reg).trigger('change');
                //$('#id_emp_birth').val(json.emp_birth).trigger('change');
                $('#id_nas').val(json.nas).trigger('change');
                $('#id_ndd').val(json.ndd).trigger('change');
                $('#id_gender').val(json.gender).trigger('change');
                $('#id_position_id').val(json.position_id).trigger('change');
                $('#id_zereg').val(json.zereg).trigger('change');
                $('#id_naj').val(json.naj).trigger('change');
                $('#id_tzeaj').val(json.tzeaj).trigger('change');
                $('#id_phone').val(json.phone).trigger('change');
                $('#id_e_mail').val(json.e_mail).trigger('change');
                $('#id_mer_zereg').val(json.mer_zereg).trigger('change');

                //$('#ModalAjiltan').show();
            },
            error : function(xhr,errmsg,err) {
            }
        });
    };

    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});