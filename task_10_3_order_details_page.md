# Task 10 – Subtask 10.3: Order Details Page

## 1. Overview

This subtask introduces the **Order Details Page** for Customers.  
It allows customers to **view detailed information about a specific order**, including the items purchased, order status, and summary details.

This subtask complements the Order History feature by enabling customers to inspect individual orders in depth.

---

## 2. Purpose

The purpose of this subtask is to:

- Provide customers with detailed visibility into individual orders
- Display order items and relevant order information
- Improve transparency and trust in the ordering process
- Maintain a clear separation between customer and seller/admin order views

---

## 3. Prerequisites

Before completing this subtask, the following should already be implemented:

- Customer dashboard route
- Order history page (Task 10.2)
- User authentication using Flask-Login
- Role-based access control for Customer users
- Order and order-item data models
- Base layout template

---

## 4. Order Details Features

This subtask includes the following customer capabilities:

- View detailed information for a selected order
- Display order items with quantities and prices
- View order status and order summary information
- Ensure order details are accessible only to the order owner

---

## 5. Access Control

- Order details routes are **restricted to authenticated Customer users**
- Customers can view **only their own order details**
- Unauthorized or unauthenticated users are blocked from accessing order details
- User identity validation is enforced before retrieving order data

This ensures order information remains private and secure.

---

## 6. Implementation Summary

- Order details routes are defined within the customer blueprint
- Order retrieval logic is scoped to the logged-in customer
- Templates extend the shared base layout for UI consistency
- Code related to this subtask is clearly marked for maintainability

---

## 7. Scope and Limitations

**Included in this subtask:**
- Customer order details view
- Order item listing
- Secure access enforcement

**Not included in this subtask:**
- Order status modification
- Invoice or payment details
- Shipment tracking
- Order cancellation or return actions

These features are handled in later tasks.

---

## 8. Outcome

After completing this subtask:

- Customers can view complete details of their orders
- Order transparency and user confidence are improved
- The system maintains strict role-based data protection
- The application supports scalable order-related features

---

## 9. Related Tasks

- Task 10.1 – Profile Page
- Task 10.2 – Order History
- Task 14 – Order Management

---
