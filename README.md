🩸 #Blood Bank Management System
📌 #Overview

This project is a Blood Bank Management System built using SQL Server.
It is designed to manage blood donations, blood units, delivery operations, hospitals, and blood requests efficiently.

The system ensures proper tracking of:

Blood storage and expiry
Delivery status
Hospital requests
Blood types compatibility
Inventory management
🏗️ #Database Structure

The system consists of the following tables:

1. Delivery

Tracks blood transportation status.

Scheduled
In Transit
Completed
Cancelled
2. BloodUnit

Stores details of collected blood units including:

Collection date
Expiry date
Status (available / used / expired)
3. BloodType

Defines blood groups and RH factor:

A, B, AB, O
/ -
4. Van

Represents transport vehicles used in deliveries.

5. BloodRequest

Handles hospital requests for blood units based on:

Priority (Normal, Urgent, Emergency)
Quantity
Status (Pending, Approved, Rejected)
6. Hospital

Stores hospital information and links to requests.

🔗 #Relationships
Delivery → BloodUnit (1-to-Many)
Delivery → Van (1-to-Many)
BloodType → BloodRequest (1-to-Many)
BloodRequest → Hospital (1-to-1 / optional)
BloodRequest → Delivery (linked delivery system)
⚙️ #Features
Create and manage blood inventory
Track blood unit expiry and usage
Handle hospital blood requests
Manage delivery system for transportation
Advanced SQL queries (JOINs, GROUP BY, CASE, Subqueries)
Data integrity using constraints and foreign keys
📊 #Sample Queries Included
Total used blood units
Requests grouped by priority
Delivery status analysis
High-demand blood requests
Blood type request statistics
Advanced JOIN operations across tables
🧠 Technologies Used
SQL Server
T-SQL (Transact-SQL)
