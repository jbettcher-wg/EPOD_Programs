#!/usr/bin/env python3

import os
import csv
import json
import glob
from collections import defaultdict

def process_csv_files():
    # Path to the TKT folder
    tkt_folder = "TKT"
    
    # Dictionary to store customer data
    customer_data = defaultdict(dict)
    
    # Find all CSV files in the TKT folder
    csv_files = glob.glob(os.path.join(tkt_folder, "*.csv")) + glob.glob(os.path.join(tkt_folder, "*.CSV"))
    
    if not csv_files:
        print(f"No CSV files found in {tkt_folder} directory")
        return
    
    # Process each CSV file
    for csv_file in csv_files:
        print(f"Processing: {csv_file}")
        
        try:
            # Read and process the CSV file
            with open(csv_file, 'r', newline='', encoding='utf-8-sig') as file:
                csv_reader = csv.reader(file)
                lines = list(csv_reader)
                
                # Extract ticket data
                ticket_data = extract_ticket_data(lines)
                
                if ticket_data:
                    # Get customer name and ticket number
                    customer_name = ticket_data.get('CustName8', 'Unknown')
                    ticket_number = ticket_data.get('tn_TicketNumber', 'Unknown')
                    
                    # Store the ticket data under the respective customer
                    customer_data[customer_name][ticket_number] = ticket_data
        except Exception as e:
            print(f"Error processing {csv_file}: {e}")
    
    # Write the data to a JSON file
    if customer_data:
        output_file = "ticket_data.json"
        with open(output_file, 'w') as file:
            json.dump(customer_data, file, indent=4)
        print(f"Data saved to {output_file}")
    else:
        print("No data was processed")

def extract_ticket_data(lines):
    """Extract relevant data from the CSV lines"""
    ticket_data = {}
    line_items = []
    notes = ""
    in_detail_section = False
    item_idx = -1
    qty_idx = -1
    
    # First pass: look for headers and main ticket info
    for i, line in enumerate(lines):
        # Skip empty lines
        if not line or not any(line):
            continue
            
        # Convert list to string for easier searching if it's a single column
        line_str = line[0] if len(line) == 1 else ",".join(line)
        
        # Extract ticket number
        if "tn_TicketNumber" in line_str:
            # Look for TKT pattern in this or next line
            ticket_pattern = None
            if "TKT" in line_str:
                ticket_pattern = line_str
            elif i+1 < len(lines) and lines[i+1] and "TKT" in ",".join(lines[i+1]):
                ticket_pattern = ",".join(lines[i+1])
                
            if ticket_pattern:
                # Extract using pattern matching
                import re
                match = re.search(r'(TKT\d+)', ticket_pattern)
                if match:
                    ticket_data['tn_TicketNumber'] = match.group(1)
        
        # Extract customer name
        if "CustName8" in line_str or "CustomerName" in line_str:
            # Look for EP pattern
            customer_pattern = None
            if "EP-" in line_str:
                customer_pattern = line_str
            elif i+1 < len(lines) and lines[i+1] and "EP-" in ",".join(lines[i+1]):
                customer_pattern = ",".join(lines[i+1])
                
            if customer_pattern:
                # Extract using pattern matching
                import re
                match = re.search(r'(EP-\d+)', customer_pattern)
                if match:
                    ticket_data['CustName8'] = match.group(1)
        
        # Look for Notes section
        if "Notes" in line_str:
            # Find notes in this line or next lines
            if len(line) > 1 and any(line[1:]):
                notes = ",".join(line[1:]).strip()
            else:
                # Look ahead for notes content
                j = i + 1
                while j < len(lines) and lines[j] and not any(keyword in ",".join(lines[j]) for keyword in ["Detail Items", "Item Description"]):
                    notes += " " + ",".join(lines[j]).strip()
                    j += 1
            
            # Clean up notes
            notes = notes.strip()
        
        # Look for the detail items section headers
        if any(keyword in line_str for keyword in ["Detail Items", "Item Description", "ItemDescription"]):
            in_detail_section = True
            # Find indices for item description and quantity
            for idx, col in enumerate(line):
                if col and ("Item" in col or "Description" in col):
                    item_idx = idx
                elif col and "Qty" in col:
                    qty_idx = idx
    
        # Process line items if we're in the detail section and have found the column indices
        if in_detail_section and item_idx >= 0 and qty_idx >= 0 and i > 0:
            # Skip the header row
            if not any(keyword in line_str for keyword in ["Detail Items", "Item Description", "ItemDescription"]):
                # Check if this line has enough columns and contains actual item data
                if len(line) > max(item_idx, qty_idx) and line[item_idx].strip() and not line[item_idx].strip().startswith("Item"):
                    try:
                        qty = line[qty_idx].strip() if qty_idx < len(line) else ""
                        # Only add if we have a meaningful description
                        if line[item_idx].strip():
                            line_items.append({
                                "ItemDescription": line[item_idx].strip(),
                                "Qty": qty
                            })
                    except IndexError:
                        continue
    
    # Add notes and line items to ticket data
    ticket_data['Notes'] = notes
    ticket_data['LineItems'] = line_items
    
    # If we still don't have the ticket number or customer name, check for specific patterns in all lines
    if 'tn_TicketNumber' not in ticket_data or 'CustName8' not in ticket_data:
        for line in lines:
            line_str = ",".join(line) if line else ""
            
            # Look for ticket number pattern
            if 'tn_TicketNumber' not in ticket_data and "TKT" in line_str:
                import re
                match = re.search(r'(TKT\d+)', line_str)
                if match:
                    ticket_data['tn_TicketNumber'] = match.group(1)
            
            # Look for customer pattern
            if 'CustName8' not in ticket_data and "EP-" in line_str:
                import re
                match = re.search(r'(EP-\d+)', line_str)
                if match:
                    ticket_data['CustName8'] = match.group(1)
    
    print(f"Extracted: Ticket={ticket_data.get('tn_TicketNumber', 'Unknown')}, Customer={ticket_data.get('CustName8', 'Unknown')}, Line Items={len(line_items)}")
    return ticket_data

if __name__ == "__main__":
    process_csv_files()
    print("Processing complete.")

