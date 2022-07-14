// Sidebar toggle
var mainAvatar = document.querySelector('.workspace-sidebar-toggle');
var workspace = document.querySelector('.workspace-data');
mainAvatar.onclick = function(){
	workspace.classList.toggle('open-sidebar');
}

// Sidebar selected toggle
var filters = document.querySelectorAll('.workspace-sidebar-filter li');
for(var f = 0; f < filters.length; f++){
	filters[f].onclick = function(){
		this.classList.toggle('selected');
	}
}

// Toggle between cards and table view
var toggler = document.querySelector('.workspace-toggles');
var table = document.querySelector('.workspace-table table');
var cards = document.querySelector('.workspace-table ul');
toggler.onclick = function(e){
		var button;
	if(e.target.tagName.toLowerCase() === 'button'){
		button = e.target;
	} else if(e.target.tagName.toLowerCase() === 'i'){
		button = e.target.parentNode;
	};
	
	if(button && !button.classList.contains('toggle-selected')){
		cards.style.display = button.value === 'cards' ? 'block' : 'none';
		table.style.display = button.value === 'table' ? 'table' : 'none';
		this.children[0].classList.toggle('toggle-selected');
		this.children[1].classList.toggle('toggle-selected');
	}
	
	
}