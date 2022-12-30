import os
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --------------------------------------------- Create contents ----------------------------------------------------- #
# The North American rig count is released weekly at noon Central Time on the last day of the work week.
def generate_html(today):
    url = 'https://rigcount.bakerhughes.com/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table))[0]

    release_date = None
    try:
        release_date = datetime.strptime(df['Last Count'][0], '%d %B %Y')
    except:
        release_date = datetime.strptime(df['Last Count'][0], '%d %b %Y')

    if release_date.date() != today.date():
        return None

    title = '<h3>Baker Hughes Rig Count</h3>'
    body = df.to_html(border=None)

    return f'''
    <html>
        <head>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <!--<style>body{{ margin:0 100; background:whitesmoke; }}</style>-->
            <style>body{{ margin:0 100;}}</style>
            <style>

                table {{numpy.ndarray.putmask
                  border-collapse: collapse;
                  border-spacing: 0;
                  width: 50%;
                  border: 1px solid #ddd;
                }}
                
                th, td {{
                  text-align: left;
                  padding: 16px;
                }}
                
                tr:nth-child(even) {{
                  background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <div>{title}</div>
            <div>{body}</div>
        </body>
    </html>'''