function like() {
  var likeIcon = document.querySelectorAll('.like'),
    likeIconArray = Array.from(likeIcon);

  likeIconArray.forEach(function (likeIcons) {
    likeIcons.addEventListener('click', likeIconFunc);
  });

}

// Comments 

function comment() {


  var commentIcon = document.querySelectorAll('.comment'),
    commentIconArray = Array.from(commentIcon);

  commentIconArray.forEach(function (commentIcons) {
    commentIcons.addEventListener('click', commentIconFunc);
  });
}



function commentIconFunc() {

  NProgress.configure({ easing: 'ease', speed: 100 });
  NProgress.configure({ trickleSpeed: 200 });

  NProgress.start();

  let comment_id = this.id.replace('comment#', '');
  let comment_like = `commentlike#${comment_id}`
  $.ajax({
    type: 'GET',
    url: '/like-comment/',
    data: {
      id: comment_id,
    },
    success: function (data) {
      document.getElementById(comment_like).innerText = data['message'];
      NProgress.done();
    }

  });
}

// function goTo(page, title, url) {
//   if ("undefined" !== typeof history.pushState) {
//     history.pushState({page: page}, title, url);
//   } else {
//     window.location.assign(url);
//   }
// }



function likeIconFunc() {

  NProgress.configure({ easing: 'ease', speed: 100 });
  NProgress.configure({ trickleSpeed: 200 });

  NProgress.start();

  id = this.id
  like_id = `like#${id}`
  $.ajax({
    type: 'GET',
    url: '/like-post/',
    data: {
      id: id,
    },
    success: function (data) {
      document.getElementById(like_id).innerText = data['message'];

      if (data['status'] == 'liked') {
        document.getElementById(`regular#${id}`).classList.remove('fa-regular');
        document.getElementById(`regular#${id}`).classList.add('fa-solid');
        document.getElementById(`regular#${id}`).id = `solid#${id}`
      }
      else if (data['status'] == 'disliked') {
        document.getElementById(`solid#${id}`).classList.add('fa-regular');
        document.getElementById(`solid#${id}`).classList.remove('fa-solid');
        document.getElementById(`solid#${id}`).id = `regular#${id}`

      }



      // goTo("another page", "example", 'profile/kevinnadar22');

      NProgress.done();

    }
  });
}


function followIconFunc() {

  NProgress.configure({ easing: 'ease', speed: 100 });
  NProgress.configure({ trickleSpeed: 200 });

  NProgress.start();

  followeduser = this.id.replace("follow#", '')
  id = this.id
  let followcount = `followcount#${followeduser}`
  $.ajax({
    type: 'GET',
    url: '/followusers/',
    data: {
      followeduser: followeduser,
    },
    success: function (data) {
      document.getElementById(id).innerText = data['message'];

      if (document.getElementById(followcount).classList.contains('follow-m')) {
        document.getElementById(followcount).innerText = data['followcount_message'];
      }
      else {
        document.getElementById(followcount).innerText = data['followcount'];
      }

      NProgress.done();
    }
  });
}


// Follow Unfollow user

var followIcon = document.querySelectorAll('.follow'),
  followIconArray = Array.from(followIcon);

followIconArray.forEach(function (followIcons) {
  followIcons.addEventListener('click', followIconFunc);
});

// End Follow Unfollow user


// Post Comment

function postcomment() {
  var postComment = document.querySelectorAll('.post-comment'),
    postCommentArray = Array.from(postComment);

  postCommentArray.forEach(function (postComments) {
    postComments.addEventListener('click', postCommentFunc);
  });
}

// End Comment

function postCommentFunc(event) {

  NProgress.configure({ easing: 'ease', speed: 100 });
  NProgress.configure({ trickleSpeed: 200 });

  NProgress.start();
  event.preventDefault()
  let comment_id = this.id.replace("post#", 'comment#')
  let id = this.id.replace("post#", '')
  let commented = document.getElementById(comment_id).value;
  document.getElementById(comment_id).value = ''

  $.ajax({
    type: 'POST',
    url: '/post-comment/',
    data: {
      post: id,
      comment: commented,
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    },
    success: function (data) {

      html = data['html']
      let htmlObject = $(html)
      let eElement = document.querySelector(`.comments-container_${id}`)
      let newElement = htmlObject[0]; //element which should be first in E

      eElement.insertBefore(newElement, eElement.firstChild);
      NProgress.done();
      start()

    }
  });
}

