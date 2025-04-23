const http = require("http");


function ObrabZapr(require, response){ //info / otvet
    console.log("otvet");
}

function connect(){
    console.log("connected");
}

server = http.createServer(ObrabZapr);

server.listen(3000, "127.0.0.1", connect);
