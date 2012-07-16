<item>
<title>${out_none value=post.title xml_escape=True /}</title>
<link>${out_none value=base_url /}posts/${out_none value=post.object_id xml_escape=True /}</link>
<comments>${out_none value=base_url /}posts/${out_none value=post.object_id xml_escape=True /}#comments-area</comments>
<pubDate>${format_datetime value=post.date format="%a, %d %b %Y %H:%M:%S +0000" /}</pubDate>
<dc:creator>${out_none value=post.author.username xml_escape=True /}</dc:creator>
${foreach item=tag from=post.tags}
    <category><![CDATA[${out_none value=tag.name /}]]></category>
${/foreach}
<guid isPermaLink="false">${out_none value=base_url /}posts/${out_none value=post.object_id xml_escape=True /}</guid>
<description><![CDATA[${out_none value=post.contents_abstract /}]]></description>
<content:encoded><![CDATA[${out_none value=post.contents /}]]></content:encoded>
</item>
