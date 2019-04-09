var Script = function () {

	jQuery("a[data-data='modal']").click(function(e){
		var h = jQuery(this).attr('href');
		jQuery(h).show();
		jQuery('.modal2' + h).show().siblings('.modal2').hide();
		e.preventDefault();
	});

	jQuery("form input[type='radio']").click(function(e){
        var h = jQuery(this).val();
        if(h == '1'){
            jQuery(this).parents('form').children().children('button').addClass("btn btn-success");
            jQuery("#usug").slideDown(200);
            jQuery('#usug input').attr('required', "True")

        }
        else{
            jQuery("#usug").slideUp(200); 
            jQuery(this).parents('form').children().children('button').removeClass("btn-success").addClass("btn-primary");  
            jQuery('#usug input').removeAttr('required')
        }
    });
	

}();