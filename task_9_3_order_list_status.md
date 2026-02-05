# Task 9 – Subtask 9.3: Order List & Status

## 1. Overview

This subtask introduces **Order List and Status Management functionality** for Sellers.  
It allows sellers to **view orders related to their products** and **update order statuses**, supporting efficient order fulfillment and tracking.

This subtask completes the core seller dashboard operations by enabling order-level interactions.

---

## 2. Purpose

The purpose of this subtask is to:

- Provide sellers with visibility into their received orders
- Enable sellers to track and manage order statuses
- Support order processing and fulfillment workflows
- Maintain clear separation between seller and customer order views

---

## 3. Prerequisites

Before completing this subtask, the following should already be implemented:

- Seller dashboard route
- Product and inventory management (Task 9.1 and Task 9.2)
- Role-based access control for Seller users
- Order data model and relationships
- Base layout template

---

## 4. Order Management Features

This subtask includes the following seller capabilities:

- View a list of orders containing the seller’s products
- Display essential order details (order ID, customer, status, quantity)
- Update the status of orders related to their products
- Ensure sellers interact only with their own orders

---

## 5. Access Control

- All order management routes are **restricted to Seller users**
- Sellers can view and update **only orders linked to their products**
- Unauthorized or unauthenticated users are blocked from accessing seller order pages
- Role validation is enforced before any order operation

This ensures secure and accurate order handling.

---

## 6. Implementation Summary

- Order listing and status update routes are defined within the seller blueprint
- Order logic is isolated from admin and customer order views
- Templates extend the shared base layout for UI consistency
- Code related to this subtask is clearly marked for maintainability

---

## 7. Scope and Limitations

**Included in this subtask:**
- Seller-specific order listing
- Order status update functionality
- Seller-only access enforcement

**Not included in this subtask:**
- Order cancellation
- Refund or return processing
- Payment handling
- Shipment tracking or delivery updates

These features are implemented in later tasks.

---

## 8. Outcome

After completing this subtask:

- Sellers can effectively manage incoming orders
- Order processing becomes structured and role-specific
- The system supports scalable seller operations
- The application is ready for advanced order lifecycle management

---

## 9. Related Tasks

- Task 9.1 – Product CRUD Pages
- Task 9.2 – Inventory Update
- Task 14 – Order Management

---
