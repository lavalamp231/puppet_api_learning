import os
import requests
import json
import pandas as pd

ca_location = '/etc/puppetlabs/puppet/ssl/certs/ca.pem'
cert = '/etc/puppetlabs/puppet/ssl/certs/canary.esxi.com.pem'
private_key = '/etc/puppetlabs/puppet/ssl/private_keys/canary.esxi.com.pem'
cwd = os.getcwd()
excel_sheet_path = (cwd + '/host_information_excel.xlsx')
print(excel_sheet_path)

def get_fact(fact):
    host = "^.*"
    url = "https://puppetdbsp.esxi.com:8081/pdb/query/v4/facts/" + fact
    query = {"query":["~", "certname", host]}
    r = requests.post(url, json=query, verify=ca_location, cert=(cert, private_key))
    return r.json()

#print(type(x))
my_dict = dict()
memory = get_fact("memory")
disks = get_fact("disks")
hypervisors = get_fact("hypervisors")
os = get_fact("os")

#print(disks)
for keys in memory:
    hostname = keys['certname']
    usedswap = keys['value']['swap']['used']
    totalmem = keys['value']['system']['total']
    usedmem = keys['value']['system']['used']
    my_dict[hostname] = {"total_memory":totalmem}
    my_dict[hostname]["used_memory"] = usedmem
    my_dict[hostname]["used_swap"] = usedswap

for keys in disks:
    #print(keys.values())
    hostname = keys['certname']
    sda_model = keys['value']['sda']['model']
    sda_size = keys['value']['sda']['size']
    sdb_model = keys['value'].get('sdb',{}).get('model', 'null')
    sdb_size = keys['value'].get('sdb',{}).get('size', 'null')
    my_dict[hostname]["sda_model"] = sda_model
    my_dict[hostname]["sda_size"] = sda_size
    my_dict[hostname]["sdb_model"] = sdb_model
    my_dict[hostname]["sdb_size"] = sdb_size
    #print(sda_model, sda_size, sdb_model, sdb_size)

for keys in hypervisors:
    hostname = keys['certname']
    hypervisor_version = keys['value']['vmware']['version']
    my_dict[hostname]["hypervisor_version"] = hypervisor_version

for keys in os:
    hostname = keys['certname']
    operating_system = keys['value']['name']
    os_version = keys['value']['distro']['release']['full']
    my_dict[hostname]["operating_system"] = operating_system
    my_dict[hostname]["os_version"] = os_version
    
#print(my_dict.keys())
column_names = ["Total Memory", "Used Memory", "Used Swap", "SDA Model", "SDA Size", "SDB Model", "SDB Size", "Hypervisor Version", "Operating System", "OS Version"]
df = pd.DataFrame(columns=column_names)
df = df.from_dict(my_dict, orient='index')
df.to_excel(excel_sheet_path)
print(df)
    #OS, mount(whatis currently mounted cap used /, /misc, device 192.168.0.199/Misc, /,  ),  