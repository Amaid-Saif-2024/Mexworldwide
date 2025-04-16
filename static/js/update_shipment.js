
$(document).ready(function() {
    const token = localStorage.getItem('token');  // Retrieve token from localStorage
    if (!token) {
        window.location.href = '/login';
    }

    const shipmentId = window.location.pathname.split('/').pop();

    // Fetch shipment data using AJAX to populate the form
    $.ajax({
        url: `/shipments?shipment_id=${shipmentId}`, // Send shipment_id as query parameter
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + token  // Add token to the Authorization header
        },
        success: function(response) {
            const shipment = response; // The shipment data is returned directly, not inside an array

            // Populate form fields with the shipment data
            $('#shipment_id').val(shipment.shipment_id);
            $('#sender_name').val(shipment.sender_name);
            $('#receiver_name').val(shipment.receiver_name);
            $('#tracking_number').val(shipment.tracking_number);
            $('#status').val(shipment.status);
            $('#cubic_measurement').val(shipment.cubic_measurement);
            $('#delivery_charges').val(shipment.delivery_charges);
            $('#description').val(shipment.description);
            $('#insurance_value').val(shipment.insurance_value);
            $('#number_of_items').val(shipment.number_of_items);
            $('#total_value').val(shipment.total_value);
            $('#total_gst').val(shipment.total_gst);
            $('#weight').val(shipment.weight);
        },
        error: function(response) {
            if (response.status === 403) {
                window.location.href = '/login';  
            }
        }
    });

    $('#update-shipment-form').submit(function(e) {
        e.preventDefault();

        const updatedShipment = {
            sender_name: $('#sender_name').val(),
            receiver_name: $('#receiver_name').val(),
            tracking_number: $('#tracking_number').val(),
            status: $('#status').val(),
            cubic_measurement: $('#cubic_measurement').val(),
            delivery_charges: $('#delivery_charges').val(),
            description: $('#description').val(),
            insurance_value: $('#insurance_value').val(),
            number_of_items: $('#number_of_items').val(),
            total_value: $('#total_value').val(),
            total_gst: $('#total_gst').val(),
            weight: $('#weight').val()
        };

        // Send the updated data using PATCH request
        $.ajax({
            url: `/update_shipment/${shipmentId}`,
            method: 'PATCH',
            contentType: 'application/json',
            headers: {
                'Authorization': 'Bearer ' + token 
            },
            data: JSON.stringify(updatedShipment),
            success: function(response) {
                alert('Shipment updated successfully!');
                window.location.href = '/'; 
            },
            error: function(response) {
                alert('Error updating shipment');
            }
        });
    });
});
