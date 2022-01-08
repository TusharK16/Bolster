import re
import os
import crud
import datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def extract_natural_lang(content):
    cleantext = BeautifulSoup(content, "lxml").text
    res = re.sub('\n+', '\n', cleantext)
    final_text = re.sub(' +',' ',res)
    return final_text.strip()

def form_json(url,path_to_screenshot,ip_address,redirect_url,ssl_certificate,page_source,page_nl):
    json_obj = {}
    json_obj['url'] = url
    json_obj['screenshot'] = path_to_screenshot
    json_obj['ip_address'] = ip_address
    json_obj['redirect_url'] = redirect_url
    json_obj['ssl_certificate'] = ssl_certificate
    json_obj['page_source'] = page_source
    json_obj['page_natural_language'] = page_nl
    json_obj['asn'] = None
    return json_obj

def run(playwright,url):
    try:
        chromium = playwright.chromium # or "firefox" or "webkit".
        browser = chromium.launch()
        page = browser.new_page()
        response = page.goto(url)
        redirect = False

        #Check for redirect
        new_url = page.url
        if new_url != url:
            redirect = True
            page.wait_for_load_state("networkidle")

        #Take Screenshot
        time = datetime.datetime.now()
        screenshot_url = 'screenshots/'+str(time)+'.png'
        page.screenshot(path=screenshot_url)

        #IP Address
        ip_address = response.server_addr()['ipAddress']

        #SSL Certificate
        ssl_certificate = response.security_details()

        #Page Source
        page_source = page.content()

        #Extract Natural Language
        natural_lang = extract_natural_lang(page_source)

        browser.close()
        json_obj = form_json(url,screenshot_url,ip_address,new_url,ssl_certificate,page_source,natural_lang)
        crud.insert_row('bolster','site_info',json_obj)
        print("Execution Done")
        return True
    except:
        print('Execution Failed')
        import traceback
        print(traceback.format_exc())
        return False

def call_me(data):
    url = data['url']
    with sync_playwright() as playwright:
        status = run(playwright,url)
        if status:
            return {'status':'Completed'}
        else:
            return {'status':'Failed'}