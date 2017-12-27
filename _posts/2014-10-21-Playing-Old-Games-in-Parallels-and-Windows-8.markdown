---
layout: post
title: "Playing Old Games in Parallels and Windows 8"
date: Tue Oct 21 2014 15:51:00
commentsOn: true
status: publish
type: post
published: true
categories: [Games]
excerpt: "This post details how to play old 90s era computer games in Parallels.  Specifically it details how to rip and mount mixed-mode (audio and data) cds."
logoUrl: null
keywords: Mixed-mode cd,audio,data,game,pc,rip,burn,mount,parallels
filepath: 2014-10-21-Playing-Old-Games-in-Parallels-and-Windows-8.markdown
disqus_identifier: Playing-Old-Games-in-Parallels-and-Windows-8
---
<p>This post is about how to get a specific class of Win95 / Win98 era video games playing properly in Parallels on OS X.&#160; Somewhat less important is that Parallels is running Windows 8 (I don’t see why it wouldn’t work with Windows 7).&#160; If you’re using a computer without a CD drive (like any of the Microsoft Surface Pros) this should still prove to be helpful since a lot of the issue actually has to do with the lack of the CD Drive.</p>  <p>Every once in a while, I get a hankering to play one of the games of my youth.&#160; The games I played back in high school or even college.&#160; The games I played when I had nothing but time to play games.&#160; One of the games I enjoyed playing long ago was <a title="Migh and Magic 6" href="http://en.wikipedia.org/wiki/Might_and_Magic_VI:_The_Mandate_of_Heaven">Might and Magic 6</a>.&#160; MM6 was one of many role-playing games developed by New World Computing.&#160; NWC was a in-house dev studio of 3DO.&#160; Neither of these still exist, though their games live on.&#160; If you haven’t played any of those games and have free time, they’re arguably worth checking out.&#160; MM6 and many other MM games are available on <a title="MM6 on GOG" href="http://www.gog.com/game/might_and_magic_6_limited_edition">Good Old Games for an incredible bargain</a>.&#160; If you want to buy the game (or any other game) on GOG, you don’t need to continue reading this, they’ve already solved the problem (at least for MM6).&#160; However, the problem we’re solving here is a bit different.&#160; If you still have the game CDs, read on.</p>  <p>The problem with many games of that era (the 90s…ahh I’m old) were that they used <a title="Mixed Mode CDs" href="http://en.wikipedia.org/wiki/Mixed_Mode_CD">Mixed Mode CDs</a>.&#160; Mixed Mode CDs solved the problem of having CD quality sound in video games.&#160; This was accomplished by having one data track on the CD (usually track 1) and then all of the other tracks were the actual music tracks.&#160; You might remember having put a game CD into a music CD player and hearing very loud static if the first track played.&#160; This was what happened when a music player tried to play the data.&#160; <em>Smarter</em>, mostly computer, CD-ROM drives could check a bit and realize that the first track was data and skip it.</p>  <p>The real problem comes when you try to duplicate one of these CDs so you can “mount” it on your machine.&#160; If you just want to reproduce the data portion of a game CD to get past the CD-check (back in the day you had to have the game CD in the drive to run the game…or you had to run a no-cd crack) this is easy enough.&#160; You can use any of tons of programs to just copy the cd.&#160; If you want to mount it to your computer or parallels image, all you need to do is generate an ISO of the CD drive. To do this, just get access to a computer with a CD drive, insert the CD, and then search for how to generate an ISO using your operating system.&#160; For OS X I know you can do this very easily with the built-in Disk Utility.&#160; From there, it’s very easy to mount an ISO using either OS X or Win8.&#160; In either system, you just double click the ISO file and it’s done.&#160; You don’t have to do anything special.&#160; However, things are much more complicated for our Mixed-Mode CDs.&#160; When you make the ISO of a Mixed-Mode CD, it only includes the data portion, not the audio.&#160; This mostly works but if you want the music as well, you’re out of luck.&#160; </p>  <p>After a lot of searching (it doesn’t help that “mixed-mode cd” isn’t an official term) I finally stumbled upon <a title="Backing up mixed mode cds" href="http://www.gog.com/forum/general/backing_up_mixed_mode_cds_in_os_x">this page</a> in the GOG forums.&#160; It is essentially the ONE article after hours of looking that solved the problem.&#160; You can take a look at the post for all the specific details but I’ll also detail them here.&#160; <strong>IF YOU DO </strong>jump directly to the article, make sure you read the comment on getting the actual device string (for step 6).</p>  <p><strong>Prereqs</strong></p>  <p>In order for this to work, you need to have quite a bit of software installed on OS X.&#160; If you’re not prepared to jump through quite a few hoops, abandon all hope (but you’re trying to play a twenty year old game so what are a few hoops).&#160; First install the following:</p>  <ul>   <li>Xcode - You can get this from the Mac App Store. </li>    <li>MacPorts - install instructions are <a href="https://www.macports.org/install.php">here</a>.&#160; This enables you to install further prereqs. </li>    <li>CDRDAO - open a Terminal and type “port install cdrdao” </li>    <li>bchunk - in the same Terminal, type “port install bchunk” </li> </ul>  



