# 🩸 Blood Bank Management System

## 📌 Overview
This project is a **Blood Bank Management System** implemented using **SQL Server (T-SQL)**.  
It simulates real-world hospital blood management including storage, requests, delivery, and tracking blood units.

---

## 🏗️ Database Description

### 1. Delivery Table
Manages transportation of blood units.

**Status Types:**
- Scheduled
- In Transit
- Completed
- Cancelled

---

### 2. BloodUnit Table
Stores blood unit information:
- Collection Date
- Expiry Date
- Status (available / used / expired)
- Linked to Delivery

---

### 3. BloodType Table
Defines blood classification:
- Blood Groups: A, B, AB, O  
- RH Factor: + / -

---

### 4. Van Table
Represents transportation vehicles:
- Plate Number
- Capacity
- Location
- Status

---

### 5. BloodRequest Table
Handles hospital requests:
- Quantity
- Priority: Normal / Urgent / Emergency
- Status: Pending / Approved / Rejected

---

### 6. Hospital Table
Stores hospital details:
- Name
- Location
- Phone
- Linked Requests

---

## 🔗 Relationships
- Delivery → BloodUnit (1:M)
- Delivery → Van (1:M)
- BloodType → BloodRequest (1:M)
- BloodRequest → Hospital
- Delivery → BloodRequest

---

## ⚙️ Features
- Blood inventory tracking
- Expiry date management
- Hospital request system
- Delivery tracking system
- Advanced SQL queries:
  - JOIN operations
  - GROUP BY & HAVING
  - Subqueries
  - CASE expressions
  - Aggregate functions

---

## 📊 Sample Insights
- Total used blood units
- Requests by priority level
- Delivery status statistics
- High-demand blood requests
- Blood type usage analysis

---

## 🧠 Technologies Used
- SQL Server
- T-SQL

---

## 🚀 How to Run
1. Open **SQL Server Management Studio (SSMS)**
2. Create database:
```sql
CREATE DATABASE bloodbank;
