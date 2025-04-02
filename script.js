document.addEventListener('DOMContentLoaded', () => {
    const epodSelect = document.getElementById('epod-select');
    const ticketsContainer = document.getElementById('tickets-container');
    const noSelection = document.getElementById('no-selection');
    
    let ticketData = {};
    
    // Fetch ticket data from JSON file
    fetch('ticket_data.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load ticket data');
            }
            return response.json();
        })
        .then(data => {
            ticketData = data;
            populateEPODDropdown(data);
        })
        .catch(error => {
            console.error('Error loading ticket data:', error);
            showErrorMessage('Failed to load ticket data. Please check the console for details.');
        });
    
    // Populate EPOD dropdown from ticket data
    function populateEPODDropdown(data) {
        const epodIds = Object.keys(data);
        
        if (epodIds.length === 0) {
            showErrorMessage('No EPOD data found in the JSON file.');
            return;
        }
        
        epodIds.forEach(epodId => {
            const option = document.createElement('option');
            option.value = epodId;
            option.textContent = epodId;
            epodSelect.appendChild(option);
        });
    }
    
    // Event listener for EPOD selection
    epodSelect.addEventListener('change', (event) => {
        const selectedEPODId = event.target.value;
        
        if (selectedEPODId) {
            displayTickets(selectedEPODId);
            noSelection.classList.add('hidden');
            ticketsContainer.classList.remove('hidden');
        } else {
            noSelection.classList.remove('hidden');
            ticketsContainer.classList.add('hidden');
        }
    });
    
    // Display tickets for the selected EPOD
    function displayTickets(epodId) {
        const epodTickets = ticketData[epodId];
        ticketsContainer.innerHTML = '';
        
        if (!epodTickets || Object.keys(epodTickets).length === 0) {
            ticketsContainer.innerHTML = '<div class="message">No tickets found for this EPOD.</div>';
            return;
        }
        
        // Loop through each ticket for the EPOD
        Object.keys(epodTickets).forEach(ticketNumber => {
            const ticket = epodTickets[ticketNumber];
            
            // Create ticket card element
            const ticketCard = document.createElement('div');
            ticketCard.className = 'ticket-card';
            
            // Add ticket header with ticket number and EPOD ID
            const ticketHeader = createTicketHeader(ticket.tn_TicketNumber, ticket.CustName8);
            
            // Add ticket notes section
            const ticketNotes = createTicketNotes(ticket.Notes);
            
            // Add line items section
            const lineItems = createLineItems(ticket.LineItems);
            
            // Assemble ticket card
            ticketCard.appendChild(ticketHeader);
            ticketCard.appendChild(ticketNotes);
            ticketCard.appendChild(lineItems);
            
            // Add ticket card to container
            ticketsContainer.appendChild(ticketCard);
        });
    }
    
    // Create ticket header with ticket number and EPOD ID
    function createTicketHeader(ticketNumber, epodId) {
        const header = document.createElement('div');
        header.className = 'ticket-header';
        
        const ticketNumberElem = document.createElement('div');
        ticketNumberElem.className = 'ticket-number';
        ticketNumberElem.textContent = `Ticket: ${ticketNumber}`;
        
        const epodIdElem = document.createElement('div');
        epodIdElem.className = 'epod-id';
        epodIdElem.textContent = `EPOD: ${epodId}`;
        
        header.appendChild(ticketNumberElem);
        header.appendChild(epodIdElem);
        
        return header;
    }
    
    // Create ticket notes section
    function createTicketNotes(notes) {
        const notesSection = document.createElement('div');
        notesSection.className = 'ticket-notes';
        
        const notesHeader = document.createElement('h3');
        notesHeader.textContent = 'Notes';
        
        const notesContent = document.createElement('p');
        notesContent.textContent = notes || 'No notes available';
        
        notesSection.appendChild(notesHeader);
        notesSection.appendChild(notesContent);
        
        return notesSection;
    }
    
    // Create line items section with table
    function createLineItems(items) {
        const lineItemsSection = document.createElement('div');
        lineItemsSection.className = 'line-items';
        
        const lineItemsHeader = document.createElement('h3');
        lineItemsHeader.textContent = 'Line Items';
        lineItemsSection.appendChild(lineItemsHeader);
        
        if (!items || items.length === 0) {
            const noItems = document.createElement('p');
            noItems.textContent = 'No line items available';
            lineItemsSection.appendChild(noItems);
            return lineItemsSection;
        }
        
        // Create table for line items
        const table = document.createElement('table');
        table.className = 'line-items-table';
        
        // Add table header
        const tableHeader = document.createElement('thead');
        const headerRow = document.createElement('tr');
        
        const descHeader = document.createElement('th');
        descHeader.textContent = 'Description';
        
        const qtyHeader = document.createElement('th');
        qtyHeader.textContent = 'Quantity';
        qtyHeader.className = 'qty-column';
        
        headerRow.appendChild(descHeader);
        headerRow.appendChild(qtyHeader);
        tableHeader.appendChild(headerRow);
        table.appendChild(tableHeader);
        
        // Add table body with line items
        const tableBody = document.createElement('tbody');
        
        items.forEach(item => {
            const row = document.createElement('tr');
            
            const descCell = document.createElement('td');
            descCell.textContent = item.ItemDescription || 'N/A';
            
            const qtyCell = document.createElement('td');
            qtyCell.className = 'qty-column';
            qtyCell.textContent = item.Qty || '0';
            
            row.appendChild(descCell);
            row.appendChild(qtyCell);
            tableBody.appendChild(row);
        });
        
        table.appendChild(tableBody);
        lineItemsSection.appendChild(table);
        
        return lineItemsSection;
    }
    
    // Display error message
    function showErrorMessage(message) {
        noSelection.innerHTML = `<p class="error">${message}</p>`;
        noSelection.classList.remove('hidden');
        ticketsContainer.classList.add('hidden');
    }
});

