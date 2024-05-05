let maxUsernameLength;
let passwordMinLength;

const AUTH_STORAGE_KEY = "thinTMS_cs_token";
const USER_STORAGE_KEY = "thinTMS_cs_user";

const LOGOUT_EVENT_NAME = "logout";

$(document).ready(() => {
    // collect necessary variables
    let hpr = $("#var_homepage_route").html();
    let wpr = $("#var_workspace_route").html();

    maxUsernameLength = $("#var_max_username_length").html();
    passwordMinLength = $("#password_min_length").html();



    // add toolbar conditional links and other interactions
    if((window.location.pathname) != hpr)
        $("#logo").attr("class", "pointer").click(() => window.location.href = hpr);
    
    
    if((window.location.pathname) == wpr)
        $("#workspace-button").remove();
    else
        $("#workspace-button").click(() => window.location.href = wpr);
    
    
    $("#logout-button").click(logout);
    $("#login-button").click(() => $("#login-menu").toggle());
    $("#register-button").click(() => $("#register-menu").toggle());

    

    // setup login form.
    $("#l-close-btn").click(() => $("#login-menu").toggle());
    $("#l-username").keyup(() => validateUsername($("#l-username"), $("#l-username-errors")));
    $("#l-password").keyup(() => validatePassword($("#l-password"), $("#l-password-errors")));
    $("#l-submit").click(tryLogin);

    // setup register form.
    $("#r-close-btn").click(() => $("#register-menu").toggle());
    $("#r-username").keyup(() => validateNewUsername($("#r-username"), $("#r-username-errors")));
    $("#r-password").keyup(() => validateNewPassword($("#r-password"), $("#r-password-errors")));
    $("#r-submit").click(tryRegister);

    // flip uam if session already exists.
    if(hasSession()){
        adjustUserAccessMenu(true);
    }
});



function logout()
{
    session = getSession();
    $.get(`${"/api/logout"}?username=${encodeURIComponent(session.username)}&token=${encodeURIComponent(session.token)}`).always(handleLogoutResponse);
}

function handleLogoutResponse(response){
    if(response.status != undefined)
        alert(`Unexpected error occured, https status code: ${response.status}, message: ${response.responseText}`);
    
    adjustUserAccessMenu(false);
    clearSession();
} // end handleLogoutResponse()


function tryLogin()
{
    if(validateUsername($("#l-username"), $("#l-username-errors")) 
    & validatePassword($("#l-password"), $("#l-password-errors")))
        $.get(`${"/api/auth"}?username=${encodeURIComponent($("#l-username").val())}&password=${encodeURIComponent($("#l-password").val())}`)
        .always((x) => $("#l-errors").html(handleUserEntryResponse(x, $("#l-username").val(), $("#login-menu"))));
} // end tryLogin()

function tryRegister()
{
    if(validateNewUsername($("#r-username"), $("#r-username-errors")) 
    & validateNewPassword($("#r-password"), $("#r-password-errors")))
       $.get(`${"/api/register"}?username=${encodeURIComponent($("#r-username").val())}&password=${encodeURIComponent($("#r-password").val())}`)
       .always((x) => $("#r-errors").html(handleUserEntryResponse(x, $("#r-username").val(), $("#register-menu"))));
} // end tryRegister()

function handleUserEntryResponse(response, username, menu){
    if(response.status != undefined)
        return response.responseText;

    adjustUserAccessMenu(true);
    menu.toggle();
    setSession(username, response.token.slice(2, -1));
    return "";
} // end handleRegisterResponse()



// TODO, not remotely secure, should be rewrote.
function setSession(username, token){
    window.localStorage.setItem(AUTH_STORAGE_KEY, token);
    window.localStorage.setItem(USER_STORAGE_KEY, username);
} // end setSession()

function getSession(){
    return {
            username: window.localStorage.getItem(USER_STORAGE_KEY),
            token: window.localStorage.getItem(AUTH_STORAGE_KEY) 
           };
} // end getSession()

function clearSession(){
    window.localStorage.removeItem(AUTH_STORAGE_KEY);
    window.localStorage.removeItem(USER_STORAGE_KEY);
    document.dispatchEvent(new Event(LOGOUT_EVENT_NAME)); // raise event here, server logout doesn't occur here, but forgetting credentials is more significant to the frontend.
} // end clearSession()

function hasSession(){
    return window.localStorage.getItem(USER_STORAGE_KEY) != null 
    && window.localStorage.getItem(AUTH_STORAGE_KEY) != null;
} // end hasSession()



let userloggedIn = false; // this should never be changed outside adjustUserAccessMenu. Could fiddle around with closures and make it part of the function outside of the global scope
function adjustUserAccessMenu(loggedIn)
{
    if(userloggedIn ^ loggedIn)
    {
        $("#logged-in-uam-buttons").toggle();
        $("#default-uam-buttons").toggle();
        userloggedIn = loggedIn;
    }
} // end adjustUserAccessMenu()





function validateUsername(inputField, outputField) 
{
    let exists = inputField.val() != "";
    let valid = exists;
    
    let message = "";
    if(!exists)
        message += "Username can not be empty.";

    outputField.html(message);
    !valid ? inputField.addClass("invalid-form-field") : inputField.removeClass("invalid-form-field");

    return valid;
}

function validatePassword(inputField, outputField)
{
    let exists = inputField.val() != "";
    let valid = exists;
    
    let message = "";
    if(!exists)
        message += "Password can not be empty.";

    outputField.html(message);
    !valid ? inputField.addClass("invalid-form-field") : inputField.removeClass("invalid-form-field");

    return valid;
}



function validateNewUsername(inputField, outputField) 
{
    let exists = inputField.val() != "";
    let validLength = inputField.val().length <= maxUsernameLength;
    let valid = exists && validLength;
    
    let message = "";
    if(!exists)
        message += "Username can not be empty.";
    
    if(!validLength)
        message += (message ? "\n<br>" : "") + `Username must at most ${maxUsernameLength} characters long.`;

    outputField.html(message);
    !valid ? inputField.addClass("invalid-form-field") : inputField.removeClass("invalid-form-field");

    return valid;
}

function validateNewPassword(inputField, outputField) 
{
    let hasAllCharacters = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^\da-zA-Z])/.test(inputField.val()); // use positive lookahead to check if after any number of any character there is at least one character from a group, for each group.
    let validLength = inputField.val().length >= passwordMinLength;
    let valid = hasAllCharacters && validLength;

    let message = "";
    if(!hasAllCharacters)
        message += "Password must contain at least one of each set: lowercase, uppercase, number, symbol.";
    
    if(!validLength)
        message += (message ? "\n<br>" : "") + `Password must at least ${passwordMinLength} characters long.`;

    outputField.html(message);
    !valid ? inputField.addClass("invalid-form-field") : inputField.removeClass("invalid-form-field");

    return valid;
}
