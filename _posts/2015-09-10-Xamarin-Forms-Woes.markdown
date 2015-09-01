---
layout: post
title: "Xamarin Forms Woes"
date: Thu Sep 10 2015 20:16:00 GMT-0800 (PST)
comments: true
status: publish
type: post
published: true
categories: [Projects,Mobile,Xamarin]
excerpt: "Some of the issues I've had trying to work with Xamarin Forms"
logoUrl: null
keywords: xamarin,forms,xamarin forms,issues,debugging,pain
filepath: 2015-09-10-Xamarin-Forms-Woes.markdown
disqus_identifier: 2015-09-10-Xamarin-Forms-Woes
---



Xamarin issue adding RestSharp to PCL:
Successfully installed 'RestSharp 105.2.3'.
Adding 'RestSharp 105.2.3' to SmartFridgeMobile.
Could not install package 'RestSharp 105.2.3'. You are trying to install this package into a project that targets 'portable-net45+win+wp80+MonoTouch10+MonoAndroid10+xamarinmac20+xamarinios10', but the package does not contain any assembly references or content files that are compatible with that framework. For more information, contact the package author.


Write once, painfully debug everywhere

Issues with toolbars not showing up and methods not firing in the same order on devices

Issues with navigation being weird on Windows Phone 
-for Page Renderer (what do you do with auth.getUI)
-when using Navigation.NavigateTo had issues with transparent pages, had to set background colors to get it to work