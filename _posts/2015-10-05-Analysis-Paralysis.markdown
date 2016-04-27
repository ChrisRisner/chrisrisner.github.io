---
layout: post
title: "Analysis Paralysis"
date: Mon Oct 5 2015 20:16:00 GMT-0800 (PST)
comments: true
status: publish
type: post
published: true
categories: [Projects]
excerpt: "A writeup about the issues I've been having deciding on my next project.  Too much analysis and not enough work."
logoUrl: null
keywords: projects,analysis paralysis,over analyizing
filepath: 2015-10-05-Analysis-Paralysis.markdown
disqus_identifier: 2015-10-05-Analysis-Paralysis
---

## Update April 27, 2016
I've been working on a native Android app for the last few months and, when it's complete, I'm actually going to use Xamarin for my next app.  After having worked with Xamarin more around //Build, I've gotten over most of the issues I had before and found some pretty delightful things.

A while back in June, I [tweeted](https://twitter.com/chrisrisner/status/614491780130717697) the words "Analysis Paralysis".  At the time I was starting to think about building a new mobile app.  As you might imagine given what I do for a living, I wanted to use Azure as the backend for the app and I wanted to be able to publish it for Android, iOS, and Windows Phone.  The question I was grappling with was how did I want to build the app.  

### How to build an app
If you've been building mobile apps for any reasonable amount of time, then you know there are options when it comes to the technology that you can use.  If you know all about this already, go ahead and skip on.  When people first started building apps for iPhones, Androids, and Windows Phones, they built what we would consider *native* apps.  For Android, this meant using Java (or at least *Androidized Java*).  For iOS, this meant using Objective-C.  And for Windows Phone, this meant C# (or Visual Basic...I think that was added at some point).  Initially this was the only way to build a mobile application on these platforms.  

Later on, other approaches came to building mobile applications.  In [2009 at a iPhoneDevCamp](http://www.eweek.com/c/a/Application-Development/PhoneGap-Simplifies-iPhone-Android-BlackBerry-Development-788189), what would eventually become Apache Cordova (or PhoneGap), was created.  This technology allows developers to build iOS and Android applications using HTML5, JavaScript, and CSS.  This also allows developers to effectively 'write once, run everywhere'.  Through a 'bridge', the JavaScript is able to call into the backend native code and APIs.  In this way, someone that is more familar with traditional web development is able to build a mobile application that still has native capabilities (think camera, GPS, sensors, connectivity to other installed apps, etc).  At some later point, Windows Phone support was added enabling developers to deliver the same application on the three major platforms (ok maybe Blackberry was available at some point as well).  Famously in [September of 2012, Mark Zuckerberg (of Facebook), said that HTML5 wasn't ready for mobile apps](http://techcrunch.com/2012/09/11/mark-zuckerberg-our-biggest-mistake-with-mobile-was-betting-too-much-on-html5/).  At the time, they were using technology very similar to Apache Cordova for their mobile Facebook app.  They started moving away from using HTML5 and instead built native apps.  Not entirely relevant to this post, but a few months later in December, [Sencha introduced Fastbook](https://www.sencha.com/blog/the-making-of-fastbook-an-html5-love-story/) which was a proof of concept to proove that an efficiently running mobile app could be built with HTML5.

The next approach to building mobile apps involved using .NET to again, 'write once, run everywhere'.  In 2001, the [mono project](http://www.mono-project.com/) was created to provide for an open source implementation of the .NET framework.  Years later, in 2011, the same creator of Mono, [Miguel De Icaza](http://www.tirania.org/blog/), helped found [Xamarin](http://xamarin.com/).  Xamarin took the work they had learned from Mono and enabled running .NET on iOS and Android devices.  So the legions of .NET developers could now use the skills they had learned to write ASP.NET Web apps, Smart Client apps, and much more, to also build applications that could run on the two biggest mobile platforms available (in addition to running code on Windows Phone).  For me, having programmed in .NET and C# for about six years, I thought Xamarin was an amazing idea.  I'll get to that more later.

There are a large number of other solutions for building mobile applications that I'm not going to highlight.  I've played with many of these, though I'm sure in the past few years even more have sprouted up.  I don't have enough experience to talk with authority about any other ones.  That said, I don't think any of them have been proven enough to warrant my attention.

### The Analysis
When I decided to start my next app, I needed to decide how I wanted to build it.  Years ago, when I took over the mobile development team at my last company, one of the things I wanted us to look into was if we should be building native apps or using a framework to build some sort of hybrid apps.  At the time, we evaluated AppCelerator, RhoMobile, PhoneGap, and a few other players.  At the time none of them delivered the experience we wanted as developers or apps that behaved the way we wanted to deliver to customers.  This isn't to say it wasn't / isn't possible to build a quality application with any of these options, just that in the two weeks we evaluated them, we didn't feel we were getting out what we needed.  We didn't try Xamarin at the time just due to the [cost](https://store.xamarin.com/) invovled.  We ended up sticking with navtive development (Java and Objective-C).

Since then, some of those frameworks have passed along the way side and things have changed for myself.  For one thing, I've done more Xamarin development for work, so that was back on the table for building my app.  Additionally, I've worked on more tooling that ties in using PhoneGap.  So I was deciding between native development, Xamarin, and PhoneGap.

### The Paralysis
Anyone facing this might run into the same problem.  At the end of the day, I had a few different motivations:

* To build a mobile app that will (eventually) be released for Android, iOS, and Windows
* To finally have a personal app in the different app marketplaces that I'm proud of (everything so far has been demo apps)
* To learn more about available mobile app dev libraries (that I probably should already know more about)
* To make use of Azure as the backend for my application
* To make use of and prove out the CI and deployment capabilties of Visual Studio Online

Most of these goals could be met using any of these three ways of building my app.  The real trade offs were in how soon I could get the app onto all of the devices I wanted (building it native for each vs using a framework) and learning more about some of the native libraries available (not as easily doable, or possible in most cases, when using a framework).  

Since I haven't really had what I'd consider proper time to start building my app, I'd make a decicsion, and then start rethinking it.  Whenever I got a little more time, instead of sticking to a decision, I'd rethink things.  Even when I'd make a decision, the rethinking made it feel like I was in a constant state of not being able to actually make a decision.  **Paralyzed!!**

### A Decision
Eventually I did make a final decision, and part of it was easy.  I've never really been enamored with PhoneGap style apps.  Sometimes these apps are built in such a way that you can tell they're using this framework and you can *feel* the lack of performance.  As Sensha went and proved, it's possible to build a **good** app of this sort (solving the delayed click in a web view [isn't hard, for example](http://phonegap-tips.com/articles/fast-touch-event-handling-eliminate-click-delay.html), but my skills don't fall within in HTML, JS, and CSS.   So PhoneGap / Cordova was out.

Now that I have access to Xamarin, I thought about building my app with Xamarin.  I've done plenty of .NET over the years (though not a lot recently) and I actually really like Xamarin Studio.  More so, last year in May, [Xamarin announced Xamarin.Forms](https://blog.xamarin.com/announcing-xamarin-3/).  Xamarin.Forms enables you to either code your UI, or write it in XAML, once and Xamarin handles creating a UI for each platform using custom elements and patterns.  Unfortuantely, Xamarin was also a no go.  Recently at work, some of my team mates and I have been working on a proof of concept and I've been building out the mobile app piece.  In order to turn things around quickly, I've been using Xamarin.  It's been rough going but I've been able to get things to work.  However, the reliability and ease of getting some pieces to work across Android, iOS, and Windows Phone has left me with some concern.  I'll write more about this in another post because it deserves more attention (and for what it's worth, I'll still recommend Xamarin to people for the right situations) but not for this project.

Native was the way to go.  I've wanted to get back to developing a native app and learn more about some of the libraries that have popped up.  Some of this desire can probably be blamed on [Donn Felker](http://www.donnfelker.com/) and [Kaushik Gopal's](http://kaush.co/) excellent and inspring [Fragmented podcast](http://fragmentedpodcast.com/).  Seriously, if you're into Android development, check out their podcast.  It's made me aware of some really cool libraries I've never tried out and has provided me with a wealth of ideas for my next app.

### What's Next?
Well the app I was originally thinking through building has been shelved.  Instead I'm going to start by building a smaller application.  I'm going to do this so I can quickly evaluate some of the aforementioned libraries as well as test out a possible method of reusing much of the source code so I can quickly port the app to several platforms.  I'm hoping to have a first release out within a few months.  I'm sure I'll end up blogging a good amount about some of the learnings and challanges I face during the process.