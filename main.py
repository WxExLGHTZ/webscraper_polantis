from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
import zipfile


# ask for log in creds
u_name = ""
u_password = ""
login_cred_empty = True

def logincred():
    os.system('clear')
    u_name = input('Username für https://www.polantis.com : ')
    u_password = input('Passwort für https://www.polantis.com : ')
    return u_name, u_password

while(login_cred_empty):
    if(u_name == "" or u_password == ""):
        print("Bitte Log in und Passwort eingeben")
        u_name, u_password = logincred()
    else:
        login_cred_empty = False



# create directories
parent_dir = os.getcwd()

dir_for_one_piece = "ikea_einteilig"
dir_for_multi_piece = "ikea_mehrteilig"

dir_for_one_piece_zip = "ikea_einteilig_zips"
dir_for_multi_piece_zip = "ikea_mehrteilig_zips"

dir_for_one_piece_obj = "ikea_einteilig_obj"
dir_for_multi_piece_obj = "ikea_mehrteilig_obj"

path_1 = os.path.join(parent_dir, dir_for_one_piece)
path_2 = os.path.join(parent_dir, dir_for_multi_piece)

path_1_zip = os.path.join(path_1, dir_for_one_piece_zip)
path_2_zip = os.path.join(path_2, dir_for_multi_piece_zip)

path_1_obj = os.path.join(path_1, dir_for_one_piece_obj)
path_2_obj = os.path.join(path_2, dir_for_multi_piece_obj)

if not os.path.exists(path_1):
    os.mkdir(path_1)

if not os.path.exists(path_2):
    os.mkdir(path_2)

if not os.path.exists(path_1_zip):
    os.mkdir(path_1_zip)

if not os.path.exists(path_2_zip):
    os.mkdir(path_2_zip)

if not os.path.exists(path_1_obj):
    os.mkdir(path_1_obj)

if not os.path.exists(path_2_obj):
    os.mkdir(path_2_obj)


# path to driver location
PATH = os.getcwd() + "/chromedriver"

# change download directory to ikea_einteilig
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : path_1}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(executable_path=PATH,options=chrome_options)

# open website
driver.get("https://www.polantis.com/ikea")

# log in to website
driver.execute_script("document.getElementById(\"dropdownLoginMenuLink\").click();")

username = driver.find_element(By.ID, 'UserName')
password = driver.find_element(By.ID, "Password")

username.send_keys(u_name)
password.send_keys(u_password)
driver.find_element(By.ID, "submitLoginButton").click()

# check if log in was successful
errorbox = False
error_icon = False
try:
    errorbox = driver.find_element(By.CLASS_NAME, "validationMessageTextContainer").is_displayed()
    error_icon = driver.find_element(By.CSS_SELECTOR, ".form-field-error").is_displayed()
except:
    print("Login erfolgreich!")


if(errorbox == True or error_icon == True):
    print("Log in oder Passwort falsch!")
else:

    # Load all objects by scrolling
    SCROLL_PAUSE_TIME = 10

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # check all checkboxes
    click = "document.querySelectorAll('input[type=\"checkbox\"]').forEach(el=>el.click())"
    driver.execute_script(click)


    # get id of each element
    ids = driver.execute_script(
       ''' shapes = []; document.querySelectorAll('input[type="checkbox"]').forEach(el=> shapes.push((el.value))); return shapes ''')

    # list of "einteilig"
    ids_one_piece =[]

    # list of "mehrteilig"
    ids_multi_piece = [207, 96, 8639, 110, 75, 1118, 216, 235, 87, 919, 94, 101, 905, 1114, 108, 233, 92, 93, 62, 234, 106,
                       79, 109, 102, 8638, 90, 874, 95, 615, 8631, 97, 15229, 236, 569, 111]

    # seperate one piece & multi piece objects
    ids_one_piece = [i for i in ids if int(i) not in ids_multi_piece]


    # download obj files ( one piece )
    for c_id in ids_one_piece:
        url = "https://www.polantis.com/download/obj/" + str(c_id) +"/checked"
        driver.get(url)

    driver.quit()


    # change download directory to ikea_mehrteilig
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : path_2}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path=PATH,options=chrome_options)

    # open website
    driver.get("https://www.polantis.com/ikea")

    # log in to website
    driver.execute_script("document.getElementById(\"dropdownLoginMenuLink\").click();")

    username = driver.find_element(By.ID, 'UserName')
    password = driver.find_element(By.ID, "Password")

    username.send_keys(u_name)
    password.send_keys(u_password)
    driver.find_element(By.ID, "submitLoginButton").click()

    # download obj files ( multi peace )
    for c2_id in ids_multi_piece:
        url = "https://www.polantis.com/download/obj/" + str(c2_id) +"/checked"
        driver.get(url)

    driver.quit()


    # sort downloaded files
    # iterate "ikea_einteilig" directory
    for path in os.listdir(path_1):
        # check if current path is a file
        if os.path.isfile(os.path.join(path_1, path)):

            src_path = os.path.join(path_1, path)
            dst_path = os.path.join(path_1_zip, path)

            # move zip files to zip directory
            os.rename(src_path,dst_path)

            # extract zips to Obj dierectory
            with zipfile.ZipFile(dst_path, 'r') as zip_ref:
                zip_ref.extractall(path_1_obj)

    # iterate "ikea_mehrteilig" directory
    for path in os.listdir(path_2):
        # check if current path is a file
        if os.path.isfile(os.path.join(path_2, path)):
            src_path = os.path.join(path_2, path)
            dst_path = os.path.join(path_2_zip, path)

            # move zip files to zip directory
            os.rename(src_path, dst_path)

            # extract zips to Obj dierectory
            with zipfile.ZipFile(dst_path, 'r') as zip_ref:
                zip_ref.extractall(path_2_obj)


    # count one_peace_obj
    count_one_piece = 0
    for dir_1 in os.listdir(path_1_obj):
        count_one_piece += 1
    print("einteilig: " + str(count_one_piece))


    # count multi_peace_obj
    count_multi_piece = 0
    for dir_2 in os.listdir(path_2_obj):
        count_multi_piece += 1
    print("mehrteilig: " + str(count_multi_piece))


