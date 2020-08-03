# online-learning-site-django
the website with django that has two type of user such as Teacher and Student.when Teacher signup to this site become staff and get some permission to can upload video and course for Student.for download course you must signup to the site.
<h1>Run Project with below Command</h1>

<h3>first create virtual env</h3>
<code>virtualenv venv<code/>

<h3>activate env<h3/>

<code>venv\Scripts\activate.bat<code/>

<h3>install django<h3/>
<code>pip install django==2.2<code/>

<h3>install requierments.txt to install django libraries<h3/>

<code>pip install -r requiermens.txt<code/>

<h3>migrate to Db<h3/>
<code>python manage.py makemigratons<code/>
<code>python manage.py migrate<code/>

<h3>run server<h3/>
<code>python manage.py runserver<code/>
