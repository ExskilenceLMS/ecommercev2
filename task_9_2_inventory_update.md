# Task 9 – Subtask 9.2: Inventory Update

## 1. Overview

This subtask introduces **Inventory Update functionality** for Sellers.  
It allows sellers to **view and update stock quantities** for their products, ensuring accurate inventory tracking within the system.

This subtask builds on the product management features introduced in Task 9.1.

---

## 2. Purpose

The purpose of this subtask is to:

- Enable sellers to manage product stock levels
- Maintain accurate inventory availability
- Prevent overselling or stock inconsistencies
- Support order processing and fulfillment workflows

---

## 3. Prerequisites

Before completing this subtask, the following should already be implemented:

- Seller dashboard route
- Product management functionality (Task 9.1)
- Role-based access control for Seller users
- Product data model with inventory fields
- Base layout template

---

## 4. Inventory Management Features

This subtask includes the following seller capabilities:

- View current inventory levels for owned products
- Update stock quantities for individual products
- Ensure inventory changes apply only to seller-owned products
- Maintain separation between different sellers’ inventories

---

## 5. Access Control

- All inventory management routes are **restricted to Seller users**
- Sellers can modify inventory **only for their own products**
- Unauthorized or unauthenticated users are blocked from accessing inventory pages
- Role validation is enforced before inventory updates

This ensures inventory data accuracy and security.

---

## 6. Implementation Summary

- Inventory update routes are defined within the seller blueprint
- Inventory logic is separated from product creation and editing
- Templates extend the shared base layout for UI consistency
- Code related to this subtask is clearly marked for maintainability

---

## 7. Scope and Limitations

**Included in this subtask:**
- Inventory listing for seller products
- Inventory quantity update functionality
- Seller-only access enforcement

**Not included in this subtask:**
- Automated stock adjustments
- Inventory alerts or notifications
- Bulk inventory updates
- Inventory history or audit logs

These enhancements may be added in future tasks.

---

## 8. Outcome

After completing this subtask:

- Sellers can maintain accurate product stock levels
- Inventory data supports reliable order processing
- The system prevents common stock-related issues
- The application is prepared for order and fulfillment integration

---

## 9. Related Tasks

- Task 9.1 – Product CRUD Pages
- Task 9.3 – Order List & Status
- Task 13 – Checkout Flow

---
