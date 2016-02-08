---
layout: post
title: "Creating a Node.js Azure Mobile App from OS X or Linux"
date: Mon Feb 08 2016 20:16:00 GMT-0800 (PST)
comments: true
status: publish
type: post
published: false
categories: [Azure,Mobile,Mobile Apps]
excerpt: "This post walks through how to easily use Fragments with the Navigation Drawer Activity available in Android Studio."
logoUrl: null
keywords: Azure,Mobile Apps,Node.js,osx,linux
filepath: 2016-02-08-Creating-a-Node-JS-Azure-Mobile-App-from-OS-X-or-Linux.markdown
disqus_identifier: 2016-02-08-Creating-a-Node-JS-Azure-Mobile-App-from-OS-X-or-Linux
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

## Connecting to you Azure account from the CLI

THe first step is to open the CLI and authenticate to your Azure account.  Open a Terminal window and enter ```azure login```.  You will be prompted to open a web browser and given a URL like http://aka.ms/devicelogin and a code to enter.  After entering the code and logging in with your Azure account, return to the terminal.

All subscriptions available to your account will be *added* to your local account and you'll be connected to the first Azure subscription as the default.  If you have multiple subscriptions and want to change to a different subscription, you can first list them off with ```azure account list``` and then change subscriptions with ```azure account set <subscriptionNameOrId>```.

## Creating a SQL Database

Now that you've authenticated from the CLI, let's create a new Mobile App.  Before we can even set up our Mobile App though, we need to create a SQL Server and Database.  We can first create a server with this command:

```azure sql server create <AdminUsername> <AdminPassword> "<Location>"```

After a few moments, the command will complete and it will print out the name of your new server.  Before we can create a new database, we need to open the SQL Server's firewall to allow us to issue commands to it.  Once you get your IP Address, you can do so with this command:

```azure sql firewall rule create <ServerName> <RuleName> <StartIPAddressRange> <EndIPAddressRange>```

You can put your public IP address in for both the start and the end here if you want.  Also, the *RuleName* can be anything.  Remember to remove this rule (via the command line or portal when you're done).  One last thing to note is that it can take up to five minutes for the rule to take effect (even if it is already showing up in the firewall rules list).  Now we're ready to create a new database with this command:

```azure sql db create <ServerName> <DatabaseName> <AdminUsername> <AdminPassword>```

If you run this command and still receive an error about not having access, it's possible you might not have used the right IP address when you created the firewall rule.  Thankfully "You don't have access" error contains the IP that Azure believes you're coming from so you can re-run the firewall rule command with that IP address (just make sure you use a different rule name).  Once you get a success back from creation, you're ready to create your Mobile App.

## Creating a Mobile App

Armed with a new SQL Server and Database, you're ready to create a Mobile App.  To do so, run the following command:

```azure mobile 



tfyc8trbat mobileappdb mobileappadmin M0bile@pp
