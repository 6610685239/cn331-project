document.querySelectorAll('.toggle-password').forEach((toggleIcon) => {
    toggleIcon.addEventListener('click', () => {
        const passwordField = toggleIcon.previousElementSibling; // Get the associated password field

        // Toggle password visibility
        if (passwordField.type === 'password') {
            passwordField.type = 'text';
            toggleIcon.classList.replace('fa-eye-slash', 'fa-eye'); // Update icon to "eye"
        } else {
            passwordField.type = 'password';
            toggleIcon.classList.replace('fa-eye', 'fa-eye-slash'); // Update icon to "eye-slash"
        }
    });
});


// Function to show the modal after registration is successful
function showModal() {
    document.getElementById('registrationModal').style.display = "block";
}

// Function to close the modal when clicking on the "X" button
function closeModal() {
    document.getElementById('registrationModal').style.display = "none";
}

// If registration is successful, you can trigger the showModal() function like this
// showModal(); (this is done after the form is validated and user is registered)

// Optionally, if you want the modal to close when the user clicks anywhere outside of the modal
window.onclick = function(event) {
    var modal = document.getElementById("registrationModal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
