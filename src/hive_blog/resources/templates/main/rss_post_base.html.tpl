<item>
    <title>${out value=post.title xml_escape=True /}</title>
    <link>${out value=base_url /}posts/${out value=post.object_id xml_escape=True /}</link>
    <comments>${out value=base_url /}posts/${out value=post.object_id xml_escape=True /}#comments-area</comments>
    <pubDate>${format_datetime value=post.date format="%a, %d %b %Y %H:%M:%S +0000" /}</pubDate>
    <dc:creator>${out value=post.author.username xml_escape=True /}</dc:creator>
    ${foreach item=tag from=post.tags}
        <category><![CDATA[${out value=tag.name /}]]></category>
    ${/foreach}
    <guid isPermaLink="false">${out value=base_url /}posts/${out value=post.object_id xml_escape=True /}</guid>
    <description><![CDATA[${out value=post.contents_abstract /}]]></description>
    <content:encoded><![CDATA[${out value=post.contents /}]]></content:encoded>
</item>
