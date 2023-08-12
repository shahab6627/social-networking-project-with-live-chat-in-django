function submitForm(){
console.log("fdfd")

    var email = $("#email").val()
    
    var name = $("#name").val()
    var gender =  $("input[name='gender']:checked").val();
    var dob = $("#dob").val()
    var password = $("#password").val()
    var confirm_password = $("#c_password").val()

    const csrf = document.getElementsByName('csrfmiddlewaretoken')
    var csrfmiddlewaretoken = csrf[0].value

    var email_pattern = /^\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$/i
    var name_pattern = /^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$/g
    // validations 
    if(email == ""){
        $('.sp_email').text('email is required'); 
        return
    }
    else if(!email_pattern.test(email)){
        $('.sp_email').text(''); 
        $('.sp_email').text('please enter valid email'); 
        return
    }
    else if(name == ""){
        $('.sp_name').text('Name is required'); 
        return
    }
    else if(!name_pattern.test(name)){
        $('.sp_name').text(''); 
        $('.sp_name').text('name is invalid'); 
        return
    }
    else if (dob == "") {
        
        $('.sp_dob').text('date is required'); 
        return
    }
    else if(password == ""){
        $('.sp_pass').text('password is required'); 
        return

    }
    else if(confirm_password == ""){
        $('.sp_cpass').text('confirm password is required'); 
        return;
    }
     else if(password != confirm_password){
        $('.sp_cpass').text('check your confirm password'); 
        return;

     }
    


    $.ajax({
        url : '',
        method : 'POST',
        data : {
            'csrfmiddlewaretoken': csrfmiddlewaretoken,
            'email' : email,
            'name' : name,
            'gender':gender,
            'date' : dob,
            'password':password

        },

        success : function(res){
            if(res.msg == "usr exists"){
                $('.sp_email').text('')
                $('.sp_email').text('this email already exists... ')
            }
            else{
                $('.user-created').html(`<span> account created successfully! a verification mail is send to  ${email}</span>`)

                $('#user_reg_form')[0].reset()
            }
        },
        error : function(err){
            console.log(err)
        }
        
    })

}

function userLogin(){
    var email = $('#email').val()
    console.log(email)
    var password = $('#password').val()
    const csrf = document.getElementsByName('csrfmiddlewaretoken')

    var csrfmiddlewaretoken = csrf[0].value

    var email_pattern = /^\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$/i

    if(email == ""){
        $('.sp_email').text('')
        $('.sp_email').text('email is required')
        return
    }
    else if(!email_pattern.test(email)){
        $('.sp_email').text('')
        $('.sp_email').text('enter a valid email')
        return
    }
    else if(password==""){
        $('.sp_password').text('password required')
        return

    }
    else{


        $.ajax({
            url : 'login',
            method: 'POST',
            data : {
                'csrfmiddlewaretoken':csrfmiddlewaretoken,
                'email':email,
                'password':password
            },

            success: function(res){
                console.log(res)
                if(res.msg == 'true'){
                    window.open("/profile");
                }
            }
        })
    }


}
