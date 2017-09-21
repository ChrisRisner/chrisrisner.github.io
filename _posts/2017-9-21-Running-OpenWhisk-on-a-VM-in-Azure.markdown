---
layout: post
title: "Running OpenWhisk on a VM in Azure"
date: Thu Sep 21 2017 9:16:00 GMT-0800 (PST)
comments: true
status: publish
type: post
published: true
categories: [Serverless,Azure,VM]
excerpt: "This post will walk through how you can deploy OpenWhisk onto a VM running in Azure."
logoUrl: null
keywords: Serverless,Azure,VM
filepath: 2017-9-21-Running-OpenWhisk-on-a-VM-in-Azure.markdown
disqus_identifier: 2017-9-21-Running-OpenWhisk-on-a-VM-in-Azure
redirect_from: 
  - /running-openwhisk-on-a-vm-in-azure/
---

I've recently been doing some evaluations of open source Serverless frameworks and seeing how well they run on Azure.  One of the first such projects I tried out was [OpenWhisk](https://openwhisk.incubator.apache.org/). OpenWhisk is a project created and open sourced by IBM.  You are able to run it on-prem and in the cloud, on top of IBM offering a managed service as part of their cloud.  As a first step in getting OpenWhisk to run, I wanted to deploy it on to a single VM running in Azure.  As I ran into a few issues, I wanted to share a walkthrough of how to get OpenWhisk running on a Linux VM in Azure.

### Creating an Azure VM

Your first step should be to create a Linux VM in Azure.  For this walk-through, I created an Ubuntu Server 16.04 LTS vm.  I chose the DS1_V2 Standard size though you'd probably get by with something smaller if desired.  In the interest of being very specific, I used the default VM settings at the time including:
* No Availability Set
* Managed Disks for storage
* Default Virtual Network, Subnet, Public IP, Network security group
* No extensions
* Auto-shutdown set to Off
* Boot Diagnostics turned On
* Guest OS diagnostics disabled
* Default storage account name

Once your VM is up and running (just a couple of minutes max), if you've done it in the Azure Portal, you should be taken to the blade in the portal for the VM.  If you didn't use the portal, you can [open it](http://portal.azure.com) and navigate to your VM.  Clicking the **Connect** button at the top of that blade will give you the **SSH** command to use to connect which should be similar to "ssh adminUserName@publicIPAddress".  Copy that into a terminal / SSH tool and connect to your VM.

### Installing and Setting Up OpenWhisk

The first step is going to be pulling down the source code for the [Apache OpenWhisk](https://github.com/apache/incubator-openwhisk) project:

  ```
  git clone https://github.com/apache/incubator-openwhisk.git
  ```

They've provided a set up script for Ubuntu which will do a decent amount of the prep work for your VM so you should run that next:

  ```
  ./incubator-openwhisk/tools/ubuntu-setup/all.sh
  ```

This will run for a few minutes and you'll follow it up with a few more package installs:

  ```
  pip install --upgrade pip
  sudo pip install ansible==2.3.0.0
  sudo apt-get install couchdb
  sudo apt-get install docker.io
  sudo pip install docker-py
  ```

Note that I've tried to minimize the need to run most of these things as root though, as near as I can tell, this is necessary for some package installs.  Next, now that CouchDB (which backs OpenWhisk) is installed, we need to create an Admin user:

  ```
  curl -s -X PUT http://localhost:5984/_config/admins/username -d '"password"'
  ```

The response to that command should just be an empty set of quotes ("").  Next we need to tell CouchDB to listen on more than just 127.0.0.1 so that we can access it from the docker containers that we'll soon be deploying.

  ```
  sudo nano /etc/couchdb/local.ini
  ```

Near the top of this file, you should see a commented out line that starts with **bind_address**.  You'll want to uncomment it and set the IP to all zeros:

  ```
  bind_address = 0.0.0.0
  ```

Save that file and then restart CouchDB:

  ```
  sudo systemctl restart couchdb.service
  ```

You're now ready to output some variables that will be used during the OpenWhisk setup:

  ```
  export OW_DB=CouchDB
  export OW_DB_USERNAME=username
	export OW_DB_PASSWORD=password
	export OW_DB_PROTOCOL=http
	export OW_DB_HOST=VMHOSTNAME
	export OW_DB_PORT=5984
  ```

Now here, the **username** nad **password** should match the values you've used when you created the CouchDB admin user above.  Also, you'll want to replace **VMHOSTNAME** with the name of your actual VM.  Next we'll run our Ansible playbooks:

  ```
  cd incubator-openwhisk/ansible
  ansible-playbook setup.yml
  ```

Since we ran the earlier Ubuntu-setup/all.sh script, some default values will have been applied for the database connection info that we'll need to override.

  ```
  nano db_local.ini
  ```

Now you'll need to replace **db_username**, **db_password**, and **db_host** with the same values you used up above.  Save your changes to that file.

Now we need to grant our user Docker access so we don't need to run future playbooks as root:

  ```
  sudo usermod -aG docker cloudadmin
  ```

We need to make this change take affect and as near as I can tell, just disconnecting and reconnecting won't do it.  To be safe, I have gone in and restarted the VM from the Azure Portal and then reconnected.  Next we'll run a nice long gradle build:

  ```
  cd ~/incubator-openwhisk
  ./gradlew distDocker
  ```

Now we can execute the rest of the playbooks:

  ```
  cd ansible
  ansible-playbook initdb.yml
  ansible-playbook wipe.yml
  ansible-playbook apigateway.yml
  ansible-playbook openwhisk.yml
  ansible-playbook postdeploy.yml
  ```

### Testing OpenWhisk

With all of our Ansible playbooks run, we can now use the **wsk** command line tool to talk to execute functions on OpenWhisk.  In order to do so, we need to either pass, or set, the API Host and Auth values for the command line.  We'll do the latter:

  ```
  cd ../bin
  ./wsk property set --apihost http://172.17.0.1:10001
  ```

In order to get the auth value out, we'll print out the value from the auth.guest file:

  ```
  cat ../ansible/files/auth.guest
  ```

Copy that value into this command:

  ```
  ./wsk property set --auth AUTHVALUE
  ```

Now finally, we can invoke something:

  ```
  ./wsk action invoke /whisk.system/utils/echo -p message hello --result
  ```

If all goes well, your output should look like this:

  ```
  {
    "message": "hello"
  }
  ```
And now you're running OpenWhisk.  From here you might expand by running on a Kubernetes cluster, deploying applications that also run on-prem, etc.


