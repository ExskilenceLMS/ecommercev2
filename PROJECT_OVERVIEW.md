# 🛒 Multi-Vendor E-Commerce Platform (Flask + MySQL)

## 📌 Overview

This project is a **Multi-Vendor E-Commerce Web Application** where multiple sellers can list and manage products, and customers can browse, purchase, and track orders through a single online marketplace.  
A platform administrator manages seller onboarding, product categories, platform settings, and system monitoring.

The application simulates a real-world **online marketplace (e.g., eBay/Amazon-style)** and demonstrates the complete e-commerce transaction lifecycle using **Role-Based Access Control (RBAC)**.

---

## 🚀 Key Features

- Multi-vendor marketplace architecture  
- Role-based access control (Admin, Seller, Customer)  
- Secure authentication & authorization  
- Product catalog & category management  
- Inventory control with overselling prevention  
- Shopping cart & checkout system  
- Order tracking & status management  
- Platform-level analytics and reporting  

---

## 🛠️ Technology Stack

- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS, Bootstrap, Jinja2
- **Database:** MySQL
- **Architecture:** MVC (Model–View–Controller)
- **Authentication:** Session-based authentication

---

## 🔐 User Roles & Responsibilities

### 1️⃣ Admin (Platform Administrator)

**Description:**  
Manages the overall marketplace infrastructure and ensures security, standardization, and compliance.

**Responsibilities:**
- Secure admin authentication
- Create and manage seller accounts
- Define product categories and subcategories
- View all products and all orders
- Manage platform-level settings (tax, branding, policies)
- Access sales and performance reports

---

### 2️⃣ Seller (Vendor)

**Description:**  
Independent sellers who list products and manage orders within the platform.

**Responsibilities:**
- Seller authentication and dashboard access
- Create, update, and remove product listings
- Manage product inventory
- View orders related to their products
- Update order status (Pending → Shipped)

---

### 3️⃣ Customer (Buyer)

**Description:**  
End-users who browse the marketplace, place orders, and track purchases.

**Responsibilities:**
- User registration and login
- Browse products using categories or search
- Add products to cart
- Place orders through checkout
- View order history and order status

---

## 🔄 Application Workflow

1. Admin creates seller accounts and manages categories  
2. Sellers list products and update inventory  
3. Customers browse products and add items to cart  
4. Customers place orders via checkout  
5. Inventory is validated and updated automatically  
6. Sellers process orders and update order status  
7. Customers track order progress in their account  

---

## 📊 High-Level Database Structure

- Users (Admin, Seller, Customer)
- Categories & Subcategories
- Products
- Inventory
- Cart & Cart Items
- Orders & Order Items
- Payments

---

## 🎯 Project Objectives

- Implement a real-world online marketplace system  
- Apply role-based access control (RBAC)  
- Prevent overselling using inventory validation  
- Maintain secure data separation between vendors  
- Understand Flask–MySQL integration  
- Build scalable e-commerce architecture  

---

## ❓ Concept Check – MCQs

### 🔐 Admin (Platform Administrator)

1. **Who is responsible for approving and managing seller accounts?**
   - [ ] Customer  
   - [x] Admin  
   - [ ] Seller  
   - [ ] Payment Gateway  

2. **Why are categories managed only by the Admin?**
   - [x] To maintain a standardized product catalog  
   - [ ] To limit seller access  
   - [ ] To disable search  
   - [ ] Categories are not important  

3. **Why can the Admin view all orders on the platform?**
   - [ ] To ship products  
   - [ ] To modify purchases  
   - [x] To monitor activity and resolve disputes  
   - [ ] To cancel orders  

4. **Who updates tax rates or platform-wide policies?**
   - [ ] Customer  
   - [ ] Seller  
   - [x] Admin  
   - [ ] Courier Service  

5. **Which feature protects access to the Admin dashboard?**
   - [ ] Reports  
   - [ ] Categories  
   - [x] Authentication & Authorization  
   - [ ] Product Search  

---

### 🏪 Seller (Vendor)

1. **Which feature shows sellers the orders placed for their products?**
   - [ ] Product Listing  
   - [x] Order Management  
   - [ ] Platform Settings  
   - [ ] User Registration  

2. **Why is inventory management essential?**
   - [ ] To update images  
   - [x] To prevent overselling  
   - [ ] To hide products  
   - [ ] To increase delivery speed  

3. **Why can sellers access only their own orders?**
   - [x] Role-based data isolation  
   - [ ] Orders are random  
   - [ ] Admin restriction error  
   - [ ] Orders are public  

4. **Who uploads product details such as price and images?**
   - [ ] Admin  
   - [x] Seller  
   - [ ] Customer  
   - [ ] Payment Service  

5. **Which order status indicates the product has been dispatched?**
   - [ ] Pending  
   - [ ] Cancelled  
   - [x] Shipped  
   - [ ] Viewed  

---

### 🧑‍💻 Customer (Buyer)

1. **Which action completes a purchase?**
   - [ ] Add to Cart  
   - [x] Checkout / Place Order  
   - [ ] Login  
   - [ ] Browse  

2. **What is the purpose of the cart?**
   - [ ] Permanent storage  
   - [x] Temporary storage before checkout  
   - [ ] Payment processing  
   - [ ] Order tracking  

3. **Why must a customer register?**
   - [ ] To manage sellers  
   - [x] To store addresses and order history  
   - [ ] To update inventory  
   - [ ] To manage categories  

4. **How can customers find specific products?**
   - [x] Search or browse categories  
   - [ ] Contact Admin  
   - [ ] Update inventory  
   - [ ] Logout  

5. **Where can customers track their order status?**
   - [ ] Cart  
   - [ ] Product Page  
   - [x] Order History  
   - [ ] Seller Dashboard  

---

