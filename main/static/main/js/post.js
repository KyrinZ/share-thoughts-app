const likePost = document.getElementById("like-post");
document.addEventListener("DOMContentLoaded", () => {
  fetch(window.location.origin + `/like-post-json/${postID}/`)
    .then((response) => {
      return response.json();
    })
    .then((jsonData) => {
      if (jsonData.liked) {
        likePost.classList.add("liked");
      } else {
        likePost.classList.remove("liked");
      }
    });
});

likePost.onclick = () => {
  likingPost(likePost, postID, totalComments);
};

const likeComment = document.querySelectorAll(".like-comment");
likeComment.forEach((button) => {
  fetch(
    window.location.origin +
      `/like-comment-json/${Number(button.dataset.commentid)}/`
  )
    .then((response) => {
      return response.json();
    })
    .then((jsonData) => {
      if (jsonData.liked) {
        button.classList.add("liked");
      } else {
        button.classList.remove("liked");
      }
    });
  button.onclick = () => {
    likingComment(button, Number(button.dataset.commentid));
  };
});

// Function for liking post
function likingPost(button, postID, totalComments) {
  fetch(window.location.origin + `/like-post/${postID}/`)
    .then((response) => {
      return response.json();
    })
    .then((jsonData) => {
      if (jsonData.liked) {
        button.classList.add("liked");
      } else {
        button.classList.remove("liked");
      }

      let like = document.getElementById(`post-${postID}`);
      let totalLike = jsonData.total_like_post;
      like.innerHTML = `likes: ${totalLike} comments: ${totalComments}`;
    });
}

// Function for liking comment
function likingComment(button, CommentID) {
  fetch(window.location.origin + `/like-comment/${CommentID}/`)
    .then((response) => {
      return response.json();
    })
    .then((jsonData) => {
      if (jsonData.liked) {
        button.classList.add("liked");
      } else {
        button.classList.remove("liked");
      }

      let like = document.getElementById(`comment-${CommentID}`);
      let totalLike = jsonData.total_like_comment;
      like.innerHTML = `likes: ${totalLike}`;
    });
}
