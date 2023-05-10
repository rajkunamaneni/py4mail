# py4mail
An email application created with py4web

## Description:
We are developing a Email Application with standard features like handling multiple accounts, sending and receiving emails, and a chat functionality. Our implementation approach is similar to that of Gmail, and we aim to incorporate the features mentioned above.

Our previous project, Assignment 3, involved creating a table to store information about birds. For this email application, we plan to expand on that concept, integrating additional features like a delete button and a email favoriting functionality to enhance the user experience. 

We have a plan to include a chat feature in our email web application, provided we have sufficient time to develop it alongside the Gmail clone's core features. The chat functionality would enable users to exchange messages with each other. However, this will be an additional feature that we may implement if time permits.

This project will require multiple html pages and databases to separate the data and information. The idea would create a seamless user experience so that user can gather information and display information. 

## Design:
This [Google Documentation](https://docs.google.com/document/d/1RwccH8KHGmGwVgCk6Ct0DpWRstz1xQFKqzbVGp4U9hM/edit?usp=sharing) has our group design demo of our project. 

## User Stories:
The first task a new user to our email web application will do is create an account. On this starting page, if a user already has an account, they can simply type their usernames and passwords in and then click “login.” If they want to create a new account, they can click “sign up” where they’ll be navigated to a sign up page. 

Here, the user will be asked to choose an email address, a password, give their first name and last name. Once account creation is complete, the user will be navigated to a page with their main inbox. 

Think of this page as a user's “homepage.” Here, the user will have a variety of functionalities to choose from. They will be able to view emails they’ve received as a list, click on individual emails to view more details and the content of the emails on a different page, and can choose to delete or star any email on their list. 

Outside of the list of emails in the inbox, the user will have a navbar available where they’ll have buttons that they can click. These buttons will consist of their sent emails, starred emails, and deleted emails.

All three of these pages are very similar to the “homepage” with a key difference of what’s highlighted in the navbar and what the user views. For example, the sent page will have the “sent” button highlighted and display a list of all the emails the user has sent rather than every email as done in the “homepage. The deleted emails and starred emails will work in a similar manner.

Below the navbar but above the list of emails, the user will have a “Search bar.” Here, they can search for emails by whoever sent the email. In the case of the page with sent emails, it will instead display whoever the user sent the email to.

If we have time, we will also implement an end-to-end chat feature similar to the one on gmail. We don’t have implementation details for this yet as this is out of the scope of our project but if we have time, we’ll add it to the scope and work it out.

## Implementation Plan:

Our group of four members has divided the tasks in our development plan, starting with using the starter code from Assignment 2 that includes the login database and page. We will customize the login page to match our design, and all team members will work together to implement the design and backend to ensure we are on the same page throughout the process.

After completing the home page, each team member will work on a specific logic piece. For instance, we will have a separate page for the Starred emails, which will require a corresponding backend and HTML page to hold that information. We will also create a separate Deleted page to store deleted emails, with a feature that enables the user to retrieve accidentally deleted messages.

We will create an inbox to store all emails, including the sender's and receiver's email addresses, content, and date. Each inbox will have a specific page to view the content of a particular email address. Finally, we will implement a feature to send emails to users, with the requirement that the user exists within our databases.

By splitting these tasks, we will ensure that each team member has an equal learning experience, and everyone will be able to contribute to the team's success.