<p><strong>Processing the cd</strong></p>  <p>Insert your cd and go back to the Terminal.&#160; Run “mount”.&#160; This should print out all the drives mounted on your computer including the cd drive.&#160; You’ll likely see two things mounted for the cd, so in my case something like this:

{% highlight console %}
/dev/disk2s0 on /Volumes/MM7_Disk2 (cd9660, local, nodev, nosuid, read-only, noowners)      
/dev/disk2 on /Volumes/Might &amp; Magic VII (cddafs, local, nodev, nosuid, read-only, noowners)
{% endhighlight %}
	
To unmount this, you’d then type “disktool -u disk2” and both items will be unmounted.&#160; Next we need to get our device path.&#160; We’ll do this by running: “sudo cdrdao scanbus”.&#160; After entering your password you’ll get something like this:

{% highlight console %}
IOService:/AppleACPIPlatformExpert/PCI0@0/AppleACPIPCI/SATA@1F,2/AppleIntelPchSeriesAHCI/PRT1@1/IOAHCIDevice@0/IOAHCISerialATAPI/IOSCSIPeripheralDeviceNub/IOSCSIPeripheralDeviceType05/IODVDServices : MATSHITA, DVD-R&#160;&#160; UJ-8A8, HB14
{% endhighlight %}

Now that you have that, we’re ready to process our CD.&#160; (You may need to reunmount your cd disk again here).&#160; In the following command, replace <strong>&lt;DEVICE&gt; </strong>with what you just got above minus the “, DVD-R UJ8A8, HB14” part:

{% highlight console %}
cdrdao read-cd --datafile image.bin --driver generic-mmc:0x20000 --device &lt;DEVICE&gt; --read-raw image.toc
{% endhighlight %}

In my case, the command looks like this:

{% highlight console %}
cdrdao read-cd --datafile image.bin --driver generic-mmc:0x20000 --device &quot;IOService:/AppleACPIPlatformExpert/PCI0@0/AppleACPIPCI/SATA@1F,2/AppleIntelPchSeriesAHCI/PRT1@1/IOAHCIDevice@0/IOAHCISerialATAPI/IOSCSIPeripheralDeviceNub/IOSCSIPeripheralDeviceType05/IODVDServices&quot; --read-raw image.toc
{% endhighlight %}

That’s going to take a little while to run.&#160; The last step is to use a tool installed with CDRDAO named toc2cue.&#160; We’ll use this to create a cue file from the toc file.&#160; Run this in terminal, “toc2cue image.toc image.cue”.&#160; </p>  <p>Now we just need to mount the file in parallels.</p>  <p><strong>Mounting in Parallels</strong></p>  <p>Before you do anything, make sure you’ve shut down the Parallels image.&#160; It can’t just be suspended.&#160; Once that is done, right click on the VM (from the VM list) and go to <strong>Configure</strong>.&#160; Then choose the <strong>Hardware</strong> tab.&#160; From this list, click the <strong>+</strong> in the bottom left and choose to add a <strong>CD/DVD</strong>.&#160; Click on the <strong>Connect To</strong> drop down and select <strong>Choose an image file…</strong>&#160; Choose the image.cue file that you generated and click OK and close the window.&#160; Start your VM up and you should see a CD drive mounted with your game on it and now when you play your game, it should play the music just fine!</p>  <p>One thing to note is that on occasion when playing MM6 the music would come over as static.&#160; I don’t think this had to do with my mounting approach as I seem to remember having this issue long ago when I wasn’t ripping and mounting the cd at all.</p>