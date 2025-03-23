// Function to toggle password visibility when the eye icon is clicked
document.addEventListener("DOMContentLoaded", function () {
    const passwordInput = document.querySelector('.password-input');  // Access the password input field
    const eyeIcon = document.querySelector('.pw_hidden');  // Access the eye icon

    eyeIcon.addEventListener("click", () => {
        // Check if password is currently hidden
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';  // Show the password
            eyeIcon.classList.remove('uil-eye-slash');  // Remove the closed-eye icon
            eyeIcon.classList.add('uil-eye');  // Add the open-eye icon
            eyeIcon.style.color = '#003366' // chnage the icon to blue when pressed
        } else {
            passwordInput.type = 'password';  // Hide the password
            eyeIcon.classList.remove('uil-eye');  // Remove the open-eye icon
            eyeIcon.classList.add('uil-eye-slash');  // Add the closed-eye icon
            eyeIcon.style.color = '#b5b5b5' //change the colour back to gray
        }
    });
    
});
