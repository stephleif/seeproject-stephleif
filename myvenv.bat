python -m venv myvenv
myvenv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
django-admin.exe startproject mysite .
cp settings.txt mysite/settings.py
python manage.py migrate
python manage.py startapp blog
python manage.py makemigrations blog
python manage.py migrate blog
cp admin.txt blog/admin.py
python manage.py createsuperuser

