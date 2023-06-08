# django_shop_m89_final

# Features
- jalali datetime with persian month and number
- profile SPA
- cart SPA
- can apply simple or nested comment system (0 to N level nested)
- can apply soft-delete on every model
- can apply soft-delete as `SOFT_CASCADE` instead `model.CASCADE` (currently implement on comment model as sample)
- create navigation-bar base nested category (can show or hide specific category)
- anonymous user cart store in session. after login, cart in session merge with user cart in database (update or create new one)
- register system apply verification email to activate user profile
- login system apply 2-step-verification with OTP-code (send via SMS or EMAIL base on user select)
- use celery for task (email and sms)
- use redis for cash and celery broker
- postgres settings include
- product detail as json (can use different detail `key:value` for any product)
- discount on product or category
- magic sale
- JWT authentication (include admin panel access)
- middleware and mixin for jwt user authentication
- permission for access to admin panel item
- some customization in admin panel for usability (search field, filter, item detail, ...)


## How to use
1. clone repository or download zip file

2. create python env and activate
   - `python -m virtualenv venv --python=python3.10`
   - `source venv/bin/activate`
3. install requirements
  - `pip install requirements.txt`
4. all migrations include in repository you can only run `python manage.py migrate` or delete all migrations from all app and run `python manage.py makemigrations && python manage.py migrate`
5. runserver `python manage.py runserver`
