var ids2Test = null;
var selectedTests = [];
var testsToExecuteData = [];

function MapTestIdsToTestNames(suites){
  var map = {};
  suites.forEach((suite, i) => {
    suite.Tests.forEach((test, j) => {
      map[test.TestID] = {"TestName": test.TestName,
                       "SuiteShortPath": suite.SuiteShortPath,
                       "NumberOfSteps": test.TestSteps.length,
                       "TestID": test.TestID};
    });
  });
  ids2Test = map;
}

function handleTestCheckboxClick(){
  if (ids2Test == null){
    MapTestIdsToTestNames()
  }
  testsToExecuteData = []
  var testExecuteElements = $('[id^="testExecuteCheckbox"]');
  var testsToExecuteList = document.getElementById("testsToExecuteList");
  var inner = "";
  for (var i = 0; i < testExecuteElements.length; i++) {
    var el = testExecuteElements[i];
    if(el.checked){
      var testID = el.id.replace("testExecuteCheckbox_", "");
      testsToExecuteData.push(ids2Test[testID]);
      var testName = ids2Test[testID]['TestName'];
      inner += "<li>" + testName + "</li>";
    }
  }
  testsToExecuteList.innerHTML = inner;
}


 function handleExecuteButton(){
   var testsDict = {'Tests': testsToExecuteData};
   $.ajax({
     url:"/execute",
     type: 'POST',
     contentType: 'application/json;charset=UTF-8',
     data: JSON.stringify(testsDict),
     success: function(){
        window.location.href = "/execute";
     }
   })
 }
