# Developers and Tasks assignment system
Developed on Windows 10 using Python 3.10.0
## Setup
1. From the command prompt run `pip install -r requirements.txt`.
2. Now run `py manage.py migrate`.
3. If you'd like to access the admin environment you must first create a user: `py manage.py createsuperuser --username admin` and manually answer the questions.
4. To run the server enter `py manage.py runserver`.
5. To run the unit tests enter `py manage.py test`.
6. To access the admin panel [http://localhost:8000/admin/](http://127.0.0.1:8000/admin/)
7. If you have an IDE/app that supports `.http` files, you may utilize `manual.http` or use it as an examples file for Postman or `curl`.
8. The entry point is [http://localhost:8000/dev_tasks/](http://localhost:8000/dev_tasks/)

# Your comments are highly appreciated!