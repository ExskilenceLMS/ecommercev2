# Task 12 – Subtask 12.2: Update Cart Quantity

## 1. Overview

This subtask introduces the **Update Cart Quantity** functionality, allowing customers to **modify the quantity of products already added to their shopping cart**.  
It improves cart usability by enabling customers to adjust selections before proceeding to checkout.

This subtask builds on the Add Product to Cart feature introduced in Task 12.1.

---

## 2. Purpose

The purpose of this subtask is to:

- Allow customers to update product quantities in their cart
- Maintain accurate cart totals and item counts
- Improve user experience during cart management
- Support a flexible shopping workflow before checkout

---

## 3. Prerequisites

Before completing this subtask, the following should already be implemented:

- Add product to cart functionality (Task 12.1)
- Cart data structure or session-based cart handling
- Product data model
- Customer authentication
- Base layout template

---

## 4. Cart Quantity Update Features

This subtask includes the following capabilities:

- Increase or decrease the quantity of items in the cart
- Validate quantity inputs before applying updates
- Ensure updates apply only to existing cart items
- Maintain user-specific cart isolation

---

## 5. Access Control

- Cart update operations are available to **authenticated users**
- Users can update quantities **only in their own cart**
- Unauthorized or unauthenticated users are prevented from modifying cart data

This ensures cart integrity and data security.

---

## 6. Implementation Summary

- Quantity update logic is defined within the cart blueprint
- Cart item validation is performed before updating quantities
- Quantity changes are reflected immediately in the cart
- Code related to this subtask is clearly marked for maintainability

---

## 7. Scope and Limitations

**Included in this subtask:**
- Update quantity functionality for cart items
- Validation of quantity changes
- User-specific cart access enforcement

**Not included in this subtask:**
- Removing items from the cart
- Cart summary or total calculation
- Checkout or payment handling
- Inventory availability checks

These features are implemented in later subtasks.

---

## 8. Outcome

After completing this subtask:

- Customers can easily adjust cart item quantities
- Cart data remains accurate and consistent
- The shopping experience becomes more flexible
- The application is prepared for cart review and checkout

---

## 9. Related Tasks

- Task 12.1 – Add Product to Cart
- Task 12.3 – Remove Item from Cart
- Task 12.4 – Cart Summary Page

---
