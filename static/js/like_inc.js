 

    const like_btn = [...document.getElementsByClassName('like-btn')]
    like_btn.forEach(like_btn=>like_btn.addEventListener('click', ()=>{
    var post_id = like_btn.getAttribute('postId')
    var button_id = like_btn.getAttribute('id')
    console.log(post_id);
    
    $.ajax({
        url : `post-like`,
        method : 'GET',
        data :{
            'post_id':post_id,
        },

        success : function(resp){
            if(resp.msg == "true"){
            document.getElementById(`${button_id}`).disabled = true;
            var lk = parseInt(document.getElementById(`like-${post_id}`).innerText)+1
            document.getElementById(`like-${post_id}`).innerHTML = lk
        }
            else{
                alert("post already like by you")
            }
           
        
        }
    })

    }))




