
gen_reg_no_data = {
	"RegNumTypeId": "sale_order_invoice_code"
}
// res = service_post(gen_reg_no_data, '/ls/api/gen-reg-no', 'POST')
// console.log(res)


function service_post(formData, url, type){
	$.ajax({
		contentType: "application/json",
		dataType: "json",
		data: JSON.stringify(formData),
		type: type,
		url: url,
	})
	.done(function(response){
		console.log(response.responseText);
		return response;
	})
}

// do_post = async () => {
// 	const location = window.location.hostname;
// 	const response = await fetch(
// 		`http://${location}:9000/api/sensors/`
// 	);
// }

// do_post = async () => {
// 	const location = window.location.hostname;
// 	const settings = {
// 		method: 'POST',
// 		headers: {
// 			Accept: 'application/json',
// 			'Content-Type': 'application/json',
// 		}
// 	};
// 	fetch(`http://${location}:9000/api/sensors/`, settings)
// 		.then(response => response.json())
// 		.then(data => console.log(data))
// }


// 	try {
// 		const fetchResponse = await do_post()
// 		const data = await fetchResponse.json();
// 		return data;
// 	} catch (e) {
// 		return e;
// 	}



const apiUrl = "http://127.0.0.1:5000/ls/api/resources/"
async function fetchResources() {
    const response =  await fetch(apiUrl)
    const json = await response.json()
		await console.log(json)
		// .catch(error => console.error(error))
}
fetchResources()