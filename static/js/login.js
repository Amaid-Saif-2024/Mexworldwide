
$(document).ready(function() {
    $('#login-form').submit(function(e) {
        e.preventDefault();

        const username = $('#username').val();
        const password = $('#password').val();

        $.ajax({
            url: '/login',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                username: username,
                password: password
            }),
            success: function(response) {
                // On successful login, storing the token in localStorage
                localStorage.setItem('token', response.token);
                alert('Login successful!');
                window.location.href = '/'; // Redirect to index page
            },
            error: function(response) {
                alert('Invalid credentials, please try again.');
            }
        });
    });
});
