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
from typing import List

import logging
import logging.config

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)
logger.info('App started!')

app = FastAPI()

class database(BaseModel):
    env_type: str
    ip: str
    port: int
    service_name: str

class walletItem(BaseModel):
    wallet_pass: str
    workdir: Optional[str] = "tmp/wallet"
    env_type: str
    ip: str
    port: int
    service_name: str

class walletMultiItem(BaseModel):
    wallet_pass: str
    workdir: Optional[str] = "tmp/wallet"
    dbs: List[database]

@app.get("/", response_class=HTMLResponse)
async def mainProg():
    '''Welcome page'''
    msg = mainPage()
    return msg

@app.get("/go.js", response_class=FileResponse)
async def mainJS():
    return FileResponse("js/go.js", media_type="application/javascript")

@app.get("/go.multi.js", response_class=FileResponse)
async def mainJS():
    return FileResponse("js/go.multi.js", media_type="application/javascript")

@app.get("/form", response_class=HTMLResponse)
async def mainProg():
    '''Welcome page'''
    msg = formPage()
    return msg

@app.get("/form2", response_class=HTMLResponse)
async def mainProg():
    '''Welcome page'''
    msg = formPage("form.multi.html")
    return msg

@app.post("/wallet/", 
    response_class=FileResponse)
async def mkwallet(file: bytes=File(...), awallet: Json[walletItem]=Form(...)):
    pfile = "deleteme"

    content = file.decode()
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
        return FileResponse("%szip.zip"%(workdir), media_type="application/x-zip-compressed")

@app.post("/wallet.multi/", response_class=FileResponse)
async def mkwallet(files: list[bytes]=File(), awallet: Json[walletMultiItem]=Form(...)):
    i = 0
    #print("files: %s"%(len(files)))
    #return {"file_sizes": [len(file) for file in files]}

    for aFile in files:
        pfile = "deleteme%s"%(i)

        content = aFile.decode()
        with open(pfile, "w") as f:
            f.write(content)
        i+=1
    workdir = ""
    homedir = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdirname:
        time.sleep(1)
        workdir = tmpdirname
        out = mkWallet(workdir, awallet.wallet_pass)
        os.chdir(homedir)
        names = []
        i = 0

        with open('%s/sqlnet.ora'%(workdir), 'w') as file:
            file.write(mkSQLNET(awallet.workdir))

        for wallet in awallet.dbs:
            names = []
            pfile = "deleteme%s"%(i)
            with open(pfile) as f:
                read_lines = f.readlines()
                for line in read_lines:
                    data = line.split(",")
                    if (data[0] not in names):
                        names.append(data[0])
                    os.chdir(homedir)
                    addWallet(workdir, awallet.wallet_pass, data[0], data[1], wallet.env_type)
            tstr = ""
            i+=1
            os.chdir(homedir)

            for name in names:
                print("%s_%s"%(name, wallet.env_type))
                tstr = "%s\n%s\n"%(tstr, mkTns(name, wallet.env_type, wallet.ip, wallet.port, wallet.service_name))
            with open('%s/tnsnames.ora'%(workdir), 'a') as file:
                file.write(tstr)

            os.remove(pfile)
        shutil.make_archive("%szip"%(workdir), 'zip', "/tmp/", workdir.replace("/tmp/", ""))
        return FileResponse("%szip.zip"%(workdir), media_type="application/x-zip-compressed")

#mktnsname

