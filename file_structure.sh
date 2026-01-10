mkdir -p Development/{blueprints,models,database,templates/{auth,admin,seller,customer,product,cart,checkout,order,payment,errors},static/css,tests/fixtures}

touch Development/{app.py,utils.py,decorators.py,rbac.py,module_mapping.py,setup_database.py}

touch Development/blueprints/{__init__.py,admin.py,auth.py,cart.py,checkout.py,customer.py,order.py,payment.py,product.py,seller.py}

touch Development/models/{__init__.py,user.py}

touch Development/database/{schema.sql,seed_data.sql,test_database_validation.sql}

touch Development/templates/{base.html,index.html}

touch Development/templates/auth/{login.html,register.html}

touch Development/templates/admin/{dashboard.html,sellers.html,create_seller.html,categories.html,create_category.html,orders.html}

touch Development/templates/seller/{dashboard.html,products.html,create_product.html,edit_product.html,inventory.html,orders.html}

touch Development/templates/customer/{dashboard.html,profile.html,orders.html,order_details.html,addresses.html,create_address.html}

touch Development/templates/product/{list.html,details.html}

touch Development/templates/cart/view.html

touch Development/templates/checkout/{review.html,confirmation.html}

touch Development/templates/order/{list.html,details.html}

touch Development/templates/payment/{process.html,success.html,invoice.html}

touch Development/templates/errors/{403.html,404.html}

touch Development/static/css/style.css

touch Development/tests/{conftest.py,conftest_playwright.py}

touch Development/tests/fixtures/users.py
