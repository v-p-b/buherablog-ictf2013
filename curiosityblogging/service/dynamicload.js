var fs = require('fs')
var vm = require('vm')

module.exports = {
    load: function load(script) {
        fs.readFile(script, function (err, data) {
            if (err) throw err;
            console.log("going to run: " +data)
            vm.runInThisContext(data.toString())
        })
    }
}


