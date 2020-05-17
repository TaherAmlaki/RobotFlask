*** Settings ***
Library  RequestsLibrary


*** Test Cases ***
Get Planet 3
    [Documentation]  Practice Get
    create session  get_star_wars  https://swapi.dev/api  verify=True
    ${response} =  get request  get_star_wars  planets/3/
    should be equal as strings  ${response.status_code}  200
    Log  ${response.json()}
