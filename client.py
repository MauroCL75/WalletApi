#!/usr/bin/python3
import requests
import argparse
import json
import logging
from pprint import pprint

logger = logging.getLogger(__name__)
logging.info("Client starting")

def params():
    parser = argparse.ArgumentParser(description='A client for the wallet API')
    parser.add_argument('-wp', '--wallet_pass', type=str, help="Wallet password")
    parser.add_argument('-pfl', '--password_file', type=str, help="password file")
    parser.add_argument('-aurl', '--api_url', type=str, 
        help="http address of the api, default is http://localhost:8000/wallet/", 
        default="http://localhost:8000/wallet/")
    parser.add_argument('-env', '--env_type', type=str, help="environment type, default is testing", 
        default="testing")
    parser.add_argument('-ip', '--ip', type=str, help="database ip, default is localhost", 
        default="localhost")
    parser.add_argument('-port', '--port', type=int, help="database port, default is 2121", 
        default=2121)
    parser.add_argument('-svc', '--service_name', type=str, help="database service name, default is alma", 
        default="alma")
    parser.add_argument('-wkdir', '--workdir', type=str, help="directory of the tnsname and wallet files, default is /tmp/wallet", 
        default="/tmp/wallet")
    parser.add_argument('-o', '--output', type=str, help="zip output filename, defautl is wallet.zip", 
        default="wallet.zip")
    args = parser.parse_args()
    return args

def go(p):
    wdata ={}
    wdata = {"wallet_pass": p.wallet_pass, 
        "env_type": p.env_type, "ip": p.ip, 
        "port": p.port, "service_name": p.service_name}
    with open(p.password_file, "rb") as f:
        wfile = f.read()
    data = {"awallet": json.dumps(wdata)}

    logging.info("data sent %s",data)
    print(type(wfile))
    r = requests.post(p.api_url, data=data, files={"file": ("afile.txt", wfile, "text/plain")}, stream=True, verify=False)
    with open(p.output, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
    print("%s written"%(p.output))

def main():
    p = params()
    go(p)

if __name__ == "__main__":
    main()
