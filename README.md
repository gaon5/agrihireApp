# Title and Description

Darfield Outdoor Hire requires an Online Hire Equipment Management System to replace its manual Excel and paper-based system, handling over 500 types of outdoor equipment. This digital solution will enhance customer booking processes, streamline equipment management, and simplify administrative tasks, ultimately boosting operational efficiency and customer service. 

# Project Objectives

The primary goals of this system are:

    1. Customer Experience: Provide customers with a user-friendly platform to browse equipment, check availability, register accounts, enable profile updates, extend hire periods, make and manage bookings, and access their prior hire records. This will make the rental process more convenient and transparent for customers.
    2. Equipment Management: Streamline equipment management for the staff, allowing them to buy add new equipment, update equipment details, retire old or damaged items by deletion, and change equipment status as “maintenance” during repairs. Maintain comprehensive and accurate records for each equipment item, including scheduled pick-up dates, items to reintegrate into the system following returns of items and track customers’ rental history.
    3. Equipment Schedule: Facilitate daily operations by helping staff prepare equipment for check-out and ensuring the timely return of rented items. This includes recording check-out and return times, and quickly addressing customer queries.
    4. Financial Transparency: Require customers to pay in advance for bookings and rental extensions, ensuring financial transparency and reducing the risk of unpaid rentals.
    5. Administrative Control: Provide the manager/administrator with the capability to perform system tasks, manage staff members, manage customer, add category and sub-category, run reports, for improved administrative control and oversight.
    6. Financial Reports: Administrators have access to comprehensive financial reports. These reports include revenue breakdowns by revenue per category, payment method, bookings and maintenance cost. It helps to track overall revenue and financial performance.

# User Roles

The system accommodates three primary user roles:

    1. Admin: This role involves managing staff and customers accounts, managing equipment category and sub-category, generating reports and updating their own accounts.
    2. Customer: Customer can view and update their profiles, choose the dates and times to hire equipment, add equipment into their wish list, view their shopping carts, and make payments.
    3. Staff: Staff can manage their accounts and profiles, view customers information including history of bookings. They can add, delete and update equipment in the system. They are responsible for making sure the equipment are picked up by the customers for each day and return them back into the system once customers have returned them. As a staff,  they can change the status of each unit of the equipment: Available, Maintenance, Hired and Terminated. Also, responsible for overseeing customers’ enquiries.

# Core Functionality

The system’s core functionality revolves around managing the entire equipment inventory by informing the user about the equipment's current status. When a customer is browsing through the Darfield Hire System the system will only show the available equipments to efficiently make bookings. When an item is hired the system intelligently categorizes their status to hired. If an equipment is in the waiting list to be maintained, either for repair or annual inspection, it is categorized as maintenance so the equipment isn’t accessible for customers to hire. 

The Darfield Outdoor Hire aims to simplify the registration process, offer a user-friendly experience for customers, and provide comprehensive tools for staff and admin to enhance operational efficiency and control.

# Usage

In the guest.py all users can use these functions:

@app.route('/')
Template: index.html

This template is the main page where user can browse equipment in Darfield Outdoor Hire and look for equipment by category. Displays pictures, category etc. There is an About Us to get more information about the website. Footer with contact info and opening hours.

@app.route('/login/', methods=['GET', 'POST'])
Template: login.html

User can type in their username and password to login or register an account.

@app.route('/logout')
Template:  index.html

After logout, redirects back to the main page.

@app.route('/register', methods=['GET', 'POST'])
Template: register.html

User can fill out registration form. If successful, redirects to main page for login.

@app.route('/reset_password', methods=['GET', 'POST'])
Template: answer.html

User enters their email address and instructions will be sent to the email. They have to answer a security question in order to change their password.

@app.route('/change_password', methods=['GET', 'POST'])
Template: change_password.html

If user has forgotten their password they will be asked to enter new password and a confirm password. If the new and confirm password matches the password will be updated.

@app.route('/dashboard', methods=['GET', 'POST'])
Template: dashboard.html

Renders different templates based on user type: admin, staff and customer.

@app.route('/edit_detail', methods=['GET', 'POST'])
Template: update_information.html

User can change personal information including title, first name, last name, phone number and email.

@app.route('/user_change_password', methods=['GET', 'POST'])
Template: change_password.html

User will be asked to enter their old password then new and confirm password. If the old password is entered correctly and the new password matches the confirmation, the password will be updated.

@app.route("/guest_cart")
Template: customer_cart.html

