from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

table = soup.find('table',attrs={'class':'table table-striped table-hover table-hover-solid-row table-simple history-data'})
tr = table.find_all('tr')
temp = [] #initiating a tuple

for i in range(1, len(tr)):
#insert the scrapping process here
    row = table.find_all('tr')[i]
    
    #get date
    date = row.find_all('td')[0].text
    date = date.strip() #for removing the excess whitespace
    
    #get weekday
    weekday = row.find_all('td')[1].text
    weekday = weekday.strip() #for removing the excess whitespace

    #get rate
    rate = row.find_all('td')[2].text
    rate = rate.strip() #for removing the excess whitespace

    temp.append((date,weekday,rate))  

temp = temp[::-1]

#change into dataframe
data = pd.DataFrame(temp, columns = ('Date','Weekday','Rate_IDR'))

#insert data wrangling here
data['Rate_IDR'] = data['Rate_IDR'].str.replace(" IDR","")
data['Rate_IDR'] = data['Rate_IDR'].str.replace(",","")
data['Rate_IDR'] = data['Rate_IDR'].astype('float64')
data['Date'] = data['Date'].astype('Datetime64')
data['Weekday'] = data['Weekday'].astype('category')
data = data.set_index('Date')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'IDR {data["Rate_IDR"].mean().round(2)}'
	card_datamin = f'IDR {data["Rate_IDR"].min().round(2)}'
	card_datamax = f'IDR {data["Rate_IDR"].max().round(2)}'    

	# generate plot
	ax = data.plot(figsize = (20,9))
	
	# Rendering plot
	# Do not change this
	
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]
    
	# render to html
	return render_template('index.html',
		card_data = card_data,
		card_datamin = card_datamin,
		card_datamax = card_datamax,                               
		plot_result=plot_result                             
		)


if __name__ == "__main__": 
    app.run(debug=True)
