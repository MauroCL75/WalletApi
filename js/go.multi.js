var dbCount = 0;

function enable() {
    var element = document.getElementById("action");
    element.classList.remove("pure-button-disabled");
    element.classList.add('pure-button');
}

function disable() {
    var element = document.getElementById("action");
    element.classList.remove("pure-button");
    element.classList.add('pure-button-disabled');
}

function CheckPassword(inputtxt) {
    if (inputtxt) {
        var passw = /^(?=.*[a-zA-Z0-9]).{4,20}(?=.*[a-zA-Z0-9]).{4,20}$/;
        if (inputtxt.value.match(passw)) {
            console.log("pass ok")
            enable();
        }
        else {
            console.log("pass weak");
            disable();
        }
    }
}

function addDB(){
    var n = dbCount;
    var m = dbCount+1;
    var aDB='DB'+m+'<br><input type="text" name="ip" placeholder="ip" id="ip'+n+'"/>:<input type="text" name="port" placeholder="port" id="port'+n+'" />';
    aDB +='/<input type="text" name="service_name" placeholder="service name" id="service_name'+n+'" />'
    aDB += '<input type="text" name="enviroment" placeholder="alias"  id="env'+n+'"/>';
    aDB += '<button class="pure-button" type="button" onclick="newDB()">add one more DB</button>';
    aDB += '<br><input type="file" name="file'+n+'" id="file'+n+'" value="password file"/><br></br>';
    aDB += '<br><br>';
    return aDB;
}

function newDB() {
    var dbs = document.getElementById("dbs");
    var html = addDB();
    //var d = document.createElement("div")
    dbs.innerHTML += html;
    dbCount += 1;
}

function getWalletMulti() {
    console.log("getWallet");
    var wallet_pass = document.getElementById("wallet_pass").value;
    var workdir = document.getElementById("workdir").value

    var dbsData = [];
    var filesData = [];
    for (var j = 0; j < dbCount; j++) {
        var ip = document.getElementById("ip" + j).value;
        var port = document.getElementById("port" + j).value;
        var service_name = document.getElementById("service_name" + j).value;
        var f = document.getElementById("file" + j).files[0];
        var env = document.getElementById("env"+j).value;
        //if (ip && port && service_name && env) {
        if (true) {
            var data = { "ip": ip, "port": port, "service_name": service_name, "env_type": env };
            console.log(JSON.stringify(data));
            dbsData.push(data)
            filesData.push(f);
        }
    }
    console.log("dbsData: "+JSON.stringify(dbsData));
    console.log("filesData "+JSON.stringify(filesData));
    var url = "/wallet.multi/"
    var indata = { "wallet_pass": wallet_pass, "workdir": workdir, "dbs": dbsData }
    console.log("url " + url);
    console.log(JSON.stringify(indata))
    
    var spin = document.getElementById("spin");
    spin.removeAttribute("hidden");

    formData = new FormData();
    formData.append("awallet", JSON.stringify(indata))
    console.log(formData);

    for (const aFile of filesData) {
        console.log(aFile);
        formData.append("files", aFile, aFile.name);
    }

    //console.log(formData);
    fetch(url,  {method: "POST", body: formData }).then( res => res.blob() )
    .then( blob => {
      var file = window.URL.createObjectURL(blob);
      window.location.assign(file);
      spin.setAttribute("hidden", "");
    });
    return false;
}

document.addEventListener("DOMContentLoaded", function(event) {
    //código a ejecutar cuando el DOM está listo para recibir acciones
    var dbs = document.getElementById("dbs");
    for (var i=0; i<1; i++){
        var html = addDB();
        dbs.innerHTML += html;
        dbCount += 1;
    }
});