If user is a customer they can see the equipments they have put into the cart. They have the option to delete, edit and increase number of equipments hired. If user is a guest they will be redirected to the main page and asked to log in.

@app.errorhandler(Exception)
Template: error.html

The error page if a page can’t be loaded to show the content.

 In staff.py the user needs to log in as a staff to access these functions:

@app.route('/staff/get_enquiries')
Template: enquiries.html

This route enables staff to access and review all customer inquiries related to equipment rentals, displaying customer ID, name, email, and the respective questions.

@app.route('/staff/check_out_list', methods=['GET', 'POST'])
Template: check_out_list.html

This route generates the page for monitoring equipment scheduled for customer pickup, displaying information such as customer ID, pickup time, and any accompanying notes. After the customer successfully picks up the equipment they've reserved for hire, staff can click "Checkout" to finalize the process.

@app.route('/staff/return_list', methods=['GET', 'POST'])
Template: return_list.html

This route renders the page for staff to monitor the equipment schedules for customer drop-off, displaying information such as customer ID, drop-off time, and any accompanying notes. After the customer has successfully dropped off the equipment once their hire period has ended, staff can click “Return” to return the equipment back into the system for other customers to book for hire.

@app.route('/staff/maintenance_list', methods=['GET', 'POST'])
Template: maintenance_list.html

This route displays a page that provides information on equipment unit (instance) IDs, their corresponding start and end dates, the type of maintenance required, and the current equipment status (e.g., Overdue, Pending, Annual Inspection). Any associated notes are also shown. After the equipment completes its maintenance process, staff can click "Finish" to return the equipment to the system, making it available for customers to book for hire.

@app.route('/staff/more_detail', methods=['GET', 'POST'])
Template: equipment_detail.html

This route presents details regarding the chosen equipment, including its image, pricing, stock number, license requirement, dimensions, description, and details about the equipment.The staff can review it and make any necessary modifications. If changes are required, they can utilize the "Update" button.

@app.route('/staff/update_equipment/<detail_id>', methods=['GET', 'POST'])
Template: update_equipment.html

This route generates the page for editing information related to the chosen equipment. Staff can access the current image and equipment details. To update the image, they can upload a new one, which will replace the previous image.

@app.route('/staff/add_equipment', methods=['GET', 'POST'])
Template: add_equipment.html

This route provides a form page where staff can upload a maximum of two images. They will select the category, sub-category, equipment name, price, stock number, minimum stock threshold, specify whether it requires a driver's license, provide measurements, descriptions, and details to add new equipment to the system.

@app.route('/staff/delete_equipment', methods=['GET','POST'])
Template: equipment_list.html

If the staff no longer want to hire out a specific equipment in Darfield Outdoor Hire they will click on “Delete” in the equipment list which will remove it from the database and website so customers’ can’t hire it anymore.

@app.route('/staff/search_result', methods=['GET', 'POST'])
Template: equipment_list.html

Staff can search for equipment within the system using criteria such as category, sub-category, or equipment name. If the equipment doesn't exist, the system will inform the staff that no such equipment is found.

@app.route('/staff/customer_list', methods=['GET', 'POST'])
Template: customer_list.html

This route displays a page that allows staff to search for customers by customer name. The customer ID, name, and phone number are promptly presented, making it convenient for staff to access their information.
@app.route('/staff/customer_details', methods=['GET', 'POST'])
Template: customer_details.html

This route presents the name, phone number, address, birth date, email, and the booking history of the chosen customer. It provides information about equipment names and rental start and end dates, giving staff an overview of the customer's past bookings with Darfield Outdoor Hire.

@app.route('/staff/equipment_list')
Template: equipment_list.html

This route generates a comprehensive list of all equipment offered by Darfield Outdoor Hire, organized by category. It includes details such as sub-category, image, equipment name, stock number, and the option to delete equipment if needed. To make it easier for staff to look for specific equipment they can search for it or add a new equipment.

@app.route('/staff/set_instance', methods = ["POST", "GET"])
Template: equipment_instance.html

This route presents a page where staff can choose an equipment name. It will then show the unit (instance) ID, e.g. displaying both units if there are 2 in stock, along with their current status. Staff can modify the status by selecting from the options: Available, Hired, Maintenance, or Terminated. When staff add a new equipment, the default status is set to "Available."

In the admin.py only the admin can access these functions:

@app.route('/admin/manage_category', methods=['GET', 'POST'])
Template: manage_category.html

This route generates a page for the admin to perform various category-related actions. They can add a new category, modify the main category by making changes and clicking "Change," or delete a category by selecting "Delete."

