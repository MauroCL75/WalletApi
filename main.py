from os import read
import time
import tempfile
import shutil
from typing import Optional

from fastapi import FastAPI, File, UploadFile 
from fastapi.responses import HTMLResponse, FileResponse

from helper import *

import logging
logger = logging.getLogger('CORE')
logger.info('CORE started!')

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def mainProg():
    '''Welcome page'''
    msg = mainPage()
    return msg

@app.get("/go.js", response_class=FileResponse)
async def mainJS():
    return FileResponse("js/go.js", media_type="application/javascript")

@app.get("/form", response_class=HTMLResponse)
async def mainProg():
    '''Welcome page'''
    msg = formPage()
    return msg

#mkwallet lista de l/p y tipo
@app.post("/wallet/{wallet_pass}/{env_type}/{ip}/{port}/{service_name}", 
    response_class=FileResponse)
async def mkwallet(wallet_pass:str, env_type: str, ip: str, 
    port: int, service_name: str, file: bytes=File(...)):
    #logger.info("file uploaded! %s",file)
    pfile = "deleteme"
    print("file %s"%(file))

    content = file.decode()
    print(content)
    with open(pfile, "w") as f:
        f.write(content)
    workdir = ""
    homedir = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdirname:
        time.sleep(1)
        workdir = tmpdirname
        out = mkWallet(workdir, wallet_pass)
        print(out)
        os.chdir(homedir)
        names = []
        with open(pfile) as f:
            read_lines = f.readlines()
            for line in read_lines:
                data = line.split(",")
                names.append(data[0])
                os.chdir(homedir)
                addWallet(workdir, wallet_pass, data[0], data[1], env_type)
        tstr = ""
        print(names)
        os.chdir(homedir)

        for name in names:
            tstr = "%s\n%s"%(tstr, mkTns(name, env_type, ip, port, service_name))
        with open('%s/tnsnames.ora'%(workdir), 'w') as file:
            file.write(tstr)
        with open('%s/sqlnet.ora'%(workdir), 'w') as file:
            file.write(mkSQLNET(workdir))
        shutil.make_archive("%szip"%(workdir), 'zip', "/tmp/", workdir.replace("/tmp/", ""))
        os.remove(pfile)
        #with open("%szip.zip"%(workdir), 'rb') as azipfile:
        #    azipfile.seek(0)
        #    response = FileResponse(azipfile, media_type="application/x-zip-compressed")
        #    response.headers["Content-Disposition"] = "attachment; filename=mywallet.zip"
        #    return response
        return FileResponse("%szip.zip"%(workdir), media_type="application/x-zip-compressed")

#mktnsname

