const http = require("http");
const fs = require("fs");

function ObrabZapr(request, response){ //info / otvet
    if (request.method == "GET"){
        console.log(request.url);
        if (request.url == "/"){
            file = "./test1/html/main.html";
        }
        else if(request.url.substring(0, 8) === "/assets/"){
            file = "./test1" + request.url;
        }
        else{
            file = "./test1/html"+request.url;
        }
        file = file.replaceAll("%20", " ");
        console.log(file);
        response.setHeader("Content-Type", "text/html; charset=utf-8;");
        fs.stat(file, (err, stats) => {
            if(stats && stats.isFile() && !err){
                fs.createReadStream(file).pipe(response);
                console.log("Файл прочитан");
            }
            else{
                response.statusCode = 404;
                response.end("<h2>File not found!</h2>");
                console.log("Файл не прочитан");
            }
        });
    }
    
}

function startServer(){                //&
    console.log("\nServer started!\n");
}

server = http.createServer(ObrabZapr);

server.listen(3000, "127.0.0.1", startServer);
