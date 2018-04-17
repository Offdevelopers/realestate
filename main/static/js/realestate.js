function increase_stat(stat, id){
	 $.get("/increase_stat", {'stat':stat, 'id':id}, function(){})
}