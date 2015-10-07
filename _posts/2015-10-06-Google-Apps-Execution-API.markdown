---
layout: post
title: "Google Apps Execution API"
date: Tue Oct 06 2015 20:16:00 GMT-0800 (PST)
comments: true
status: publish
type: post
published: true
categories: [Google,APIs]
excerpt: "Google releases a new way of using Google Apps Scripts via an API."
logoUrl: null
keywords: google,google apps,apis,mobile
filepath: 2015-10-06-Google-Apps-Execution-API.markdown
disqus_identifier: 2015-10-06-Google-Apps-Execution-API
---

What timing?  I just wrote a [post that mentioned building an app that made use of Google Apps Scripts as an API](http://chrisrisner.com/Xamarin-Forms-Woes/) and Google just [announced](http://googledevelopers.blogspot.com/2015/09/run-apps-script-code-from-anywhere.html) a new Execution API to basically make what I did easier.  If you're not aware, Google Apps Script enable you to write JavaScript scripts that are able to interact with different Google services including Docs, Sheets, GMail, Drive, etc.  If you want to build something that interacts with those programs, that's how you do it.  As far as I'm aware, you've been able to take those scripts and expose them via HTTP for quite a while (though you need to deal with authorization and authentication in some interesting manners).  

That's exactly what I did for my Budget project.  I created an Apps Script which could pull data out of Sheets including my weekly, monthly, and daily budget as well as update that data.  This was exposed via HTTP and required my Google user auth in order to access (both the script and the Sheet have to be authorized for the user).  From my mobile app I could call that script's endpoint in order to access the data and update my budget from my mobile app.  It wasn't a terrible pain getting the script working but getting it exposed correctly and accessing it from the mobile app was a pain.

This looks like it's making the exposing and access easier.  Much of that is from [client side libraries and quickstart samples](https://developers.google.com/apps-script/guides/rest/?utm_campaign=execution-API-924&utm_source=gdbc&utm_medium=blog).  Even with that making it easier, I'm not sure I'd consider Google Apps Scripts to be part of a very scalable and reliable architecture.  It's possible to do your Apps Script development in Eclipse, but it all feels very immature.  Maybe I just don't like using JavaScript for everything.