---
layout: post
title: "Using Fragments with the Navigation Drawer Activity"
date: Mon Dec 07 2015 20:16:00 GMT-0800 (PST)
comments: true
status: publish
type: post
published: true
categories: [Android]
excerpt: "This post walks through how to easily use Fragments with the Navigation Drawer Activity available in Android Studio."
logoUrl: null
keywords: android,fragments,navigation drawer,navigation
filepath: 2015-12-07-Using-Fragments-with-the-Navigation-Drawer-Activity.markdown
disqus_identifier: 2015-12-07-Using-Fragments-with-the-Navigation-Drawer-Activity
redirect_from: 
  - /using-fragments-with-the-navigation-drawer-activity/
---

I've been working on a new Android application and just recently ran into a problem that I was surprised didn't have a clearer solution.  The primary means of navigation in the app was going to be a [Navigation Drawer](https://www.google.com/design/spec/patterns/navigation-drawer.html#navigation-drawer-specs).  If you've used an Android device, you've almost certainly seen and used this design pattern:

<img src="http://storage.chrisrisner.com/images/android-navigation-drawer.png" alt="HockeyApp Versions" class="centeredInContent"/>

The Navigation Drawer is a slide out menu that enables users to navigate around the different areas of the application.  Typically, when the user taps one of the items on the menu, the content page is reloaded.  Instead of starting a new activity where the user has to go *back* (via the back button or a back button in the top left of the screen), the navigation drawer (usually via the familiar [hamburger button](https://en.wikipedia.org/wiki/Hamburger_button) stays available as you go from one area of the app to others (it seems like it's common for a few pages to launch and require the back button such as Settings and Help).

If you go into Android Studio right now and create a new application and base it off the Navigation Drawer Activity, you'll get a very basic app with a single activity and the nav drawer will be set up fairly similarly to what you see above.  What you won't see though, is how to actually navigate between different "content pages" when you tap the different menu options in the nav drawer!  If you are familiar with some Android development, this might be a bit surprising.  It use to be that the way you got from one *page* to another was to have several *Activities* and to use an [intent to launch each new activity](http://chrisrisner.com/31-Days-of-Android--Day-5-Adding-Multiple-Activities-and-using-Intents/).  This doesn't really mesh with the nav drawer though as you'd have to have the same nav drawer on several activities

###Enter the Fragment
 When Android moved from 2.X to 3.X, they were moving from only focusing on phone form factors to also tablets.  3.X was never officially released to run on phones, but they started thinking about how to make page constructs that weren't just in the form of actvities tied to layouts.  The solution they came up with was [Fragments](http://developer.android.com/guide/components/fragments.html).  A fragment is a way of composing a part of an activity.  It has it's own lifecycle, deals with it's own inputs, and each activity can contain multiple fragments.  The easiest way to see fragments in action is to create a new application and use the **Master / Detail Flow**.  This creates an application that works on both tablets and phones and shows how you can show multiple fragments at once (on the tablet) or a single fragment (on the phone).  The bulk of the code is the same regardles of if you're showing one fragment or both which is part of the reason you use fragments, so you don't have to reproduce code in multiple places.
 
 ###The Problem
 The problem I ran into with the Navigation Drawer sample is again that it doesn't really demonstrate how you should do navigation inside of it.  As I said before, you can always use the old route of launching new activities.  However, you'll need to then reuse the navigation drawer everywhere.  This can be done and someone I was tweeting with about this issue even put together a [sample of it on GitHub](https://github.com/karnamsupreeth/drawersample).  Unfortunately, if you run that, you'll see that the navigation between different activities isn't as smooth as I'd like it to be.  Namely, the nav drawer doesn't slide back before showing the new activities content.  What I want to happen is when the user taps an item on the nav drawer, the content page should already be loading / loaded while the drawer slides back to be closed.  As far as I've seen so far, this can't be done with multiple activities.  But it can with fragments.  One thing to note is that I believe you could also do custom view inflation and deflation though you'd be wrapping everything in one activity.
 
 ###What's wrong with Fragments
 Before I get into the specifics of adding fragments to the nav drawer sample, I just want to say that I don't hate fragments, I just don't like them.  Just a few [searches](https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=fragments%20vs%20activities) online will yield a lot of conversations about whether fragments are good or [bad](https://corner.squareup.com/2014/10/advocating-against-android-fragments.html).  Because fragments live inside of an activity, and both the activity and fragment have lifecycle and event handling, things cna be overly complex.  Additionally there are memory implications and other concerns you might run into.  Suffice to say, I'm going forward with fragments in my solution though that doesn't mean I'm sold on them being the best solution.
 
 ###Adding Fragments to the Sample
 