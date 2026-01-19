# Task 9 – Subtask 9.1: Product CRUD Pages

## 1. Overview

This subtask introduces **Product CRUD (Create, Read, Update, Delete) functionality** for Sellers.  
It enables sellers to **manage their own products**, including viewing, adding, and editing product information through a dedicated seller dashboard.

This subtask forms the core of seller-side operations and is essential for enabling product listings in the system.

---

## 2. Purpose

The purpose of this subtask is to:

- Allow sellers to manage their product catalog
- Provide interfaces for creating and updating products
- Enforce seller-level access control for product operations
- Support future inventory and order workflows

---

## 3. Prerequisites

Before completing this subtask, the following should already be implemented:

- Seller dashboard route (Task 9)
- Role-based access control for Seller users
- Seller blueprint structure
- Product data model
- Base layout template

---

## 4. Product Management Features

This subtask includes the following seller capabilities:

- View a list of products owned by the seller
- Access a product creation form
- Add new products to the catalog
- Edit existing product details
- Maintain ownership isolation between different sellers

---

## 5. Access Control

- All product management routes are **restricted to Seller users**
- Sellers can access **only their own products**
- Unauthorized or unauthenticated users are blocked from accessing seller product pages
- Role validation occurs before executing product operations

This ensures product data integrity and security.

---

## 6. Implementation Summary

- Product CRUD routes are defined within the seller blueprint
- Product listing, creation, and update logic is separated for clarity
- Templates extend the shared base layout for consistent UI
- Code related to this subtask is clearly marked for maintainability

---

## 7. Scope and Limitations

**Included in this subtask:**
- Product listing for sellers
- Product creation workflow
- Product editing functionality
- Seller-only access enforcement

**Not included in this subtask:**
- Product deletion
- Inventory quantity management
- Product approval workflows
- Product analytics

These features are implemented in later tasks.

---

## 8. Outcome

After completing this subtask:

- Sellers can manage their product catalog independently
- Product data is securely isolated per seller
- The system supports scalable product management
- The application is ready for inventory and order integration

---

## 9. Related Tasks

- Task 8 – Admin Dashboard
- Task 9.2 – Inventory Update
- Task 11 – Product Listing & Search

---
