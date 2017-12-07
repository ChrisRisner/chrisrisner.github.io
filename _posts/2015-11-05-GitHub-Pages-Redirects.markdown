---
layout: post
title: "GitHub Pages Redirects"
date: Thu Nov 05 2015 20:16:00
commentsOn: true
status: publish
type: post
published: true
categories: [GitHub,Web]
excerpt: "A quick tip on setting up redirects with GitHub Pages."
logoUrl: null
keywords: GitHub Pages,Redirects
filepath: 2015-11-05-GitHub-Pages-Redirects.markdown
disqus_identifier: 2015-11-05-GitHub-Pages-Redirects
redirect_from: 
  - /github-pages-redirects/
---

A short while ago I [switched by blog over to GitHub Pages](http://chrisrisner.com/Changing-Blog-Platforms-Again/).  One of the issues I've ran into occasionally since then were people reporting 404s on some of my blog posts.  Up until today I've been handling these one at a time and only as they came up.  It was starting to become clear though that there were a few issues that were prevalent from the switchover.

## Case Sensitivity
It seems like there is no [shortage of debate no whether or not URLs should be case sensative](http://stackoverflow.com/questions/7996919/should-url-be-case-sensitive) but most blog engines seem to treat URLs the same regardless of casing.  This was certainly true of my blog when it was hosted on [Veritas](http://chrisrisner.com/Veritas--Creating-a-Blog-Engine-with-MVC-2-and--Net-4-0-%E2%80%93-Part-1/).  However, GitHub Pages is definitely very case sensative.  If I (or anyone else) had linked to page on my site using casing other than what the actual filename specified, a 404 would come up.  Unfortuantely, after doing some digging, it doesn't appear there is any easy option for turning case sensitivity off.

## The Fix
Fortunately, there is [guidance](https://help.github.com/articles/redirects-on-github-pages/) on using gem named [jekyll-redirect-from](https://github.com/jekyll/jekyll-redirect-from) to set up redirects.  Unfortunatly, this is not a "install it and everything will work" sort of solution.  Instead, you need to go into each page and in it's [front matter](http://jekyllrb.com/docs/frontmatter/) you have to specify what URLs should point to it.  If you wanted to allow for *ANY* variation in casing, you'd end up with quite a few lines there (2^x where x is the number of letters in your page title in fact).  Instead, I was most concerned with the most common url format, where all letters were lowercase.  So for this page, where the URL would be:

`http://chrisrisner.com/GitHub-Pages-Redirects`

I put this in the front matter:

```
redirect_from: 
  - /github-pages-redirects/
```

One issue I ran into when I first set this up was that if you don't put the trailing **/** then when you navigate to the page using the redirect URL, Chrome (and maybe other browsers) will redirect but then also open the save dialog.  From what I found it looks like if you don't put the trailing **/** or a valid extension, the server [serves it up as an octet-stream](https://github.com/jekyll/jekyll/issues/3513).  So make sure you test out your redirects and you're not causing that to happen.

In the course of doing this I also found a mess of other pages that had gotten screwed up due to the dreaded single quote vs apostrophe issue.  However, now many of the 404s I knew about, and even more ones that I didn't, have been fixed.  