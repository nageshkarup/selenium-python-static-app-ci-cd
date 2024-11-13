document.addEventListener('DOMContentLoaded', function () {

  // Handle Logout Action on Dashboard Page
  const logoutButton = document.getElementById('logoutButton');
  if (logoutButton) {
      logoutButton.addEventListener('click', function () {
          // Remove only session-specific data to retain user credentials
          sessionStorage.removeItem('isLoggedIn');  // Assuming you use 'isLoggedIn' to check if the user is logged in

          // Redirect to sign-in page
          window.location.href = 'signin.html';
      });
  }

  // Handle Sign-Up Form Submission
  const signupForm = document.getElementById('signupForm');
  if (signupForm) {
      signupForm.addEventListener('submit', function (e) {
          e.preventDefault();  // Prevent form submission

          // Get user inputs
          const name = document.getElementById('name').value;
          const email = document.getElementById('email').value;
          const password = document.getElementById('password').value;

          // Store user info in sessionStorage (credentials for re-signing in)
          sessionStorage.setItem('name', name);
          sessionStorage.setItem('email', email);
          sessionStorage.setItem('password', password);

          // Store logged-in state (this flag can help us determine if user is logged in)
          sessionStorage.setItem('isLoggedIn', true);

          // Redirect to sign-in page after successful sign-up
          window.location.href = 'signin.html';
      });
  }

  // Handle Sign-In Form Submission
  const signinForm = document.getElementById('signinForm');
  if (signinForm) {
      signinForm.addEventListener('submit', function (e) {
          e.preventDefault();  // Prevent form submission

          // Get user inputs
          const email = document.getElementById('email').value;
          const password = document.getElementById('password').value;

          // Check if the email and password match with sessionStorage data
          if (email === sessionStorage.getItem('email') && password === sessionStorage.getItem('password')) {
              // Set the logged-in state flag
              sessionStorage.setItem('isLoggedIn', true);

              // Redirect to welcome (dashboard) page after successful sign-in
              window.location.href = 'welcome.html';
          } else {
              alert('Invalid credentials, please sign up first.');
          }
      });
  }

  // Display the name on the dashboard (if user is logged in)
  const userNameSpan = document.getElementById('userName');
  if (userNameSpan) {
      const name = sessionStorage.getItem('name');
      if (name) {
          userNameSpan.textContent = name;
      } else {
          userNameSpan.textContent = 'Guest'; // Fallback in case name is not found
      }
  }
});
