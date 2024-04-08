$(document).ready(function(){
  callonce();
  setInterval(readMails,10000);
  
});



function callonce(){    
    $.ajax({
        url: 'http://127.0.0.1:5000/authorize',
        type: 'post',
        dataType: 'json',
        success: function(response) {
                console.log(response);
                  },
        error:  function(response) {
                console.log(response.responseText);
        }
      });                
}


function readMails(){    
  $.ajax({
      url: 'http://127.0.0.1:5000/readMail',
      type: 'post',
      dataType: 'json',
      success: function(response) {
              console.log(response);
                },
      error:  function(response) {
              console.log(response.responseText);
      }
    });                
}

function changeMessage(data){
  $("#message").html( '<center>'+
                      '</center>'+data
                    );             

}
