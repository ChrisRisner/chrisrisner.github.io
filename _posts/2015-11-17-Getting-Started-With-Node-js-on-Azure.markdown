---
layout: post
title: "Getting Started with Node.js on Azure"
date: Tue Nov 17 2015 20:16:00 GMT-0800 (PST)
comments: true
status: publish
type: post
published: true
categories: [Azure,Node.js,Web,Javascript]
excerpt: "A quick write up on how to get started with Node.js on Azure"
logoUrl: null
keywords: azure,node.js,web,javascript,getting started
filepath: 2015-11-17-Getting-Started-With-Node-js-on-Azure.markdown
disqus_identifier: 2015-11-17-Getting-Started-With-Node-js-on-Azure
redirect_from: 
  - /getting-started-with-node-js-on-azure/
---



For a while now I've been focusing on a number of different technologies on Azure outside of my usual focus on mobile development.  Today, I decided it would be a good idea to share some of the stuff I've learned.  In this post, I'm going to walkthrough how you can get started on Azure with Node.js applications.  I'm going to go through this as though you're setting up a new computer, so some of the steps might prove to be unnecessary for you.  If you haven't installed Node, Git, or Visual Studio Code (or whatever editor you prefer) yet, proceed on to the <a href="#Setup">Setup</a>.  If you're ok with skipping those steps, go jump to <a href="#creatingYourFirstNodeApp">Creating your First Node App</a>.

## Setup<a name="setup">&nbsp;</a>

