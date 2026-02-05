# Task 14 – Subtask 14.2: Order Status Updates

## 1. Overview

This subtask introduces **Order Status Updates**, allowing sellers to **update the status of orders related to their products**.  
It enables sellers to manage order progress and communicate fulfillment stages through order statuses.

This subtask builds upon Seller Order Management introduced in Task 14.1.

---

## 2. Purpose

The purpose of this subtask is to:

- Enable sellers to update order statuses
- Track the lifecycle of an order
- Provide customers with visibility into order progress
- Maintain consistent order state transitions

---

## 3. Prerequisites

Before completing this subtask, the following should already be implemented:

- Seller order management (Task 14.1)
- Order and order item data models
- Seller authentication and role-based access
- Defined order status values
- Base layout template

---

## 4. Order Status Update Features

This subtask includes the following seller capabilities:

- Update order status (e.g., Pending, Processing, Shipped, Completed)
- Validate allowed status transitions
- View current status before applying updates
- Ensure status updates reflect correctly for customers

---

## 5. Access Control

- Order status update actions are restricted to **authenticated sellers**
- Sellers can update **only orders associated with their products**
- Unauthorized or non-seller users are denied access

This ensures order integrity and role-based security.

---

## 6. Implementation Summary

- Order status update logic is defined within the seller blueprint
- Status validation rules are enforced before applying changes
- Order records are updated in a controlled workflow
- Code related to this subtask is clearly marked for maintainability

---

## 7. Scope and Limitations

**Included in this subtask:**
- Seller-driven order status updates
- Status validation and persistence

**Not included in this subtask:**
- Automated status changes
- Customer-initiated status updates
- Notifications or alerts
- Refund or cancellation handling

These features are implemented in later tasks.

---

## 8. Outcome

After completing this subtask:

- Sellers can manage order progress effectively
- Order status changes are consistent and secure
- Customers gain visibility into order fulfillment stages
- The system supports a complete order lifecycle

---

## 9. Related Tasks

- Task 14.1 – Seller Order Management
- Task 14.3 – Order Fulfillment
- Task 10.2 – Order History

---
