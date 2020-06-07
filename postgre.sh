#!/usr/bin/bash

az group create --name playground --location northeurope
az configure --defaults location=northeurope group=playground

# create postgre server
pg_name=<insert postgre server name here>
pg_password=<insert postgre server password here>
GB=400
let storage=${GB:-5}*1024
az postgres server create \
--name $pg_name \
--resource-group playground \
--admin-user myadmin \
--admin-password $pg_password \
--sku-name GP_Gen5_2 \
--version 11 \
--storage-size $storage

# firewall self IP
self_ip=<insert your client ip here>

az postgres server firewall-rule create \
--server $pg_name \
--name AllowMyIP \
--start-ip-address $self_ip \
--end-ip-address $self_ip

vm_ip=<insert your VM public ip here>

az postgres server firewall-rule create \
--server $pg_name \
--name AllowMyIP2 \
--start-ip-address $vm_ip \
--end-ip-address $vm_ip

# get connections settings
az postgres server show --name $pg_name


