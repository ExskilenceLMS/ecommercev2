# Task 10 – Subtask 10.2: Order History

## 1. Overview

This subtask introduces the **Order History feature** for Customers.  
It allows customers to **view a list of their past orders**, providing transparency and easy access to order-related information.

This subtask builds on the customer dashboard and profile functionality introduced earlier in Task 10.

---

## 2. Purpose

The purpose of this subtask is to:

- Provide customers with visibility into their past orders
- Allow customers to track order activity and statuses
- Improve customer experience through order transparency
- Maintain clear separation between customer and seller/admin order views

---

## 3. Prerequisites

Before completing this subtask, the following should already be implemented:

- Customer dashboard route
- Customer profile page (Task 10.1)
- User authentication using Flask-Login
- Role-based access control for Customer users
- Order data model and relationships
- Base layout template

---

## 4. Order History Features

This subtask includes the following customer capabilities:

- View a list of all orders placed by the customer
- Display essential order details (order ID, date, status, total)
- Access individual order records for review
- Ensure order data is specific to the logged-in customer

---

## 5. Access Control

- Order history routes are **restricted to authenticated Customer users**
- Customers can view **only their own orders**
- Unauthorized or unauthenticated users are blocked from accessing order history pages
- User identity is validated before retrieving order data

This ensures order information remains private and secure.

---

## 6. Implementation Summary

- Order history routes are defined within the customer blueprint
- Order listing logic is separated from seller and admin order views
- Templates extend the shared base layout for UI consistency
- Code related to this subtask is clearly marked for maintainability

---

## 7. Scope and Limitations

**Included in this subtask:**
- Customer order history listing
- Secure access to customer-specific order data

**Not included in this subtask:**
- Order status updates
- Order cancellation or returns
- Payment details or invoices
- Detailed order item breakdown

These features are implemented in subsequent tasks.

---

## 8. Outcome

After completing this subtask:

- Customers can easily review their past orders
- Order visibility improves trust and transparency
- The system maintains strict role-based data isolation
- The application is prepared for detailed order views

---

## 9. Related Tasks

- Task 10.1 – Profile Page
- Task 10.3 – Order Details Page
- Task 13 – Checkout Flow

---
