var resp

$(document).ready(function(e){
	$('#upload').on('click', function () {
		var form_data = new FormData();
		var ins = document.getElementById('multiFiles').files.length;
		
		if(ins == 0) {
			$('#msg').html('<span style="color:red">Select at least one file</span>');
			return;
		}
		
		for (var x = 0; x < ins; x++) {
			form_data.append("files[]", document.getElementById('multiFiles').files[x]);
		}

		$.ajax({
			url: '/commerce/ui/images/',
			dataType: 'json', // what to expect back from server
			cache: false,
			contentType: false,
			processData: false,
			data: form_data,
			type: 'post',
			success: function (response) { // display success response
				$('#msg').html('');
				resp = response
				console.log(response)
				for (file in response.files){
					console.log(response.files[file]["htmlData"]);
					$('.imagesList').append(response.files[file]["htmlData"]);
				}
				$.each(response, function (key, data) {							
					if(key !== 'message') {
						$('#msg').append(key + ' -> ' + data + '<br/>');
					} else {
						$('#msg').append(data + '<br/>');
					}
				})
			},
			error: function (response) {
				$('#msg').html(response.message); // display error response
			}
		});
	});
});