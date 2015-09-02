---
layout: post
title: "Analysis Paralysis"
date: Sun Aug 30 2015 20:16:00 GMT-0800 (PST)
comments: true
status: publish
type: post
published: true
categories: [Projects]
excerpt: "A writeup about the issues I've been having deciding on my next project.  Too much analysis and not enough work."
logoUrl: null
keywords: projects,analysis paralysis,over analyizing
filepath: 2015-08-30-Analysis-Paralysis.markdown
disqus_identifier: 2015-08-30-Analysis-Paralysis
---

A while back in June, I [tweeted](https://twitter.com/chrisrisner/status/614491780130717697) the words "Analysis Paralysis".  At the time I was starting to think about building a new mobile app.  As you might imagine given what I do for a living, I wanted to use Azure as the backend for the app and I wanted to be able to publish it for Android, iOS, and Windows Phone.  The question I was grappling with was how did I want to build the app.  

##How to build an app
If you've been building mobile apps for any reasonable amount of time, then you know there are options when it comes to the technology that you can use.  If you know all about this already, go ahead and skip on.  When people first started building apps for iPhones, Androids, and Windows Phones, they built what we would consider *native* apps.  For Android, this meant using Java (or at least *Androidized Java*).  For iOS, this meant using Objective-C.  And for Windows Phone, this meant C# (or Visual Basic...I think that was added at some point).  Initially this was the only way to build a mobile application on these platforms.  

Later on, other approaches came to building mobile applications.  In [2009 at a iPhoneDevCamp](http://www.eweek.com/c/a/Application-Development/PhoneGap-Simplifies-iPhone-Android-BlackBerry-Development-788189), what would eventually become Apache Cordova (or PhoneGap).  This technology allowed developers to build iOS and Android applications using HTML5, JavaScript, and CSS.  This also allowed developers to effectively 'write once, run everywhere'.  Through a 'bridge', the JavaScript is able to call into the backend native code and APIs.  In this way, someone that is more familar with traditional web development is able to build a mobile application that still has native capabilities (think camera, GPS, sensors, connectivity to other installed apps, etc).  At some later point, Windows Phone support was added enabling developers to deliver the same application on the three major platforms (ok maybe Blackberry was available at some point as well).  Famously in [September of 2012, Mark Zuckerberg (of Facebook fame), said that HTML5 wasn't ready for mobile apps](http://techcrunch.com/2012/09/11/mark-zuckerberg-our-biggest-mistake-with-mobile-was-betting-too-much-on-html5/).  At the time, they were using technology very similar to Apache Cordova for their mobile Facebook app.  They started moving away from using HTML5 and instead building native apps.  Not entirely relevant to this post, but a few months later in December, [Sencha introduced Fastbook](https://www.sencha.com/blog/the-making-of-fastbook-an-html5-love-story/) which was a proof of concept to proove that an efficiently running mobile app could e built with HTML5.

The next approach to building mobile apps involved using .NET to again, 'write once, run everywhere'.  In 2001, the [mono project](http://www.mono-project.com/) was created to provide for an open source implementation of the .NET framework.  Years later, in 2011, the same creator of Mono, [Miguel De Icaza](http://www.tirania.org/blog/), helped found [Xamarin](http://xamarin.com/).  Xamarin took the work they had learned from Mono and enabled running .NET on iOS and Android devices.  So the legions of .NET developers could not use the skills they had to write ASP.NET Web apps, Smart Client apps, and much more, could also build applications that could run on the two biggest mobile platforms available (in addition to Windows Phone).  For me, having programmed in .NET and C# for about six years, thought Xamarin was an amazing idea.  I'll get to that more later.

There are a large number of other solutions for building mobile applications that I'm not going to highlight that I won't bother mentioning.  I've played with many of these, though I'm sure in the past couple yeras even more have sprouted up.  I don't have enough experience to talk about any other ones.  That said, I don't think any of them have been proven enough to warrant my attention.

##The Analysis
When I decided to start my next app, I needed to decide how I wanted to build it.  Years ago, when I took over the mobile development team at my last company, one of the things I wanted us to look into was if we should be building native apps or using a framework to build some sort of hybrid apps.  At the time, we evaluated AppCelerator, RhoMobile, PhoneGap, and a few other players.  At the time none of them delivered the experience we wanted as developers or apps that behaved the way we wanted to deliver to customers.  This isn't to say it wasn't / isn't possible to build a quality application with any of these options, just that in the two weeks we evaluated them, we didn't feel we were getting out what we needed.  We didn't try Xamarin at the time just due to the cost invovled.  We ended up sticking with navtive development (Java and Objective-C).

Since then, some of those frameworks have passed along the way side and things have changed for myself.  For one thing, I've done more Xamarin development for work, so that was back on the table for building my app.  Additionally, I've worked on more tooling that ties in using PhoneGap.  So I was deciding between native development, Xamarin, and PhoneGap.

##The Paralysis
Anyone facing down this might run into the same problem.  At the end of the day, I had a few different motivations:
* To build a mobile app that will (eventually) be released for Android, iOS, and Windows
* To finally have a personal app in the different app marketplaces that I'm proud of (everything so far has been demo apps)
* To learn more about available mobile app dev libraries (that I probably should already know more about)
* To make use of Azure as the backend for my application
* To make use of and prove out the CI and deployment capabilties of Visual Studio Online

Most of these goals could be met using any of these three ways of building my app. 


read this https://en.wikipedia.org/wiki/Analysis_paralysis

