---
layout: post
title: "Using PEAR with Windows Azure Websites and PHP"
date: Mon Jul 23 2012 10:57:00
commentsOn: true
status: publish
type: post
published: true
categories: [PHP, Azure, IIS, Web]
excerpt: "This article walks a user through using PEAR with Windows Azure Websites.  This necessitates making adjustments to a .user.ini file to specify what the include path is."
logoUrl: null
keywords: Windows Azure,PHP,Azure,PEAR,PEAR on Azure,Windows Azure Websites
filepath: 2012-07-23-Using-PEAR-with-Windows-Azure-Websites-and-PHP.markdown
disqus_identifier: Using-PEAR-with-Windows-Azure-Websites-and-PHP
---
<p><strong>UPDATE 7-26-2012:  The tutorial linked to below has since been updated to use Composer.  You should use Composer but if for some reason you want to use your own PEAR directory, you can continue with the below.</strong>
</p>

<p><img style="margin: 0px 0px 5px 5px; display: inline; float: right" title="Windows Azure" alt="Windows Azure" align="right" src="http://chrisrisner.com/upload/windowsazurevertical.jpg" />If you’ve started to play around with <a href="https://www.windowsazure.com/en-us/home/scenarios/web-sites/">Windows Azure Websites</a> and PHP and you want to use <a title="PEAR" href="http://pear.php.net/">PEAR</a>, you may have run into problems.&#160; As of now, PEAR extensions aren’t officially supported on Windows Azure Websites.&#160; </p>  <p>If you go through <a title="Windows Azure Websites in PHP with Storage" href="https://www.windowsazure.com/en-us/develop/php/tutorials/website-with-storage/">this tutorial</a> on the Windows Azure website, it actually instructs you to use PEAR and to push your site up to Windows Azure Websites at the end.&#160; If you follow all of the steps, the site will work flawlessly on your own computer but will return 500 errors when you try to run it on Windows Azure.&#160; It’s not exactly easy to figure out the specific reason for this as there isn’t any error information outputted to the browser.&#160; In order to get any more information out of your site, you’ll need to create a <strong>.user.ini</strong> file and set <strong>display_errors = On </strong>as <a title="Windows Azure Websites and .users.ini file" href="http://blogs.msdn.com/b/silverlining/archive/2012/07/10/configuring-php-in-windows-azure-websites-with-user-ini-files.aspx">described here</a>.&#160; The <strong>.user.ini</strong> file allows you to override some options from the <strong>php.ini</strong> file.&#160; In this case you’re telling IIS to display error information.&#160; If you do that, and then run your site, you’ll see the following error:

{% highlight console %}
My ToDo List (powered by PHP and Azure Tables)
Not working? Warning: require_once(HTTP/Request2.php): failed to open stream: No such file or directory in C:\DWASFiles\Sites\phpsassample\VirtualDirectory0\site\wwwroot\WindowsAzure\Common\
Internal\Http\HttpClient.php on line 33 Fatal error: require_once(): Failed opening required 'HTTP/Request2.php' (include_path='.;C:\php\pear') in C:\DWASFiles\Sites\phpsassample\VirtualDirectory0\site\wwwroot\WindowsAzure\Common\Internal\Http\HttpClient.php on line 33
{% endhighlight %}

This is because, as I said before, PEAR extensions aren’t supported.&#160; Thankfully, there is a way around this.&#160; It includes copying the PEAR directory into the root directory of your web application and then pushing it up with your website.&#160; So, on OSX, my PEAR directory is located at /Users/chrisner/pear.&#160; I copied that whole directory into my website’s root folder.&#160; Now, let’s say you’re accessing PEAR or Windows Azure libraries from different sub-folders.&#160; Unfortunately, the &quot;<strong>require_once</strong>” call isn’t smart enough to search your whole site directory for a file and the <strong>php.ini</strong> isn’t set up to include your directory either.&#160; Thankfully, the <strong>.user.ini</strong> file can rescue us again.&#160; In addition to the <strong>display_errors</strong> line, we can add a <strong>include_path</strong> which will override what is in the <strong>php.ini</strong>:

{% highlight console %}
display_errors = On     <br />include_path=".;C:\DWASFiles\Sites\phpsassample\VirtualDirectory0\site\wwwroot\Pear";
{% endhighlight %}

As you can see from the errors outputted above, my website is located in <strong>C:\DWASFiles\Sites\phpsassample\VirtualDirectory0\site\wwwroot\</strong>.&#160; This means that the PEAR folder I push to the server will be located in that directory.&#160; So, if you set the <strong>include_path</strong> to be that PEAR directory, whenever any PHP file tries to include a PEAR PHP file, it will find it there.&#160; Now this leaves one obvious issue that you will have to deal with:&#160; updates.&#160; Since you’re pushing the PEAR directory to the site on your own, you’d need to handle updating any of those files manually.&#160; On the flip side, you can use Composer which is supported.</p>