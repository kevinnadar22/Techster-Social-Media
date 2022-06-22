var likeIcon = document.querySelectorAll('.like'),
likeIconArray = Array.from( likeIcon );

likeIconArray.forEach(function(likeIcons) {
    likeIcons.addEventListener('click', likeIconFunc);
  });


  
function likeIconFunc(){

    id = this.id
    like_id = `like#${id}`
    $.ajax({
        type:'GET',
        url:'/like-post/',
        data:{
          id:id,
        },
        success: function(data){
          document.getElementById(like_id).innerText = data['message'];

            if (data['status'] == 'liked'){
              document.getElementById(`regular#${id}`).classList.remove('fa-regular');
              document.getElementById(`regular#${id}`).classList.add('fa-solid');
              document.getElementById(`regular#${id}`).id = `solid#${id}`
            }
            else if (data['status'] == 'disliked'){
              document.getElementById(`solid#${id}`).classList.add('fa-regular');
              document.getElementById(`solid#${id}`).classList.remove('fa-solid');
              document.getElementById(`solid#${id}`).id = `regular#${id}`
                
            }
    
        }
      });
}


var commentIcon = document.querySelectorAll('.comment'),
commentIconArray = Array.from( commentIcon );

commentIconArray.forEach(function(commentIcons) {
  commentIcons.addEventListener('click', commentIconFunc);
  });


  
function commentIconFunc(){
    console.log(this.id)
    let comment_id = this.id.replace('comment#', '');
    let comment_like = `commentlike#${comment_id}`
    $.ajax({
        type:'GET',
        url:'/like-comment/',
        data:{
          id:comment_id,
        },
        success: function(data){
          document.getElementById(comment_like).innerText = data['message'];
 
        }
      });
}