@app.route('/admin/manage_subcategory', methods=['GET', 'POST'])
Template: manage_subcategory.html

This route provides a page for adding a new sub-category that complements a main category or for updating the existing subcategory and category combination. The admin has the option to edit the sub-category name and apply changes by clicking "Change," or they can delete the sub-category and its association with the main category.

@app.route('/admin/manage_staff', methods=['GET', 'POST'])
Template: manage_staff.html

This route displays a page that allows searching for a staff member by name, adding a new staff member to the system, editing their personal information, creating a new password, or deleting the staff. It also provides information such as staff ID, email, name, registration date, and last login date for each staff member.

@app.route('/admin/manage_customer', methods=['GET', 'POST'])
Template: manage_customer.html

This route displays a page that allows searching for a customer by name, adding a new customer to the system, editing their personal information, creating a new password, or deleting the customer. It also provides information such as customer ID, email, name, registration date, and last login date for each customer.

@app.route('/admin/delete_user', methods=['GET', 'POST'])
Redirect back to manage_customer.html or manage_staff.html

After the admin has removed a customer or staff member from the system, the system will redirect back to the respective customer or staff list, depending on which user type has been deleted.

@app.route('/admin/password', methods=['GET', 'POST'])
Template: manage_customer.html or manage_staff.html

This route is for admin to set a new password for customer and staff by entering new password and confirm password. If both passwords match and meet the requirements the update will be successful.

@app.route('/admin/financial_report', methods=['GET', 'POST'])
Template: financial_report.html

This route displays the option for an annual report or monthly report. There is a pie chart illustrating the revenue earned from different categories and payment method. Additionally, it includes a bar graph that depicts the monthly income for each month. This provides the admin with valuable insights into the financial performance of Darfield Outdoor Hire.

@app.route('/admin/maintenance_report', methods=['GET', 'POST'])
Template: maintenance_report.html

This route offers the choice between generating an annual or monthly report. There is a pie chart illustrating the number of maintenance done for different categories and another pie chart to show the cost from maintenance for the different categories. Also a bar graph to show the total maintenance completed for each month.  This information provides valuable insights into maintenance-related data for the admin.

@app.route('/admin/equipment_report', methods=['GET', 'POST'])
Template: equipment_report.html

This route provides the option to select between generating an annual or monthly report. It includes pie charts that visually represent the number of bookings and booking hours for different categories. Additionally, there's a bar graph depicting the total number of bookings and booking hours per month.

In customer.py the user needs to log in as a customer to access these functions:

@app.route('/equipments', defaults={'category': None, 'sub': None})
@app.route('/equipments/<category>', defaults={'sub': None})
@app.route('/equipments/<category>/<sub>')
Template: equipments.html

The first route displays all the equipment available for customers to browse. The second route allows equipment filtering based on selected categories. The third route shows equipment by choosing a category and then selecting a subcategory.

@app.route('/equipments/search_equipment', methods=['GET', 'POST'])
Template: equipments.html

In this route, customers can perform equipment searches by entering the equipment's name, and the results will display the equipment corresponding to the entered name.

@app.route('/equipments/<category>/<sub>/detail', defaults={'detail_id': None})
@app.route('/equipments/<category>/<sub>/detail/<detail_id>', methods=['GET', 'POST'])
Template: equipment_detail.html

The route provides comprehensive information about the equipment when the "Hire Now" option is selected. It displays the equipment name, measurements, description, details, and pricing options for half-day or full-day rentals. To initiate direct hiring or add to the cart, customers must select both available start and end dates, along with the corresponding start and end times.

@app.route('/user_wishlist', methods=['GET', 'POST'])
Template: wishlist.html

This route showcases the equipment that customers have favourited by clicking on the heart icon while browsing. It serves as a way to save and track equipment items they're interested in, even if they aren't ready to make an immediate purchase. If customers decide to rent such equipment, they can conveniently access it directly from their wishlist.

@app.route('/add_favorite/<int:equipment_id>', methods=['GET', 'POST'])
Template: Varies

This route allows customers to add equipment to their wish list by clicking on the heart icon. This can be achieved from any page with equipments whether it be after searching for the specific equipment, filtering through category and/or subcategory.

@app.route('/remove_favorite/<int:equipment_id>', methods=['GET', 'POST'])
Template: Varies

This route allows customers to remove the equipment from their wish list. It can be achieved by clicking on the heart icon again from their wish list or through the catalogue.

@app.route('/bookings')
Template: bookings.html

