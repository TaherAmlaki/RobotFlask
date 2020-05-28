var done = false;
var result = null;

function PeriodicCheckOfExecutionStatus(){
   $.ajax({
        url: $SCRIPT_ROOT + "/_execution_status",
        type: 'GET',
        success: function(data){
          let tests = data['tests'];
          let executionStatus = data['execution'];
          if(executionStatus === "done"){
              done = true;
              result = data;
          }

          for(var test in tests){
              if (!tests.hasOwnProperty(test)){
                  continue;
              }
              var pb_id = "#pb_" + test;
              $(pb_id).css('width', tests[test][0] + '%');
              $(pb_id).html(tests[test][0]+'% (' + tests[test][1] + ")");
              if (tests[test][1] === "FAIL"){
                  $(pb_id).removeClass("bg-success");
                  $(pb_id).addClass("bg-danger");
              }
          }
        },
        complete: function(){
            if (done === false){
                setTimeout(PeriodicCheckOfExecutionStatus, 2000);
            } else {
              console.log(result);
              if (result != null && result.hasOwnProperty("execution")){
                let allPassed = true;
                let numberOfPassed = 0;
                let numberOfFailed = 0;
                let tests = result['tests']
                for(let test in tests){
                  console.log("test ==> ", test);
                  if (tests[test][1] == "PASS") {
                    numberOfPassed++;
                  } else {
                    numberOfFailed++;
                    allPassed = false;
                  }
                }
                if (allPassed == true) {
                  $("#resultMsgText").html(numberOfPassed + " tests are executed and all passed");
                } else {
                  let msg = numberOfPassed + " tests are passed and " + numberOfFailed + " tests failed."
                  $("#resultMsg").removeClass("alert-success");
                  $("#resultMsg").addClass("alert-warning");
                  $("#resultMsgText").html(msg);
                }

                if (result.hasOwnProperty("logs") && result['logs'] != null && 0 < result['logs'].length){
                  let ul = $("#logsUL");
                  for(let i=0; i< result['logs'].length; i++){
                    let li = '<li><a href="/view-report/'+ result['logs'][i] + '#">'+ result['logs'][i] + '</a></li>';
                    ul.append(li);
                  }
                } else {
                  $("#resultHtmlLogP").remove();
                  $("#logsUL").remove();
                }
                $("#resultMsg").show('fade');
              }
            }
        }
   });
}

setTimeout(PeriodicCheckOfExecutionStatus, 200);
