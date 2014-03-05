<div id="add-post-form-area">
    <div class="title"></div>
    <form action="${out value=base_path /}posts" method="post">
        <input class="date-text-field small left" type="text" name="post[date]" value="YYYY-MM-DD" data-current_status="${out value=post.get_date_formatted xml_escape=True /}" data-original_value="YYYY-MM-DD" />
        <div class="dropbox left margin-left">
            <div class="dropbox-selected-value">Active</div>
            <div class="dropbox-button"></div>
            <div class="clear"></div>
            <div class="dropbox-options">
                <ul>
                    <li>Active</li>
                    <li>Inactive</li>
                </ul>
            </div>
        </div>
        <div class="clear"></div>
        <input type="text" name="post[title]" value="Title" data-current_status="${out value=post.title xml_escape=True /}" data-original_value="Title" />
        <textarea name="post[contents]" data-current_status="Contents" data-original_value="Contents">${out value=post.contents xml_escape=True /}</textarea>
        <div class="clear"></div>
        <div class="form-buttons">
            <div id="preview" class="button-large">Preview</div>
            <div id="post" class="button-large">Post</div>
        </div>
        <div class="clear"></div>
    </form>
</div>
${if item=post value=None operator=neq}
    <div class="separator"></div>
    ${include file="post_show_base_contents.html.tpl" /}
${/if}
