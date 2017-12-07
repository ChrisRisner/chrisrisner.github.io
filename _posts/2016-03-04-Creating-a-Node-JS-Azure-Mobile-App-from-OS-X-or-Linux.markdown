---
layout: post
title: "Creating a Node.js Azure Mobile App from OS X or Linux"
date: Fri Mar 04 2016 20:16:00
commentsOn: true
status: publish
type: post
published: true
categories: [Azure,Mobile,Mobile Apps]
excerpt: "This post walks through how to easily use Fragments with the Navigation Drawer Activity available in Android Studio."
logoUrl: null
keywords: Azure,Mobile Apps,Node.js,osx,linux
filepath: 2016-03-04-Creating-a-Node-JS-Azure-Mobile-App-from-OS-X-or-Linux.markdown
disqus_identifier: 2016-03-04-Creating-a-Node-JS-Azure-Mobile-App-from-OS-X-or-Linux
redirect_from: 
  - /creating-a-node-js-azure-mobile-app-from-os-x-or-linux/
---

In today's post, I'm going to walk through how you can set up a new Azure Mobile App backend running Node.js entirely from OS X or Linux.  To do this we'll use the following tools:

* [Azure CLI](https://azure.microsoft.com/en-us/documentation/articles/xplat-cli-install/)
* [Yeoman](http://yeoman.io/)
* [Visual Studio Code](https://code.visualstudio.com/)
* [Azure Subscription](https://azure.microsoft.com/en-us/pricing/free-trial/?WT.mc_id=A3F51C28C)
* [Node.js](https://nodejs.org/en/)

I won't go through installation steps for each of those pieces, you can find that at the accompanying link.  Instead we'll focus on what to do once you have everything installed.

### Connecting to you Azure account from the CLI

The first step is to turn on Azure Resource Management mode using the following command:

```azure config mode arm```

Next, authenticate to your Azure account.  Open a Terminal window and enter 

```azure login```

You will be prompted to open a web browser and given a URL like http://aka.ms/devicelogin and a code to enter.  After entering the code and logging in with your Azure account, return to the terminal.

All subscriptions available to your account will be *added* to your local account and you'll be connected to the first Azure subscription as the default.  If you have multiple subscriptions and want to change to a different subscription, you can first list them off with 

```azure account list``` 

and then change subscriptions with 

```azure account set <subscriptionNameOrId>```

### Creating a Resource Group

Within Azure, instances of any services you create are done so as part of a **Resource Group**.  This is a logical container that holds related resources for an application.  What matters here is that we need to create a Resource Group before we can create any resources.  You can [read more about Resource Groups and Azure Resource Manager (which we'll mention a bit more delow) here](https://azure.microsoft.com/en-us/documentation/articles/resource-group-overview/).  To create our group, we run this command:

```azure group create -n <ResourceGroupName> -l "<Location>"```

So for my group, I ran this command:

```azure group create -n MyMobileAppResourceGroup -l "West US"```

Shortly there after, you'll get the output of that command:

```
info:    Executing command group create
+ Getting resource group MyMobileAppResourceGroup                              
+ Creating resource group MyMobileAppResourceGroup                             
info:    Created resource group MyMobileAppResourceGroup
data:    Id:                  /subscriptions/<SubscriptionID>/resourceGroups/MyMobileAppResourceGroup
data:    Name:                MyMobileAppResourceGroup
data:    Location:            westus
data:    Provisioning State:  Succeeded
data:    Tags: null
data:    
info:    group create command OK
```  
Now we're ready to create our Mobile App.

### Creating our Mobile App (and SQL DB)

Many resources in Azure have specific sections under them for manipulation of those resources.  You can see a full list by just running

```azure ```


at the command line.  As of writing, that includes resources such as webapps, vms, storage accounts,and many more.  What it currently doesn't include is anything for Mobile Apps.  This means that we have to handle the creation of our Mobile App a bit differently.  Thankfully, Azure Resource Manager has support for templates (JSON files) which declaritively define a deployment.  Put planely, these are JSON files that detail the pieces involved in a deployment such as what services to create (a SQL DB and Mobile App) along with any information needed to create those resources (i.e. names, locations, usernames, passwords, etc).  You can take an existing architecture and get a template from it, or you can start with the many [pre-created templates available on GitHub](https://github.com/Azure/azure-quickstart-templates) to start your deployment.  Today we're specifcially going to make use of a [template for a Mobile App](https://github.com/Azure/azure-quickstart-templates/tree/master/101-mobile-app-create).  Within that repository there are two JSON files:  [azuredeploy.json](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/101-mobile-app-create/azuredeploy.json) and [azuredeploy.parameters.json](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/101-mobile-app-create/azuredeploy.parameters.json).  You'll want to download both of those files locally to your computer.

Before we can deploy the template, you'll need to edit the **azuredeploy.parameters.json** file to specify the name of your Mobile App, the SQL Server username and password, and the location:

```
{
  "$schema": "http://schema.management.azure.com/schemas/2015-01-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "appName": {
      "value": "mobileappfromthecli"
    },
    "location": {
      "value": "West US"
    },
    "sqlServerAdminLogin": {
      "value": "NewAdmin"
    },
    "sqlServerAdminPassword": {
      "value": "My$up3rPassWERD"
    }
  }
}
```    

With that done, we can now deploy to Azure with this command:

```azure group deployment create -f azuredeploy.json -e azuredeploy.parameters.json -g MyMobileAppResourceGroup -n MyMobileAppDeployment```

Here we're specifying the template file, the parameters file, the group to deploy to, and the name of the deployment.  This command will take a few minutes to complete but when it's done, you should see something like this:

```
info:    Executing command group deployment create
+ Initializing template configurations and parameters                          
+ Creating a deployment                                                        
info:    Created template deployment "MyMobileAppDeployment"
+ Waiting for deployment to complete                                           
data:    DeploymentName     : MyMobileAppDeployment
data:    ResourceGroupName  : MyMobileAppResourceGroup
data:    ProvisioningState  : Succeeded
data:    Timestamp          : 2016-03-04T06:25:53.9360068Z
data:    Mode               : Incremental
data:    Name                     Type          Value                       
data:    -----------------------  ------------  ----------------------------
data:    appName                  String        mobileappfromthecli         
data:    location                 String        West US                     
data:    hostingPlanSettings      Object        [object Object]             
data:    sqlServerAdminLogin      String        NewAdmin                    
data:    sqlServerAdminPassword   SecureString  undefined                   
data:    sqlDatabaseEdition       String        Basic                       
data:    sqlDatabaseCollation     String        SQL_Latin1_General_CP1_CI_AS
data:    sqlDatabaseMaxSizeBytes  String        1073741824                  
info:    group deployment create command OK
```

Here we get a lot of details back indicating that everything was provisioned successfully.  This means that we've succesfully created a Mobile App, a SQL Server, a SQL Database, and a Notification Hub.  Today we're just focusing on the Mobile App.

### Setting up a Git repo

Unfortunately, we've reached an impasse as far as what can be done from the command line.  We can (and will) generate our app backend using the command line, but we can't really set up a way to deploy that code to our Mobile App.  Instead, we'll go to the Azure Portal to star the next step.

Open up the [Azure Portal](http://portal.azure.com) and look for **App Services** on the left navigation (if it isn't showing up, look for **Browse** at the bottom and then find **App Services** from there).  Find your App Service in the list (if this is the first thing you've created, there will only be one listed).  We're focusing on doing as much as possible from the command line today, but everything we've done so far (create our App Service and connected services) can be done from the portal along with MANY things that can't (like what we're about to do).  When oyu first open your App Service, the **Settings** blade should be open by default, but if not, at the top of your App Service's blade, you should see **Settings** with the familiar gear image.  Click that and then in the Settings blade (to the right of your App Service), look for **Continuous Deployment** underneath **PUBLISHING**.

Here we'll need to choose **Choose Source** to configure deployment.  There are many (7 at writing) different options for deployment, to make things easy today, we'll just choose **Local Git Repository**.  This will create a Git repository within Azure which we can push and pull from to deploy changes to our Mobile App backend.  After a few moments, the process will complete and the body should change to say "No deployments found."

Next we need to set up credentials.  Under **Continuous Deployment** you should see **Deployment credentials**.  Once you've gone into that blade you can enter a username and password for Git and FTP.  

The last thing we'll do in the portal for now is get our Git URL.  Return to the **Settings** blade and scroll up to **Properties**.  Within that blade you'll see **Git URL**.  Grab that for later.

### Creating a Node backend

You should have already installed Yeoman (listed in the tools at the top).  I left out one tool that plugs into Yeoman.  If you haven't used Yeoman before, it's a tool for scaffolding out projects.  If you've used something like Visual Studio, Eclipse, or Xcode before, you've almost certainly had the File -> New Project experience.  When it comes to developing in Visual Studio Code (or sublime text, atom, etc), trying to create a new project type wizard for each editor would be a bit excessive.  For that reason, ther are thousands of generators that can be installed into Yeoman to help scaffold our *projects* of all types (Node, wordpress, jeykll, asp.net, etc).  For today, you'll need to install the azure-mobile-apps generator with this command:

```
sudo npm install -g yo generator-azure-mobile-apps
``` 

Note that you may not *need* to use *sudo* but I did so I've included it.  Next we create our backend:

```yo azure-mobile-apps```

**NOTE** that this drops files into the directory you're in so create a directory for your app first.  That will generate a bunch of files including a fully functioning backend for our apps.  

### Deploying to Azure

First we need to setup git locally in the directory you just created your mobile app in:

```git init```

Now we add the remote using the Git URL that you got above:

```git remote add origin https://username@MyMobileApp.scm.azurewebsites.net:443/MyMobileApp.git```

Now we can add, commit our files, and push to Azure:

```
git add .
git commit -m "Initial check-in"
git push origin master
```

You'll be prompted for the password which you entered in the credentials blade above.  It will take a few minutes to push the code up to the server and restart your site.  If you now browse to the site (you can do so easily by returning to the portal and clicking the **Browse** button in the blade for your App Service) you'll be taken to a page which says:

**You've encountered an Azure Mobile Apps Site**

That is our default homepage.  The next step is to test out the Tables and APIs functionality provided by our Mobile App.  Currently, the mobile app generator creates one table and one API, though both of them require authenticated clients.  We'll turn off authentication in order to properly test things out (in an easier manner).  

### Turning off Auth and adding Todo Items

Open up [Visual Studio Code](http://code.visualstudio.com/) (or your editor of choice) and open the directory for your Mobile App.  Inside of hte **server** folder, you'll see the folders **api** and **tables**.  Start by opening **api/example.js**.  Near the bottom, you'll see:

```api.get.access = 'authenticated';```

You'll need to change that to anonymous like so:

```api.get.access = 'anonymous';```

If you haven't played with Mobile Apps / Services before, changing from authenticated to anonymous means we don't have to send over a Mobile Apps Auth Token in order to call the API.  Since we're just going to test out our APIs and tables from the command line (without a real app) we aren't going to authenticate today.

Next open up **tables/example.js** and edit:

```table.access = 'disabled';```

To be:

```table.access = 'anonymous';```

The last thing we'll do is add a new table for Todo Items.  Create a new file within the **tables** directory and name it **todoitem.js** and put in the following contents:

```
var azureMobileApps = require('azure-mobile-apps');

var table = azureMobileApps.table();

// Defines the list of columns
table.columns = {
    "text": "string",
    "complete": "boolean"
};
// Turns off dynamic schema
table.dynamicSchema = false;

module.exports = table;
```  

Now you can push all of your changes back up to Azure:

```
git add .
git commit -m "Updating tables and APIs"
git push origin master
```

### Testing from the command line

Normally, the next step would be to create an iOS, Android, or Windows app to start hitting your Mobile App backend.  That's outside the scope of today (but if you want to get started quickly, you can go to the **Quick Start** option under the **Settings** for your Mobile App to generate clients quickly).  Today we're going to test wiht CURL which is a command line tool for creating HTTP requests.  We'll start simple and just pull down the home page.  Go to the command line and enter this (make sure you change the URL to match your app's):

```curl http://<YourMobileApp>.azurewebsites.net/```

This should output the HTMl for your web page.  Next let's try hitting our APIs:

```curl --header "ZUMO-API-VERSION:2.0.0" http://<YourMobileApp>.azurewebsites.net/api/example```

If you took a look at the **api/example.js** you'll know when you do a GET request against it, it just take a data object with one value in it and returns it as JSON.  So when we make the above request, we get the following:

```{"example":20}```

Next up, let's call the tables:

```curl --header "ZUMO-API-VERSION:2.0.0" http://mobileappfromthecli-n3ajngt3gbvjs.azurewebsites.net/tables/example```

This will just return **[]** because the *example* table isn't set up to really do anything.  The Todo Item table will be much better:

```url --header "ZUMO-API-VERSION:2.0.0" http://mobileappfromthecli-n3ajngt3gbvjs.azurewebsites.net/tables/todoitem```

Right now, this will also return **[]** becuase there is no data in our table.  Let's add some:

```curl --data '{"text":"test","complete":false}' --header "Content-Type: application/json" -X POST --header "ZUMO-API-VERSION:2.0.0" http://mobileappfromthecli-n3ajngt3gbvjs.azurewebsites.net/tables/todoitem```

Here, we're doing a similar request as before but we're passing in **data**, changing the **Content-Type** with an additional header, and lastly we're changing the request type with the **-X** parameter so we can do a POST instead of a GET.  When we post that item, we'll get back the updated item which includes the content of what we sent up in addition to the following field: id, version, createdAt, updatedAt, and deleted.

Now that we've inserted data, let's pull the data again and see what comes out:

```url --header "ZUMO-API-VERSION:2.0.0" http://mobileappfromthecli-n3ajngt3gbvjs.azurewebsites.net/tables/todoitem```

We should get back a list of all items we've saved so far (so in our case one item):

```[{"id":"427a9e3d-32a6-483f-9e51-9c4a82349d96","version":"AAAAAAAAB9I=","createdAt":"2016-03-04T17:48:04.368Z","updatedAt":"2016-03-04T17:48:04.384Z","deleted":false,"text":"test","complete":false}]```

### Summary

Today we walked through how you can create an Azure Mobile App from the command line using open source tools like Yeoman, the Azure CLI, Node.js, and Visual Studio Code.  The [Azure Portal](http://portal.azure.com) provides a great experience for doing all of this as well, in addition to even more features that Azure Web Apps provides.