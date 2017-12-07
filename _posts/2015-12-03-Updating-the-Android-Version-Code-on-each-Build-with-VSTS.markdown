---
layout: post
title: "Updating the Android Version Code on each Build with VSTS"
date: Thu Dec 03 2015 20:16:00
commentsOn: true
status: publish
type: post
published: true
categories: [Android,Azure,Visual Studio Team Services,CI]
excerpt: "This post walks through how you can update your Android APK's version code for each build."
logoUrl: null
keywords: android,ci,vso,visual studio team services,hockeyapp
filepath: 2015-12-03-Updating-the-Android-Version-Code-on-each-Build-with-VSTS.markdown
disqus_identifier: 2015-12-03-Updating-the-Android-Version-Code-on-each-Build-with-VSTS
redirect_from: 
  - /updating-the-android-version-code-on-each-build-with-vsts/
---

A few weeks back, I posted about how you could set up [Continuous Integration and Delivery with Visual Studio Team Services and HockeyApp](chrisrisner.com/Setting-Up-Continuous-Integration-for-Android-with-VSTS-and-HockeyApp/) (at the time it was Visual Studio Online).  Since then at the Connect() event that happened a little later in November we announced [even better integration between VSTS and HockeyApp](https://channel9.msdn.com/Events/Visual-Studio/Connect-event-2015/011).  We'll look at some of those integrations another time as for today, I want to talk about how to deal with a very specific problem.

When building your Android applications and creating APKs, each APK has a *Version Code* and a *Version Name*.  The *Version Name* is shown to users both in the Google Play Store as well as if they go to *App Info* on the device.  Outside of that it doesn't really mean anything.  The *Version Code*, however, is used to determine whether one version is older than another and is not shown to users.  Typically, these values are set in the **defaultConfig** section of the **build.gradle** file.  One issue I ran into when I was deploying through HockeyApp last time was that the version of my app never changed:

<img src="http://storage.chrisrisner.com/images/hockeyapp-versions.png" alt="HockeyApp Versions" class="centeredInContent"/>

I wouldn't really want the *Version Name* to change until I'm ready for a release but the *Version Code* should change so it would be easier to distinguish between one build and another.  Especially if I wanted to tie issues occuring in a specific release of the app back to code changes that occurred between builds.  

After doing some looking, it seems like many people have gone down a route of modifying their **build.gradle** file so that when gradle runs, it parses the file, looks for the Version Code, updates it and then writes the changes back to the file.  This is a great solution if you're building locally and alone.  However, I'm using a version control and build system (VSTS) and I'm really not sure how or if it's possible to, as part of the build, grab the **build.gradle** file, update the *Version Code* and then commit that file back to the repo.  More so, I'm not entirely sure I would want to have my commit history littered with automated version changes.  This means I needed to find a different way to handle it.  

Short of making the script ping a web service running somewhere that would persist and increase a number with each ping, doing a simple number for the *Version Code* didn't seem like it would work.  Fortunately, there is something that is always increasing that is available right in the gradle file: the [date](https://stackoverflow.com/questions/21405457/autoincrement-versioncode-with-gradle-extra-properties/28043555#28043555)!  In order to get this setup, I altered my **build.gradle** file (the one for *Module: app* if you're in Android Studio) to be like this:

{% highlight groovy %}
android {
	...
	defaultConfig {
        applicationId "com.myapps.anapp"
        minSdkVersion 21
        targetSdkVersion 23
        versionCode getVersionCodeTimestamp()
        versionName "1.0"
    }
	...
}
def getVersionCodeTimestamp() {
    def currentDate = new Date()
    def formattedDate = currentDate.format('yyMMddHHmm')
    def code = formattedDate.toInteger()
    return code
}
...
{% endhighlight %}

The important parts here are that we're setting the **versionCode** to the method **getVersionCodeTimestamp()**.  In that method we're getting the current date and formatting it to be **yyMMddHHmm**.  We could leave off the hour and the minute but if I do multiple builds each day, I might want to have that there to distinguish them.  After that we cast it as an integer as the **versionCode** is expected to be one.  Once I've committed and pushed that change to VSTS and run another build, we start seeing a different code every time we build:

<img src="http://storage.chrisrisner.com/images/hockey-app-different-version-codes.png" alt="HockeyApp Versions" class="centeredInContent"/>

This makes identifying what version of the app ties into what issues and what code changes much easier!  It may also be possible to replace the Version Code with the build number for VSTS.  That may be preferable for some people as that integer will likely be considerably smaller.  If I find that is possible, I'll post again.