This route displays customer's booking history, featuring details such as the equipment name, booking date, cost, start and end dates of the rental period, and the option to extend the return date if desired.

@app.route('/update_booking', methods=['POST'])
Template: direct to payment_form.html or bookings.html

If customer extended the hire period from start date by a week it will take the customer to the payment page. If the extension date has already extended by a week then it will redirect them back to the bookings page.

@app.route('/payment_form', methods=['GET', 'POST'])
Template: payment_form.html

This route renders the page for customers to make payments for extending their hire period. It provides information about the equipment name, the booking date, the updated cost, the starting hire date, the new hire return date, and the revised duration. Additionally, it offers payment options through Paypal, Mastercard, or Credit.

@app.route('/faq')
Template: faq.html

This route arranges questions by topic and provides corresponding answers, allowing customers to acquire insights into the operations of Darfield Outdoor Hire.

@app.route('/contact', methods=['GET', 'POST'])
Template: contact.html

The route renders the form page where customers can input their first and last name, email, phone number, location, specify the type of inquiry, and compose their question. It also provides alternative methods to get in touch with them, including by phone, email, or visiting their physical store.

@app.route('/customer_cart')
Template: customer_cart.html

This route renders the page for customer to  review the equipment before proceeding with payment. It displays the equipment items in their cart, including details like quantity, rental start and end dates, prices, and provides options to edit or delete the equipment. To continue with the payment process, customers are required to check the small box next to the items they wish to purchase.

@app.route('/add_to_cart', methods=['POST', 'get'])
Template: @app.route('/equipments/<category>/<sub>/detail/<detail_id>', methods=['GET', 'POST'])

This route enables customers to place the equipment they wish to rent into the shopping cart once they've selected their preferred dates and times for the rental period.

@app.route('/delete_item', methods=['POST'])
Template: customer_cart.html

This route deletes the equipment item from the shopping cart when the customer decides not to proceed with the rental.

@app.route('/edit_details', methods=['POST', 'GET'])
Template: customer_cart.html

This route allows customers to modify the equipment rental duration and quantity in the shopping cart, providing flexibility in case they have a change of mind.
@app.route('/payment', methods=['POST', 'GET'])
Template: payment.html

This route renders the page for customer to select a payment method and view the total price of the equipment hire before clicking on “Pay Now.”

@app.route('/complete_payment', methods=['POST','get'])
Template: direct to customer_cart.html

This route completes the payment for hiring the equipment and takes the customer back to the shopping cart.

@app.route('/driver_license', methods=['POST','get'])
Template: driver_license.html

This route renders the page for customer to enter their driver’s license and have the option to upload a photo of their license.

@app.route('/hire_now', methods=['POST','get'])
Template: payment.html

This route directly leads the customer to the shopping cart page once they have chosen the equipment's start and end dates and times.

@app.route('/hire_now_driver_license', methods=['POST','get'])
Template: driver_license.html

This route renders the page for customer to enter their driver’s license and have the option to upload a photo of their license.

# Account emails and passwords

    email:
    admin@hire.com
    staff@hire.com
    customer@hire.com
    
    password:
    Userpassword1 (for every account)

# Credit

Leo played a major role in making sure the project codes functioned correctly. He is a team player who willingly assists other team members with their user stories and provides solutions on how to approach them. He has successfully completed all the user stories assigned to him in every sprint and go beyond what is expected for each sprint by completing over user stories for next week.

Nicholas has demonstrated exceptional leadership skills as the product owner by ensuring that everyone stays on task and offering assistance to team members who need help with their code. He has maintained his focus on completing the high prioritised user stories to ensure the completion of the project. His work ethic is impressive, and he consistently delivers results. Nicholas has completed all the user stories assigned to him for every sprint. 

Silver is always eager to tackle new challenges and take on additional tasks. His work on the PowerPoint presentation has been outstanding and welcomed any feedback. He was responsible for the layout of the Darfield Outdoor Hire website and delivered an impressive design which we were all proud of. Silver has consistently completed all the user stories assigned to him in every sprint. 

Jamin has been instrumental in ensuring the accuracy of spelling and grammar in the Darfield Outdoor Hire.. Her work for ensuring the adding and updating equipment function of the project worked as expected has been excellent. She successfully completed the majority of the user stories assigned to her in every sprint. 

Summer is enthusiastic about learning how to code new functions and remains focused on tasks. Her work on the testing part of the project has been exceptional and has given helpful feedback. She has completed majority of the user stories assigned to her in every sprint. 

Everyone has actively participated in all meetings and discussions, maintaining open communication about the progress of the user stories. 