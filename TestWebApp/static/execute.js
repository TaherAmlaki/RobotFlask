var done = false;

function PeriodicCheckOfExecutionStatus(){
   $.ajax({
        url:"/_execution_python",
        type: 'GET',
        contentType: 'application/json;charset=UTF-8',
        success: function(data){
            console.log(data);
            for(var test_id in data){
                if (!data.hasOwnProperty(test_id)){
                    continue;
                }
                console.log(test_id, data[test_id])
                if(test_id === "execution" && data[test_id] === "done"){
                    done = true;
                }
                var pb_id = "#pb_" + test_id
                $(pb_id).css('width', data[test_id][0] + '%');
                $(pb_id).html(data[test_id][0]+'%');
                if (data[test_id][1] === "FAIL"){
                    $(pb_id).removeClass("bg-success");
                    $(pb_id).addClass("bg-danger");
                }
            }
        },
        complete: function(){
            if (done === false){
                setTimeout(PeriodicCheckOfExecutionStatus, 200);
            }
        }
   });
}

setTimeout(PeriodicCheckOfExecutionStatus, 200);

