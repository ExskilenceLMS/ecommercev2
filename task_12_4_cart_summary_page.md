# Task 12 – Subtask 12.4: Cart Summary Page

## 1. Overview

This subtask introduces the **Cart Summary Page**, allowing customers to **review all items currently added to their shopping cart** before proceeding to checkout.  
It provides a consolidated view of cart contents along with quantity and pricing information.

This subtask completes the core cart management functionality.

---

## 2. Purpose

The purpose of this subtask is to:

- Provide customers with a clear overview of their cart
- Display cart items with quantities and prices
- Help customers verify their selections before checkout
- Serve as a transition point between cart management and checkout

---

## 3. Prerequisites

Before completing this subtask, the following should already be implemented:

- Add product to cart functionality (Task 12.1)
- Update cart quantity functionality (Task 12.2)
- Remove item from cart functionality (Task 12.3)
- Cart data structure or session-based cart handling
- Customer authentication
- Base layout template

---

## 4. Cart Summary Features

This subtask includes the following customer capabilities:

- View all items currently in the cart
- Display product name, quantity, and price
- Show cart subtotal or total amount
- Access actions to update quantities or remove items

---

## 5. Access Control

- Cart summary page is accessible to **authenticated users**
- Each user can view **only their own cart**
- Unauthorized or unauthenticated users are redirected appropriately

This ensures cart data privacy and security.

---

## 6. Implementation Summary

- Cart summary route is defined within the cart blueprint
- Cart data is retrieved from session or persistent storage
- Templates extend the shared base layout for UI consistency
- Code related to this subtask is clearly marked for maintainability

---

## 7. Scope and Limitations

**Included in this subtask:**
- Cart summary page
- Display of cart items and totals
- Secure user-specific cart access

**Not included in this subtask:**
- Checkout or payment processing
- Tax or shipping calculations
- Discount or coupon handling
- Order placement logic

These features are implemented in later tasks.

---

## 8. Outcome

After completing this subtask:

- Customers can review their cart before checkout
- Cart information is clear and transparent
- The shopping flow is structured and user-friendly
- The application is ready for checkout and order processing

---

## 9. Related Tasks

- Task 12.1 – Add Product to Cart
- Task 12.2 – Update Cart Quantity
- Task 12.3 – Remove Item from Cart
- Task 13 – Checkout Flow

---
