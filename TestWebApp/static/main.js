var ids2Test = null;
var ids2Suite = null;

var testsToExecuteData = [];
var testsToExecuteListElement = document.getElementById("testsToExecuteList");
var testCheckboxes = $('[id^="testExecuteCheckbox"]');
var suiteCheckboxes = $('[id^="suiteExecuteCheckbox"]');

function MapTestIdsToTestNames(suites) {
  let testsMap = {};
  let suitesMap = {}
  suites.forEach((suite, i) => {
    suitesMap[suite.SuiteID] = {
      "SuiteName": suite.SuiteName,
      "SuiteShortPath": suite.SuiteShortPath,
      "Tests": suite.Tests
    };
    suite.Tests.forEach((test, j) => {
      testsMap[test.TestID] = {
        "TestName": test.TestName,
        "SuiteID": suite.SuiteID,
        "SuiteShortPath": suite.SuiteShortPath,
        "NumberOfSteps": test.TestSteps.length,
        "TestID": test.TestID
      };
    });
  });
  ids2Test = testsMap;
  ids2Suite = suitesMap;
}


for (let i = 0; i < testCheckboxes.length; i++) {
  let el = testCheckboxes[i];
  let testID = el.id.replace("testExecuteCheckbox_", "");
  el.addEventListener('change', function() {
    if (this.checked) {
      updateTestsToExecute({
        "type": "test",
        "action": "add",
        "id": testID
      });
    } else {
      updateTestsToExecute({
        "type": "test",
        "action": "remove",
        "id": testID
      });
    }
  });
}

for (let i = 0; i < suiteCheckboxes.length; i++) {
  let el = suiteCheckboxes[i];
  let suiteID = el.id.replace("suiteExecuteCheckbox_", "");
  el.addEventListener('change', function() {
    if (this.checked) {
      updateTestsToExecute({
        "type": "suite",
        "action": "add",
        "id": suiteID
      });
    } else {
      updateTestsToExecute({
        "type": "suite",
        "action": "remove",
        "id": suiteID
      });
    }
  });
}

function checkChangedSuite(data){
  if (data['type'] == 'suite') {
    let s = ids2Suite[data['id']];
    let checkValue = false;
    if (data['action'] == 'add') {
      checkValue = true;
    }
    for (let i = 0; i < s['Tests'].length; i++) {
      let id = "testExecuteCheckbox_" + s['Tests'][i]['TestID'];
      document.getElementById(id).checked = checkValue;
    }
  } else if (data['type'] == 'test') {
    let id = ids2Test[data['id']]['SuiteID'];
    let s = ids2Suite[id];
    let checked = [];
    let unchecked = [];
    for (let i = 0; i < s['Tests'].length; i++) {
      let tID = s['Tests'][i]['TestID'];
      if (document.getElementById("testExecuteCheckbox_" + tID).checked) {
        checked.push(1);
      } else {
        unchecked.push(1);
      }
    }
    let el = document.getElementById("suiteExecuteCheckbox_" + id);
    if (checked.length + unchecked.length == 1){
      if (data['action'] == 'add') {
        el.checked = true;
      } else {
        el.checked = false;
      }
    } else if (checked.length * unchecked.length == 0){
      el.checked = true;
    } else {
      el.checked = false;
    }
  }
}


function updateTestsToExecute(data) {
  let inner = "";
  testsToExecuteData = [];
  checkChangedSuite(data);

  for (let id in ids2Suite) {
    let s = ids2Suite[id];
    let el = document.getElementById("suiteExecuteCheckbox_" + id);
    if (el.checked) {
      testsToExecuteData.push({
        "type": "suite",
        "data": s
      });
      let suiteName = s['SuiteName'];
      inner += "<li>Suite: " + suiteName + "</li>"
    } else {
      for (let i = 0; i < s['Tests'].length; i++) {
        let tID = s['Tests'][i]['TestID'];
        if (document.getElementById("testExecuteCheckbox_" + tID).checked) {
          testsToExecuteData.push({
            'type': 'test',
            'data': ids2Test[tID]
          });
          let testName = ids2Test[tID]['TestName'];
          inner += "<li>Test: " + testName + "</li>"
        }
      }
    }
  }
  testsToExecuteList.innerHTML = inner;
}


function handleExecuteButton() {
  let executionCheckbox = document.getElementById("executeParallel");
  let logCheckbox = document.getElementById("logHtml");
  var testsDict = {
    'tests': testsToExecuteData,
    'parallel': executionCheckbox.checked,
    'log': logCheckbox.checked
  };
  $.ajax({
    url: $SCRIPT_ROOT + "/_execution_start",
    type: 'POST',
    contentType: 'application/json;charset=UTF-8',
    data: JSON.stringify(testsDict),
    success: function(response) {
      if (response.redirect) {
        window.location.href = $SCRIPT_ROOT + response.redirect;
      }
    }
  });
}

window.onload = function(){
  for(let i=0; i<suiteCheckboxes.length; i++){
    suiteCheckboxes[i].checked = false;
  }
  for(let i=0; i<testCheckboxes.length; i++){
    testCheckboxes[i].checked = false;
  }
}
