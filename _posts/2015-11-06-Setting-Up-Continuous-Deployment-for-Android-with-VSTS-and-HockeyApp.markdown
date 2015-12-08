---
layout: post
title: "Setting up Continuous Deployment for Android with VSTS and HockeyApp"
date: Fri Nov 06 2015 20:16:00 GMT-0800 (PST)
comments: true
status: publish
type: post
published: true
categories: [Android,Azure,Visual Studio Team Services,CI]
excerpt: "How to set up Continous Integration for an Android app with Visual Studio Online"
logoUrl: null
keywords: android,ci,vso,visual studio online,hockeyapp
filepath: 2015-11-06.Setting-up-Continuous-Deployment-for-Android-with-VSTS-and-HockeyApp.markdown
disqus_identifier: 2015-11-06-Setting-up-Continous-Deployment-for-Android-with-VSO-and-HockeyApp
redirect_from: 
  - /Setting-Up-Continuous-Integration-for-Android-with-VSO-and-HockeyApp/
  - /setting-up-continuous-integration-for-android-with-vso-and-hockeyapp/
  - /setting-up-continuous-deployment-for-android-with-vso-and-hockeyapp/
---

###Shortly after this post, Visual Studio Online was rebranded as Visual Studio Team Services.  Same great service, more logical name!

