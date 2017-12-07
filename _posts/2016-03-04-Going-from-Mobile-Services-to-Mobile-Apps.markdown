---
layout: post
title: "Going from Mobile Services to Mobile Apps"
date: Fri Mar 04 2016 20:16:00
commentsOn: true
status: publish
type: post
published: true
categories: [Azure,Mobile,Mobile Apps,Mobile Services]
excerpt: "This post explains the migration from Azure Mobile Services to Azure Mobile Apps."
logoUrl: null
keywords: Azure,Mobile Apps,Node.js,osx,linux
filepath: 2016-03-04-Going-from-Mobile-Services-to-Mobile-Apps.markdown
disqus_identifier: 2016-03-04-Going-from-Mobile-Services-to-Mobile-Apps
redirect_from: 
  - /going-from-mobile-services-to-mobile-apps/
---

I've held off on updating my blog to really talk about Azure Mobile Apps as I was waiting for the .NET and Node.js backends for Mobile Apps to GA.  Now that they have, I think it's time to point every one in that direction.  I've posted quite a lot on using Azure Mobile Services as the backend for Android, iOS, Windows, Xamarin, and PhoneGap apps, and many of the things I've talked about are still important, but people should be thinking about using Azure Mobile Apps instead of Mobile Services to backend their mobile apps going forward.  I've put a link in all of my posts directing people here so that I can explain what's new with Azure Mobile Apps and why you should look at them.

### Azure Mobile Apps
[Azure Mobile Apps](https://azure.microsoft.com/en-us/documentation/articles/app-service-mobile-value-prop/) is a Platform-as-a-Service that exist to provide an easy way to set up a backend for mobile applications (running on any OS).  These backends support several features out of the box including: easy data storage, user authentication and authorization, push notifications, backend job processing, and much more.  Using something like Mobile Apps enables you to have a powerful backend that you don't have to spend valuable time building so that you can focus on building the best client applications you can.  Several years ago, Microsoft released a service named Azure Mobile Services.  This was effectively the first version of a backend service inside Azure.  That means that Azure Mobile Apps is version 2.  In addition to all of the features that Mobile Services provided, Mobile Apps provides additional funcationlity including easy and more powerful scaling, deployment slots, traffic routing and management, VPN support, and much more.  

Going forward, anyone looking at using a backend service in Azure for their mobile applications should be looking at the Azure Mobile Apps service.  I'll be posting more about using Azure Mobile Apps soon, but wanted to point people in the right direction.  You can find below a number of links relevant to Azure Mobile Apps and converting from Mobile Services:

* [What are Mobile Apps?](https://azure.microsoft.com/en-us/documentation/articles/app-service-mobile-value-prop/)
* [Migrating your existing Mobile Service to Mobile Apps](https://azure.microsoft.com/en-us/documentation/articles/app-service-mobile-migrating-from-mobile-services/)
* [How does App Service help if you're using Mobile Services](https://azure.microsoft.com/en-us/documentation/articles/app-service-mobile-value-prop-migration-from-mobile-services/)
* [Mobile Apps learning map](https://azure.microsoft.com/en-us/documentation/learning-paths/appservice-mobileapps/)
* [Working with the Mobile Apps .NET backend](https://azure.microsoft.com/en-us/documentation/articles/app-service-mobile-dotnet-backend-how-to-use-server-sdk/)
* [Working with the Mobile Apps Node.js backend](https://azure.microsoft.com/en-us/documentation/articles/app-service-mobile-node-backend-how-to-use-server-sdk/) 