# An Ansible Module Demonstrating Creation, Validation and Deletion of HyperFlex Datastores
## THIS IS NOT FOR PRODUCTION! THIS IS AN EXAMPLE ONLY. 

This is demo code to show what is possible, but has not been tested extensively outside of the demo purpose for which it was written. We do not recommend running this code in production environment without testing and review of the code to ensure it meets your environments requirements. 

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
- **name**: The **name** attribute should be something that doesn't exist in your environment if you will be using Create or Delete in the test.yaml

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

