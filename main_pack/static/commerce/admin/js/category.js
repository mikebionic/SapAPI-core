
var category_fields = ['ownerCategory','categoryName','categoryDesc','categoryIcon']

$('newCategory').click(function(event){
	addCategory();
	clearField(".txt-input")
})

function clearField(field_class){
	$(field_class).val('');
}