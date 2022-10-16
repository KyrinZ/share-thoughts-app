let counter = 1;
document.addEventListener("DOMContentLoaded", load);

// Infinite scroll function
window.onscroll = () => {
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
    load();
  }
};

// makes api request after infinite scroll event is called
function load() {
  if (counter < totalPaginatedPages + 1) {
    const start = counter;

    fetch(window.location.origin + `/post-json/page${start}`)
      .then((response) => {
        return response.json();
      })
      .then((myJson) => {
        myJson.forEach(add_post);
      });
    counter++;
  }
}

// Funtion to add post
function add_post(data) {
  const post = document.createElement("div");
  post.className = "post";
  document.querySelector(".all-posts").append(post);

  // Head of post
  const profilePic = document.createElement("div");
  profilePic.className = "post-profile-pic";
  const img = document.createElement("img");
  img.src = data.profile_pic;
  profilePic.append(img);
  post.append(profilePic);

  const postLink = document.createElement("a");
  postLink.href = window.location.origin + `/post/${data.post_id}`;
  const postUsername = document.createElement("h4");
  const datePosted = document.createElement("span");
  postUsername.id = "head";
  postUsername.innerHTML = data.username;
  if (data.show_nickname) {
    postUsername.innerHTML = data.nickname;
  }
  datePosted.innerHTML = data.date_posted;
  postUsername.append(datePosted);
  postLink.append(postUsername);
  post.append(postLink);

  // Content of post
  const postTextField = document.createElement("p");
  postTextField.innerHTML = data.text_field;
  post.append(postTextField);

  // Comments for the post
  allComments = data.comments;
  allComments.forEach((commentData) => {
    const comment = document.createElement("div");
    comment.className = "post-comment";

    // Head of the comment
    const commentUsername = document.createElement("h5");
    const dateCommented = document.createElement("span");
    commentUsername.innerHTML = commentData.username;
    if (commentData.show_nickname) {
      commentUsername.innerHTML = commentData.nickname;
    }
    dateCommented.innerHTML = commentData.date_commented;
    commentUsername.append(dateCommented);
    comment.append(commentUsername);

    // Content of comment
    const commentTextField = document.createElement("p");
    commentTextField.innerHTML = commentData.text_field;
    comment.append(commentTextField);

    post.append(comment);
  });

  // Like and Comment section
  const postButtons = document.createElement("div");
  postButtons.className = "post-buttonsAndstatus";

  // Status of the post (like count and comment count)
  const postStatus = document.createElement("div");
  postStatus.className = "post-status";
  const likesANDcomment = document.createElement("h5");
  likesANDcomment.id = data.post_id;
  likesANDcomment.innerHTML = `likes: ${data.total_likes} comments: ${data.total_comments}`;
  postStatus.append(likesANDcomment);
  postButtons.append(postStatus);

  // Link to post page
  const viewFullPostLink = document.createElement("a");
  viewFullPostLink.href = window.location.origin + `/post/${data.post_id}`;
  const underlined = document.createElement("u");
  underlined.innerHTML = "view full";
  viewFullPostLink.append(underlined);
  postButtons.append(viewFullPostLink);

  // Buttons for like and comment
  const buttons = document.createElement("div");
  buttons.className = "post-comment-btns";
  const likeButton = document.createElement("button");
  const commentButton = document.createElement("button");
  likeButton.innerHTML = "like";
  commentButton.innerHTML = "comment";
  likeButton.onclick = () =>
    likingPost(likeButton, data.post_id, data.total_comments);
  commentButton.onclick = () =>
    (location.href = window.location.origin + `/post/${data.post_id}`);
  buttons.append(likeButton);
  buttons.append(commentButton);
  postButtons.append(buttons);

  // Adding css to like button that are liked
  fetch(window.location.origin + `/like-post-json/${data.post_id}/`)
    .then((response) => {
      return response.json();
    })
    .then((jsonData) => {
      if (jsonData.liked) {
        likeButton.classList.add("liked");
      } else {
        likeButton.classList.remove("liked");
      }
    });

  post.append(postButtons);
}

// Liking function for the post
function likingPost(button, postID, totalComments) {
  // first fetch is to trigger the backend to make changes to database
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
      const like = document.getElementById(postID);
      const totalLike = jsonData.total_like_post;
      like.innerHTML = `likes: ${totalLike} comments: ${totalComments}`;
    });
}
