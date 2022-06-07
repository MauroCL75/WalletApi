# WalletAPI

This is an API to generate wallet configuration. 

Since this is very sensitive, no password information is stored a long time.
All the information to generate the wallet must be provided at run time.

This should run in production a secure web server or on localhost.

The API will return a zip file with the wallet and a tnsname/sqlnet config. Edit the sqlnet to match your production config and set your TNS_ADMIN parameter to the wallet location.

# API documentation
Please go to [here](/docs)

# Password file format
For each schema, use a text file with this format:

    USER1,PASSWORD1
    USER2,PASSWORD2
    USER3,PASSWORD3
    ...

# Generated tnsnames
They will have this format:

    USER1_ENVIRONMENT

# Server installation

0-Install the [PortableWallet](https://github.com/MauroCL75/PortableWallet)

1-Install a virtual enviroment:

    virtualenv venv
    source venv/bin/activate

2-Install the pip environment:

    pip -r requirements.txt

3-Start the server

    uvicorn main:app

Or install and run the docker container:

    docker build -t walletapi .
    docker run -p 8000:8000 walletapi:latest uvicorn --host 0.0.0.0 main:app

Go to the [main page](http://localhost:8000)

# Using this

Ways to use this:

1-The curl way. You could run for example:

    curl --form "file=@test.txt"  --form 'awallet={"wallet_pass": "mypasshere", "workdir": "/where/the/wallet/and/tns/will/live", "env_type": "testing", "ip": "ora.ip.at.work.com", "port": 1521, "service_name": "ORCL"}'
    localhost:8000/wallet/ --output /tmp/allw.zip

2-The html way. Please fill [this form](/form)

3-Use the [provided python script](https://github.com/MauroCL75/WalletApi/raw/main/client.py). See the source code:

    python client.py --help

# Templates

You can modify the sqlnet and tnsnames templates to match your needs. They are based on jinja.

# Dependency

This API depends on the [PortableWallet](https://github.com/MauroCL75/PortableWallet).

# Source code

Hosted at github. It's available [here](https://github.com/MauroCL75/WalletApi). You cloud be there actually.
