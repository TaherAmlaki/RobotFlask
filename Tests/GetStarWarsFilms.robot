*** Settings ***
Library  RequestsLibrary


*** Test Cases ***
Get Film 1
    [Documentation]  Practice Get
    create session  get_star_wars  https://swapi.dev/api  verify=True
    ${response} =  get request  get_star_wars  films/1/
    should be equal as strings  ${response.status_code}  200
    Log  ${response.json()}


Get Film 2
    [Documentation]  Practice Get
    create session  get_star_wars  https://swapi.dev/api  verify=True
    ${response} =  get request  get_star_wars  films/2/
    should be equal as strings  ${response.status_code}  200
    Log  ${response.json()}
