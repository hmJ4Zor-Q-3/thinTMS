*** Settings ***
Documentation    Test that the user menu acts as intended under certain conditions.
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
Test Default Options Are Present
    Start Local Test Server
    Open Homepage
    Mouse Over    id:account-button
    Element Should Be Visible    login-button
    Element Should Be Visible    register-button
    Element Should Not Be Visible    workspace-button
    Element Should Not Be Visible    logout-button
    [Teardown]    Close

Test Register Menu Successful Registration
    Start Local Test Server
    Open Homepage
    Mouse Over    id:account-button
    Click Button    register-button
    Element Should Be Visible    register-menu
    Input Text    r-username    afndok
    Input Password    r-password    Arvi9cewo0_30
    Click Button    r-submit
    Element Should Not Be Visible    register-menu
    [Teardown]    Close

Test Register Menu No Username
    Start Local Test Server
    Open Homepage
    Mouse Over    id:account-button
    Click Button    register-button
    Element Should Be Visible    register-menu
    Input Password    r-password    Arvi9cewo0_30
    Click Button    r-submit
    Element Should Be Visible    register-menu
    [Teardown]    Close

Test Register Menu Long Username
    Start Local Test Server
    Open Homepage
    Mouse Over    id:account-button
    Click Button    register-button
    Element Should Be Visible    register-menu
    Input Text    r-username    123456789_123456789_123456789_1
    Input Password    r-password    Arvi9cewo0_30
    Click Button    r-submit
    Element Should Be Visible    register-menu
    [Teardown]    Close

Test Register Menu No Password
    Start Local Test Server
    Open Homepage
    Mouse Over    id:account-button
    Click Button    register-button
    Element Should Be Visible    register-menu
    Input Text    r-username    username
    Click Button    r-submit
    Element Should Be Visible    register-menu
    [Teardown]    Close

Test Register Menu Short Password
    Start Local Test Server
    Open Homepage
    Mouse Over    id:account-button
    Click Button    register-button
    Element Should Be Visible    register-menu
    Input Text    r-username    username_0
    Input Password    r-password    Aa0_
    Click Button    r-submit
    Element Should Be Visible    register-menu
    [Teardown]    Close

Test Register Menu Weak Password
    Start Local Test Server
    Open Homepage
    Mouse Over    id:account-button
    Click Button    register-button
    Element Should Be Visible    register-menu
    Input Text    r-username    uuuuunem
    Input Password    r-password    arvi9cewo0_30
    Click Button    r-submit
    Element Should Be Visible    register-menu
    [Teardown]    Close

Test That Logged In Options Are Present
    Start Local Test Server
    Open Homepage
    Register User    uName    ,_0Pjbhbhbhb
    Click Button    account-button
    Element Should Not Be Visible    login-button
    Click Button    account-button
    Element Should Not Be Visible    register-button
    Click Button    account-button
    Element Should Be Visible    workspace-button
    Click Button    account-button
    Element Should Be Visible    logout-button
    [Teardown]    Close



Test Logout Button
    Start Local Test Server
    Open Homepage
    Register User    uName    ,_0Pjbhbhbhb
    Click Button    account-button
    Click Button    logout-button
    Click Button    account-button
    Element Should Be Visible    login-button
    Click Button    account-button
    Element Should Be Visible    register-button
    Click Button    account-button
    Element Should Not Be Visible    workspace-button
    Click Button    account-button
    Element Should Not Be Visible    logout-button
    [Teardown]    Close

Test Login Menu Successful Login
    Start Local Test Server
    Open Homepage
    Register User    afndok    Arvi9cewo0_30
    Logout
    Click Button    account-button
    Click Button    login-button
    Element Should Be Visible    login-menu
    Input Text    l-username    username
    Input Password    l-password    Arvi9cewo0_30
    Click Button    l-submit
    Element Should Be Visible    login-menu
    [Teardown]    Close

Test Login Menu No Username
    Start Local Test Server
    Open Homepage
    Click Button    account-button
    Click Button    login-button
    Element Should Be Visible    login-menu
    Input Password    l-password    Arvi9cewo0_30
    Click Button    l-submit
    Element Should Be Visible    login-menu
    [Teardown]    Close

Test Login Menu No Password
    Start Local Test Server
    Open Homepage
    Mouse Over    id:account-button
    Click Button    login-button
    Element Should Be Visible    login-menu
    Input Text    l-username    username
    Click Button    l-submit
    Element Should Be Visible    login-menu
    [Teardown]    Close

Test Login Menu Not Registered
    Start Local Test Server
    Open Homepage
    Click Button    account-button
    Click Button    login-button
    Element Should Be Visible    login-menu
    Input Text    l-username    username
    Input Password    l-password    Arvi9cewo0_30
    Click Button    l-submit
    Element Should Be Visible    login-menu
    [Teardown]    Close



Test The Workspace Button Conditions
    Start Local Test Server
    Open Homepage
    Register User    afndok    Arvi9cewo0_30
    Click Button    account-button
    Click Button    workspace-button
    Current Page Is    ${WORKSPACE_URL}
    Click Button    account-button
    Page Should Not Contain Element    id:workspace-button
    [Teardown]    Close
