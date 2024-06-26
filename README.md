﻿# YfinanceDjangoApp
#### 1. Clone the app from github to your local PC.
Simply create a new folder, for example on your Desktop and then use your editor, for example VS Code to cd into this created folder. 
Run the cloning command in the terminal. **git clone https://github.com/kevinopix/YfinanceDjangoApp.git**
#### 2. Create a file named .env and add a variable called DJANGO_SECRET_KEY, for which you would have a secret key value for the app. Such a value would be a mix of letters and numbers
An example would be DJANGO_SECRET_KEY=d3d*7&fiurenfasu&6+=u_1jtt6vw6%q@pd_tmf=g$@)k-rc!e99(4b(p2+jas+h&k6
#### 3. Activate a virtual environment within the folder.
This will be required to install necessary packages which will be required to successfully operate the application.
#### 4. Install the necessary packages.
To do this, make sure you cd into the application where the requirements.txt file exists and then run the command.
**pip install -r requirements.txt**
#### 5. Run: python manage.py makemigrations
This is going to prepare the models created (data tables)
#### 6. Run: python manage.py migrate
This will create the tables and ensure necessary relationships are made.
#### 6. Run: python manage.py collectstatic
This will save static files needed to run the applications in the static files location you have provided.
These include inbuilt CSS and Javascript used to render the admin side, by default. 
On localhost, you should be able to see a staticfiles folder created, from where the static files are saved.
#### 7. Run: python manage.py createsuperuser
Follow the prompts, add a username and password, to allow access to the Django admin side. This will be critical, so take note of the username and password used.
#### 8. Run: python manage.py runserver
This command will start up the server and you should be able to access the app from http://127.0.0.1:8000/
Accessing the admin side would be http://127.0.0.1:8000/admin
#### 9. Run: python manage.py import_companies ValidStockSymbols.csv
There exists a file called **import_companies.py** within the **company/management/commands** folder. The command utilizes the **ValidStockSymbols.csv** file attached and pushes the company records to the database created. The default database is a sqlite3 database. For application in production, this would need to be updated from a sqlite database to a PostgreSQL database, preferrably.
Run server again and check in the admin that the data is saved in DB. http://127.0.0.1:8000/admin
#### 10. Run: python manage.py import_stockinfo ValidStockInfo.parquet
There exists another file called **import_stockinfo.py** within the **company/management/commands** folder. The command utilizes the **ValidStockInfo.parquet** file attached and pushes the stock info records to the database created. This command takes a while to run since there exists more than 500k records. Make yourself a cup of coffee, or tea.
Run server again and check in the admin that the data is saved in DB. http://127.0.0.1:8000/admin
#### 11. Run: python manage.py import_company_metrics
There exists another file called **import_company_metrics.py** within the **company/management/commands** folder. The command utilizes the StockInfo data pushed to look for the latest records by each company. Storing this as a separate dataset reduces the time that would be required to access each company's latest record. Plus other details like first recorded date and all. 
Run server again and check in the admin that the data is saved in DB. http://127.0.0.1:8000/admin
#### 12. View App And Details
#### 13. Navigate to http://127.0.0.1:8000/dataTool/pull and utilize the functionality to check for new values based on the latest record date by company and push these new values to the database. 
This can be a task performed at specific times during the day or night, using a CRON job.