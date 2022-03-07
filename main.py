import os
import requests
import json

ca_location = '/etc/puppetlabs/puppet/ssl/certs/ca.pem'
cert = '/etc/puppetlabs/puppet/ssl/certs/canary.esxi.com.pem'
private_key = '/etc/puppetlabs/puppet/ssl/private_keys/canary.esxi.com.pem'

def get_fact():
    host = "^.*"
    url = "https://puppetdbsp.esxi.com:8081/pdb/query/v4/facts/memory"
    query = {"query":["~", "certname", host]}
    r = requests.post(url, json=query, verify=ca_location, cert=(cert, private_key))
    return r.json()

x = get_fact()
#print(type(x))

for keys in x:
#    print(keys)
    hostname = keys['certname']
    #print(hostname)
    usedswap = keys['value']['swap']['used']
    #print(usedswap)
    totalmem = keys['value']['system']['total']
    #print(totalmem)
    usedmem = keys['value']['system']['used']
    #print(usedmem)

    memory_dict = dict()
    memory_dict = {"hostname": hostname, "usedswap": usedswap, "totalmem": totalmem, "usedmem": usedmem}
    print(memory_dict)