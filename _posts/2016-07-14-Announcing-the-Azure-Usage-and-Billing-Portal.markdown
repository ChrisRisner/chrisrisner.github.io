---
layout: post
title: "Announcing the Azure Usage and Billing Portal"
date: Thu Jul 14 2016 9:16:00 GMT-0800 (PST)
comments: true
status: publish
type: post
published: true
categories: [Azure]
excerpt: "This post describes the release of the open soure project the Azure Usage and Billing Portal."
logoUrl: null
keywords: Azure
filepath: 2016-07-14-Announcing-the-Azure-Usage-and-Billing-Portal.markdown
disqus_identifier: 2016-07-14-Announcing-the-Azure-Usage-and-Billing-Portal
redirect_from: 
  - /announcing-the-azure-usage-and-billing-portal/
---

Today I'm excited to [announce](https://azure.microsoft.com/en-us/blog/announcing-the-release-of-the-azure-usage-and-billing-portal/) that we've released the [Azure Usage and Billing Portal](https://github.com/Microsoft/AzureUsageAndBillingPortal) as an open source project on GitHub.  The Azure Usage and Billing Portal is a solution which enables you to review the usage and resulting billing information across multiple subscriptions.  Currently, if you are an Azure consumer using multiple subscriptions, you're options for viewing all of the usage over any given time period aren't that great.  The Azure Portal enables you to view usage and billing for individual subscriptions one at a time (both a breakdown of current charges, cost by service, and cost by resource) but if you're using multiple subscriptions, trying to review all of the information there is inefficient.  Furthermore, you are able to download a CSV file of Azure consumption for each subscription, but that is a manual process and would require processing afterwards.

Last year, Microsoft announced [new APIs](https://azure.microsoft.com/en-us/documentation/articles/billing-usage-rate-card-overview/) to provide a way to programmatically pull information on usage and rate cards for your subscriptions.  Included in that announcement were a number of [samples](https://azure.microsoft.com/documentation/samples/?term=billing) demonstrating how you can pull information for your own subscriptions.  When this announcment came out, we had already been seeing requests from customers we were working with for a way to visualize and track their spend.  This spurred my team into action to build something which would make consuming and seeing this data easier.  

Once deployed, you can now register any subscriptions you want so that the daily usage will be polled and displayed in an easy to use Power BI dashboard.  This dashboard enables you to slice data in many ways including by subscription, by resource type, by resource name, by geo, by date, and more.  Furthermore, you can use the SQL Database that stores the usage and billing to build any sort of interface / alerting on top of the data you want.  

Mustafa Kasap, the lead engineer on this project, wrote up a [great blog post](https://blogs.msdn.microsoft.com/mustafakasap/2016/07/14/welcome-azure-usage-and-billing-portal/) describing the project a bit more including some helpful images.   

We've got a lot of plans for future feature additions and already a few issues to fix.  We welcome any contributions or feedback on the project either on the blog posts or as issues on the [GitHub site](https://github.com/Microsoft/AzureUsageAndBillingPortal).  