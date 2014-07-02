<div id="sign-up-form-area">
    <div class="title"></div>
    <form action="${out value=base_path /}signup" id="signin-form" method="post">
        <h1>Your info:</h1>
        <input type="text" class="" name="user[name]" value="Name" data-current_status="${out value=session.user_registration.name xml_escape=True /}" data-original_value="Name"/>
        <input type="text" class="" name="user[email]" value="Email" data-current_status="${out value=session.user_registration.email xml_escape=True /}" data-original_value="Email"/>
        <h1>Account info:</h1>
        <input type="text" class="" name="user[username]" value="Username" data-current_status="${out value=session.user_registration.username xml_escape=True /}" data-original_value="Username" />
        <input type="password" class="small" name="user[_parameters][password]" value="******" data-current_status="" data-original_value="******" />
        <input type="password" class="small right" name="user[_parameters][confirm_password]" value="******" data-current_status="" data-original_value="******" />
        <div class="form-buttons">
            <div id="cancel" class="button-large">Cancel</div>
            <div id="post" class="button-large">Sign Up</div>
        </div>
        <div class="clear"></div>
    </form>
</div>
