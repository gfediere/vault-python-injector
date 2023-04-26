#!/usr/bin/python3

import hvac
from hvac import Client
from hvac.api.auth_methods import Kubernetes
import random
import string
import logging
import time
import os
import requests


log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" 
logging.basicConfig(format = log_format, level = logging.INFO)
logger = logging.getLogger()

vault_server = os.environ['vault_server']
vault_role = os.environ['vault_role']
mount_point = os.environ['mount_point']
path = os.environ['path']
client = Client(vault_server)

f = open('/var/run/secrets/kubernetes.io/serviceaccount/token')
jwt = f.read()

try:
  Kubernetes(client.adapter).login(
      role=vault_role,
      jwt=jwt
  )
except requests.exceptions.ConnectionError:
  logger.error("cannot authenticate on " + vault_server + " with role: " + vault_role)

if client.is_authenticated():
  logger.info("client Authenticated")

  # Continuously read and write secrets
  while True:
    randomPwd= "".join(random.choice(string.ascii_letters) for i in range(8))
    try:
      client.secrets.kv.v2.create_or_update_secret(
        mount_point=mount_point,
        path=path,
        secret=dict(user=randomPwd),
      )
      logger.info("New password for path: " + mount_point + "/" + path + ": " + randomPwd)
    except hvac.exceptions.VaultError:
      logger.error("Cannot update password on mount point: " + mount_point + "/" + path)
    time.sleep(60)
else:
  logger.error("client not Authenticated")