Last year in November, I helped with an event in New York called Connect().  At that event, one of the things we showed off was the next generation build system for [Visual Studio Online (VSO)](https://www.visualstudio.com/).  This system enabled building of all sorts of apps.  More than just building the apps though, it also enabled running unit tests, fulfilling the needs of continuous integration, and also allowed for additional abilities like packaging up an application, sending the results somewhere, and much more.  What was so great, and was really the reason for my involvement, was that this next-gen build system worked with so many platforms and programming languages.  Of primary importance to me: Android and iOS.  You can [watch the full announcement related to the VSO build system here](https://channel9.msdn.com/Events/Visual-Studio/Connect-event-2014/015) if you like.

##HockeyApp

Not long after Connect() (in fact only a month later), [Microsoft announced it was acquiring HockeyApp](http://hockeyapp.net/blog/2014/12/11/hockeyapp-joins-microsoft.html).  If you haven't heard of HockeyApp, it enables you to distribute Android, iOS, and Windows Phone apps through a beta distribution channel, gather feedback, as well as crash analytics.  If you're an iOS developer, you've probably heard of TestFlight which provided similar functionality prior to being acquired by Apple (and kind of does again).  On the Android side, Google eventually added beta distribution to Google Play, but at the time it wasn't as fully featured as HockeyApp.  If you're using those services and are building apps for both iOS and Android, that's two completely different processes.  HockeyApp provides one streamlined process for all kinds of apps.

##The Point

The point of all of this is that if you add these two pieces together, we should be able to make an Android application, set up continuous integration with VSO, then tie into HockeyApp for beta distribution.  What we should be able to do is build our app whenever the code is checked into VSO, run the unit tests, and if they pass, deliver a new version of our application to HockeyApp to distribute to our beta testers.  How magical would this be?  Well today, I'm going to explain how to do it.

##Visual Studio Online

The first step is you need to create an account on VSO.  You can do that by going to the [Visual Studio homepage](https://www.visualstudio.com/) and clicking the link for **Get started for free** under Visual Studio Online.  That will prompt you to login with a Microsoft account (or a work or school account).  Now if you're not familiar with VSO, in my mind it is first and foremost a version control system.  A **FREE** one that has support for both Git and Team Foundation.  Within the free tier of VSO, you can have up to five contributors.  So you can have up to 5 people all contributing on the same project for free.  Above and beyond the source control, you also get project management: work items, bugs, tasks, etc.  

When you first sign up, you'll [create your first project](https://www.visualstudio.com/en-us/get-started/setup/connect-to-visual-studio-online).  This is where you can choose between using Git and Team Foundation Server.  Once that is done, you'll need to check your code in.  I won't dive into all of the details of getting your code into VSO but you can [read more about it here](https://www.visualstudio.com/get-started/code/share-your-code-in-git-vs).  Once your code is in, it's time to get building set up.

##Let's Get Building

Now that your code is checked in, it's time to set up a build.  You first need to navigate to your projects home page and then go to the **BULD** tab.  You can also find it by going to a URL that will look like this https://<YourOrgName>.visualstudio.com/DefaultCollection/<YourProject>/_build.  Make sure you replace the two placeholders there.  For example, my org name is *ChrisRisner* and your project would be named whatever you created in the steps above. 

<img src="http://storage.chrisrisner.com/images/vso-build-def.png" alt="VSO Build Definition" style="width:500px;" class="centeredInContent"/>

If this is a brand new project, you won't likely have a Build Definition already.  Click the green addition symbol in the top left to add a new definition.  Currently there are only four definitions available (Visual Studio, Xamarin.Android, Xamarin.iOS, and Xcode).  None of these will work for us, so choose **Empty** and click OK.  The next step is to begin to add some build steps so click the **+ Add build step...** link.

<img src="http://storage.chrisrisner.com/images/vso-build-steps.png" alt="VSO Build Definition" style="width:500px;" class="centeredInContent"/>

Here we're looking for the first (currently) option for **Android Build**.  Click the *Add* button next to that and then click the *Close* button at the bottom.  

<img src="http://storage.chrisrisner.com/images/vso-android-build-config.png" alt="VSO Build Definition" style="width:500px;" class="centeredInContent"/>

Now we can configure the Android Build steps.  For *Location of Gradle Wrapper* navigate to find your **gradlew.bat**.  For *Project Directory* choose where your project resides in the repository.  For *Gradle Arguments* depending on when you do this, there may be a default one for **build**.  If nothing is there, put in **clean build** to ensure APKs are compiled.  You then have some options for *Android Virtual Device*, *Emulator Options*, and *Control Options*.  We may look at those in more detail another time.  For now, *Save* your changes.  Once you've done so the *Queue build...* button should now be available to be clicked.  Go for it!  If you haven't done anything different from above (create a Queue, used different branches, etc) you'll be able to click *OK* on the next pop-up and the build will be queued.  Since we're not using our own build agent but a public grouping of them, you may have to wait for the build to start, but you should immediately be taken to a window with a text console that will print out as the build proceeds:

<img src="http://storage.chrisrisner.com/images/vso-build-in-progress.png" alt="VSO Build in Progress" class="centeredInContent"/>

You'll need to give that some time.  On my fairly simple app (a few activities and a few dependencies) the build took 4.4 minutes to complete.  If you have a success, you'll get something like this:

<img src="http://storage.chrisrisner.com/images/vso-build-successful.png" alt="VSO Build Successful" class="centeredInContent"/>

If your build wasn't succesful, you'll get a much less fun **Build Failed**.  However, you'll be able to get all of the details on *WHY* it failed:

<img src="http://storage.chrisrisner.com/images/vso-build-failed.png" alt="VSO Build Failed" class="centeredInContent"/>

The screenshot above is from an earlier build I'd done on my project.  At that point, VSO wasn't yet including the proper repositories for the **appcompat** and **design** libraries within **com.android.support**.  Hopefully if you run into any issues it has to do with something you can fix.  If it's something like the issue above, [reach out to the VSO team for help](https://www.visualstudio.com/en-us/support/support-overview-vs).  

##Setting up HockeyApp
The next step is to connect our build so when it's done, it sends something over to HockeyApp.  If you don't already have an account, you can sign up for a [free trial at HockeyApp.net](http://hockeyapp.net).  Once that is done, you should [create a new app](http://support.hockeyapp.net/kb/app-management-2/how-to-create-a-new-app) (unless you already have an app setup).  After that we're going to do some work on the command line to add the HockeyApp task to VSO.  Go to the Terminal and enter the following:

{% highlight console %}
sudo npm install -g tfx-cli
tfx login
{% endhighlight %}

When you log in, the first prompt will be for your *Collection URL*.  You can get this from the URL of your VSO project.  Unless you've set up custom collections, you're probably looking at a URL like this: https://<YourOrgName>.visualstudio.com/DefaultCollection.  The second prompt is for your *Personal Access Token*.  In order to generate an Access Token, you should go to VSO, click on your name in the top right, and click on **My profile**.  From there [follow these steps to create an Access Token](http://roadtoalm.com/2015/07/22/using-personal-access-tokens-to-access-visual-studio-online/).  Afterwards, enter your token in the Terminal and proceed and you should receive a *logged in successfully* message.  Next we install another node module and upload it:

{% highlight console %}
sudo npm install -g http://aka.ms/vsohockeytask
cd /usr/local/lib/node_modules/
tfx build tasks upload ./ --overwrite
{% endhighlight %}

You should then see a message that the task was uploaded successfully.

## Connecting HockeyApp and our build
Return to VSO in the browser.  Go back to your Build Definition and click the Edit button.  Click the *Add build step...* button and find HockeyApp (you'll need to switch the filter to *All* or *Deploy*) and click *Add:

<img src="http://storage.chrisrisner.com/images/vso-hockeyapp-build-step.png" alt="VSO HockeyApp Build Step" class="centeredInContent"/>

Now you can close that window and open the **HockeyApp** build step you just added.  Now we have quite a few config options to look at:

<img src="http://storage.chrisrisner.com/images/vso-hockey-app-build-step-config.png" alt="VSO HockeyApp Build Step" class="centeredInContent"/>

I'll provide some detail on the current options but you can also [read about them here](http://support.hockeyapp.net/kb/third-party-bug-trackers-services-and-webhooks/how-to-use-hockeyapp-with-team-foundation-server-tfs-or-visual-studio-online-vso).

* HockeyApp API Token: This is a token which you can [generate for all apps or a specific app here](https://rink.hockeyapp.net/manage/auth_tokens)
* App ID: This is the ID which you can find at the homepage for your app within HockeyApp.  If you leave it blank, HockeyApp will try to auto figure things out based off the Bundle ID or Identifier of the app.
* Binary File Path: Based off of creating a new project in Android Studio, the path here should be: *{AnythingBeforeTheAppFolder}\app\build\outputs\apk\app-debug.apk*.  So for example, my path is *android\app\build\outputs\apk\app-debug.apk*.
* Symbols File Path: The path to your **mappings.txt** file if one is being generated.  Not required.
* Release Notes: Any release notes you'd like to be entered to be sent over to HockeyApp for the app release.
* Publish?: Should HockeyApp users you've set up be able to download this version.
* Mandatory?: Is this a mandatory install for users.
* Notify Users?: Should users be notified that there is a new version for them to download.
* Download Restrictions: These allow you to restrict who can download this version based off tags, teams, and users defined in HockeyApp.
* Control Options: Normal Build Step options for enabling, continuing on error, and if it should always be run.

Once you're done, click *Save* and hit *Queue build...*.  After hits the queue and builds, you should see the task for HockeyApp at the bottom:

<img src="http://storage.chrisrisner.com/images/vso-hockeyapp-task-running.png" alt="VSO HockeyApp Task Running" class="centeredInContent"/>

After that, if you go into HockeyApp you should see a new version of your application:

<img src="http://storage.chrisrisner.com/images/hockeyapp-versions.png" alt="HockeyApp Versions" class="centeredInContent"/>

Since I had added myself as a user of the app and chose to *Publish* and *Notify Users*, I received an email shortly afterwards telling me there was a new version of my application and had it installed through the HockeyApp Android app moments later!

## Summary
With Visual Studio Online, we have the ability to easily create Git repos for source control management, as well as the ability to manage our projects with work items, bugs, tasks, kanban boards etc.  By connecting that with the build system, we're able to easily set up Continuous Integration.  Adding HockeyApp to the mix gives us the last piece with Continuous Delivery.  Now we can easily enable our application to be built with every check-in and delivered right to our beta testers.