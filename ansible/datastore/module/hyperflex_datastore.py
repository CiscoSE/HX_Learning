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



def run_module():
    module_args = dict(
        hx_connect_ip=dict(type='str', required=True),
        hx_connect_user=dict(type='str', required=True),
        hx_connect_password=dict(type='str', required=True, no_log=True),
        mode=dict(type="str", required=True, choices=['Create','Delete', 'Verify']),
        name=dict(type="str", required=True),
        volumeSize=dict(type="int", required=False),
        sizeDescriptor=dict(type="str",required=False,choices=['GB','TB'], default='TB'),
        blockSize=dict(type="str",required=False, choices=['4K','8K'], default='4K')
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

    result['authSuccess'] = "Maybe"
    result['driveID'] = 'Defined in the future'

    module.exit_json(**result)

class hyperFlex():
    def __init__(self):
        return

    def getData():
        return

def main():
    run_module()


if __name__ == '__main__':
    main()
