
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

function getWallet(){
    console.log("getWallet");
    var wallet_pass = document.getElementById("wallet_pass").value
    var env_type = document.getElementById("env_type").value
    var ip = document.getElementById("ip").value
    var port = document.getElementById("port").value
    var service_name = document.getElementById("service_name").value
    var url = "/wallet/"+wallet_pass+"/"+env_type+"/"+ip+"/"+port+"/"+service_name
    console.log("url "+url);
    var f = document.getElementById("file").files[0]
    formData = new FormData();
    formData.append("file", f)
    fetch(url,  {method: "POST", body: formData}).then( res => res.blob() )
    .then( blob => {
      var file = window.URL.createObjectURL(blob);
      window.location.assign(file);
    });
    return false;
}
