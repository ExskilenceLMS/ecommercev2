# Task 13 – Subtask 13.1: Order Review Page

## 1. Overview

This subtask introduces the **Order Review Page**, which allows customers to **review their order before final placement**.  
It serves as the final confirmation step in the checkout process, ensuring customers can verify all order details.

This subtask marks the beginning of the checkout flow.

---

## 2. Purpose

The purpose of this subtask is to:

- Provide a clear summary of the customer’s order
- Allow customers to review cart items and pricing
- Enable selection of delivery or shipping information
- Prevent accidental or incorrect order placement

---

## 3. Prerequisites

Before completing this subtask, the following should already be implemented:

- Cart summary page (Task 12.4)
- Customer authentication
- Cart data structure or persistent cart handling
- Product and order data models
- Base layout template

---

## 4. Order Review Features

This subtask includes the following customer capabilities:

- View all items included in the order
- Display quantities, prices, and order subtotal
- Review delivery or shipping information
- Confirm order details before placement

---

## 5. Access Control

- Order review page is accessible to **authenticated customers**
- Each customer can review **only their own order**
- Unauthorized or unauthenticated users are redirected appropriately

This ensures order data privacy and security.

---

## 6. Implementation Summary

- Order review route is defined within the checkout blueprint
- Order data is derived from the current cart state
- Templates extend the shared base layout for UI consistency
- Code related to this subtask is clearly marked for maintainability

---

## 7. Scope and Limitations

**Included in this subtask:**
- Order review page
- Display of order items and pricing
- Final review before order placement

**Not included in this subtask:**
- Order creation or database persistence
- Payment processing
- Order confirmation logic
- Invoice generation

These features are implemented in subsequent subtasks.

---

## 8. Outcome

After completing this subtask:

- Customers can review their order before checkout
- Errors or mistakes can be caught before order placement
- The checkout flow becomes structured and reliable
- The application is prepared for order placement logic

---

## 9. Related Tasks

- Task 12.4 – Cart Summary Page
- Task 13.2 – Place Order Logic
- Task 13.3 – Order Confirmation Page

---
