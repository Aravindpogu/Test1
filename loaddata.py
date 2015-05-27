'''
Created on May 15, 2015
This script is used to load data to the server. It uses simple \
HTTP post requests with basic authentication.
File names must follow the convention of modelname_ordernumber.
For example, to laod permissions, the file name must be something like permissions_001.json
@author: apogu
'''

from argparse import ArgumentParser
from os import listdir
from os.path import isfile, join
from requests.auth import HTTPBasicAuth
import json, os, requests, threading, string, ConfigParser

statistics = []

def getUrl(filename, config, data):
    section = os.path.basename(filename).split("_")[0]
    url = config.get(section, "url")
    if "?" not in url:
        return url
    else:
        count = url.count("?")
        for i in range(count):
            key = config.get(section, "primary_key" + `i+1`)
            key_value = data.get(key)
            url = string.replace(url, "?", key_value, 1)
        return url
        
def get_primary_key(filename, config):
    section = os.path.basename(filename).split("_")[0]
    return config.get(section, "primary_key")

def load_from_file(username, password, address, override, headers, config, filename):
    global statistics
    data_list = json.loads(open(filename).read())
    
    for data in data_list.get("results"):
        url = address + getUrl(filename, config, data)
        r = requests.post(url, data=json.dumps(data), headers=headers,
                      auth=HTTPBasicAuth(username, password))
        statistics.append("status_code: " +  `r.status_code` + " and response is: "+ r.content )
        if override and r.status_code not in [201,400,401, 404]:
            put_url = url + data.get(get_primary_key(filename, config)) + "/"
            r = requests.put(put_url, data=json.dumps(data), headers=headers,
                      auth=HTTPBasicAuth(username, password))
            statistics.append("status_code: " +  `r.status_code` + " and response is: "+ r.content)
            
def load_from_directory(username, password, address, override, headers, config, directory):
    threads = []
    file_list = [f for f in listdir(directory) if isfile(join(directory, f))]

    for f in file_list:
        t = threading.Thread(target=load_from_file, args=(username, password, address, 
                                                          override, headers, config, join(directory, f)))
        t.start()
        threads.append(t)

    #Wait for threads to finish
    for thread in threads:
        thread.join()

def get_args():
    parser = ArgumentParser(description='Load data to the server')
    parser.add_argument('-u', '--username', help='user name', required=True)
    parser.add_argument('-p', '--password', help='password', required=True)
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--directory', help='directory location to load from all the files present in that directory')
    group.add_argument('-f', '--filename', help='provide filename to load data from a single file')
    
    parser.add_argument('-c', '--conf', help='config file location')
    parser.add_argument('-o', '--override', help='override', action='store_true')
    parser.add_argument('-a', '--address', help='IP Address/hostname (with port if needed) for the server')
    args = vars(parser.parse_args())
    return args

def main():
    args = get_args()  
    username = args['username']
    password = args['password']
    directory = args['directory']
    filename = args['filename']
    conf = args['conf']
    override = args['override']
    address = args['address']
    if not address:
        address = 'http://127.0.0.1:8000'
      
    headers = {'Accept': 'application/json;version=1',
               'Content-Type': 'application/json;version=1;charset=UTF-8'}
      
    config = ConfigParser.RawConfigParser()
    if not conf:
        config.read(os.path.join(os.getcwd(), "myconfig.cfg"))
    else:
        config.read(conf)
          
    if directory:
        load_from_directory(username, password, address, override, headers, config, directory)
    elif filename:
        load_from_file(username, password, address, override, headers, config, filename)
          
    for s in statistics:
        print s
      
    print "------------------------------------------"
    print "total number of requests", len(statistics)
        
if __name__ == '__main__': main()
