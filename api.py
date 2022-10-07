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
	time.sleep(6)

	driver.find_element(By.ID, 'cookies-agree-all').click()

	product_title = driver.find_element(By.CLASS_NAME, 'pdp-title').text
	product_price = driver.find_element(By.CLASS_NAME, 'pdp-prices').text

	infos = driver.find_elements(By.CLASS_NAME, 'info')

	title1 = infos[0].find_element(By.TAG_NAME, 'h3').text
	contents1 = infos[0].find_elements(By.TAG_NAME, 'li')

	txt_contents1 = ""
	for line in contents1:
		txt_contents1 = txt_contents1 + line.text + " "

	title2 = infos[1].find_element(By.TAG_NAME, 'h3').text
	contents2 = infos[1].find_elements(By.TAG_NAME, 'li')

	txt_contents2 = ""
	for line in contents2:
		txt_contents2 = txt_contents2 + line.text + ""

	# Nutrients
	title3 = infos[2].find_element(By.TAG_NAME, 'h4').text
	sub_title = infos[2].find_element(By.TAG_NAME, 'p').text

	trs = infos[2].find_elements(By.TAG_NAME, 'tr')
	txt_contents3 = ""

	for tr in trs:
		if (tr.get_attribute("class") == "table-row _info" or tr.get_attribute("class") == "table-sub-row _info"):
			txt_contents3 = txt_contents3 + tr.text + " "

	title4 = infos[4].find_element(By.TAG_NAME, 'h3').text
	contents4 = infos[4].find_elements(By.TAG_NAME, 'li')

	txt_contents4 = ""
	for line in contents4:
		txt_contents4 = txt_contents4 + line.text + " "

	EAN = driver.find_element(By.XPATH, '//span[contains(@itemprop, "sku")]').text

	data = {
		"title" : product_title,
		"price" : product_price,
		"Información general" : {
			"title" : title1,
			"content" : txt_contents1
		},
		"Ingredientes y alérgenos" : {
			"title" : title2,
			"content" : txt_contents2
		},
		"Nutrientes" : {
			"title" : title3,
			"sub title" : sub_title,
			"content" : txt_contents3
		},
		"Conservación y utilización" : {
			"title" : title4,
			"content" : txt_contents4
		},
		"EAN" : EAN,
	}

	return json.dumps(data)

app.run(debug=True)