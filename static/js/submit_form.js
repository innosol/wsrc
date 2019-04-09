function submitForm_modal_general_ajax(form_id){
  $(form_id).submit(function (e) {
    e.preventDefault();
    if($(form_id).data('submitted') === true)
    {
      console.log('form submitted!');
    }
    else 
    {
      $(form_id).data('submitted', true);
      var data = new FormData($(this).get(0));
      $(".se-pre-con").fadeIn();
      $.ajax({
          type: $(this).attr('method'),
          url: $(this).attr('action'),
          data: data,
          cache: false,
          contentType: false,
          processData: false,
          success: function (xhr, ajaxOptions, thrownError) {
              if ( $(xhr).find('.errorlist').length > 0 ) {
                  $(form_id).data('submitted', false);
                  $('#Modal_general').html(xhr);
              }
              else {
                  location.reload();
                  console.log(xhr);
              }
              $(".se-pre-con").hide();
          },
          error: function (xhr, ajaxOptions, thrownError) {
            $(form_id).data('submitted', false);
            if (xhr.status === 0){
              alert('Холболтын алдаа. Сүлжээгээ шалгана уу.');
            }
            else if (xhr.status == 404) {
              alert('Алдаа 404. Хуудас эсвэл мэдээлэл олдсонгүй.');
            }
            else if (xhr.status == 500) {
              alert('Алдаа 500. Серверийн дотоод алдаа.');
            }
            else if (xhr.status == 403) {
              alert('Алдаа 403. Хандах эрх олгогдоогүй байна.')
            }
            else {
              alert('Тодорхойгүй алдаа.');
              console.log(xhr);
              console.log(ajaxOptions);
              console.log(thrownError);
            }
            $(".se-pre-con").hide();
          }
      });
    }
  });
}







function submit_tz_choose_form(form_id){
  $(form_id).submit(function (e) {
    e.preventDefault();
    if($(form_id).data('submitted') === true)
    {
      console.log('form submitted!');
    }
    else 
    {
      $(form_id).data('submitted', true);
      var data = new FormData($(this).get(0));
      $(".se-pre-con").fadeIn();
      $.ajax({
          type: $(this).attr('method'),
          url: $(this).attr('action'),
          data: data,
          cache: false,
          contentType: false,
          processData: false,
          success: function (xhr, ajaxOptions, thrownError) {
              if ( $(xhr).find('.errorlist').length > 0 ) {
                  $(form_id).data('submitted', false);
                  $('#Modal_general').html(xhr);

              }
              else {
                  //location.reload();
                  //console.log(xhr);
                  var success_div_id = $(form_id).attr('success-div-id');

                  $(success_div_id).html(xhr);
                  $('#Modal_general').hide()


                  $(".overlay").hide();

                  $('#javascript-alert-container').fadeIn().delay(10000).fadeOut();
              }
              
              $(".se-pre-con").hide();
              
          },
          error: function (xhr, ajaxOptions, thrownError) {
            $(form_id).data('submitted', false);
            if (xhr.status === 0){
              alert('Холболтын алдаа. Сүлжээгээ шалгана уу.');
            }
            else if (xhr.status == 404) {
              alert('Алдаа 404. Хуудас эсвэл мэдээлэл олдсонгүй.');
            }
            else if (xhr.status == 500) {
              alert('Алдаа 500. Серверийн дотоод алдаа.');
            }
            else if (xhr.status == 403) {
              alert('Алдаа 403. Хандах эрх олгогдоогүй байна.')
            }
            else {
              alert('Тодорхойгүй алдаа.');
              console.log(xhr);
              console.log(ajaxOptions);
              console.log(thrownError);
            }
            $(".se-pre-con").hide();
          }
      });
    }
  });
}




function submit_ajax_turshilt(form_id){
  $(form_id).submit(function (e) {
    e.preventDefault();
    if($(form_id).data('submitted') === true)
    {
      console.log('form submitted!');
    }
    else 
    {
      $(form_id).data('submitted', true);
      var data = new FormData($(this).get(0));
      $(".se-pre-con").fadeIn();
      $.ajax({
          type: $(this).attr('method'),
          url: $(this).attr('action'),
          data: data,
          cache: false,
          contentType: false,
          processData: false,
          success: function (xhr, ajaxOptions, thrownError) {
              if (xhr.stat == "error"){
                alert('error');
                console.log(xhr.error_messages);
                var onj = jQuery.parseJSON(xhr.error_messages);
                //console.log(onj);
                $.each(onj, function(key, value) {
                    console.log(key, value);
                });
                //var p = xhr.error_messages;
                //var p = {
                //        "p1": {"value1": "happy"},
                //        "p2": "value2",
                //        "p3": "value3"
                //    };
                //for (var key in p) {
                //  if (p.hasOwnProperty(key)) {
                //    alert(key + " -> " + p[key]);
                //  }
                //}
              }
              else {
                alert('success');
              }
              
              $(".se-pre-con").hide();
              
          },
          error: function (xhr, ajaxOptions, thrownError) {
            $(form_id).data('submitted', false);
            if (xhr.status === 0){
              alert('Холболтын алдаа. Сүлжээгээ шалгана уу.');
            }
            else if (xhr.status == 404) {
              alert('Алдаа 404. Хуудас эсвэл мэдээлэл олдсонгүй.');
            }
            else if (xhr.status == 500) {
              alert('Алдаа 500. Серверийн дотоод алдаа.');
            }
            else if (xhr.status == 403) {
              alert('Алдаа 403. Хандах эрх олгогдоогүй байна.')
            }
            else {
              alert('Тодорхойгүй алдаа.');
              console.log(xhr);
              console.log(ajaxOptions);
              console.log(thrownError);
            }
            $(".se-pre-con").hide();
          }
      });
    }
  });
}