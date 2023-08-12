function sendInvitation(){

   var invit_btn = document.getElementById('invitation-btn')

   var send_to = invit_btn.getAttribute('send-to-id')
   var send_from = invit_btn.getAttribute('send-from')


$.ajax({

    url : '/send-invitation',
    method : 'GET',
    data : {
        'send_to':send_to,
        'send_from':send_from
    },

    success : function(resp){
        if(resp.msg == "true"){
            invit_btn.innerHTML = "request send"
            invit_btn.disabled = true
        }
    }
})
   
}