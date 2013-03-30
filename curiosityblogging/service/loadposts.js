var fs = require("fs")
var md = require("./metadata.js")


function load() {
    posts = []

    files = fs.readdirSync("posts/")
    for (f in files) {
        if (!/metadata$/.test(files[f])) {
            if (fs.existsSync("posts/"+ files[f] + ".metadata")) {
                var file_content = fs.readFileSync("posts/"+files[f])
                var metadata = fs.readFileSync("posts/"+files[f]+".metadata").toString().replace(/\s/g,'')
                if (metadata == md.calc(file_content).toString()) {
                    posts.push(files[f])
                }
            }
        }
    }
    return posts
}

module.exports = {load:load}
