// Hive Solutions Blog
// Copyright (C) 2010-2012 Hive Solutions Lda.
//
// This file is part of Hive Solutions Blog.
//
// Hive Solutions Blog is confidential and property of Hive Solutions Lda.,
// its usage is constrained by the terms of the Hive Solutions
// Confidential Usage License.
//
// Hive Solutions Blog should not be distributed under any circumstances,
// violation of this may imply legal action.
//
// If you have any questions regarding the terms of this license please
// refer to <http://www.hive.pt/licenses/>.

// __author__    = João Magalhães <joamag@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision$
// __date__      = $LastChangedDate$
// __copyright__ = Copyright (c) 2010-2012 Hive Solutions Lda.
// __license__   = Hive Solutions Confidential Usage License (HSCUL)

jQuery(document).ready(function() {
    // retrieves the browser name and converts it to lowercase
    var browserName = BrowserDetect.browser.toLowerCase();

    // retrieves the browser version
    var browserVersion = BrowserDetect.version;

    // retrieves the browser operative system and converts it to lowercase
    var browserOs = BrowserDetect.os.toLowerCase();

    // retrieves the body
    var _body = jQuery("body");

    // adds the browser classes to the body item
    _body.addClass(browserName);
    _body.addClass(browserName + "-" + browserVersion);
    _body.addClass(browserOs);

    // creates the text field
    jQuery(":text, :password").textfield();

    // creates the text area
    jQuery("textarea").textarea();

    jQuery("#comments-form-area > .button-large").click(function() {
                jQuery(this).hide();
                jQuery("#comments-form-area > form").fadeIn(200);
                jQuery.scrollTo(jQuery("#comments-form-area > form"), 800, {
                            offset : {
                                top : -50,
                                left : 0
                            }
                        });
            });

    jQuery("form").each(function(index, element) {
        jQuery("div#post", element).click(function() {
            jQuery("#window-captcha").window("show");
            jQuery("#window-captcha").bind("valid_captcha",
                    function(event, captcha) {
                        // adds the captcha to the form element as an hidden element
                        jQuery(element).append("<input type=\"hidden\" name=\"captcha\" value=\""
                                + captcha + "\" />");

                        // submits the form (with the captcha value)
                        element.submit();
                    });
            jQuery("#window-captcha input#captcha").val("");
            jQuery("#window-captcha input#captcha").focus();
        });
    });

    jQuery("form").each(function(index, element) {
        jQuery("div#preview", element).click(function() {
            jQuery(element).append("<input type=\"hidden\" name=\"post[_parameters][preview]\" value=\"true\" />")
            element.submit();
        });
    });

    jQuery(".button-openid").click(function() {
                // retrieves the parent form
                var parentForm = jQuery(this).parents("form");

                // shows the openid area
                jQuery("#openid-area", parentForm).fadeIn(300);
            });

    jQuery("#openid-area #login").click(function() {
        // retrieves the parent form
        var parentForm = jQuery(this).parents("form");

        // retrieves the return address element
        var returnAddress = jQuery("input[name=return_address]", parentForm);

        // retrieves the return address value
        var returnAddressValue = returnAddress.val();

        // resolves the signin url
        var signinUrl = jQuery.resolveurl("signin");

        // sets the new value in the return address
        returnAddress.val(returnAddressValue + "#comments-form-area");

        // sets the new action in the parent form
        parentForm.attr("action", signinUrl);

        // submits the form
        parentForm.submit();
    });

    jQuery("#window-captcha").bind("refresh_captcha", function() {
        // retrieves the captcha element
        var captchaElement = jQuery("#window-captcha #captcha");

        // retrieves the timestamp from the date
        // and converts it to string
        var date = new Date();
        var timestamp = date.getTime();
        var timestampString = String(timestamp);

        // retrieves the captcha (original) src value
        var srcValue = captchaElement.attr("data-src")
                ? captchaElement.attr("data-src")
                : captchaElement.attr("src");

        // saves the captcha original src value
        captchaElement.attr("data-src", srcValue);

        // adds the sharp value to the src value, in order
        // to force an image reload
        captchaElement.attr("src", srcValue + "?" + timestampString);
    });

    jQuery("#window-captcha #captcha-refresh").click(function() {
                // triggers the refresh captcha event
                jQuery("#window-captcha").trigger("refresh_captcha");

                // resets the value of the input field associated with
                // the definition of the captcha value and then runs
                // the focus operation in it
                jQuery("#window-captcha input#captcha").val("");
                jQuery("#window-captcha input#captcha").focus();
            });

    jQuery("#window-captcha div#post").click(function() {
        // retrieves the captcha value
        var captchaValue = jQuery("#window-captcha input#captcha").val();

        // resolves the captcha url
        var captchaUrl = jQuery.resolveurl("captcha");

        jQuery.ajax({
                    type : "get",
                    url : captchaUrl,
                    data : {
                        captcha : captchaValue
                    },
                    success : function(data, textStatus) {
                        // retrieves the window captcha
                        var windowCaptcha = jQuery("#window-captcha");

                        // triggers the valid captcha event and hides
                        // captcha window
                        windowCaptcha.trigger("valid_captcha", [captchaValue]);
                        windowCaptcha.window("hide");
                    },
                    error : function() {
                        // retrieves the window captcha and uses it to
                        // trigger the refresh event in it
                        var windowCaptcha = jQuery("#window-captcha");
                        windowCaptcha.trigger("refresh_captcha");

                        // resets the value of the input field associated with
                        // the definition of the captcha value and then runs
                        // the focus operation in it
                        jQuery("#window-captcha input#captcha").attr("value",
                                "");
                        jQuery("#window-captcha input#captcha").focus();
                    }
                });
    });

    // creates the overlay
    jQuery("#overlay").overlay();

    // creates the window container
    jQuery("#window-container").windowcontainer();

    // creates the dropboxes
    jQuery(".dropbox").dropbox();

    // creates the windows
    jQuery(".window").window();

    // creates the date text field
    jQuery(".date-text-field").datetextfield();
});
