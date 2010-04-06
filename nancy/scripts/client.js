// Comprueba que un campo es de tipo text o password y no está vacío.
function notEmpty(field)
{
	if((field.tagName!="INPUT" && field.tagName!="TEXTAREA") || (field.type!="text" && field.type!="password" && field.type!="textarea"))
	{
		alert("Invalid argument.");
		return false;
	}
	if(field.value.replace(/ /g, "") == "")
	{
		if(field.id == "") alert(field.name+" cannot be an empty string.");
		else alert(field.id+" cannot be an empty string.");
		return false;
	}
	return true;
}
