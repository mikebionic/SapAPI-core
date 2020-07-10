// other UI actions
$('.newIconBtn').click(function(e){
  $('.newIconCard').show('slow');
  $('.minimizeIcon').show('slow');
  $('.newIconBtn').hide('slow');
});
$('.addIconBtn').click(function(e){
  $('.newIconBtn').show('slow');
  $('.newIconCard').hide('slow');
  $('.minimizeIcon').hide('slow');
});
$('.minimizeIcon').click(function(e){
  $('.newIconBtn').show('slow');
  $('.newIconCard').hide('slow');
  $('.minimizeIcon').hide('slow');
});
//////

// $('body').delegate('.removeIconBtn','click',function(){
// 	ownerId = $(this).attr('ownerId');
// 	name = $(this).attr('name');
// 	icon_category = $(this).attr('icon_category');
// 	formData = {
// 		'category':icon_category,
// 		'name':name
// 	}
// 	removeIcon(formData,url=url_prefix+'/ui/svg-icons/');
// });


// var removeIcon = function(formData,url){
// 	$.ajax({
// 		contentType:"application/json",
// 		dataType:"json",
// 		data:JSON.stringify(formData),
// 		type : 'DELETE',
// 		url : url,
// 		success: function(response){
// 			if(response.status == 'deleted'){
// 				successToaster(response.responseText);
// 				$('.'+formId).val(response[formId]);
// 			}
// 			else if(response.status == 'regGenerated'){
// 				warningToaster(response.responseText);
// 				$('.'+response.regNoForm).val(response.regNo);
// 			}
// 			else{errorToaster(response.responseText);}
// 		}
// 	})
// }

$(document).ready(function(e){
	$('#upload').on('click', function () {
		var form_data = new FormData();
		var ins = document.getElementById('multiFiles').files.length;
		
		if(ins == 0) {
			alert('Select at least one file');
			return;
		}
		
		for (var x = 0; x < ins; x++) {
			form_data.append("files[]", document.getElementById('multiFiles').files[x]);
		}

		$.ajax({
			url: url_prefix+'/ui/svg-icons/',
			dataType: 'json',
			cache: false,
			contentType: false,
			processData: false,
			data: form_data,
			type: 'POST',
			success: function (response){
			  $('.newIconBtn').show('slow');
			  $('.newIconCard').hide('slow');
			  $('.minimizeIcon').hide('slow');
				for (file in response.data){
					responseIcon = response.data[file]["htmlData"];
					$('.iconsList #tab-Others .categoryIcons').append(responseIcon);
				}
			},
			error: function (response) {
				$('#msg').html(response.message);
			}
		});
	});
});