
$(document).ready(function() {
    const token = localStorage.getItem('token');  
    if (!token) {
        window.location.href = '/login'; 
    }
    // Handling form submission to track shipment
    $('#track-shipment-form').submit(function(e) {
        e.preventDefault();

        const trackingNumber = $('#tracking_number').val();  // Get the tracking number from the input field

        // Send request to the server to track the shipment
        $.ajax({
            url: '/track',  // API endpoint for tracking
            method: 'GET',
            data: { tracking_number: trackingNumber }, 
            headers: {
                'Authorization': 'Bearer ' + token 
            },
            success: function(response) {
               $('#error-message').hide();
                $('#shipment-info').show();  
                // Populate only the relevant fields
                $('#sender_name').text(response.sender_name);
                $('#receiver_name').text(response.receiver_name);
                $('#tracking_number_display').text(response.tracking_number);
                $('#status').text(response.status);
                $('#weight').text(response.weight);
                $('#delivery_charges').text(response.delivery_charges);
            },
            error: function(response) {
                $('#error-message').show();
                $('#shipment-info').hide();  // Hide shipment info if not found
            }
        });
    });
});
