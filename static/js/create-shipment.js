
$(document).ready(function() {
    const token = localStorage.getItem('token');  

    
    if (!token) {
        window.location.href = '/login';
    }

    
    $('#create-shipment-form').submit(function(e) {
        e.preventDefault();

        const newShipment = {
            sender_name: $('#sender_name').val(),
            sender_address: $('#sender_address').val(),
            sender_phone: $('#sender_phone').val(),
            receiver_name: $('#receiver_name').val(),
            receiver_address: $('#receiver_address').val(),
            receiver_phone: $('#receiver_phone').val(),
            service_type: $('#service_type').val(),
            weight: $('#weight').val(),
            insurance_value: $('#insurance_value').val(),
            cubic_measurement: $('#cubic_measurement').val(),
            status: $('#status').val(),
            number_of_items: $('#number_of_items').val(),
            total_value: $('#total_value').val(),
            total_gst: $('#total_gst').val(),
            description: $('#description').val(),
            delivery_charges: $('#delivery_charges').val(),
        };
        console.log(newShipment);
        // Send the new shipment data using POST request
        $.ajax({
            url: '/create_shipment',  
            method: 'POST',
            contentType: 'application/json',
            headers: {
                'Authorization': 'Bearer ' + token 
            },
            data: JSON.stringify(newShipment),
            success: function(response) {
                alert('Shipment created successfully!');
                window.location.href = '/';
            },
            error: function(response) {
                if (response.status === 403) {
                    
                    window.location.href = '/login'; 
                }
                
            }
        });
    });
});
