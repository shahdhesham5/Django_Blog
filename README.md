# Django_Blog
Our blog is built using Django, Bootstrap, and JavaScript.\
Users don't have to sign up to view posts, yet they will need to login to
be able to post, like and comment on posts.
Posts are categorized, which makes it easier to reach your desired category.
Searching by tags and posts' titles is also available in our blog.
hope you enjoy it.


## Content
* [Setup](#setup)
* [Usage](#usage)
* [Features](#features)
* [Demo](#demo)
* [Authors](#authors)



## Setup

```bash
git clone https://github.com/shahdhesham5/Django_Blog.git
```
- The project doesn't include the settings.py, but you can download it from this link.
[settings.zip](https://github.com/shahdhesham5/Django_Blog/files/8089427/settings.zip)
- Make sure to install
    -   `pip install fontawesome-free`
    -   `pip install pymysql`
- Create database called blogdb in MySQL, and use the USERNAME and PASSWORD for your database in settings.py.
- On your admin panel make sure to create two groups, admin and blockedusers.
- You must create a Superuser and add it to admin group that you created.
- To be able to send emails, make sure to change email settings in settings.py which EMAIL_HOST_USER and EMAIL_HOST_PASSWORD.
- The email you will use, you must allow low security apps from its settings.


## Usage
Once the project is all set, activate your env, run the server, and go to url: (your localhost server)/blogapp/home/

## Features
For Admins they can:
-  promote normal users to be admins.
-  Block/unblock/delete users.
-  CRUD on posts, comments, categories, tags.

For logged in Users they can:
- post, like and comment.
- delete and edit their posts.
- send messages to the admin in case they got blocked.


## Demo



## Authors

- Created by 
    - [@ranawael1](https://github.com/ranawael1)
    - [@shahdhesham5](https://github.com/shahdhesham5 ) 
    - [@sohila-mo](https://github.com/sohila-mo) 
    - [@shadybassily](https://github.com/shadybassily) 