// End Comment


// Delete Comment

function deletecomment() {
  var deleteComment = document.querySelectorAll('.deletecomment'),
    deleteCommentArray = Array.from(deleteComment);

  deleteCommentArray.forEach(function (deleteComments) {
    deleteComments.addEventListener('click', deleteCommentFunc);
  });

}


function deleteCommentFunc(event) {
  NProgress.configure({ easing: 'ease', speed: 100 });
  NProgress.configure({ trickleSpeed: 200 });

  NProgress.start();
  event.preventDefault()
  id = this.id
  let deletedComment = this.id.replace("deletecomment#", '')

  $.ajax({
    type: 'GET',
    url: '/deletecomment/',
    data: {
      comment: deletedComment,
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    },
    success: function (data) {
      if (data['status'] == 'success') {
        commentHTML = id.replace("deletecomment#", 'commentbox#')
        document.getElementById(commentHTML).remove()

        NProgress.done();
        start()
      }

    }
  });
}



// Favorites

function favoritesIcon() {
  var makeFavorites = document.querySelectorAll('.favorites'),
    makeFavoritesArray = Array.from(makeFavorites);

  makeFavoritesArray.forEach(function (makeFavorite) {
    makeFavorite.addEventListener('click', makeFavoriteFunc);
  });

}


function makeFavoriteFunc(event) {
  NProgress.configure({ easing: 'ease', speed: 100 });
  NProgress.configure({ trickleSpeed: 200 });

  NProgress.start();

  event.preventDefault()
  id = this.id
  let favorites = this.id.replace("favorites#", '')

  $.ajax({
    type: 'GET',
    url: '/createfavorite/',
    data: {
      post_id: favorites,
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    },
    success: function (data) {

      html = data['html']
      let eElement = document.getElementById(id)

      eElement.innerHTML = html;

      NProgress.done();
      start()
    }
  });
}


// Delete Post

function deleteIcon() {
  var deletePost = document.querySelectorAll('.delete'),
    deletePostArray = Array.from(deletePost);

  deletePostArray.forEach(function (deletePostElem) {
    deletePostElem.addEventListener('click', deletePostFunc);
  });

}


function deletePostFunc(event) {

  NProgress.configure({ easing: 'ease', speed: 100 });
  NProgress.configure({ trickleSpeed: 200 });

  NProgress.start();


  event.preventDefault()
  id = this.id
  let deleted_post = this.id.replace("delete#", '')

  $.ajax({
    type: 'GET',
    url: '/deletepost/',
    data: {
      deleted_post: deleted_post,
    },
    success: function (data) {
      console.log(data);
      if (data['status'] == 'success') {
        window.location.replace("/");
      }

      NProgress.done();
      start()
    }
  });
}



function hideDropdown() {
  dropdown = document.querySelectorAll('.uk-open')
  dropdownArray = Array.from(dropdown);

  dropdownArray.forEach(function (dropDownElem) {
    dropDownElem.classList.remove('uk-open')
  })
}

function markAsRead() {


  NProgress.configure({ easing: 'ease', speed: 100 });
  NProgress.configure({ trickleSpeed: 200 });

  NProgress.start();

  $.ajax({
    type: 'GET',
    url: '/markasread/',
    success: function (data) {

      document.getElementById('notification_dropdown_scrollbar').innerHTML = data[1]

      NProgress.done();
    }
  });
}


function markAsReadFunc() {
  document.getElementById('mark-all-as-read').addEventListener('click', markAsRead)
}



function start() {
  deleteIcon()
  postcomment()
  comment()
  like()
  deletecomment()
  favoritesIcon()
  markAsReadFunc()
}

start()


