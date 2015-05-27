'''
Created on May 22, 2015
This script is used to load configurations.
@author: apogu
'''

import ConfigParser

def get_config():
    config = ConfigParser.RawConfigParser()
    
    config.add_section('users')
    config.set('users', 'url', '/api/vcpe/users/')
    config.set('users', 'primary_key', 'username')
    
    config.add_section('groups')
    config.set('groups', 'url', '/api/vcpe/groups/')
    config.set('groups', 'primary_key', 'name')
    
    config.add_section('permissions')
    config.set('permissions', 'url', '/api/vcpe/permissions/')
    config.set('permissions', 'primary_key', 'codename')
    
    config.add_section('customers')
    config.set('customers', 'url', '/api/vcpe/customers/')
    config.set('customers', 'primary_key', 'customer_name')
    
    config.add_section('targets')
    config.set('targets', 'url', '/api/vcpe/targets/')
    config.set('targets', 'primary_key', 'name')
    
    config.add_section('service-profiles')
    config.set('service-profiles', 'url', '/api/vcpe/service-profiles/')
    config.set('service-profiles', 'primary_key', 'id')
    
    config.add_section('audits')
    config.set('audits', 'url', '/api/vcpe/audits/')
    config.set('audits', 'primary_key', 'id')
    
    config.add_section('topologies')
    config.set('topologies', 'url', '/api/vcpe/customers/?/topologies/')
    config.set('topologies', 'primary_key1', 'customer_name')
    config.set('topologies', 'primary_key', 'site_name')
    
    config.add_section('service-instances')
    config.set('service-instances', 'url', '/api/vcpe/customers/?/service-instances/')
    config.set('service-instances', 'pprimary_key1', 'customer_name')
    config.set('service-instances', 'primary_key', 'sid')
    
    config.add_section('sites')
    config.set('sites', 'url', '/api/vcpe/customers/?/sites/')
    config.set('sites', 'primary_key1', 'customer_name')
    config.set('sites', 'primary_key', 'topo_name')
    
    config.add_section('links')
    config.set('links', 'url', '/api/vcpe/customers/?/sites/?/links/')
    config.set('links', 'primary_key1', 'customer_name')
    config.set('links', 'primary_key2', 'site_name')
    config.set('links', 'primary_key', 'link_name')
    
    config.add_section('account')
    config.set('account', 'url', '/api/vcpe/user/account/')
    return config

# Writing our configuration file to 'myconfig.cfg'
if __name__ == '__main__':
    config = get_config()
    
    with open('myconfig.cfg', 'wb') as configfile:
        config.write(configfile)
