// modal general id-tai modal dotor data load hiih haruulah function
function modal_general_load_show(url){
  $('#Modal_general').load(url, function (response, status, xhr) {
    if(status == "error"){
      if (xhr.status === 0){
        alert('Холболтын алдаа. Сүлжээгээ шалгана уу.');
      }
      else if (xhr.status == 404) {
        alert('Алдаа 404. Хуудас эсвэл мэдээлэл олдсонгүй.');
      }
      else if (xhr.status == 500) {
        alert('Алдаа 500. Серверийн дотоод алдаа.')
      }
      else if (xhr.status == 403) {
        alert('Алдаа 403. Хандах эрх олгогдоогүй байна.')
      }
      else {
        alert('Тодорхойгүй алдаа.');
        console.log(response);
        console.log(status);
        console.log(xhr.status);
      }

    }
    else
    {
      $('#Modal_general').show().siblings('.modal1-uuganaa').hide();
      $("#Modal_general form").attr("action", url);
      $('.overlay').show();

      $(".input-small.zar").keyup(function( event ) {
        if (!/^\d*\.?\d*$/.test($(this).val())) {
          $(this).val('0');
        }
      });
    }
  });

}

// div_id id-tai div dotor data load hiij bairluulah function
function div_load_function(url, div_id){
  $(div_id).load(url, function (response, status, xhr) {
    if(status == "error"){
      if (xhr.status === 0){
        alert('Холболтын алдаа. Сүлжээгээ шалгана уу.');
      }
      else if (xhr.status == 404) {
        alert('Алдаа 404. Хуудас эсвэл мэдээлэл олдсонгүй.');
      }
      else if (xhr.status == 403) {
        alert('Алдаа 403. Хандах эрх олгогдоогүй байна.')
      }
      else if (xhr.status == 500) {
        alert('Алдаа 500. Серверийн дотоод алдаа.')
      }
      else {
        alert('Тодорхойгүй алдаа.');
        console.log(response);
        console.log(status);
        console.log(xhr.status);
      }
    }
  });
}


$('.ajax_div_load').click(function(){
  var url = ($(this).attr('url-data'));
  modal_general_load_show(url);
});

// tusgai zovshoorliin huseltiin delgerengui dotor ajax link daragdahad load hiih code
$('#huselt_delgerengui_div').on('click', '.ajax_div_load', function(e){
  e.preventDefault();
  var url = ($(this).attr('url-data'));
  modal_general_load_show(url);
});

// baiguullaga menu baiguullaga delgerengui div dotor ajax link daragdahad load hiih code
$('#baiguullaga_delgerengui_div').on('click', '.ajax_div_load', function(e){
  e.preventDefault();
  var url = ($(this).attr('url-data'));
  modal_general_load_show(url);
});

// hunii noots menu ajiltan list div dotor ajax link daragdahad modal general load hiih code
$('#ajiltan_list').on('click', '.ajax_div_load', function(e){
  e.preventDefault();
  var url = ($(this).attr('url-data'));
  modal_general_load_show(url);
});

// tonog tohooromjiin list div dotor ajax link daragdahad modal general load hiih code
$('#tonog_tohooromj_list').on('click', '.ajax_div_load', function(e){
  e.preventDefault();
  var url = ($(this).attr('url-data'));
  modal_general_load_show(url);
});

$('#ua_list').on('click', '.ajax_div_load', function(e){
  e.preventDefault();
  var url = ($(this).attr('url-data'));
  modal_general_load_show(url);
});


// modal general dotor ajax button daragdahad modal general load hiih code
$('#Modal_general').on('click', '.ajax_div_load', function(e){
  e.preventDefault();
  var url = ($(this).attr('url-data'));
  modal_general_load_show(url);
});

// ajax link daragdahad todorhoi div-d ajax load hiih code
$('.ajax_delgerengui_load').click(function(){
  var url = ($(this).attr('url-data'));
  var div_id = ($(this).attr('div-id'));  // medeellig bairluulah div
  div_load_function(url, div_id);
});

// ajax ehleh uyd hiih code
//$(document).ajaxStart(function() {
        //$(this).show();
//        alert('ajax start');
//    })
//    .ajaxStop(function() {
        //$(this).hide();
//        alert('ajax stop');
//    });

// modal general hide hiih code
$('#Modal_general').on('click', '.close', function(e){
  e.preventDefault();
  //alert('success');
  $('#Modal_general').hide();
  $('.overlay').hide();
});

$('#Modal_general').on('click', '[data-data="close"]', function(e){
  e.preventDefault();
  //alert('success');
  $('#Modal_general').hide();
  $('.overlay').hide();
});

// modal general hide hiih code
$('#Modal_general').on('click', '.div-close-button', function(e){
  e.preventDefault();
  //alert('success');
  $('#Modal_general').hide();
  $('.overlay').hide();
});


