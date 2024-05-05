*** Settings ***
Documentation    Test that the workspace redirects correctly under certain conditions.
Library    tms_lib.py
Library    SeleniumLibrary



*** Variables ***
${HOST}    127.0.0.1
${PORT}    5000
${DOMAIN}    http://${HOST}:${PORT}
${DB_PATH}    test_database.db

${HOMEPAGE_URL}    ${DOMAIN}/
${HOMEPAGE_TITLE}    Homepage
${WORKSPACE_URL}    ${DOMAIN}/workspace
${WORKSPACE_TITLE}    Worspace



*** Keywords ***
Start Local Test Server
    Start Server    ${HOST}    ${PORT}    ${DB_PATH}

Open Homepage
    Open Browser    ${HOMEPAGE_URL}

Open Workspace
    Open Browser    ${WORKSPACE_URL}

Current Page Is
    [Arguments]    ${COMPARISON_URL}
    ${URL}    Get Location
    Should Be Equal As Strings   ${URL}    ${COMPARISON_URL}

Register User
    [Arguments]    ${USERNAME}    ${PASSWORD}
    Mouse Over    id:account-button
    Click Button    register-button
    Input Text    r-username    ${USERNAME}
    Input Password    r-password    ${PASSWORD}
    Click Button    r-submit

Logout
    Click Button    Account
    Click Button    logout-button
   
Close
    Close Browser    
    Close Server



*** Test Cases ***
Test Workspace Redirects To Homepage When Not Logged In.
    [Documentation]    Test that when navigating to the homepage it changes the page to the homepage unless logged in.
    Start Local Test Server
    Open Workspace
    Current Page Is    ${HOMEPAGE_URL}
    [Teardown]    Close

Test Workspace Doesn't Redirects To Homepage When Logged In
    [Documentation]    Test that when navigating to the homepage it doesn't change the page to the homepage when already logged in.
    Start Local Test Server
    Open Homepage
    Register User    testUser    TestUser_@4@@
    Go To    ${WORKSPACE_URL}
    Current Page Is    ${WORKSPACE_URL}
    [Teardown]    Close

Test Workspace Redirects To Homepage On Logout.
    [Documentation]    Test that when in the workspace and logged in, logging out changes/redirects the page to the homepage
    Start Local Test Server
    Open Homepage
    Register User    testUser    TestUser_@@3
    Go To    ${WORKSPACE_URL}
    Current Page Is    ${WORKSPACE_URL}
    Logout
    Current Page Is    ${HOMEPAGE_URL}
    [Teardown]    Close
