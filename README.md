# technooka-task

git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

python -m venv venv
venv\Scripts\activate 

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py runserver

http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/redoc/
