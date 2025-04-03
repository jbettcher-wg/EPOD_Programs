How to Run the EPOD Ticket Viewer Website

To run the EPOD Ticket Viewer website, you need to follow these two steps:

Step 1: Process the ticket data
First, run the Python script to process the CSV files in the TKT folder and generate the ticket_data.json file:

python3 process_tickets.py

Step 2: Start a local web server
Then, start a simple HTTP server to serve the website:

python3 -m http.server 8000

Once the server is running, you can access the website by opening a browser and navigating to:

http://localhost:8000

This will display the EPOD Ticket Viewer interface where you can select an EPOD ID from the dropdown to view service history.

To stop the server when you're done, press Ctrl+C in the terminal.