In this seciton, we'll talk through installing a number of tools.  For the sake of this guide, I'll be doing most of the steps assuming that you're using OS X or Linux.  The steps should be similar if you're on Windows (though if you are, I'd recommend taking a look at the [Node Tools for Visual Studio](https://www.visualstudio.com/en-us/features/node-js-vs.aspx).  First we'll need to install Node.  

### Installing Node
Open the Terminal (&#8984; + Space and type in Terminal) and run the following command:

`node --version && npm --version`

If that comes back with *command not found* you'll probably need to install Node.  You can do so by visiting the [Node.js homepage](https://nodejs.org/) and downloading the correct version for your OS.

It's probably a good idea to update your version of Node if you're running an older version.  The following commands will perform that update, however, it should be **NOTED** that this can mess things up on complicated Node installs.  If you're at the point where you have a complicated Node set up, hopefully you've skipped on to <a href="#creatingYourFirstNodeApp">creating your first Node App</a> anyway.

{% highlight console %}
sudo npm cache clean -f
sudo npm intall -g n
sudo n stable
{% endhighlight %}


### Installing Git
Next you'll want to make sure you have Git installed.  You can do so by running the following command:

`git --version`

If you don't have Git installed, you can grab it from the [Git homepage](http://git-scm.com/).  

### Installing Visual Studio Code
<img style="width:100px;float:right;padding-left:20px" src="http://storage.chrisrisner.com/images/vscode.ico"/>If you've done a lot of Node development already, chances are good you already have a development environment you like to use.  If that isn't the case, I'd highly recommend [Visual Studio Code](https://code.visualstudio.com/).  Code is a lightweight code editor with intellisense, code assistance, navigation, and debugging built-in.  This editor works on OS X, Linux, and Windows, so no matter where you're developing you can use it.  Head to the [Code homepage](https://code.visualstudio.com/) and grab the installer for your platform.

## Creating your First Node App<a name="creatingYourFirstNodeApp">&nbsp;</a>
Now that you have all the prereqs installed, let's create our first app on Azure.  Now, we could choose to create a local app first, then upload that to Azure, but today we'll do things in a slightly more easy manner.  I'll post a followup article walking through creating a local site and putting it on Azure later (as there can be a few other steps).  We're going to start things off from the [Azure portal](http://portal.azure.com).  If you don't already have an Azure account, you can sign up for a [Free Azure Subscription here](https://azure.microsoft.com/en-us/pricing/free-trial/?WT.mc_id=A3F51C28C).  Don't worry, everything we're going to do today is in the free tier of Azure so even if you've already used the free trial benefits of Azure, our web application won't cost a thing.  

Let's go ahead and open the [Azure portal](http://portal.azure.com). You should get something that looks like this:

<img class="centeredInContent" style="width:550px;" src="http://storage.chrisrisner.com/images/azure-preview-portal.png"/>

This is our administrative and control center for everything in Azure.  There's quite a lot that can also be done from the command line, but we'll be using the portal today.  On the left side, click **New** then seelct **See all** to the right of MARKETPLACE, and select **Everything** from the Marketplace list.  Lastly, search for *node.js* and select **Express Web App** and then click *Create*:

<img class="centeredInContent" style="width:550px;" src="http://storage.chrisrisner.com/images/azure-portal-new-express-app.png"/>

If you haven't used [Express](http://expressjs.com/) before, it's a minimal web application framework for Node.js.  After clicking *Create* you'll be asked to name your app as well as pick an *App Service Plan/Location* and a *Resource Group*.  Click on the App Service Plan and this is where you can select what tier you want to run in (as well as the location).  To ensure you're staying within the Free Tier, select the *Pricing Tier* and then click *View all* at the top right.  At the very bottom you'll see the **F1 Free** tier which runs on shared infrastructure (and does not allow custom domains).  Select that (or go ahead and select something else if you're planning on paying).  Finish by naming your App Service Plan and choosing a location.  Next you can specify a *Resource Group* which is just a logical collection of resources.  This is useful if you want to check billing and usage for a specific group, limit access and roles to those groups, as well as a few other reasons.  When that's all done, click *Create*.  Those blades will close and after your app is created, you'll be taken to the blade for it.

Once your site finishes deploying and you're taken to the blade for it, at the top you'll see a *Browse* link that will take you to your running web app:

<img class="centeredInContent" style="width:550px;" src="http://storage.chrisrisner.com/images/azure-portal-web-app.png"/>

That will take you to the default Express site which just says:

<h1>Express</h1><p>Welcome to Express</p>

And that's all it takes to get our Node site running.

## Pulling Down the Code

The next step is to pull down the code so we can make changes and push it back up to Azure.  FTPS is always an option and it's enabled for all web apps if you want to use that.   Since we installed Git up above though, let's use that.  Return to the Azure portal and your web app.  Up above where we clicked on *Browse* go ahead and click on *Settings*.  This will open a Settings blade with many different options.  If you're new to Azure, the first thing you need to do is scroll down until you find *Deployment credentials* and click on that.  Here you can set a username and password to use with both Git and FTPS.  The username will need to be unique so you may have to try a couple times before you succeed.  Once that is done and saved, return to Settings and click on *Continuous Deployment* and then click on *Choose Source*.  There are a number of options we can connect our site to including Visual Studio Online, OneDrive, Local GIT, GitHub, BitBucket, Dropbox, and External Repository.  Today we're interested in pulling down the sample code that was already generated (as opposed to deploying from an existing code source elsewhere) so choose **Local Git Repository** then hit *Ok*.  You'll now be taken to a blade that says *No deployments found* becuase we haven't deployed any changes yet.  Return to Settings and go to the top and find *Properties*.  Scroll down on the Properties blade until you find *GIT URL* and copy the url.  Return to the terminal and clone your repo with the following:

`git clone <yourGitUrl>`

That should pull all of the code down locally.  Let's look at the file structure we have:

* public - Contains any static content we want to serve up (stylesheets, images, etc)
* routes - Contains JS files for any specific routes in our app (index, user)
* views - Contains any *Jade* layout files used by our routes
* node_modules - All installed Node modules
* package.json - A JSON file specifying all Node packages we're using
* favicon.ico - The small icon that shows up for your site in the browser
* server.js - The server file that sets up Express, sets up routes, etc
* web.config - A web configuration file that tells the web server running web apps to run Node

Let's take a quick look at the **web.config** file so we understand what's going on:

{% highlight xml %}
<!-- 
     This configuration file is required if iisnode is used to run node processes behind
     IIS or IIS Express.  For more information, visit:

     https://github.com/tjanczuk/iisnode/blob/master/src/samples/configuration/web.config
-->
<configuration>
     <system.webServer>
          <handlers>
               <!-- indicates that the app.js file is a node.js application to be handled by the iisnode module -->
               <add name="iisnode" path="server.js" verb="*" modules="iisnode"/>
          </handlers>
          <rewrite>
               <rules>                    
                    <!-- Don't interfere with requests for node-inspector debugging -->
                    <rule name="NodeInspector" patternSyntax="ECMAScript" stopProcessing="true">                    
                        <match url="^server.js\/debug[\/]?" />
                    </rule>

                    <!-- First we consider whether the incoming URL matches a physical file in the /public folder -->
                    <rule name="StaticContent">
                         <action type="Rewrite" url="public{REQUEST_URI}"/>
                    </rule>

                    <!-- All other URLs are mapped to the Node.js application entry point -->
                    <rule name="DynamicContent">
                         <conditions>
                              <add input="{REQUEST_FILENAME}" matchType="IsFile" negate="True"/>
                         </conditions>
                         <action type="Rewrite" url="server.js"/>
                    </rule>

               </rules>
          </rewrite>
          <!-- You can control how Node is hosted within IIS using the following options -->
        <!--<iisnode      
          node_env="%node_env%"
          nodeProcessCommandLine="&quot;%programfiles%\nodejs\node.exe&quot;"
          nodeProcessCountPerApplication="1"
          maxConcurrentRequestsPerProcess="1024"
          maxNamedPipeConnectionRetry="3"
          namedPipeConnectionRetryDelay="2000"      
          maxNamedPipeConnectionPoolSize="512"
          maxNamedPipePooledConnectionAge="30000"
          asyncCompletionThreadCount="0"
          initialRequestBufferSize="4096"
          maxRequestBufferSize="65536"
          watchedFiles="*.js"
          uncFileChangesPollingInterval="5000"      
          gracefulShutdownTimeout="60000"
          loggingEnabled="true"
          logDirectoryNameSuffix="logs"
          debuggingEnabled="true"
          debuggerPortRange="5058-6058"
          debuggerPathSegment="debug"
          maxLogFileSizeInKB="128"
          appendToExistingLog="false"
          logFileFlushInterval="5000"
          devErrorsEnabled="true"
          flushResponse="false"      
          enableXFF="false"
          promoteServerVars=""
         />-->
        <iisnode watchedFiles="*.js;node_modules\*;routes\*.js;views\*.jade"/>
     </system.webServer>
</configuration>
{% endhighlight %}

You can read through the invidual lines to understand what's going on specifically but concisely, we're telling IIS (which is what is running our web app) to run Node and run the **server.js** file.  

## Running Locally
The next step is to run our site locally.  Return to the terminal and navigate to your site's root directory.  Then type this:

`node server.js`

That should start your application listening on port **3000**.  So go to the browser and navigate to **http://127.0.0.1:3000** and you should see the same web site running.  

## A Small Change
Now, open the site in whatever editor you prefer and open the *routes/index.js* file and make a change to the title (here I've changed it to **AzureExpress**):

{% highlight javascript %}
/*
 * GET home page.
 */

exports.index = function(req, res){
  res.render('index', { title: 'AzureExpress' });
};
{% endhighlight %}

Now open up *views/index.jade* and modify the text (here I've added *on Azure* to the end):

{% highlight jade %}
extends layout

block content
  h1= title
  p Welcome to #{title} on Azure
{% endhighlight %}

Now we can use Git in the terminal to commit our changes like so:

{% highlight console %}
git add .
git commit -m "Modifying the index"
git push origin master
{% endhighlight %}

If you stay in the terminal now, you'll see a number of *remote* updates that indicate that Azure is doing a redeploy of your site.  After a few moments you should messages that say *Finished successfully* and *Deployment successful*.  If you return to your site in the browser, you should now see it is updated.  If you go back into Settings and Continuous Deployment in the portal, you should also now see that a new deployment has shown up:

<img class="centeredInContent" style="width:550px;" src="http://storage.chrisrisner.com/images/azure-portal-node-deployment.png"/>

You can also click on that deployment and see a log of the deployment steps as well as redeploy older versions.  

## Summary

Today we went from zero to having Node, Git, and Visual Studio Code installed.  We also deployed a new Node.js Express app into Azure, pulled the code down, made local changes, and redeployed it using Git.  All of this in only a matter of minutes and without having to do anything complex.  From here though, the sky is the limit in what you can build.  Additionally there are a LOT of features of Web Apps that we didn't look at.  A great way to get started with understanding some of the other built-in features is to scroll down the Settings blade in the portal.  