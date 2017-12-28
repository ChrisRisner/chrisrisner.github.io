---
layout: post
title: "Switching Comments to StaticMan"
date: Wed Dec 27 2017 9:16:00
commentsOn: true
status: publish
type: post
published: true
categories: [GitHub,Blogging]
excerpt: "This post will walk through how you can deploy OpenWhisk onto a VM running in Azure."
logoUrl: null
keywords: GitHub,Blogging
filepath: 2017-12-27-Switching-Comments-to-StaticMan.markdown
disqus_identifier: 2017-12-27-Switching-Comments-to-StaticMan
redirect_from: 
  - /switching-comments-to-staticman/
---

Six years ago, when I was still using my own custom built blog engine, I switched the comment system over to using [Disqus](https://chrisrisner.com/Importing-Comments-into-Disqus).  At the time, this change made a lot of sense.  With just a little bit of additional markup per page, Disqus would render all of the comments and the comment form and handle everything for me, including the ability to do moderation.  Recently, when I [switched over to GitHub](https://chrisrisner.com/Changing-Blog-Platforms-Again), I kept on with Disqus as it was relatively easy and there were instructions on how to integrate.  Unfortunately, one of the issues with Disqus is that it loads quite a bit of JavaScript including ads.  While the JavaScript is not blocking, I wouldn't be entirely surprised if the long time for the page to actually finish loading didn't impact some ratings by a few certain search engines.  Plus, the only way to remove the ads (which aren't even relevant to the material of the site in anyway), is to pay.  

### A First Replacement: CommentIt

I'd taken a very brief look some months ago about finding a replacement that would work with GitHub pages.  Since GitHub pages are generated using [Jekyll](https://jekyllrb.com/) there isn't really a backend that can be used to run the comment engine.  I was chatting about it with one of my teammates at work and he mentioned he'd recently setup a new site on GitHub pages and had used [CommentIt](https://commentit.io/) to handle this comments.  Once you give CommentIt access to your GitHub repo and put some markdown on your site (to display comments and to put a comment form on the page), everything works.  CommentIt runs the backend javascript that actually handles processing comments.  Whenever a comment is made, it creates a pull request against your repo.  The one big issue both he and I had with CommentIt was that it puts comments into the Front Matter for your blog posts.  I'd much rather prefer comments end up in a different file or location.

### StaticMan

While looking around further, I stumbled upon [this post on mademistakes.com](https://mademistakes.com/articles/jekyll-static-comments/) about changing from Disqus or an external site to use [StaticMan](https://staticman.net/) for comments on GitHub Pages.  StaticMan functions similarly to CommentIt except it puts every comment in a separate file in your repo under the */data/comments/[slug]* path.  Additionally, there is support for replies, notifications, and Captchas. [Getting started is quite easy](https://staticman.net/docs/) and fully documented.  I did go down the route of trying to further customize my rendering and interface similar to what MadeMistakes.com had done and thought it would be good to share some of the implementation details.  Of particular importance, I'd look at the following files (on top of the JS and SCSS files):

* [/_includes/comments.html](https://github.com/ChrisRisner/chrisrisner.github.io/blob/master/_includes/comments.html)
* [/_includes/comment.html](https://github.com/ChrisRisner/chrisrisner.github.io/blob/master/_includes/comment.html)
* [_config.yml](https://github.com/ChrisRisner/chrisrisner.github.io/blob/master/_config.yml)
* [staticman.yml](https://github.com/ChrisRisner/chrisrisner.github.io/blob/master/staticman.yml)


One of the big things I want to call out because I ran into issues with it multiple times is the ordering of the comments.  Specifically, ordering didn't seem to be the same when running the site locally and when it was showing up in GitHub Pages.  I want to share what the **comments.html** looks like:

```
{% assign count = 0 %}
{% assign comments = (site.data.comments[page.slug] | where_exp: 'item', 'item.replying_to == ""' | sort: 'date') %} 
{% assign comments = (comments | sort) %}
{% for comment in comments %}              
  {% if comment[1].replying_to == "" %}    
    {% assign index       = (forloop.index | minus: count) %}
    {% assign r           = comment[1].replying_to %}
    {% assign replying_to = r | to_integer %}
    {% assign avatar      = comment[1].avatar %}
    {% assign email       = comment[1].email %}
    {% assign name        = comment[1].name %}
    {% assign url         = comment[1].url %}
    {% assign date        = comment[1].date %}
    {% assign message     = comment[1].message %}
    {% include comment.html index=index replying_to=replying_to avatar=avatar email=email name=name url=url date=date message=message %}
    
  {% else %}
  {% assign count = count | plus: 1 %}
  {% endif %}
{% endfor %}
```

For some reason, the query where we're trying to get comments that have nothing in the *replying_to* field doesn't work.  I've seen other examples where they compare against blank as in *where_exp: 'item', 'item.replying to == blank'* but that didn't work for me either.  The sorting was very bizarre and didn't make very much sense as, as near as I could tell, different rebuilds of the site lead to different ordering of the comments.

### Importing Disqus Comments

The next step was to export the comments from Disqus which I did with [these instructions](https://help.disqus.com/customer/portal/articles/472149-comments-export).  From there, I built a [program to translate the XML into YML comment files](https://github.com/ChrisRisner/DisqusToStaticManComments).  Once that was done, I just needed to copy the comments over and push them up to my repo.  Now all of my comments are showing and their in the correct order.