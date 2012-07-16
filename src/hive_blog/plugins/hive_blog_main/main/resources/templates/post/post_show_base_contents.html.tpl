<div class="post ${if item=preview value=None operator=neq}post-preview${/if}">
    <div class="post-header">
        <div class="post-date">${out_none value=post.get_day xml_escape=True /},<br /><span>${out_none value=post.get_month xml_escape=True /}</span></div>
        <h1 class="post-title">
            <a href="${out_none value=base_path /}posts/${out_none value=post.object_id xml_escape=True /}">${out_none value=post.title xml_escape=True /}</a>
        </h1>
        <div class="clear"></div>
    </div>
    <div class="post-body">
        ${out_none value=post.contents /}
    </div>
    <div class="post-footer">
        <div class="post-signature">by <a href="#">${out_none value=post.author.username xml_escape=True /}</a></div>
        <div class="clear"></div>
        <p>
            <span>Tags</span> .
            ${foreach item=tag from=post.tags}
                <a href="#">${out_none value=tag.name xml_escape=True /}</a>,
            ${/foreach}
        </p>
        <p>
            <span>Comments</span> . <a href="${out_none value=base_path /}posts/${out_none value=post.object_id xml_escape=True /}#comments-area">${count value=post.comments  /} Responses</a>
        </p>
        <p>
            <span>Social</span> .
            ${include file="../social/social_show_base_contents.html.tpl" /}
        </p>
    </div>
</div>
