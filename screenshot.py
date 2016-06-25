from os import path
from selenium import webdriver
from PIL import Image
from io import BytesIO
from flask import send_from_directory


def generate_screenshot_file(filename, baseurl, id):
    # url = path.join(baseurl, id)
    url = baseurl
    "/static/images/{}.jpg".format(id)
    driver = webdriver.PhantomJS()
    driver.set_window_size(1200, 630) # set the window size that you need
    driver.get(url)
    img = driver.get_screenshot_as_png()
    im = Image.open(BytesIO(img) )
    imr = im.resize((600,315), Image.ANTIALIAS)
    imr.save(filename, 'JPEG', quality=90)



# def get_screenshot(baseurl,id):
#     dir = "/static/images"
#     filename = "{}/{}.jpeg".format(dir,id)
#     if path.exists(filename) and path.isfile(filename):
#         return  send_from_directory(dir,filename)
#     else:
#         return generate_screenshot(filename, baseurl, id )

