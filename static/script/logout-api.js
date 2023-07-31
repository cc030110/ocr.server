$('#login-menu').show();

function logout(){
  $.ajax({
      "url": `/api/v1/users/logout`,
      "method" : "POST",
      "timeout": 0,
      "headers":{
          "Content-Type": "application/json",
          'X-CSRFToken': csrftoken
      }
  }).done(function (response){
      if(response.logout==='success'){
          alert("로그아웃 되었습니다.")
          location.href = '/';
      }else{
          location.href = '/login';
      }
  }).fail(function (error) {
      console.log("error : ", error);
  })
}

