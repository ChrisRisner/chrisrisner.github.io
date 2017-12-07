---
layout: post
title: "Getting Realm to Build Xamarin Apps with VSTS"
date: Wed Dec 14 2016 9:16:00
commentsOn: true
status: publish
type: post
published: true
categories: [Azure,CI,Visual Studio Team Services,Xamarin]
excerpt: "When adding Realm to a Xamarin project, by default building with Visual Studio Team Services is broken.  This post will explain how to get it to work."
logoUrl: null
keywords: Azure,Visual Studio Team Services,Continuous Integration,Xamarin,Realm
filepath: 2016-12-14-Getting-Realm-to-Build-Xamarin-Apps-with-VSTS.markdown
disqus_identifier: 2016-12-14-Getting-Realm-to-Build-Xamarin-Apps-with-VSTS
redirect_from: 
  - /getting-realm-to-build-xamarin-apps-with-vsts/
---

I've recently been working on a Xamarin.Forms project for Android and 
iOS and recently came across an issue that took some experimenting to get
fixed so I thought I would share it for anyone else that might run into it.

Realm is a database designed for mobile applications and offers a safe,
easy, non-ORM replacement for SQLite.  The intent is that you can, for the
most part, mark your data model objects as **RealmObject**s and Realm 
will handle all of the persistence for you.  As with anything, it gets
more complicated than that but so far it's still much better for what
I'm doing than SQLite.  If I needed the ability to do offline synchronization
with an online data source, I'd be looking at [Azure Mobile Apps](https://azure.microsoft.com/en-us/services/app-service/mobile/)
, but as I don't I'm fine with what Realm will do for me.

Adding Realm to your Xamarin.Forms application just requires adding the 
[Realm NuGet](https://www.nuget.org/packages/Realm/) package to your projects.
From there, you should be able to compile your projects without any issues.

However, if you have Continuous Integration set up to auto-build your projects
and run tests with every build, it's possible to run into an issue.  I use
[Visual Studio Team Services](https://www.visualstudio.com/team-services/) to
build all of my mobile projects and then deliver them to [HockeyApp](http://hockeyapp.net)
for beta testing.  I'll have to post more about setting up the Build Definition
(the steps for building and uploading my compiled applications) but want to 
focus on the issue that having Realm in your projects has with the build
process.

When you add Realm to your projects, it adds a Target as part of the package.  
That step, called **CopyRealmWeaver** which copies **RealmWeaver.Fody.dll** as
part of the build process.  I won't get into what [Fody](https://github.com/Fody/Fody)
is but it's a necessary part of using Realm.  The XML found in the **Realm.targets**
has the following inside of it:  

```xml
<Target Name="CopyRealmWeaver" BeforeTargets="FodyTarget">
  <Message Text="CopyRealmWeaver" />
  <Error 
    Text="Solution directory was not set. If you are building via xbuild, specify by adding a /p:SolutionDir=/path/to/solution/folder argument. See github.com/realm/realm-dotnet/issues/656"
    Condition="'$(SolutionDir)' == ''" />
  <Copy SourceFiles="$(MSBuildThisFileDirectory)../tools/RealmWeaver.Fody.dll" DestinationFolder="$(SolutionDir)/Tools" />
</Target>
```

What this does is check to make sure **$(SolutionDir)** has been specified
as part of the call to xbuild, or in the case of VSTS, msbuild.  Provided that
value has been specified, it then copies the **RealmWeaver.Fody.dll** from a tools
directory in the packages folder into the Solution directory.

## What's wrong here

The problem here is that when compiling with VSTS, there is some step that changes
the SolutionDir value to **\*undefined\***.  When I ran into this, it was 
especially weird as I couldn't seem to find a reference to VSTS, build, and
**\*undefined\*** anywhere.  I did find a [Stack Overflow post](http://stackoverflow.com/questions/635346/prebuild-event-in-visual-studio-replacing-solutiondir-with-undefined) 
about Visual Studio replacing **$(SolutionDir)** with **\*undefined\*** which
wasn't the solution to my problem exactly but did get me on the right path.  From there, 
I took a look at the call to MSBuild to see what was showing up:

```
2016-12-13T19:23:38.1392477Z ##[command]"C:\Program Files (x86)\MSBuild\14.0\bin\msbuild.exe" "C:\a\1\s\src\Droid\MyApp.Android.csproj" /nologo /nr:false /dl:CentralLogger,"C:\a\_tasks\XamarinAndroid_27edd013-36fd-43aa-96a3-7d73e1e35285\1.1.1\ps_modules\MSBuildHelpers\Microsoft.TeamFoundation.DistributedTask.MSBuild.Logger.dll";"RootDetailId=39592de0-fb1c-4156-a73e-b2e8ee77129e|SolutionDir=C:\a\1\s\src\Droid"*ForwardingLogger,"C:\a\_tasks\XamarinAndroid_27edd013-36fd-43aa-96a3-7d73e1e35285\1.1.1\ps_modules\MSBuildHelpers\Microsoft.TeamFoundation.DistributedTask.MSBuild.Logger.dll"  /p:configuration="Release" /p:_MSDeployUserAgent="VSTS_db204fe6-401b-4488-b9c9-02229bdeafd2_build_25_317" /t:PackageForAndroid /p:OutputPath="C:\a\1\b/Release" /p:JavaSdkDirectory=" C:\Program Files (x86)\Java\jdk1.8.0_102"
```

What I want to highlight from that call to msbuild is **SolutionDir=C:\a\1\s\src\Droid**.  It 
*seems* like we're specifying a Solution Directory, but the error shows us that somehow,
that is being overwritten.  So we need to override that overwrite and ensure a value
is in fact being passed in. 

![Build Xamarin Additional Arguments]({{ site.url }}/upload/realm-vsts-build-arguments.png)

Thankfully, the Build Xamarin project build step has a spot for **Additional Arguments** at
the bottom.  In this case, I set the solution directory to the directory of my overall solution
file and where the tools directory containing the RealmWeaver.Fody.dll is at.  The format
of the argument is important so this is what you should be using (adjusting the path for your)
tools folder location of course:

**/p:SolutionDir="src"**

With that done, I was able to run builds without any issue.  This seem to be an Android only
issue so you shouldn't need to change anything on your iOS build.  

## Update 2-16-2017: A new error

After a recent update (to my code base), I found that my workaround was no longer working.  The new error I was seeing was:

```
FodyTarget:
  Fody: Fody (version 1.29.4.0) Executing
  Fody: ProjectDirectory: 'D:\a\1\s\src\MyApp\MyApp.PCL\'.
  Fody: AssemblyPath: 'D:\a\1\s\src\MyApp\MyApp.PCL\obj\Release\MyApp.PCL.dll'
  Fody: Found path to weavers file 'D:\a\1\s\src\MyApp\MyApp.PCL\FodyWeavers.xml'.
##[error]Fody: SolutionDir "D:\a\1\s\src\MyApp\MyApp.PCL\src" does not exist.
```

What this appears to be doing is adding the **SolutionDir** that I specified above to the end of the PCL's path.  I was able to fix this once again by changing my **Additional Arguments** to:

**/p:SolutionDir="/"**

I suspect this was due to a change in the **Realm.targets** XML file for the newer version of Realm that I updated to when I updated NuGets.