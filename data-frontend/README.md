# data-frontend
Survey website for gathering data

## Requirements:
- Python 3
- Nginx

## Instructions:
- <code> pip3 install -r requirements.txt </code>
- fill the data-frontend.ini
- <code> uwsgi --ini data-fronend.ini </code>
- fill the nginx file
- <code> sudo cp data-frontend.nginx /etc/nginx/sites-available/data-frontend </code>
- <code> sudo ln -s /etc/nginx/sites-available/data-frontend /etc/nginx/sites-enabled/ </code>
- <code> sudo rm /etc/nginx/sites-enabled/default </code>
- <code> sudo nginx </code>
