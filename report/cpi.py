import os
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# --------------------------------------------- Create contents ----------------------------------------------------- #
# From BLS, monthly, begining of next month. one-month seasonal-adjustment cpi
def generate_html(today):
    url = 'https://www.bls.gov/feed/bls_latest.rss'
    page = requests.get(url)
    content = page.content.decode('utf-8')
    soup = BeautifulSoup(page.content, 'lxml')

    ss = soup.find_all('span')[0].text
    ss_month = ss.split(' ')[-2]

    first = today.replace(day=1)
    lastMonth = first - timedelta(days=1)
    lastMonth = lastMonth.strftime("%B")

    if ss_month != lastMonth:
        return None

    title = '<h3>Consumer Price Index, seasonally adjusted</h3>'
    body = ss

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
            <div><a href="https://fred.stlouisfed.org/series/CPIAUCSL">Historical from Fred</a> </div>
        </body>
    </html>'''