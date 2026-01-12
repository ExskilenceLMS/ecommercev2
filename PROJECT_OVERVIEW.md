# 🛒 E-Commerce Project (Multi-Vendor Platform)

## 📌 Project Overview
This project is a fully functional Multi-Vendor E-Commerce platform designed to facilitate online trading between multiple sellers and customers. The system is built to mimic real-world "Digital Shopping Mall" operations where an Administrator manages the infrastructure, Sellers manage their individual shops/products, and Customers browse and purchase items.

The goal is to understand the complete lifecycle of an e-commerce transaction, from product listing to order fulfillment, while implementing Role-Based Access Control (RBAC).

---

## 🛠️ Tech Stack
* **Language:** Python
* **Web Framework:** Flask
* **Templating Engine:** Jinja2
* **Database:** MySQL
* **Modules:** Product, Category, Inventory, Cart, Order, Payment

---

## 🔷 Phase 1: System Understanding & Design
### 🔹 Part 1: Requirement Analysis — Roles & Features

The system is divided into three distinct user roles. Below is a detailed breakdown of the features and responsibilities for each role.

---

### 1️⃣ Role: Admin (Platform Owner)
**Concept:** The Admin is the "Mall Owner." They do not sell products but own the building, set the rules, and ensure security.

#### 📋 Features & Responsibilities
* **Login & Logout (Security Guard):**
    * *What:* A secure entry point restricted to authorized administrators only.
    * *Why:* To protect sensitive business data and platform settings from unauthorized access.
* **Create / Manage Sellers (Leasing Office):**
    * *What:* The Admin is the only one who can create accounts for Sellers.
    * *Why:* This vetting process prevents scammers from joining the platform. It ensures only verified vendors can sell.
* **Create Categories & Subcategories (Mall Signage):**
    * *What:* Defining the organization structure (e.g., Electronics > Laptops).
    * *Why:* Sellers cannot create their own categories. This prevents chaos (e.g., one seller using "Cellphones" and another "Mobiles") and keeps the catalog standardized.
* **View All Products & Orders (Surveillance):**
    * *What:* A master view of every product and every order across the entire platform.
    * *Why:* Necessary for dispute resolution (e.g., if a customer claims a seller never shipped an item) and general oversight.
* **Manage Platform-level Settings (Building Maintenance):**
    * *What:* Controlling global variables like the Website Name, Logo, Tax Rates, or Shipping Policies.
* **View Sales Reports (Business Analytics):**
    * *What:* High-level charts showing total revenue and growth.
    * *Why:* To track the health and success of the entire business.

#### ❓ Admin Role MCQs
1.  **Who acts as the "Mall Owner" deciding who is allowed to sell products?**
    * [ ] Customer
    * [x] Admin
    * [ ] Seller
    * [ ] Guest
2.  **Why doesn't the Admin allow Sellers to create their own Categories?**
    * [x] To keep the catalog organized and standardized.
    * [ ] Because Sellers don't know how to type.
    * [ ] To charge extra money for categories.
    * [ ] Categories are not important.
3.  **What is the purpose of the Admin viewing "All Orders"?**
    * [ ] To buy the items for themselves.
    * [ ] To delete successful orders.
    * [x] To oversee platform activity and resolve disputes.
    * [ ] To pack the products.
4.  **If a new Tax Law is passed, who updates the tax percentage in "Platform Settings"?**
    * [ ] Every Customer individually
    * [ ] The Seller
    * [x] The Admin
    * [ ] The Courier Service
5.  **Which feature ensures that only the Mall Owner can access sensitive settings?**
    * [ ] View Sales Reports
    * [ ] Create Categories
    * [x] Login (Authentication)
    * [ ] Add to Cart

---

### 2️⃣ Role: Seller / Store Staff (Shopkeeper)
**Concept:** The Seller rents a shop within the mall. They focus only on their own products and sales.

#### 📋 Features & Responsibilities
* **Login (Shop Key):**
    * *What:* Authenticates the user and redirects them specifically to the "Seller Dashboard."
