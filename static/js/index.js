
$(document).ready(function() {
    // Get the token from localStorage
    const token = localStorage.getItem('token');

    
    if (!token) {
        window.location.href = '/login';  
    }

    
    function loadShipments(page = 1) {
        const sortBy = $('#sort_by').val();
        const order = $('#order').val();

        $.ajax({
            url: '/shipments',
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + token  
            },
            data: {
                page: page,
                sort_by: sortBy,
                order: order
            },
            success: function(response) {
                const shipments = response.shipments;
                const totalPages = response.total_pages;
                const currentPage = response.current_page;

               
                $('#shipments-list').empty();

               
                shipments.forEach(function(shipment) {
                    const row = `
                        <tr>
                            <td>${shipment.shipment_id}</td>
                            <td>${shipment.sender_name}</td>
                            <td>${shipment.receiver_name}</td>
                            <td>${shipment.tracking_number}</td>
                            <td>${shipment.status}</td>
                            <td>${shipment.created_at}</td>
                            <td>
                                <button class="btn btn-info btn-sm view-btn" data-id="${shipment.shipment_id}">View</button>
                                <button class="btn btn-warning btn-sm update-btn" data-id="${shipment.shipment_id}">Update</button>
                                <button class="btn btn-danger btn-sm delete-btn" data-id="${shipment.shipment_id}">Delete</button>
                            </td>
                        </tr>
                    `;
                    $('#shipments-list').append(row);
                });

             
                $('#pagination-nav .pagination').empty();
                for (let i = 1; i <= totalPages; i++) {
                    const activeClass = (i === currentPage) ? 'active' : '';
                    const pageLink = `<li class="page-item ${activeClass}"><a class="page-link" href="javascript:void(0);" data-page="${i}">${i}</a></li>`;
                    $('#pagination-nav .pagination').append(pageLink);
                }
            },
            error: function(response) {
                if (response.status === 403) {
                    
                    window.location.href = '/login';  
                }
            }
        });
    }

    
    loadShipments();

    
    $('#apply_filters').click(function() {
        loadShipments();
    });

    // Pagination click event
    $(document).on('click', '.page-link', function() {
        const page = $(this).data('page');
        loadShipments(page);
    });

    // View Shipment
    $(document).on('click', '.view-btn', function() {
        const shipmentId = $(this).data('id');
        window.location.href = `/view_shipment/${shipmentId}`;
    });

    // Update Shipment
    $(document).on('click', '.update-btn', function() {
        const shipmentId = $(this).data('id');
        window.location.href = `/update_shipment/${shipmentId}`;
    });

    // Delete Shipment
    $(document).on('click', '.delete-btn', function() {
        const shipmentId = $(this).data('id');
        if (confirm("Are you sure you want to delete this shipment?")) {
            $.ajax({
                url: `/delete_shipment/${shipmentId}`,
                method: 'DELETE',
                headers: {
                    'Authorization': 'Bearer ' + token  // Send token in the request headers
                },
                success: function(response) {
                    alert(response.message);
                    loadShipments();
                },
                error: function(response) {
                    if (response.status === 401) {
                        alert('Session expired or invalid token. Please log in again.');
                        window.location.href = '/login';  // Redirect to login if unauthorized
                    }
                }
            });
        }
    });
});
