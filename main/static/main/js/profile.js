// Profile form open/close animation
const profileButton = document.getElementById("profile-settings");
profileButton.addEventListener("click", () => {
  const profileForm = document.getElementById("profile-settings-form");

  height = profileForm.scrollHeight;
  if (profileForm.clientHeight === 0) {
    profileForm.style.height = height + "px";
    profileForm.style.transform = "scaleY(1)";
  } else {
    profileForm.style.height = "0px";
    profileForm.style.transform = "scaleY(0)";
  }
  return false;
});

// Password form open/close animation
const passwordButton = document.getElementById("password-button");
passwordButton.addEventListener("click", () => {
  const passwordForm = document.getElementById("password-form");

  height = passwordForm.scrollHeight;
  if (passwordForm.clientHeight === 0) {
    passwordForm.style.height = height + "px";
    passwordForm.style.transform = "scaleY(1)";
  } else {
    passwordForm.style.height = "0px";
    passwordForm.style.transform = "scaleY(0)";
  }
  return false;
});
