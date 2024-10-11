import http          from 'node:http';
import {Server}      from 'socket.io';
import url from 'url';
import {readFile}    from 'node:fs';
import path from 'path';
import bd from 'mongodb';
const {MongoClient} = bd;

/////////////////////////////////// Variables ///////////////////////////////////
var tipos = { "html": "text/html", "css": "text/css"};
var luminosidadAct = 100;
var temperaturaAct = 20; 
var humoAct = 0; 
var umbralTempMax = 35;
var umbralLumMax = 200;
var umbralHumoMax = 20;
var umbralHumoMax2 = 50;
var umbralTempMin = 10;
var umbralLumMin = 50;
var persiana = false; 
var aireAcondicionado = false;
var antiincendios = false; 

/////////////////////////////////// Funcion Agente ///////////////////////////////////
function agente(){
	var resultado = {mensajes: []};

	if( temperaturaAct > umbralTempMax){
		aireAcondicionado = true;
		resultado.mensajes.push("ALARMA: LÍMITE MÁXIMO DE TEMPERATURA");
		console.log("** Agente: se sobrepasa el limite máximo de temperatura **");
	}
	if( temperaturaAct < umbralTempMin){
		aireAcondicionado = false;
		resultado.mensajes.push("ALARMA: LÍMITE MÍNIMO DE TEMPERATURA");
		console.log("** Agente: se sobrepasa el limite mínimo de temperatura **");
	}

	if( luminosidadAct > umbralLumMax ){
		persiana = true;
		resultado.mensajes.push("ALARMA: LÍMITE MÁXIMO DE LUMINOSIDAD");
		console.log("** Agente: se sobrepasa el limite máximo de luminosidad **");
	}
	if( luminosidadAct < umbralLumMin ){
		persiana = false;
		resultado.mensajes.push("ALARMA: LÍMITE MÍNIMO DE LUMINOSIDAD");
		console.log("** Agente: se sobrepasa el limite mínimo de luminosidad **");
	}

	if( humoAct > umbralHumoMax ){
		persiana = false;
		resultado.mensajes.push("ALARMA: LÍMITE 1 MAXIMO DE HUMO");
		console.log("** Agente: se sobrepasa el limite 1 de humo **");

	}
	if( humoAct > umbralHumoMax2 ){
		persiana = false;
		antiincendios = true;
		resultado.mensajes.push("ALARMA: LÍMITE 2 MAXIMO DE HUMO");
		console.log("** Agente: se sobrepasa el limite 2 de humo **");
	}
	if( humoAct < umbralHumoMax ){
		antiincendios = false;
	}

	if( humoAct < umbralHumoMax && luminosidadAct > umbralLumMax ){
		persiana = true;
	}

	return resultado;
}

/////////////////////////////////// Servidor ///////////////////////////////////
var httpServer = http.createServer( (request, response) => {
		var direccion = url.parse(request.url).pathname;

		if( direccion == "/"){
			direccion = "/usuario.html";
		} else if(direccion == "/sensores") {
			direccion = "/sensores.html";
		}
		var archivo = path.join(process.cwd(), direccion);

		readFile(archivo, function(err, data){
			if (!err) {
				var extension = path.extname(archivo).split(".")[1];
				var tipo = tipos[extension];
				response.writeHead(200, tipo);
				response.write(data);
			}
			else {
				response.writeHead(500, {"Content-Type": "text/plain"});
				response.write('Error de lectura en el fichero: '+ direccion);
			}
			response.end();

		});
	}
);

