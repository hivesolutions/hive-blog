// Hive Solutions Blog
// Copyright (c) 2008-2020 Hive Solutions Lda.
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
// __copyright__ = Copyright (c) 2008-2020 Hive Solutions Lda.
// __license__   = Hive Solutions Confidential Usage License (HSCUL)

(function(jQuery) {
    jQuery.fn.textfield = function(method, options) {
        // the default values for the menu
        var defaults = {};

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = jQuery.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        /**
         * Initializer of the plugin, runs the necessary functions to initialize
         * the structures.
         */
        var initialize = function() {
            _appendHtml();
            _registerHandlers();
        };

        /**
         * Creates the necessary html for the component.
         */
        var _appendHtml = function() {
            // iterates over all the items in the matched object
            matchedObject.each(function(index, element) {
                // retrieves the element reference
                var elementReference = jQuery(element);

                // retrieves the current status
                var currentStatus = elementReference.attr("data-current_status");

                // retrieves the current error
                var currentError = elementReference.attr("data-error");

                // retrieves the original value
                var originalValue = elementReference.attr("data-original_value");

                // in case there is an error
                if (currentError) {
                    // adds the invalid mode class
                    elementReference.addClass("invalid");
                } else if (currentStatus !== "") {
                    elementReference.val(currentStatus);
                }

                // retrieves the current value
                var currentValue = elementReference.val();

                // in case the current value is the original one
                if (currentValue === originalValue) {
                    // adds the lower (background) mode class
                    elementReference.addClass("lower");
                }
            });
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            // registers for the focus event
            matchedObject.focus(function(event) {
                // retrieves the element
                var element = jQuery(this);

                // retrieves the current value
                var currentValue = element.val();

                // retrieves the original value
                var originalValue = element.attr("data-original_value");

                // retrieves the current error
                var currentError = element.attr("data-error");

                // retrieves the current status
                var currentStatus = element.attr("data-current_status");

                // in case the current value is
                // the original one
                if (currentValue === originalValue) {
                    // sets the value attribute to empty
                    element.val("");

                    // removes the lower class
                    element.removeClass("lower");

                    // in case there is an error
                    if (currentError !== "") {
                        // removes the invalid mode class
                        element.removeClass("invalid");
                    }
                }

                // adds the active class
                element.addClass("active");
            });

            // registers for the blur event
            matchedObject.blur(function(event) {
                // retrieves the element
                var element = jQuery(this);

                // retrieves the current value
                var currentValue = element.val();

                // retrieves the original value
                var originalValue = element.attr("data-original_value");

                // retrieves the current error
                var currentError = element.attr("data-error");

                // retrieves the current status
                var currentStatus = element.attr("data-current_status");

                // in case the current value is empty
                if (currentValue === "") {
                    // sets the value attribute to the original value
                    element.val(originalValue);

                    // adds the lower class
                    element.addClass("lower");

                    // in case there is an error
                    if (currentError !== "") {
                        // adds the invalid mode class
                        element.addClass("invalid");
                    }
                }

                // removes the active class
                element.removeClass("active");
            });
        };

        // initializes the plugin
        initialize();

        // returns the object
        return this;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.textarea = function(method, options) {
        // the default values for the menu
        var defaults = {};

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = jQuery.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        /**
         * Initializer of the plugin, runs the necessary functions to initialize
         * the structures.
         */
        var initialize = function() {
            _appendHtml();
            _registerHandlers();
        };

        /**
         * Creates the necessary html for the component.
         */
        var _appendHtml = function() {
            // iterates over all the items in the matched object
            matchedObject.each(function(index, element) {
                // retrieves the element reference
                var elementReference = jQuery(element);

                // retrieves the current status
                var currentStatus = elementReference.attr("data-current_status");

                // retrieves the current error
                var currentError = elementReference.attr("data-error");

                // retrieves the original value
                var originalValue = elementReference.attr("data-original_value");

                // in case there is an error
                if (currentError !== "") {
                    // adds the invalid mode class
                    elementReference.addClass("invalid");
                } else if (currentStatus !== "") {
                    // in case the browser is webkit based the text area
                    // requires some time before it is changed
                    // otherwise the browser might crash
                    if (jQuery.browser.safari) {
                        // sets the timeout function to change the
                        // text area value
                        setTimeout(function() {
                            elementReference.get(0).value = currentStatus;
                            elementReference.removeClass("lower");
                        }, 10);
                    } else {
                        // sets the text area value
                        elementReference.get(0).value = currentStatus;
                    }
                }

                // retrieves the current value
                var currentValue = elementReference.get(0).value;

                // in case the current value is the original one
                if (currentValue === originalValue) {
                    // adds the lower (background) mode class
                    elementReference.addClass("lower");
                }
            });

        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            // registers for the focus event
            matchedObject.focus(function(event) {
                // retrieves the element
                var element = jQuery(this);

                // retrieves the current value
                var currentValue = element.get(0).value;

                // retrieves the original value
                var originalValue = element.attr("data-original_value");

                // retrieves the current error
                var currentError = element.attr("data-error");

                // retrieves the current status
                var currentStatus = element.attr("data-current_status");

                // in case the current value is
                // the original one
                if (currentValue === originalValue) {
                    // sets teh value reference value as empty
                    element.get(0).value = "";

                    // removes the lower class
                    element.removeClass("lower");

                    // in case there is an error
                    if (currentError !== "") {
                        // removes the invalid mode class
                        element.removeClass("invalid");
                    }
                }

                // adds the active class
                element.addClass("active");
            });

            // registers for the blur event
            matchedObject.blur(function(event) {
                // retrieves the element
                var element = jQuery(this);

                // retrieves the current value
                var currentValue = element.get(0).value;

                // retrieves the original value
                var originalValue = element.attr("data-original_value");

                // retrieves the current error
                var currentError = element.attr("data-error");

                // retrieves the current status
                var currentStatus = element.attr("data-current_status");

                // in case the current value is empty
                if (currentValue === "") {
                    // sets teh value reference value as the original value
                    element.get(0).value = originalValue;

                    // adds the lower class
                    element.addClass("lower");

                    // in case there is an error
                    if (currentError !== "") {
                        // adds the invalid mode class
                        element.addClass("invalid");
                    }
                }

                // removes the active class
                element.removeClass("active");
            });
        };

        // initializes the plugin
        initialize();

        // returns the object
        return this;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.window = function(method, options) {
        // the default values for the menu
        var defaults = {};

        // sets the default method value
        var method = method ? method : "default";

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = jQuery.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        /**
         * Initializer of the plugin, runs the necessary functions to initialize
         * the structures.
         */
        var initialize = function() {
            _appendHtml();
            _registerHandlers();
        };

        /**
         * Creates the necessary html for the component.
         */
        var _appendHtml = function() {
            jQuery(".window-container").append(matchedObject);
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            jQuery(".close-button", matchedObject).click(function() {
                _hide(matchedObject, options);
            });
        };

        var _toggle = function(matchedObject, options) {
            // in case the matched object is not visible
            if (matchedObject.is(":visible")) {
                // hides the overlay
                _hide(matchedObject, options);
            } else {
                // shows the overlay
                _show(matchedObject, options);
            }
        };

        var _show = function(matchedObject, options) {
            jQuery(".overlay").overlay("show");
            jQuery(".window-container").show();
            matchedObject.show();

            // scrolls the contents to the matched object
            jQuery.scrollTo(matchedObject, 800, {
                offset: {
                    top: -50,
                    left: 0
                }
            });
        };

        var _hide = function(matchedObject, options) {
            jQuery(".overlay").overlay("hide");
            jQuery(".window-container").hide()
            matchedObject.show();
        };

        // switches over the method
        switch (method) {
            case "toggle":
                _toggle(matchedObject, options);
                break;

            case "show":
                _show(matchedObject, options);
                break;

            case "hide":
                _hide(matchedObject, options);
                break;

            case "default":
                // initializes the plugin
                initialize();
                break;
        }

        // returns the object
        return this;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.windowcontainer = function(method, options) {
        // the default values for the menu
        var defaults = {};

        // sets the default method value
        var method = method ? method : "default";

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = jQuery.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        /**
         * Initializer of the plugin, runs the necessary functions to initialize
         * the structures.
         */
        var initialize = function() {
            _appendHtml();
            _registerHandlers();
        };

        /**
         * Creates the necessary html for the component.
         */
        var _appendHtml = function() {
            // adds the window container class to the matched object
            matchedObject.addClass("window-container");
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {};

        // initializes the plugin
        initialize();

        // returns the object
        return this;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.dropbox = function(method, options) {
        // the default values for the menu
        var defaults = {};

        // sets the default method value
        var method = method ? method : "default";

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = jQuery.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        /**
         * Initializer of the plugin, runs the necessary functions to initialize
         * the structures.
         */
        var initialize = function() {
            _appendHtml();
            _registerHandlers();
        };

        /**
         * Creates the necessary html for the component.
         */
        var _appendHtml = function() {};

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            // retrieves the button object
            var buttonObject = jQuery(".dropbox-button", matchedObject);

            buttonObject.click(function(event) {
                // toggles the box
                _toggleBox(matchedObject, options);
            });
        };

        var _toggleBox = function(matchedObject, options) {
            // retrieves the options object
            var optionsObject = jQuery(".dropbox-options", matchedObject);

            // in case the options object is not visible
            if (optionsObject.is(":visible")) {
                // hides the box
                _hideBox(matchedObject, options);
            } else {
                // shows the box
                _showBox(matchedObject, options);
            }
        };

        var _showBox = function(matchedObject, options) {
            // retrieves the options object
            var optionsObject = jQuery(".dropbox-options", matchedObject);

            // shows the options object
            optionsObject.show();
        };

        var _hideBox = function(matchedObject, options) {
            // retrieves the options object
            var optionsObject = jQuery(".dropbox-options", matchedObject);

            // hides the options object
            optionsObject.hide();
        };

        // switches over the method
        switch (method) {
            case "toggle":
                _toggleBox(matchedObject, options);
                break;

            case "show":
                _showBox(matchedObject, options);
                break;

            case "hide":
                _hideBox(matchedObject, options);
                break;

            case "default":
                // initializes the plugin
                initialize();
                break;
        }

        // returns the object
        return this;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.datetextfield = function(method, options) {
        // the default values for the menu
        var defaults = {};

        // sets the default method value
        var method = method ? method : "default";

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = jQuery.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        /**
         * Initializer of the plugin, runs the necessary functions to initialize
         * the structures.
         */
        var initialize = function() {
            _appendHtml();
            _registerHandlers();
        };

        /**
         * Creates the necessary html for the component.
         */
        var _appendHtml = function() {
            // for each of the matched objects
            matchedObject.each(function(index, element) {
                var textFieldElement = jQuery(this);

                // retrieves the matched object's name attribute
                var elementName = textFieldElement.attr("name");

                // creates the markup for the date field container
                var dateFieldContainerHtml = "<div class=\"date-text-field-container\"></div>";

                // creates the inner hidden field
                var innerFieldHtml = "<input type=\"hidden\" name=\"" + elementName + "\"/>";

                // creates the date text field container
                // by wrapping the text field element
                textFieldElement.wrap(dateFieldContainerHtml);

                // retrieves the container
                var dateTextFieldContainer = textFieldElement.parent();

                // appends the inner field to the container
                dateTextFieldContainer.append(innerFieldHtml);

                // removes the matched object's name attribute
                textFieldElement.removeAttr("name");

                // updates the timestamp
                __updateTimestampField(textFieldElement, options);
            });
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            // when the matched object changes
            matchedObject.keyup(function(eventObject) {
                // retrieves the text field element
                var textFieldElement = jQuery(this);

                // updates the timestamp field
                __updateTimestampField(textFieldElement, options);
            });
        };

        var __updateTimestampField = function(matchedObject, options) {
            // retrieves the container
            var dateTextFieldContainer = matchedObject.parent();

            // retrieves the inner field
            var innerFieldElement = jQuery(":hidden", dateTextFieldContainer);

            // retrieves the current value in the text field
            var textFieldValue = matchedObject.val();

            // converts the date value to an utc timestamp
            var timestampMiliseconds = Date.parseUtc(textFieldValue);

            // converts the utc timestamp to seconds
            var timestamp = isNaN(timestampMiliseconds) ? null : timestampMiliseconds / 1000;

            // in case no parse was possible
            if (timestamp === null || timestamp === undefined) {
                // adds the invalid class to the text field
                matchedObject.addClass("invalid");
            } else {
                // otherwise removes eventual invalid class
                matchedObject.removeClass("invalid");
            }

            // sets the timestamp in the inner date field
            innerFieldElement.val(timestamp);
        };

        // initializes the plugin
        initialize();

        // returns the object
        return this;
    };
})(jQuery);
