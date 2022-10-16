const postButton = document.querySelector("#Post");

// Post form open/close collapse animation
postButton.addEventListener("click", () => {
  let postForm = document.querySelector("#Post-form");

  postButton.classList.toggle("close-style");

  height = postForm.scrollHeight;
  if (postForm.clientHeight === 0) {
    postForm.style.height = height + "px";
    postForm.style.transform = "scaleY(1)";
    postButton.innerHTML = "Close";
  } else {
    postForm.style.height = "0px";
    postForm.style.transform = "scaleY(0)";
    postButton.innerHTML = "+ Share your thoughts +";
  }
});
