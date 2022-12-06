**Starting The Application**
-
To start the application, all you need
to do is start the python file named `wsgi.py`

The application will be hosted on your local host
on port `5000` by default. This application
is not meant to be a production-level web application.

**Pre-loaded data:**
-
* 2 Users
* 3 Vehicles

There are two users preloaded
that take part in the blockchain
process. One user (user@gmail.com)
is simply the customer, and can buy
any available vehicles that are not
already present, and bought in the
blockchain. The other user (vendor@gmail.com)
is a vendor, and can add vehicles, making
them available to customers for 
the set price. 

It is worth noting that neither
of these emails are real.

New *customers* can be added at
signup, however there is no way
to add new vendors for this
demonstration. Passwords added 
to the database are hashed
however, should not be relied
on regardless.

**Credentials**
-
* user@gmail.com / 123
* vendor@gmail.com / 123

**Pages:**
-
* /
* /login
* /logout
* /signup
* /<user_type>/dashboard
* /transactions
* /chain/view
