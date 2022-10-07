import json
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

@app.route('/api', methods = ['GET'])
def get_data():
	
	target_link = request.args.get('link')

	data = {}
	
	options = Options()
	options.headless = True
	options.add_argument("user-agent=Chrome/106.0.5249.103")
	options.add_argument("--window-size=1920,1080")
	options.add_argument("--start-maximized")
	options.add_argument("--disable-blink-features=AutomationControlled")
	options.add_experimental_option("excludeSwitches", ["enable-automation"])
	options.add_experimental_option('useAutomationExtension', False)

	driver = webdriver.Chrome(options=options)
	driver.get(target_link)
	time.sleep(10)

	driver.find_element(By.ID, 'cookies-agree-all').click()

	product_title = driver.find_element(By.CLASS_NAME, 'pdp-title').text
	product_price = driver.find_element(By.CLASS_NAME, 'pdp-prices').text

	data[1] = product_title
	data[2] = product_price

	infos = driver.find_elements(By.CLASS_NAME, 'info')

	title1 = infos[0].find_element(By.TAG_NAME, 'h3').text
	contents1 = infos[0].find_elements(By.TAG_NAME, 'li')

	txt_contents1 = ""
	for line in contents1:
		txt_contents1 = txt_contents1 + line.text + " "

	data['Información general'] = {1: title1, 2: txt_contents1}

	title2 = infos[1].find_element(By.TAG_NAME, 'h3').text
	contents2 = infos[1].find_elements(By.TAG_NAME, 'li')

	txt_contents2 = ""
	for line in contents2:
		txt_contents2 = txt_contents2 + line.text + ""

	data['Ingredientes y alérgenos'] = {1: title2, 2: txt_contents2}

	# Nutrients
	title3 = infos[2].find_element(By.TAG_NAME, 'h4').text
	sub_title = infos[2].find_element(By.TAG_NAME, 'p').text

	trs = infos[2].find_elements(By.TAG_NAME, 'tr')
	txt_contents3 = ""

	for tr in trs:
		if (tr.get_attribute("class") == "table-row _info" or tr.get_attribute("class") == "table-sub-row _info"):
			txt_contents3 = txt_contents3 + tr.text + " "

	data['Nutrientes'] = {1:title3, 2: sub_title, 3: txt_contents3}

	title4 = infos[4].find_element(By.TAG_NAME, 'h3').text
	contents4 = infos[4].find_elements(By.TAG_NAME, 'li')

	txt_contents4 = ""
	for line in contents4:
		txt_contents4 = txt_contents4 + line.text
	return jsonify(data)


app.run(debug=True)