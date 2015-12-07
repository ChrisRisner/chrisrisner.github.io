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

**TLDR**: If you want to grab the sample code, it's [available on GitHub](https://github.com/ChrisRisner/AndroidFragmentNavigationDrawer).

I've been working on a new Android application and just recently ran into a problem that I was surprised didn't have a clearer solution.  The primary means of navigation in the app was going to be a [Navigation Drawer](https://www.google.com/design/spec/patterns/navigation-drawer.html#navigation-drawer-specs).  If you've used an Android device, you've almost certainly seen and used this design pattern:

<img src="http://storage.chrisrisner.com/images/android-navigation-drawer.png" alt="HockeyApp Versions" class="centeredInContent"/>

The Navigation Drawer is a slide out menu that enables users to navigate around the different areas of the application.  Typically, when the user taps one of the items on the menu, the content page is reloaded.  Instead of starting a new activity where the user has to go *back* (via the back button or a back button in the top left of the screen), the navigation drawer (usually via the familiar [hamburger button](https://en.wikipedia.org/wiki/Hamburger_button)) stays available as you go from one area of the app to others (it seems like it's common for a few pages to launch and require the back button such as Settings and Help).

If you go into Android Studio right now and create a new application and base it off the Navigation Drawer Activity, you'll get a very basic app with a single activity and the nav drawer will be set up fairly similarly to what you see above.  What you won't see though, is how to actually navigate between different "content pages" when you tap the different menu options in the nav drawer!  If you are familiar with some Android development, this might be a bit surprising.  In earlier days of Android development the way you got from one *page* to another was to have several *Activities* and to use an [intent to launch each new activity](http://chrisrisner.com/31-Days-of-Android--Day-5-Adding-Multiple-Activities-and-using-Intents/).  This doesn't really mesh with the nav drawer though as you'd have to have the same nav drawer on several activities

###Enter the Fragment
When Android moved from 2.X to 3.X, they were moving from only focusing on phone form factors to also tablets.  3.X was never officially released to run on phones, but they started thinking about how to make page constructs that weren't just in the form of actvities tied to layouts.  The solution they came up with was [Fragments](http://developer.android.com/guide/components/fragments.html).  A fragment is a way of composing a part of an activity.  It has it's own lifecycle, deals with it's own inputs, and each activity can contain multiple fragments.  The easiest way to see fragments in action is to create a new application and use the **Master / Detail Flow**.  This creates an application that works on both tablets and phones and shows how you can show multiple fragments at once (on the tablet) or a single fragment (on the phone).  The bulk of the code is the same regardles of if you're showing one fragment or both which is part of the reason you use fragments, so you don't have to reproduce code in multiple places.
 
###The Problem
The problem I ran into with the Navigation Drawer sample is again that it doesn't really demonstrate how you should do navigation inside of it.  As I said before, you can always use the old route of launching new activities.  However, you'll need to then reuse the navigation drawer everywhere.  This can be done and someone I was tweeting with about this issue even put together a [sample of it on GitHub](https://github.com/karnamsupreeth/drawersample).  Unfortunately, if you run that, you'll see that the navigation between different activities isn't as smooth as I'd like it to be.  Namely, the nav drawer doesn't slide back before showing the new activities content.  What I want to happen is when the user taps an item on the nav drawer, the content page should already be loading / loaded while the drawer slides back to be closed.  As far as I've seen so far, this can't be done with multiple activities.  But it can with fragments.  One thing to note is that I believe you could also do custom view inflation and deflation though you'd be wrapping everything in one activity.

**NOTE**: After I'd already started this post, *karnamsupreeth* updated his code sample to provide a brief delay after tapping a nav item and launching the new activity.  This was MUCH closer to what I originally thought of and is a valid way of handling things if you want to use Activities.  I'll continue to post the fragment solution but I'd definitely consider using his example as well.  It still doesn't actually *load* the new activity until after the delay so you're note sliding the drawer back to reveal the new content that has been loaded.

###What's wrong with Fragments
Before I get into the specifics of adding fragments to the nav drawer sample, I just want to say that I don't hate fragments, I just don't like them.  Just a few [searches](https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=fragments%20vs%20activities) online will yield a lot of conversations about whether fragments are good or [bad](https://corner.squareup.com/2014/10/advocating-against-android-fragments.html).  Because fragments live inside of an activity, and both the activity and fragment have lifecycle and event handling, things can be overly complex.  Additionally there are memory implications and other concerns you might run into.  Suffice to say, I'm going forward with fragments in my solution though that doesn't mean I'm sold on them being the best solution.

###The Initial Layout
When you first create the Navigation Drawer Activity, there are 5 files we'll look at:

* MainActivity.java - this is the code behind for everything in our app.
* activity_main.xml - this is the layout for the app including the nav drawer and an *include* for the app_bar_main.
* app_bar_main.xml - this is the layout with the toolbar (at the top), a floating action button (at the bottom right), and an *include* for content_main.
* content_main.xml - this is the layout for the *content* of the main page.
* nav_header_main.xml - this is the UI for the top part of the nav drawer.

Now I've already said that I don't think this is the best example of how to do navigation becuase it doesn't show you what to do when you tap an item in the nav drawer (it only demonstrates how to get the event when an item is tapped in the **onNavigationItemSelected** method).  Furthermore, from looking at how it displays the content, it's not clear what to do.  In the **MainActivity**'s *onCreate* method there is a call to:

{% highlight java %}
setContentView(R.layout.activity_main);
{% endhighlight %}

This is what you typically see in an Activity and binds the UI of a layout file to the Activity code.  In this case, the activity_main layout contains the nav drawer and an *include* statement for the app_bar_main.  The app_bar_main in turn contains the toolbar at the top and does an *include* on the content_main.  It would seem like the solution is to replace the content of the second *include* whenever the user taps an item on the menu.  However, you can't really replace an *include* like that.  We could use custom views and inflate and replace them whenever we want, but that might require a significant amount of additional work (or maybe not, hopefully someone can provide a solution that does that).  Adding fragments ends up being relatively easy.

###Adding Fragments to the Sample
First, open up the **app_bar_main.xml**, comment out the *include* and add a new *FrameLayout*:

{% highlight xml %}
<!--<include layout="@layout/content_main" />-->

<FrameLayout
  android:id="@+id/flContent"
  android:layout_width="match_parent"
  android:layout_height="match_parent"
  android:layout_marginTop="?attr/actionBarSize"/>
{% endhighlight %}

This *FrameLayout* is what we'll use to load our fragments into.  Next, you'll want to add a few fragments.  To do so, right click on your project, or go to File --> New and from the Fragment list choose *Fragment (Blank)*.  Add at least two fragments to your project so you can demonstrate moving between them.  The next step is to load a fragment when the app first launches.  Go to the **MainActivity**'s *onCreate* method and put the following in after the call to **setSupportActionBar**:

{% highlight java %}
Fragment fragment = null;
Class fragmentClass = null;
fragmentClass = FragmentOne.class;
try {
    fragment = (Fragment) fragmentClass.newInstance();
} catch (Exception e) {
    e.printStackTrace();
}

FragmentManager fragmentManager = getSupportFragmentManager();
fragmentManager.beginTransaction().replace(R.id.flContent, fragment).commit();
{% endhighlight %}

You'll then need to add **OnFragmentInteractionListener** to the interfaces your MainActivity implements and also implement the **onFragmentInteraction** method.  Finally, in the **onNavigationItemSelected** method, you can add the ability to load different fragments when menu items are tapped:

{% highlight java %}
public boolean onNavigationItemSelected(MenuItem item) {
    // Handle navigation view item clicks here.
    int id = item.getItemId();
    Fragment fragment = null;
    Class fragmentClass = null;
    if (id == R.id.nav_camera) {
        fragmentClass = FragmentOne.class;
    } else if (id == R.id.nav_gallery) {
        fragmentClass = FragmentTwo.class;
    } else if (id == R.id.nav_slideshow) {
        fragmentClass = FragmentOne.class;
    } else if (id == R.id.nav_manage) {
        fragmentClass = FragmentTwo.class;
    } else if (id == R.id.nav_share) {
        fragmentClass = FragmentOne.class;
    } else if (id == R.id.nav_send) {
        fragmentClass = FragmentTwo.class;
    }
    try {
        fragment = (Fragment) fragmentClass.newInstance();
    } catch (Exception e) {
        e.printStackTrace();
    }
    FragmentManager fragmentManager = getSupportFragmentManager();
    fragmentManager.beginTransaction().replace(R.id.flContent, fragment).commit();

    DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
    drawer.closeDrawer(GravityCompat.START);
    return true;
} 
{% endhighlight %}

Here I'm just loading one of the two fragments I've added to my app.  Note that becuase I have two different fragments, I had to implement the interfaces for both **FragmentOne.OnFragmentInteractionListener** and **FragmentTwo.OnFragmentInteractionListener**.  

That's all you need to do to implement fragment loading in your Navigation Drawer.  What the user taps a menu item, the drawer will slide back in smoothly and the new fragment will have already started / finished loading.  This also prevents any possible jankiness that you *could* see when launching a new activity.  One last thing to note is that if you switch to a different fragment and then rotate the device or cause another recreation of the activity, the code above will cause the first fragment to be reloaded.  One easy way to deal with that is to  wrap the fragment block in the *onCreate* method in a check to see if the **savedInstanceState** is not null like this:

{% highlight java %}
protected void onCreate(Bundle savedInstanceState) {
    ...
    if (savedInstanceState == null) {
        //Fragment load code
    }
    ...
}
{% endhighlight %}

One actual last thing is that ther are definitely optimizations you could make on the code and event handling here but this is a good start.  You can grab the [source code from this demo on GitHub](https://github.com/ChrisRisner/AndroidFragmentNavigationDrawer).