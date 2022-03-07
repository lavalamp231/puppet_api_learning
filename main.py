import os
import requests

ca_location = '/etc/puppetlabs/puppet/ssl/certs/ca.pem'
cert = '/etc/puppetlabs/puppet/ssl/certs/canary.esxi.com.pem'
private_key = '/etc/puppetlabs/puppet/ssl/private_keys/canary.esxi.com.pem'

def get_fact():
    #test