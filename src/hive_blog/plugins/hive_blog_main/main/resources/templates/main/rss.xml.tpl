<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:wfw="http://wellformedweb.org/CommentAPI/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
    <title>Hive Solutions - The diary</title>
    <atom:link href="${out_none value=base_url /}rss" rel="self" type="application/rss+xml" />
    <link>http://blog.hive.pt</link>
    <description>Hive Solutions - The diary</description>
    <pubDate>${datetime format="%a, %d %b %Y %H:%M:%S +0000" /}</pubDate>
    <generator>http://hive.pt/colony</generator>
    <language>en</language>
        ${foreach item=post from=posts}
            ${include file="rss_post_base.html.tpl" /}
        ${/foreach}
    </channel>
</rss>
