---
layout: post
title: "Open Sourcing Azure Storage Explorer for Mobile"
date: Wed Feb 07 2017 9:16:00
commentsOn: true
status: publish
type: post
published: true
categories: [GitHub,Open source,Xamarin]
excerpt: "This post walks through the open source release of a reference application version of Azure Storage Explorer built for Android and iOS."
logoUrl: null
keywords: GitHub,Open source,Xamarin
filepath: 2018-2-07-Open-Sourcing-Azure-Storage-Explorer-for-Mobile.markdown
disqus_identifier: 2018-2-07-Open-Sourcing-Azure-Storage-Explorer-for-Mobile
redirect_from: 
  - /open-sourcing-azure-storage-explorer-for-mobile/
---

Some time ago, I started working on a mobile version of the [Azure Storage Explorer](http://storageexplorer.com).  The intent of this app was that anything you could do from the ASE app on Windows, MacOS, or Linux, you'd be able to do on Android and iOS.  There were a few different reasons I wanted to build this:

* I wanted to spend time building out a real application using [Xamarin](http://xamarin.com).
* There were a few situations where I thought it would be handy to have access to my storage accounts while away from my computer.
* I wanted to start auto-backing up any photos I took with my phone to Azure Storage.

Fast forward through several months of working on the app in my spare time (which is to say not very frequently) and I had a number of scenarios around Storage working.  What I didn't have, was a strong use case or motivation to release and support the app.  Additionally, after talking with more people, it didn't seem like there was a very strong use case for the mobile version of ASE.  As with many other things, if there wasn't a customer need, there probably wasn't going to be much usage, and therefore there wouldn't be much in the way of support.  So rather than releasing an app to the App Store and Google Play and let it languish, I decided it would be better to just open source the app.


## Releasing the Souce Code for ASE Mobile

Effective today, you can now access all source code and assets for [Azure Storage Explorer for Android and iOS on GitHub](https://github.com/ChrisRisner/AzureStorageExplorer).  I think this is a great reference app as it details:

* How to build a semi-sophisticated Xamarin app for Android and iOS.
* How to use different UI elements depending on the platform (iOS makes use of tabs while Android uses the slide out menu).
* How to access a number of different Azure Storage capabilities (see below).
* How to mix usage of Azure REST APIs and libraries.

## Credit to Other Devs

I couldn't have built this without ~~stealing~~ borrowing from many other devs.

* I heavily referenced the app architecture and patterns from the [Xamarin Evolve 2016 Mobile App](https://github.com/xamarinhq/app-evolve).  James and Pierce did a great job with this app and made it very easy to look through and reuse.
* I'll call out [James Montemagno](https://montemagno.com/) again as I made use of a large assortment of the Xamarin plugins he builds and supports.
* Developers at [Realm](https://realm.io/) and [Rg.Plugins.Popup](https://github.com/rotorgames/Rg.Plugins.Popup) for their technical support.
* Everyone that works on [Visual Studio Team Services](https://www.visualstudio.com/vso/) and [Visual Studio App Center](https://appcenter.ms/).  Throughout developement, I used VSTS for continuous integration and App Center to deliver the app to test devices and track errors and analytics.

## Outstanding Issues

There are a number of issues I never got around to including:

* Testing against a large quantity of blobs, table rows, etc.  
* Editing table schema and rows.
* Any sort of advanced querying of data.
* Currently the app only works with Classic Storage Accounts due to how I am pulling subscriptions and storage accounts (i.e. the APIs I used).  This wouldn't be very difficult to convert over but I never got to it.

## How to Build it?

In order to build and run the application, there are a few things you should do and a few things you need to do:

* In the [src/AzureStorageExplorer/Helpers/Constants.cs](https://github.com/ChrisRisner/AzureStorageExplorer/blob/master/src/AzureStorageExplorer/Helpers/Constants.cs) class, there are a number of API Keys that need to be set.  First is the **AuthClientId** which is the value you get from Azure Active Directory after you create an app with appropriate permissions.  Second is the **MobileCenterId** which is the value you get after creating an app in Visual Studio App Center (yeah it used to be called Mobile Center).  You'll note that there are different values based off of if you're in Debug or not as well as if you're in iOS or Android.
* If you're building and running in iOS, you'll need to create an App ID and all the appropriate bundle identifiers, etc.  Because there is certain functionality that requires iCloud access, for the App ID, you'll need to set up iCloud access (I used iCloud.azurestorageexplorer as the container name).
* I haven't compiled against the absolute latest versions of iOS / Android / Xamarin but I don't anticipate any issues.
* One thing to keep in mind is that I pulled in the actual code for the Rg.Plugins.Popup library.  This is only directly used in the iOS project and was done to alleviate an issue where popups weren't working if you were *too deep* down the navigational stack.  I believe they've fixed this in a preview version of the plugin (v1.1.0-pre1 and beyond) but haven't tested this yet.

## Would you use it?

If you see this and think you'd have use for the app if it was easily available on the App Store and Google Play, please let me know.  I left this project because it didn't seem like there was a solid enough use case for it.  I'd love to be wrong about that.  If you need any help getting the [app](https://github.com/ChrisRisner/AzureStorageExplorer) built, please reach out or file an issue on the [GitHub repo](https://github.com/ChrisRisner/AzureStorageExplorer).