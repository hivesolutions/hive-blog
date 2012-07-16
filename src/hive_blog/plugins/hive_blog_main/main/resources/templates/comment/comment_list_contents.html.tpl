<div id="comments-area">
    ${foreach item=comment index=comment_index from=post.comments}
        <div class="comment ${if item=comment.author.object_id value=post.author.object_id operator=eq}author${/if}">
            <div class="comment-number">${out_none value=comment_index format="%02.d" xml_escape=True /}</div>
            <div class="comment-avatar">
                <img src="http://www.gravatar.com/avatar/${out_none value=comment.author.get_gravatar_hash xml_escape=True /}" height="50" width="50" alt="" />
            </div>
            <div class="comment-contents">
                <span class="comment-date">${out_none value=comment.get_day xml_escape=True /}  ${out_none value=comment.get_month xml_escape=True /}</span>. ${out_none value=comment.author.name xml_escape=True /} wrote:
                <p class="comment-body">${out_none value=comment.contents xml_escape=True /}</p>
                <div class="comment-actions">
                    <a href="#">Reply</a>
                    <a href="#">Ping</a>
                </div>
            </div>
            <div class="clear"></div>
        </div>
    ${/foreach}
    <div id="comments-form-area">
        <div class="button-large ${if item=session_user_information value=None operator=neq}hidden${/if}">Post a comment</div>
        <form action="${out_none value=base_path /}comments" id="comment-form" class="${if item=session_user_information value=None operator=eq}hidden${/if}" method="post">
            ${if item=session_user_information value=None operator=eq}
                <h1>Login using:</h1>
                <div class="auth-buttons">
                    <div class="button-twitter">Twitter</div>
                    <div class="button-facebook">Facebook</div>
                    <div class="button-openid">OpenID</div>
                    <div class="clear"></div>
                </div>
                <div id="openid-area">
                    <input type="text" id="openid-field" name="openid[value]" value="OpenID" data-current_status="" data-original_value="OpenID" />
                    <div class="form-buttons-small">
                        <div id="login" class="button-large">Login</div>
                        <div class="clear"></div>
                    </div>
                </div>
                <h1>Or</h1>
                <input type="hidden" id="username-field" name="comment[author][username]" value="${uuid /}" />
                <input type="text" id="name-field" name="comment[author][name]" value="Name" data-current_status="" data-original_value="Name" />
                <input type="text" class="small" id="email-field" name="comment[author][email]" value="Email" data-current_status="" data-original_value="Email" />
                <input type="text" class="small" id="website-field" name="comment[author][website]" value="Website" data-current_status="" data-original_value="Website" />
                <h1>And then</h1>
            ${/if}
            <textarea name="comment[contents]" data-current_status="" data-original_value="Your comment">Your comment</textarea>
            <br />
            <input type="hidden" name="comment[post][object_id]" value="${out_none value=post.object_id xml_escape=True /}" />
            <input type="hidden" name="return_address" value="${out_none value=return_address xml_escape=True /}" />
            <div class="form-buttons">
                <div id="cancel" class="button-large">Cancel</div>
                <div id="post" class="button-large">Post</div>
                <div class="clear"></div>
            </div>
        </form>
    </div>
</div>
