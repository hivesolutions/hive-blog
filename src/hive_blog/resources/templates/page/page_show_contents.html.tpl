${foreach item=post from=posts}
    ${include file="../post/post_show_base_contents.html.tpl" /}
${/foreach}
${if item=previous_page value=None operator=neq}
    <a href="${out value=base_path /}pages/${out value=previous_page xml_escape=True /}"><div id="previous-button" class="control-button">Newer Posts</div></a>
${/if}
${if item=next_page value=None operator=neq}
    <a href="${out value=base_path /}pages/${out value=next_page xml_escape=True /}"><div id="next-button" class="control-button">Older Posts</div></a>
${/if}
