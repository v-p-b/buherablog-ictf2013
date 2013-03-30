var dy = require('./dynamicload.js')
var path = require('path')
var md = require('./metadata.js')
var http = require('http')
var dynpost = require('./loadposts.js')
var crypto = require('crypto')
var fs = require('fs')
var url = require('url')
var nunjucks = require('nunjucks');
var env = new nunjucks.Environment();
var tmpl = env.getTemplate('blog_template.html');

http.createServer(function(request,response) {
    console.log("Got request for " + request.url)
    if (request.url == "/") {
        response.writeHeader(200, {"Content-Type": "text/html"});
        posts = dynpost.load()
        data = ""
        for (p in posts) {
            data += "<a href=read?id="+posts[p]+">Blog post "+posts[p]+"</a><br>"
        }
        response.write(tmpl.render({blogpost:data}))
        response.end()
    }
    else if (request.url.indexOf("store") >= 0) {
        response.writeHeader(200, {"Content-Type": "text/html"});
        p = url.parse(request.url, true)
        if("username" in p.query && "value" in p.query && "cookie" in p.query) {
            if (!fs.existsSync("flags/"+p.query["username"])) {
                fs.writeFile("flags/"+p.query["username"], p.query["cookie"] +"\n"+ p.query["value"], function (err){
                    if (err) throw err;
                })
                response.write("OK")
                response.end()
            } else {
                response.write("FLAG NOT OVERWRITTEN")
                response.end()
            }
        }
        response.write("Error")
        response.end()
    }
    else if (request.url.indexOf("retrieve") >= 0) {
        response.writeHeader(200, {"Content-Type": "text/html"});
        p = url.parse(request.url, true)
        if("username" in p.query && "cookie" in p.query) {
            try {
                var data = fs.readFileSync("flags/"+p.query["username"]).toString()
                if (data.split("\n")[0] == p.query["cookie"])
                    response.write(data.split("\n")[1])
                else {
                    response.write("Invalid cookie")
                }
            } catch(e) {
                response.write("Invalid user")
            }
        }
        response.end()
    }
    else if (request.url.indexOf("upload") >= 0) {
        response.writeHeader(200, {"Content-Type": "text/html"});
        request.on('data', function (chunk) {
            p = url.parse(request.url, true)
            if ("name" in p.query) {
                if (path.normalize("posts/"+p.query["name"]).indexOf("posts") == 0) {
                    fs.writeFile("posts/"+p.query["name"], chunk, function (err){
                        if (err) throw err;
                    })
                    fs.writeFile("posts/"+p.query["name"]+".metadata", md.calc(chunk), function (err){
                        if (err) throw err;
                    })
                }
            }

        })
        response.write("upload");
        response.end()
    } else if(request.url.indexOf("read") >= 0) {
        response.writeHeader(200, {"Content-Type": "text/html"});
        p = url.parse(request.url, true)
        if ("id" in p.query && md.checkfile(p.query["id"])) {
            fs.readFile("posts/"+p.query["id"], function (err, data) {
                if (err) throw err;
                response.write(tmpl.render({blogpost:data}))
                response.end()
            })
        } else {
            response.write("something went wrong...");
            response.end()
        }
    } else if (request.url.indexOf("bootstrap") >= 0) {
        sp = request.url.split("/")
        file = sp[sp.length-1]
        type = sp[sp.length-2]
        if (type == "js")
            response.writeHeader(200, {"Content-Type": "application/javascript"});
        else if (type == "css")
            response.writeHeader(200, {"Content-Type": "text/css"});
        fs.readFile("bootstrap/"+type+"/"+file, function (err, data) {
            if (err) throw err;
            response.write(data)
            response.end()
        })
    } else if (request.url == "/curiosity_cat.png") {
        response.writeHeader(200, {"Content-Type": "img/png"});
        fs.readFile("curiosity_cat.png", function (err, data) {
            if (err) throw err;
            response.write(data)
            response.end()
        })

    }
    else {
        response.writeHeader(404, {"Content-Type": "application/javascript"});
        response.write("Invalid request")
        response.end()

    }

}).listen(8089)

