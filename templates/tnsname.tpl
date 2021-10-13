{{info.name.upper()}}_{{info.env_type.upper()}} = 
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = {{info.ip}})(PORT = {{info.port}}))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = {{info.service_name}})
    )
  )