$(document).ready(function () {
  const token = localStorage.getItem('token');
  if (!token) {
    window.location.href = '/login';
  }

  const shipmentId = window.location.pathname.split('/').pop();

  $.ajax({
    url: `/shipments?shipment_id=${shipmentId}`,
    method: 'GET',
    headers: {
      Authorization: 'Bearer ' + token,
    },
    success: function (shipment) {
      // Render HTML
      $('#shipment_id').text(shipment.shipment_id);
      $('#sender_name').text(shipment.sender_name);
      $('#receiver_name').text(shipment.receiver_name);
      $('#tracking_number').text(shipment.tracking_number);
      $('#status').text(shipment.status);
      $('#created_at').text(shipment.created_at);
      $('#cubic_measurement').text(shipment.cubic_measurement);
      $('#delivery_charges').text(shipment.delivery_charges);
      $('#description').text(shipment.description);
      $('#insurance_value').text(shipment.insurance_value);
      $('#number_of_items').text(shipment.number_of_items);
      $('#total_value').text(shipment.total_value);
      $('#total_gst').text(shipment.total_gst);
      $('#weight').text(shipment.weight);

      // PDF generation
      $('#download_invoice').click(function () {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        const grandTotal = (
          parseFloat(shipment.total_value || 0) +
          parseFloat(shipment.total_gst || 0) +
          parseFloat(shipment.delivery_charges || 0)
        ).toFixed(2);

        doc.setFontSize(20);
        doc.text("INVOICE", 85, 15);
        doc.setFontSize(10);
        doc.text(`Date: ${new Date(shipment.created_at).toLocaleDateString()}`, 150, 20);
        doc.line(10, 22, 200, 22);

        // Sender & Receiver
        doc.setFontSize(12);
        doc.text("From:", 10, 30);
        doc.text(shipment.sender_name, 10, 35);
        doc.text("To:", 140, 30);
        doc.text(shipment.receiver_name, 140, 35);

        const tableData = [
          ["Shipment ID", shipment.shipment_id],
          ["Tracking Number", shipment.tracking_number],
          ["Status", shipment.status],
          ["Weight", shipment.weight + " kg"],
          ["Cubic Measurement", shipment.cubic_measurement],
          ["Number of Items", shipment.number_of_items],
          ["Insurance Value", "$" + shipment.insurance_value],
          ["Total Value", "$" + shipment.total_value],
          ["Total GST", "$" + shipment.total_gst],
          ["Delivery Charges", "$" + shipment.delivery_charges],
          ["Description", shipment.description],
        ];

        doc.autoTable({
          startY: 45,
          head: [['Field', 'Value']],
          body: tableData,
          theme: 'grid',
          headStyles: { fillColor: [22, 160, 133] },
          styles: { fontSize: 10, cellPadding: 3 },
        });

        // Grand Total
        let finalY = doc.lastAutoTable.finalY || 90;
        doc.setFontSize(13);
        doc.setTextColor(0, 102, 51);
        doc.text(`Grand Total: $${grandTotal}`, 14, finalY + 15);

        doc.save(`invoice_${shipment.tracking_number}.pdf`);
      });
    },
    error: function (response) {
      if (response.status === 403) {
        window.location.href = '/login';
      } else if (response.status === 404) {
        alert('Shipment not found.');
        window.location.href = '/shipments';
      } else {
        alert('An error occurred. Please try again.');
      }
    },
  });
});
