#Automated script to claim the free packepub book of the day to your packtpub account.
#Author D.N. Amerasinghe <nivanthaka@gmail.com>
#!/usr/env python

import requests
from lxml import html
import sys

session_requests = requests.session()

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

login_url = "https://www.packtpub.com/packt/offers/free-learning"
parent_url = "https://www.packtpub.com"

result = session_requests.get(login_url, headers = headers)

tree = html.fromstring(result.text)

#print result.text

authenticity_token = list(set(tree.xpath("//input[@name='form_build_id']/@value")))[0]

if authenticity_token is None:
    sys.exit(1)

payload = {
	"email": "<LOGIN EMAIL>", 
	"password": "<LOGIN PASSWORD>",
	"form_id" : "packt_user_login_form",
	"form_build_id" : authenticity_token
}

result = session_requests.post(
	login_url, 
	data = payload,
	headers = headers
)
#headers = dict(referer=login_url)

#print result.text

logged_in_chk = list(set(tree.xpath("//div[@id='account-bar-logged-in']")))[0]

#print logged_in_chk

if logged_in_chk is None:
    print "Unable to login. Exiting...."
    sys.exit(1)
    
else:
    print "Logged in..."
    
claim_url = list(set(tree.xpath("//a[@class='twelve-days-claim']/@href")))[0]
claim_url = parent_url + claim_url
#print claim_url
session_requests.get(claim_url, headers = headers)