MongoClient.connect("mongodb://localhost:27017/", { useUnifiedTopology: true }, function(err, db) {
	if (err) {
		console.error("Error al conectar con bd:", err);
		return;
	}

	httpServer.listen(8080);
	var io = new Server(httpServer);
	var baseDatos = db.db("mibd");
	var n=0;

	baseDatos.createCollection("historialCambios", function(err, collection){
		if (err) {
            console.error("Error al crear la colección:", err);
            return;
        }

		io.sockets.on('connection', function(client) {
			var id = "Clienten con id: " + n;
			n++;
			console.log('Nueva conexión de ' + client.request.socket.remoteAddress + ':' + client.request.socket.remotePort);
			client.emit('my-address', {host:client.request.socket.remoteAddress, port:client.request.socket.remotePort, id:id});


			client.on('output-evt', function () {
				client.emit('output-evt',  {temperatura: temperaturaAct, luminosidad: luminosidadAct, humo: humoAct, estadoAC: aireAcondicionado,  estadoPersiana: persiana, estadoIncendio: antiincendios });
			});

			var agenteInicio = agente();
			if( agenteInicio.mensajes.length > 0 )
				io.sockets.emit('all-alarm', agenteInicio.mensajes);
	
			io.sockets.emit('all-values', {temperatura: temperaturaAct, luminosidad: luminosidadAct, humo: humoAct, estadoAC: aireAcondicionado,  estadoPersiana: persiana, estadoIncendio: antiincendios } );

			client.on('obtenerHistorial', function () {
				collection.find().toArray(function(err, results){
					client.emit('obtenerHistorial', results);
				});
			});

			client.on('AC', function (data) {
				if(aireAcondicionado){
					aireAcondicionado = false;
				} else {
					aireAcondicionado = true;
				}

				var insertion =  {client: data.datos.client, change: data.datos.change, port: data.datos.port, time: data.datos.time};
				collection.insertOne(insertion, {safe:true},  function(err, result) {});


				console.log('Modificado el estado del aire acondicionado');
				io.sockets.emit('all-values', {temperatura: temperaturaAct, luminosidad: luminosidadAct, humo: humoAct, estadoAC: aireAcondicionado,  estadoPersiana: persiana, estadoIncendio: antiincendios } );

			});

			client.on('persiana', function (data) {
				if(persiana){
					persiana = false;
				} else {
					persiana = true;
				}

				var insertion =  {client: data.datos.client, change: data.datos.change, port: data.datos.port, time: data.datos.time};
				collection.insertOne(insertion, {safe:true},  function(err, result) {});


				console.log('Modificado el estado de la persiana');
				io.sockets.emit('all-values', {temperatura: temperaturaAct, luminosidad: luminosidadAct, humo: humoAct, estadoAC: aireAcondicionado,  estadoPersiana: persiana, estadoIncendio: antiincendios } );
			});

			client.on('humo', function (data) {
				if(antiincendios){
					antiincendios = false;
				} else {
					antiincendios = true;
				}

				var insertion =  {client: data.datos.client, change: data.datos.change, port: data.datos.port, time: data.datos.time};
				collection.insertOne(insertion, {safe:true},  function(err, result) {});

				console.log('Modificado el estado del Sistema antiincendios');
				io.sockets.emit('all-values', {temperatura: temperaturaAct, luminosidad: luminosidadAct, humo: humoAct, estadoAC: aireAcondicionado,  estadoPersiana: persiana, estadoIncendio: antiincendios  } );
			});


			client.on('sensor-changes', function(data) {
				luminosidadAct = data.luminosidadNew;
				temperaturaAct = data.temperaturaNew;
				humoAct = data.humoNueva;

				console.log('Modificado el estado de los sensores');
				var insertion = {client: data.datos.client, change: data.datos.change, port:data.datos.port,time: data.datos.time};
				collection.insertOne(insertion, {safe:true},  function(err, result) {});

				var agenteVar = agente();
				io.sockets.emit('all-values', {temperatura: temperaturaAct, luminosidad: luminosidadAct, humo: humoAct, estadoAC: aireAcondicionado,  estadoPersiana: persiana, estadoIncendio: antiincendios  } );

				if( agenteVar.mensajes.length > 0 ) 
					io.sockets.emit('all-alarm', agenteVar.mensajes);
			});

			client.on('disconnect', function() {
				console.log('El cliente '+client.request.socket.remoteAddress+' se ha desconectado');
			});

		});

	});
});

console.log('Servicio MongoDB iniciado');
console.log('Simulación activa');