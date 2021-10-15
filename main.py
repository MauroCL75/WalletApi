from os import read
import time
import tempfile
import shutil
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form, Depends, Body 
from fastapi.param_functions import Body 
from fastapi.responses import HTMLResponse, FileResponse

from pydantic import BaseModel, Json
from helper import *

import logging
logger = logging.getLogger('CORE')
logger.info('CORE started!')

app = FastAPI()

class walletItem(BaseModel):
    wallet_pass: str
    workdir: Optional[str] = "tmp/wallet"
    env_type: str
    ip: str
    port: int
    service_name: str

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

@app.post("/wallet/", 
    response_class=FileResponse)
async def mkwallet(file: bytes=File(...), awallet: Json[walletItem]=Form(...)):
    pfile = "deleteme"

    content = file.decode()
    print(content)
    with open(pfile, "w") as f:
        f.write(content)
    workdir = ""
    homedir = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdirname:
        time.sleep(1)
        workdir = tmpdirname
        out = mkWallet(workdir, awallet.wallet_pass)
        os.chdir(homedir)
        names = []
        with open(pfile) as f:
            read_lines = f.readlines()
            for line in read_lines:
                data = line.split(",")
                names.append(data[0])
                os.chdir(homedir)
                addWallet(workdir, awallet.wallet_pass, data[0], data[1], awallet.env_type)
        tstr = ""
        os.chdir(homedir)

        for name in names:
            tstr = "%s\n%s"%(tstr, mkTns(name, awallet.env_type, awallet.ip, awallet.port, awallet.service_name))
        with open('%s/tnsnames.ora'%(workdir), 'w') as file:
            file.write(tstr)
        with open('%s/sqlnet.ora'%(workdir), 'w') as file:
            file.write(mkSQLNET(awallet.workdir))
        shutil.make_archive("%szip"%(workdir), 'zip', "/tmp/", workdir.replace("/tmp/", ""))
        os.remove(pfile)
        #with open("%szip.zip"%(workdir), 'rb') as azipfile:
        #    azipfile.seek(0)
        #    response = FileResponse(azipfile, media_type="application/x-zip-compressed")
        #    response.headers["Content-Disposition"] = "attachment; filename=mywallet.zip"
        #    return response
        return FileResponse("%szip.zip"%(workdir), media_type="application/x-zip-compressed")

#mktnsname

