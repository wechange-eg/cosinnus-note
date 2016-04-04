$(function() {
    
    $.cosinnus.FACEBOOK_INTEGRATION_PERMISSIONS = 'publish_actions';
    $.cosinnus.FACEBOOK_INTEGRATION_APP_ID = '463936933800913';
    
    
 // This is called with the results from from FB.getLoginStatus().
    function statusChangeCallback(response) {
      console.log('statusChangeCallback');
      console.log(response);
      // The response object is returned with a status field that lets the
      // app know the current login status of the person.
      // Full docs on the response object can be found in the documentation
      // for FB.getLoginStatus().
      if (response.status === 'connected') {
        // Logged into your app and Facebook.
        testAPI();
      } else if (response.status === 'not_authorized') {
        // The person is logged into Facebook, but not your app.
        console.log('The person is logged into Facebook, but not your app')
      } else {
        // The person is not logged into Facebook, so we're not sure if
        // they are logged into this app or not.
        console.log('The person is not logged into Facebook')
      }
    }

    // This function is called when someone finishes with the Login
    // Button.  See the onlogin handler attached to it in the sample
    // code below.
    function checkLoginState() {
      FB.getLoginStatus(function(response) {
        statusChangeCallback(response);
      });
    }
    
    
    $.cosinnus.loadFacebookIntegration = function() {
        window.fbAsyncInit = function() {
            FB.init({
              appId      : $.cosinnus.FACEBOOK_INTEGRATION_APP_ID,
              cookie     : true,  // enable cookies to allow the server to access 
                                  // the session
              xfbml      : false,  // parse social plugins on this page
              version    : 'v2.5' // use graph api version 2.5
            });

            // Now that we've initialized the JavaScript SDK, we call 
            // FB.getLoginStatus().  This function gets the state of the
            // person visiting this page and can return one of three states to
            // the callback you provide.  They can be:
            //
            // 1. Logged into your app ('connected')
            // 2. Logged into Facebook, but not your app ('not_authorized')
            // 3. Not logged into Facebook and can't tell if they are logged into
            //    your app or not.
            //
            // These three cases are handled in the callback function.

            FB.getLoginStatus(function(response) {
              statusChangeCallback(response);
            });

        };
        
        (function(d, s, id) {
            var js, fjs = d.getElementsByTagName(s)[0];
            if (d.getElementById(id)) return;
            js = d.createElement(s); js.id = id;
            js.src = "//connect.facebook.net/en_US/sdk.js";
            fjs.parentNode.insertBefore(js, fjs);
          }(document, 'script', 'facebook-jssdk'));
        
        $.cosinnus.facebookIntegrationLoaded = true;
    };
    
    $.cosinnus.doFacebookLogin = function() {
        if (typeof FB.login === 'undefined') {
            alert('It seems you have installed an Addon that is blocking you from accessing the Facebook login. Please disable addons such as Ghostery to continue!');
        } else {
            FB.login(function(response) {
                statusChangeCallback(response);
                
            }, {scope: $.cosinnus.FACEBOOK_INTEGRATION_PERMISSIONS});
        }
    }
    
    $('#loadFacebookIntegrationButton').click(function(){
        $.cosinnus.loadFacebookIntegration();
        $(this).hide();
        $('#loginFacebookIntegrationButton').show();
    });
    
    $('#loginFacebookIntegrationButton').click(function(){
        $.cosinnus.doFacebookLogin();
    });
});

