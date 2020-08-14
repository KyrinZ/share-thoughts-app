const loginButton = document.getElementById("log-in");
const registerButton = document.getElementById("register");

// Links to login page
loginButton.onclick = () => {
  location.href = window.location.origin + "/login/";
};

// Links to register page
registerButton.onclick = () => {
  location.href = window.location.origin + "/register/";
};
