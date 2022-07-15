import jinja2
import markdown
import os
import logging

PWALLETDIR="./PortableWallet"

def mainPage(README="./README.md"):
    '''The main page. Just the markdown page'''
    out = ""
    with open(README) as f:
        read_data = f.read()
        out = markdown.markdown(read_data)
        file_loader = jinja2.FileSystemLoader('./templates')
        env = jinja2.Environment(loader=file_loader)
        template = env.get_template("content.html")
        out = template.render(info={"content": out})
    return out

def mkTns(name, env_type, ip, port, service_name):
    '''I create tns'''
    print("mkTns %s %s %s %s %s"%(name, env_type, ip, port, service_name))
    file_loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=file_loader)
    out = ""
    #for name in names:
    template = env.get_template("tnsname.tpl")
    info = {"name": name, "env_type": env_type, 
        "ip": ip, "port": port, "service_name": service_name}
    print("data %s"%( info))
    single = template.render(info = info )
    #    out = "%s\n%s"%(out, single)
    return single

def mkSQLNET(directory):
    '''I create the sqlnet file'''
    file_loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=file_loader)
    out = ""
    template = env.get_template("sqlnet.tpl")
    out = template.render(info={"directory": directory})
    return out

def mkWallet(directory, wallet_pass):
    '''Make a wallet on directory'''
    os.chdir(PWALLETDIR)
    mkwalletCMD = "./mkw.sh %s %s"%(directory, wallet_pass)
    cmd = os.system(mkwalletCMD)
    estatus = cmd
    return {"mkWallet": estatus}

def addWallet(directory, wallet_pass, login, password, env=None):
    '''Add a tns, schema and password'''
    os.chdir(PWALLETDIR)
    tname = login.upper()
    if (env!=None):
        tname = "%s_%s"%(login.upper(), env.upper())

    opts = "%s %s %s %s %s"%(directory, tname, 
        login, password, wallet_pass)
    print("ADDWALLET %s"%(opts))
    addwalletCMD = "./addcred.sh %s" % (opts)
    addwalletCMD = addwalletCMD.replace("\n", "")     
    cmd = os.system(addwalletCMD)
    estatus = cmd
    return {"addWallet": estatus}

def formPage(page="form.html", tempdir="./templates"):
    '''Simple form to test this'''
    file_loader = jinja2.FileSystemLoader(tempdir)
    env = jinja2.Environment(loader=file_loader)
    out = ""
    template = env.get_template(page)
    out = template.render()
    return out

def jsPage(script="go.js"):
    with open("js/%s"%(script)) as jsf:
        out = jsf.read()
        return out