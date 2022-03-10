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

my_dict = dict()
memory = get_fact("memory")
disks = get_fact("disks")
hypervisors = get_fact("hypervisors")
os = get_fact("os")
mount = get_fact("mountpoints")

for keys in memory:
    hostname = keys['certname']
    usedswap = keys['value']['swap']['used']
    totalmem = keys['value']['system']['total']
    usedmem = keys['value']['system']['used']
    my_dict[hostname] = {"total_memory":totalmem}
    my_dict[hostname]["used_memory"] = usedmem
    my_dict[hostname]["used_swap"] = usedswap

for keys in disks:
    hostname = keys['certname']
    sda_model = keys['value']['sda']['model']
    sda_size = keys['value']['sda']['size']
    sdb_model = keys['value'].get('sdb',{}).get('model', 'null')
    sdb_size = keys['value'].get('sdb',{}).get('size', 'null')
    my_dict[hostname]["sda_model"] = sda_model
    my_dict[hostname]["sda_size"] = sda_size
    my_dict[hostname]["sdb_model"] = sdb_model
    my_dict[hostname]["sdb_size"] = sdb_size

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
    
for keys in mount:
    mount_root_filesystem = keys['value']['/']['filesystem']
    mount_root_capacity = keys['value']['/']['capacity']
    mount_root_size = keys['value']['/']['size']
    mount_root_device = keys['value']['/']['device']
    mount_root_options = keys['value']['/']['options']
    mount_root_available = keys['value']['/']['available']
    mount_root_size_bytes = keys['value']['/']['size_bytes']
    mount_root_avail_bytes = keys['value']['/']['available_bytes']
    mount_root_used = keys['value']['/']['used']
    mount_misc_filesystem = keys['value'].get('/Misc',{}).get('filesystem', 'null')
    mount_misc_capacity = keys['value'].get('/Misc',{}).get('capacity', 'null')
    mount_misc_size = keys['value'].get('/Misc',{}).get('size', 'null')
    mount_misc_device = keys['value'].get('/Misc',{}).get('device', 'null')
    mount_misc_options = keys['value'].get('/Misc',{}).get('options', 'null')
    mount_misc_available = keys['value'].get('/Misc',{}).get('available', 'null')
    mount_misc_size_bytes = keys['value'].get('/Misc',{}).get('size_bytes', 'null')
    mount_misc_avail_bytes = keys['value'].get('/Misc',{}).get('available_bytes', 'null')
    mount_misc_used = keys['value'].get('/Misc',{}).get('used', 'null')
    my_dict[hostname]["filesystem_root"] = mount_root_filesystem
    my_dict[hostname]["capacity_root"] = mount_root_capacity
    my_dict[hostname]["size_root"] = mount_root_size
    my_dict[hostname]["device_root"] = mount_root_device
    my_dict[hostname]["options_root"] = mount_root_options
    my_dict[hostname]["available_root"] = mount_root_available
    my_dict[hostname]["size_bytes_root"] = mount_root_size_bytes
    my_dict[hostname]["available_bytes_root"] = mount_root_avail_bytes
    my_dict[hostname]["used_root"] = mount_root_used
    my_dict[hostname]["filesystem_misc"] = mount_misc_filesystem
    my_dict[hostname]["capacity_misc"] = mount_misc_capacity
    my_dict[hostname]["size_misc"] = mount_misc_size
    my_dict[hostname]["device_misc"] = mount_misc_device
    my_dict[hostname]["options_misc"] = mount_misc_options
    my_dict[hostname]["available_misc"] = mount_misc_available
    my_dict[hostname]["size_bytes_misc"] = mount_misc_size_bytes
    my_dict[hostname]["available_bytes_misc"] = mount_misc_avail_bytes
    my_dict[hostname]["used_misc"] = mount_misc_used

#print(my_dict)


column_names = ["Total Memory", "Used Memory", "Used Swap", "SDA Model", "SDA Size", "SDB Model", "SDB Size", "Hypervisor Version", "Operating System", "OS Version", "filesystem_root", "capacity_root", "size_root", "device_root", "options_root", "available_root", "size_bytes_root", "available_bytes_root", "used_root", "filesystem_misc", "capacity_misc", "size_misc", "device_misc", "options_misc", "available_misc", "size_bytes_misc", "available_bytes_misc", "used_misc"]
df = pd.DataFrame(columns=column_names)
df = df.from_dict(my_dict, orient='index')
df.to_excel(excel_sheet_path)

#print(df)