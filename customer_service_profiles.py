#
# Copyright (c) 2015 Juniper Networks, Inc. All rights reserved.
#

"""
This is a script to get all the service profiles associated with a customer
"""
from api_server_views import *
from argparse import ArgumentParser
import requests
import json

def main():
    args = get_args()  
    address = args['address']
    if not address:
        address = 'http://localhost:9788'
    cust_name = args['customer_name']
    uuid = args['uuid']
    customer = None
    if cust_name:
        customer = get_customer(address, cust_name)
    elif uuid:
        customer = requests.get(address + "/customer/" + uuid)
        
    if customer:
        customer_json = customer.json().get("customer")
        if customer_json:
            print get_customer_service_profiles(address, customer_json) + \
                    get_customer_group_service_profiles(address, customer_json) + \
                    get_global_customer_service_profiles(address)
    
def get_args():
    parser = ArgumentParser(description='get service profiles of customer')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--customer_name', help='customer name')
    group.add_argument('-i', '--uuid', help='customer uuid')
    
    parser.add_argument('-a', '--address', help='IP Address/hostname (with port if needed) for the server')
    args = vars(parser.parse_args())
    return args

def get_customer(address, cust_name):
    r = requests.get(address + "/customers")
    data_list = r.json()
    
    for data in data_list.get("customers"):
        if data.get("fq_name")[2] == cust_name:
            id = data.get("uuid")
            return requests.get(address + "/customer/" + id)
        

def get_customer_service_profiles(address, customer):
    nfv_sp_list = []
    nfv_sp_refs = customer.get("nfvServiceProfile_refs")
    if not nfv_sp_refs:
        return nfv_sp_list
    
    for nfv_sp in nfv_sp_refs:
        id = nfv_sp.get("uuid")
        response = requests.get(address + "/nfvServiceProfile/" + id)
        nfv_sp_list.append(response.json())
    return nfv_sp_list    
        
            
def get_customer_group_service_profiles(address, customer):
    nfv_sp_list = []
    customer_grp_refs = customer.get("customerGroup_back_refs")
    if not customer_grp_refs:
        return nfv_sp_list
    for customer_grp in customer_grp_refs:
        customer_grp_id = customer_grp.get("uuid")
        customer_grp_response = requests.get(address + "/customerGroup/" + customer_grp_id)
        actual_customer_grp = customer_grp_response.json().get("customerGroup")
        for nfv_sp in actual_customer_grp.get("nfvServiceProfile_refs"):
            id = nfv_sp.get("uuid")
            response = requests.get(address + "/nfvServiceProfile/" + id)
            nfv_sp_list.append(response.json())
    return nfv_sp_list 
    
def get_global_customer_service_profiles(address):
    nfv_sp_list = []
    nfv_service_profile_refs = requests.get(address + "/nfvServiceProfiles")
    if not nfv_service_profile_refs:
        return nfv_sp_list
    for nfv_sp_ref in nfv_service_profile_refs.json().get("nfvServiceProfiles"):
        nfv_sp_json = requests.get(address + "/nfvServiceProfile/" + nfv_sp_ref.get("uuid")).json()
        if nfv_sp_json.get("nfvServiceProfile").get("nfvServiceProfile_global"):
            nfv_sp_list.append(nfv_sp_json)
    return nfv_sp_list    
    
if __name__ == '__main__':
    main()
