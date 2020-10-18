
var url = window.location.href

// Agregado para evitar que un onclick arruine las url
if(url.slice(-1) == '#')
{
	url = url.substring(0, url.length - 1);
}

function view(name) {
	
	var historico_url = url + '/' + name + '/historico'
	
	window.location = historico_url
}

var tabla_url = url + '/tabla?limit=4'

$.get(tabla_url, function(paises) {	

	var table_data = '';
	size = paises.length

	for(var i= 0; i < size; i++)
	{
		pais = paises[i]['country'];
		ganados = personas[i]['wins'];
		empatados = personas[i]['draws'];
		perdidos = personas[i]['loses'];

		table_data += '<tr>';
		table_data += '<td>'+pais+'</td>';
		table_data += '<td>'+ganados+'</td>';
		table_data += '<td>'+empatados+'</td>';
		table_data += '<td>'+perdidos+'</td>';
		table_data += '</tr>';

	}
	$("#list_table").append(table_data);
	

}); 

      
