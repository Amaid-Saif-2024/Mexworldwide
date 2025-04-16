
$(document).ready(function() {
    $('#register-form').submit(function(e) {
        e.preventDefault();

        const username = $('#username').val();
        const email = $('#email').val();
        const password = $('#password').val();

        $.ajax({
            url: '/register',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                username: username,
                email: email,
                password: password
            }),
            success: function(response) {
                alert('User registered successfully!');
                window.location.href = '/login'; // Redirect to login page
            },
            error: function(response) {
                alert('Registration failed: ' + response.responseJSON.message);
            }
        });
    });
});
