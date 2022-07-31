#!/usr/local/bin/python3

"""
Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""


from __future__ import absolute_import, division, print_function

__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"
__metaclass__ = type

DOCUMENTATION = r'''
---
module: hyperflex_datastore
short_description: Create and Delete Datastores from HyperFlex for Demo Purposes
options:
    hx_connect_ip:
        description: IP of HX Connect Management IP
        required: true
        type: str
    hx_connect_user:
        description: User name to logon ot HX connect
        required: true
        type: str
    hx_connect_password:
        description: HX Connect Password
        required: true
        type: str
    mode:
        description: This will be "Create", "Verify" or "Delete"
        required:   true
        type:   str
    name:
        description: Name of the datastore to create, verify or delete.
        required:   true
        type:   str
    volumeSize:
        description: Size of the disk volume to be created (Only applies on creation)
        required:   true
        type: int
    sizeDescriptor:
        description: By default we assume terrabytes, but you can modify to GB using this option.
        required:   false
        type: str
    blockSize:
        description: This can be 4K or 8K
        required:   true
        type: str
'''
EXAMPLES = r'''
# Create a Datastore
- name: Create Datastore
  hyperflex_datastore:
    hx_connect_ip: SomeIP
    hx_connect_user: someUser
    hx_connect_password: SomePassword
    mode: Create
    name: Demo-Datastore1
    VolumeSize: 1024
    sizeDescriptor: TB
    blockSize: 4K
# Delete a Datastore
- name: Delete Datastore
  hyperflex_datastore:
    hx_connect_ip: SomeIP
    hx_connect_user: someUser
    hx_connect_password: SomePassword
    mode: Delete
    name: Demo-Datastore1

# Verify a datastore
- name: Verify Datastore
  hyperflex_datastore:
    hx_connect_ip: SomeIP
    hx_connect_user: someUser
    hx_connect_password: SomePassword
    mode: Verify
    name: Demo-Datastore1
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url
import re,json



def run_module():
    module_args = dict(
        hx_connect_ip=dict(type='str', required=True),
        hx_connect_user=dict(type='str', required=True),
        hx_connect_password=dict(type='str', required=True, no_log=True),
        mode=dict(type="str", required=True, choices=['Create','Delete', 'Verify']),
        name=dict(type="str", required=True),
        volumeSize=dict(type="int", required=False),
        sizeDescriptor=dict(type="str",required=False,choices=['GB','TB'], default='TB'),
        blockSize=dict(type="str",required=False, choices=['4K','8K'], default='4K'),
        validate_certs=dict(type='bool',required=False, default=True)
    )
    result = dict(
        changed=False,
        authSuccess='',
        driveID=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)
    
    #######################################################################################
    # Start HyperFlex tasks here. 
    #######################################################################################

    #Authentication 
    auth = {
        "username": module.params['hx_connect_user'],
        "password": module.params['hx_connect_password'],
        "client_id": "HxGuiClient",
        "client_secret": "Sunnyvale",
        "redirect_uri": "https://localhost:8080/aaa/redirect"
    }

    required_fields = {
        "name": module.params['name'],
        "hx_connect_ip": module.params['hx_connect_ip']
    }

    if (module.params['mode']=='Create'):
        required_fields.update({"volumeSize": module.params['volumeSize']})
        required_fields.update({"sizeDescriptor": module.params['sizeDescriptor']})
        required_fields.update({"blockSize": module.params['blockSize']})
        result['createDrive']=hyperFlex(auth,module).createDatastore(required_fields)
    elif (module.params['mode']=='Delete'):
        result['deleteDrive']=hyperFlex(auth,module).deleteDatastore(required_fields)
    elif(module.params['mode']=='Verify'):
        result['verifyDrive']=hyperFlex(auth,module).verifyDatastore(required_fields)

#    result['authSuccess'] = hyperFlex(auth, module.params['hx_connect_ip']).createDatastore(module)
    result['driveID'] = 'Defined in the future'

    module.exit_json(**result)

class hyperFlex():
    def __init__(self, auth, module):
        self.module = module
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'   
        }
        self.auth = auth
        return

    def getData(self, hx_url, method, data):
        response, info = fetch_url(module=self.module, url=hx_url, headers=self.headers, method=method,data=data)
        #TODO If result is not 200, exit out with error... We are done... 
        return response, info
    
    def getToken(self,hx_connect_ip):
        hx_url = f"https://{hx_connect_ip}/aaa/v1/auth?grant_type=password"
        #print(hx_url)
        returned_data, info = self.getData(hx_url=hx_url, data=json.dumps(self.auth), method="POST")
        #TODO Ensure you got a token back by checking return result.
        self.headers["Authorization"] = f"Bearer {json.loads(returned_data.read())['access_token']}"
        return  self.headers["Authorization"]
    
    def createDatastore(self, required_fields):        
        ####### Six steps #######
        # 1) Get authorization token
        token_request_raw = self.getToken(required_fields['hx_connect_ip'])
        # 2) check token
        # 3) Check for existing datastore of the same name
        verify_request_raw = self.verifyDatastore(required_fields)
        # 4) Create Datastore if it does not already exist
        # 5) verify that the creation work.
        # 6) return properties or fail the procedure
        return f"{verify_request_raw}"
    def deleteDatastore(self,required_fields):
        # 1) Get authorization token
        # 2) check token
        # 3) Check for existing datastore of the same name
        # 4) Check for VMs in the data store (Must be zero or we will not delete it)
        # 5) Delete Datastore if it exists and has no systems in it.
        return
    
    def verifyDatastore(self,required_fields):
        # 1) Get authorization token
        if (self.headers.get('Authorization') is None):
            token = self.getToken(required_fields['hx_connect_ip'])
        # 2) Check for existing datastore of the same name
        hx_url = f"https://{required_fields['hx_connect_ip']}/rest/datastores"
        returned_data, info = self.getData(hx_url=hx_url, data=None, method='GET')
        return json.loads(returned_data.read())

def main():
    run_module()


if __name__ == '__main__':
    main()
