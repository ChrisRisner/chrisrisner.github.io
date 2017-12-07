---
layout: post
title: "Xamarin iOS Error Confusion"
date: Mon Mar 06 2017 9:16:00
commentsOn: true
status: publish
type: post
published: true
categories: [Xamarin,iOS,Forms,Errors]
excerpt: "While adding iCloud connectivity to Xamarin.iOS application, I ran into a weird erorr and wanted to share how to fix it."
logoUrl: null
keywords: Xamarin,iOS,Forms,Errors
filepath: 2017-3-6-Xamarin-iOS-Error-Confusion.markdown
disqus_identifier: 2017-3-6-Xamarin-iOS-Error-Confusion
redirect_from: 
  - /xamarin-ios-error-confusion/
---

As I've continued working on the Xamarin.Forms application I've been building, 
I've learned a lot.  One of the issues I ran into was an error in the iOS version of
my application and as I didn't find an easy to understand solution, I thought I would
document it here.  I'll list the error first then explain the scenario and how to fix
it.

### AX Exchange error: Error Domain=Accessibility Code=0 "Remote service does not respond to _accessibilityMachPort" UserInfo={NSLocalizedDescription=Remote service does not respond to _accessibilityMachPort}

Part of the application revolves around uploading files.  For Android this isn't very
difficult and it even makes *sense* as Android has a file system you can access and
external storage in the form of SD cards.  With iOS you can store files for your own
app but not others (for the most part).  However, you can access a user's iCloud
if they grant you permission.  To this end, I started looking at the [FilePicker Plugin for Xamarin and Windows](https://github.com/Studyxnet/FilePicker-Plugin-for-Xamarin-and-Windows).

In theory what this plugin would do is with one call open up a file picker connected
to iCloud on iOS and to the disk on Android (and who knows on Windows).  This plugin
works great for Android.  However, for iOS calling the **PickFile** method results in 
this error:

**This functionality is not implemented in the portable version of this assembly. You should reference the NuGet package from your main application project in order to reference the platform-specific implementation.**

At the time of writing, it appears the author [knows](https://github.com/Studyxnet/FilePicker-Plugin-for-Xamarin-and-Windows/issues/28)
about the issue but hasn't yet pushed a fix out to NuGet.  So instead, I took that code
and baked it into my app for Android and iOS and it worked for both.  However, when the
picker pops up to let you pick a file from iCloud, it comes along with the error 
being printed out to Application Output over and over and over again:

### AX Exchange error: Error Domain=Accessibility Code=0 "Remote service does not respond to _accessibilityMachPort" UserInfo={NSLocalizedDescription=Remote service does not respond to _accessibilityMachPort}

I did a bit of searching and didn't find anything **DIRECTLY** related to the FilePicker
but I did find something about custom keyboards and external testing frameworks.  
Xamarin.iOS apps are wired to use **Calabash** for testing with Xamarin Test Cloud and
you will find this in the **AppDelegate**:

```C#
#if ENABLE_TEST_CLOUD
			Xamarin.Calabash.Start();
#endif
```

Commenting that out led to the error no longer occurring.  I'm not 100% sure what the
is causing this issue but at least there is a quick fix.