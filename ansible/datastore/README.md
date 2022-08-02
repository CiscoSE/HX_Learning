# An Ansible Module Demonstrating Creation, Validation and Deletion of HyperFlex Datastores
## THIS IS NOT FOR PRODUCTION! THIS IS AN EXAMPLE ONLY. 

This is demo code to show what is possible, but has not been tested extensively outside of the demo purpose for which it was written. We do not recommend running this code in production environments without testing and review of the code to ensure it meets your environments requirements. 

## How to run this demo
We assume that you have ansible configured to use python3. Any other option may impact your ability to run this demo example. This module only works with ansible, and was tested with ansible version 2.10.8 with python version 3.10.4 on ubuntu.

### Create an inventory File

Your inventory file should have the following entries in it saved as .ini file. Yaml inventory files are also possible, but that example is not provided here:

```
[hx_connect]
10.0.0.01	hx_connect_ip='10.0.0.1' hx_connect_user='administrator@vsphere.local' hx_connect_password='YourPasswordHere'
```

For the purposes of these directions, we assume the file is named **private.inventory.ini** and is in the same directory as the **test.yaml** playbook.

### Verify the test.yaml file
Make sure that the test.yaml file reflects your intentions before running it. Do not assume that the version in github is safe to run. We recommend you verify the following fields:

- **mode**: The mode variable can be **Create**, **Verify** or **Delete**.
  - The only safe mode is **Verify**
  - Only change **mode** in the vars area of test.yaml. This setting also impacts the behavior of output. 
- **name**: The **name** attribute should be something that doesn't exist in your environment if you will be using Create or Delete in the test.yaml

These additional options should be considered as well, but likely work fine for most demos:

- **volumeSize**: This is the size of the datastore you want to create based on the sizeDescriptor. If you want a 1 terabyte volume you can do 1024 for volume size and set the size descriptor to GB, or you can set volumeSize to 1 and set sizeDescriptor to TB. 
- **sizeDescriptor**: This can be set to TB or GB. If this attribute is not set, it is assumed to be GB. When set to GB, entries in volumeSize will be multiplied by 2^30. When sizeDescriptor is set to TB, volumeSize will be multiplied by 2^40.
- **blockSize**: This must be set to 4K or 8K. When set to 4K, bock size is set to 4096. When set to 8K, block size is set to 8192.

These settings should not be changed as they come from the INI file.

- **hx_connect_ip** - Management IP address for HX Connect.
- **hx_connect_user** - User name to log on to Hyperflex. This can be **admin** but is most often a vCenter authenticated user.
- **hx_connect_password** - Password for the hx_connect_user. 

### Copy the hyperflex_datastore.py file to the "configured module search path"
The configured module search path can be found by running the following ansible command:

```
ansible --version
ansible 2.10.8
  config file = None
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  executable location = /usr/bin/ansible
  python version = 3.10.4 (main, Jun 29 2022, 12:14:53) [GCC 11.2.0]
```

In this example you need to copy the **hyperflex_datastore.py** file to the **/usr/share/ansible/plugins/modules** directory. Your directory may be different. Only the paths listed under **configured module search path** are valid locations for this file.

### To run the demo
From the same directory as the **test.yaml** file, run the following command:
```
ansible-playbook -i private.inventory.ini test.yaml
```