* **Add / Update Products (Stocking Shelves):**
    * *What:* Uploading product names, descriptions, prices, and images.
    * *Why:* Without this data input, the "shelves" of the website would be empty.
* **Manage Inventory / Stock (Warehouse Check):**
    * *What:* Updating the quantity of items available (e.g., "I have 5 red shirts left").
    * *Why:* Critical to prevent **Overselling**. If stock hits 0, the system must stop customers from buying that item.
* **View Received Orders (Order Pad):**
    * *What:* A list of items that customers have purchased specifically from this seller.
    * *Why:* Functions as a "To-Do List" so the seller knows what to pack.
* **Update Order Status (Communication):**
    * *What:* Changing the status of an order (Pending → Packed → Shipped).
    * *Why:* Keeps the customer informed. It prevents customers from calling support to ask, "Where is my package?"

#### ❓ Seller Role MCQs
1.  **What is the "To-Do List" for a Seller?**
    * [ ] Manage Platform Settings
    * [x] View Received Orders
    * [ ] Browse Products
    * [ ] Register
2.  **Why is "Manage Inventory" critical?**
    * [ ] It changes the color of the website.
    * [x] It prevents selling items that don't exist (Overselling).
    * [ ] It allows the Admin to spy on the seller.
    * [ ] It deletes old products.
3.  **When a Seller logs in, why can't they see another Seller's orders?**
    * [x] The system filters data to show only their own records.
    * [ ] They are not wearing glasses.
    * [ ] The other seller blocked them.
    * [ ] The Admin forgot to turn on that feature.
4.  **Who is responsible for taking a photo of the product and uploading it?**
    * [ ] The Customer
    * [ ] The Admin
    * [x] The Seller
    * [ ] The Bank
5.  **Which status update indicates the package has left the Seller's warehouse?**
    * [ ] Pending
    * [ ] Cancelled
    * [x] Shipped
    * [ ] Viewed

---

### 3️⃣ Role: Customer (The Shopper)
**Concept:** The End-User who browses the aisles and purchases items.

#### 📋 Features & Responsibilities
* **Register & Login (Membership Card):**
    * *What:* Creating a secure account.
    * *Why:* Essential for saving shipping addresses (convenience) and maintaining an Order History (tracking purchases).
* **Browse Products & Categories (Window Shopping):**
    * *What:* Using search bars and filters to find specific items (e.g., "Sneakers" or "Kitchenware").
* **Add Products to Cart (Shopping Basket):**
    * *What:* A temporary holding area for items.
    * *Why:* Allows the user to select multiple items before making a final payment decision. Items here are not yet "sold."
* **Place Orders (Checkout Counter):**
    * *What:* The final transaction.
    * *Why:* This complex step involves checking stock, deducting money, reducing inventory, and generating a receipt (Order ID).
* **View Order History (Receipt Book):**
    * *What:* A dashboard showing past purchases and current status.
    * *Why:* Allows the customer to track if their item has been "Shipped" or "Delivered."

#### ❓ Customer Role MCQs
1.  **Which feature represents the "Checkout Counter" experience?**
    * [ ] Add to Cart
    * [x] Place Orders
    * [ ] Login
    * [ ] View History
2.  **What is the "Cart" used for?**
    * [ ] To permanently store items you bought.
    * [x] To hold items temporarily before you decide to pay.
    * [ ] To send items to the Admin.
    * [ ] To write reviews.
3.  **Why does a Customer need to "Register"?**
    * [ ] To become a Seller.
    * [x] To link their address and past orders to a secure account.
    * [ ] To change the price of products.
    * [ ] To see the Admin Dashboard.
4.  **How does a Customer find a specific type of product (e.g., "Watches")?**
    * [x] By using "Browse Categories" or Search.
    * [ ] By emailing the Seller.
    * [ ] By using "Manage Inventory".
    * [ ] By logging out.
5.  **If a Customer wants to see if their order has been "Shipped", where do they look?**
    * [ ] In the Cart.
    * [ ] On the Seller's profile.
    * [x] In "View Order History".
    * [ ] They cannot check.