*** Settings ***
Library  RequestsLibrary


*** Keywords ***
Check Status Code
    [Arguments]  ${response}
    should be equal as strings  ${response.status_code}  200


*** Test Cases ***
Get Planet 3
    [Documentation]  Practice Get
    ${starwars_base_url}=  set variable  https://swapi.dev/api
    create session  get_star_wars  ${starwars_base_url}  verify=True
    ${response} =  get request  get_star_wars  planets/3/
    Check Status Code  ${response}
    sleep  15
    log to console  ${response.json()}
