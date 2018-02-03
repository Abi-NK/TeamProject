<h1>CS2810 Team Project Team 5</h1>
<h5>Django Tutorial v.2.0.1 for FreeBSD</h5>
<p>This is the Django tutorial on creating web apps. Using FreeBSD, Python 3 and Django 2.0.1.</p>
<h2>Getting Started</h2>
<p>Download git via your operating systems package manager or download the GUI at https://git-scm.com/downloads, alternativly to compile from source, visit https://git-scm.com/downloads, or use wget https://github.com/git/git</p>
<p>Using github, 'clone' the RMS repository and checkout branch 'tutorial-Rodney'.</p>
<code>git clone https://github.com/RHUL-CS-Projects/TeamProject2018_05.git && cd TeamProject2018_05</code>
<code>git checkout tutorial-Rodney</code>
<h2>Prerequisites</h2>
<li>Git</li>
<li>FreeBSD 12</li>
<li>Python 3.5 - 3.7</li>
<li>Django 2.0.1</li>
<li>SQLite 3</li>
<h2>Installing</h2>
<li>Database setup / re-cache</li>
<code>python3 manage.py migrate</code>
<li>Django re-cache Models</li>
<p>In the example below, polls is the application name, contained in a folder called polls.
<code>python3 manage.py makemigrations polls && python3 manage.py migrate</code>
<li>Create Django Superuser for admin</li>
<code>python3 manage.py createsuperuser</code>
<p>Enter a username, email, and password, run the server, and visit the admin page below to login with your username and password.</p>
<li>Run the server locally</li>
<p>python3 manage.py runserver</p>
<p>Polls App Page: <a href= "http://127.0.0.1:8000/polls/">http://127.0.0.1:8000/polls/</a></p>
<p>Admin Page: <a href= "http://127.0.0.1:8000/admin/">http://127.0.0.1:8000/admin/</a></p>
<p>Visit the above links</p>
<h2>Running the tests</h2>
<li>Identify a bug from the shell</li>
<p>Call the function from the shell to see a false positive, or confirm bug exists.</p>
<code>python3 manage.py shell</code>
<li>Create a test to expose the bug</li>
<p>All tests have a def begining with'test_' in the polls/tests.py file</p>
<code>gedit polls/tests.py</code>
<li>Running Tests</li>
<p>Issue the command below to run all of the tests in polls/tests.py</p>
<code>python3 manage.py test polls</code>
<li>Fixing the bug and confirm fix by re-running tests</li>
<p>Edit the required file to fix the bug, e.g. polls/models.py, and run the test again.</p>
<code>gedit polls/models.py</code>
<code>python3 manage.py test polls</code>
<h2>Deployment</h2>
<p>Edit the mysite/settings.py file to include the below.
<li>Set Debug to false</li>
<code>DEBUG = False</code>
<li>Change secret key must be a large random value and it must be kept secret</li>
<code>import os<br>
SECRET_KEY = os.environ['SECRET_KEY']</code>
<p>Or from a file</p>
<code>with open('/etc/secret_key.txt') as f:<br>
SECRET_KEY = f.read().strip()</code>
<li>Set ALLOWED_HOSTS</li>
<code>ALLOWED_HOSTS = ['example.com']</code>
<li>Redirect all server HTTP traffic to HTTPS, only HTTPS to Django</li>
<code>CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True</code>
<p>Run checks to go live.</p>
<code>python3 manage.py check --deploy</code>
<p>Any additional error please refer to the documentation at https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/</p>
<h2>Built With</h2>
<li>FreeBSD 12 - The operating system</li>
<li>Django 2 - The web framework</li>
<li>IDE - Gedit</li>
<h3>Optional</h3>
<li>Heroku - Dependency Management and Hosting</li>
<h2>Versioning</h2>
<p>There will only ever be one version released and this code will not be maintained with future Django Updates.</p>
<h2>Authors</h2>
<li>Rodney Olav C. Melby - Royal Holloway University London</li>
<h2>License</h2>
<p>This group project is licensed under the GPLV1 License - see https://www.gnu.org/licenses/old-licenses/gpl-1.0.en.html for details.</p>
<h2>Acknowledgments</h2>
<p>Thanks to GitHub, GNU, Django, Heroku, and Royal Holloway University London</p>
