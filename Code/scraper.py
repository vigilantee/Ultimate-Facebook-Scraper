import getpass
import calendar
import os
import platform
import shutil
import sys
import sysconfig
import urllib.request

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# -------------------------------------------------------------
# -------------------------------------------------------------


# Global Variables

driver = None

# whether to download photos or not
download_uploaded_photos = True
download_friends_photos = True

# whether to download the full image or its thumbnail (small size)
# if small size is True then it will be very quick else if its false then it will open each photo to download it
# and it will take much more time
friends_small_size = True
photos_small_size = True

total_scrolls = 5000
current_scrolls = 0
scroll_time = 5

old_height = 0


# -------------------------------------------------------------
# -------------------------------------------------------------

def get_facebook_images_url(img_links):
    urls = []

    for link in img_links:

        if link != "None":
            valid_url_found = False
            driver.get(link)

            try:
                while not valid_url_found:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "spotlight")))
                    element = driver.find_element_by_class_name("spotlight")
                    img_url = element.get_attribute('src')

                    if img_url.find('.gif') == -1:
                        valid_url_found = True
                        urls.append(img_url)

            except EC.StaleElementReferenceException:
                urls.append(driver.find_element_by_class_name("spotlight").get_attribute('src'))

            except:
                print("Exception (facebook_image_downloader):", sys.exc_info()[0])

        else:
            urls.append("None")

    return urls


# -------------------------------------------------------------
# -------------------------------------------------------------

# takes a url and downloads image from that url
def image_downloader(img_links, folder_name):
    img_names = []

    try:
        parent = os.getcwd()
        try:
            folder = os.path.join(os.getcwd(), folder_name)
            if not os.path.exists(folder):
                os.mkdir(folder)

            os.chdir(folder)
        except:
            print("Error in changing directory")

        for link in img_links:
            img_name = "None"

            if link != "None":
                img_name = (link.split('.jpg')[0]).split('/')[-1] + '.jpg'

                if img_name == "10354686_10150004552801856_220367501106153455_n.jpg":
                    img_name = "None"
                else:
                    try:
                        urllib.request.urlretrieve(link, img_name)
                    except:
                        img_name = "None"

            img_names.append(img_name)

        os.chdir(parent)
    except:
        print("Exception (image_downloader):", sys.exc_info()[0])

    return img_names


# -------------------------------------------------------------
# -------------------------------------------------------------

def check_height():
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != old_height


# -------------------------------------------------------------
# -------------------------------------------------------------

# helper function: used to scroll the page
def scroll():
    global old_height
    current_scrolls = 0

    t=1

    while (True):
        try:
            t+=1
            if t ==5:
                return
            if current_scrolls == total_scrolls:
                return

            old_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(driver, scroll_time, 0.05).until(lambda driver: check_height())
            current_scrolls += 1
        except TimeoutException:
            break

    return


# -------------------------------------------------------------
# -------------------------------------------------------------

# --Helper Functions for Posts

def get_status(x):
    status = ""
    try:
        status = x.find_element_by_xpath(".//div[@class='_5wj-']").text
    except:
        try:
            status = x.find_element_by_xpath(".//div[@class='userContent']").text
        except:
            pass
    return status


def get_div_links(x, tag):
    try:
        temp = x.find_element_by_xpath(".//div[@class='_3x-2']")
        return temp.find_element_by_tag_name(tag)
    except:
        return ""


def get_title_links(title):
    l = title.find_elements_by_tag_name('a')
    return l[-1].text, l[-1].get_attribute('href')


def get_title(x):
    title = ""
    try:
        title = x.find_element_by_xpath(".//span[@class='fwb fcg']")
    except:
        try:
            title = x.find_element_by_xpath(".//span[@class='fcg']")
        except:
            try:
                title = x.find_element_by_xpath(".//span[@class='fwn fcg']")
            except:
                pass
    finally:
        return title


def get_time(x):
    time = ""
    try:
        time = x.find_element_by_tag_name('abbr').get_attribute('title')
        time = str("%02d" % int(time.split(", ")[1].split()[1]), ) + "-" + str(
            ("%02d" % (int((list(calendar.month_abbr).index(time.split(", ")[1].split()[0][:3]))),))) + "-" + \
               time.split()[3] + " " + str("%02d" % int(time.split()[5].split(":")[0])) + ":" + str(
            time.split()[5].split(":")[1])
    except:
        pass

    finally:
        return time


def extract_and_write_posts(data, filename):
    try:
        f = open(filename, "w", newline='\r\n')
        f.writelines(' ID || LIKES' + '\n' + '\n')

        for x in data:
            try:

                # line = str(time) + " || " + str(type) + ' || ' + str(title) + ' || ' + str(status) + ' || ' + str(link) + "\n"
                line = str(x) + "\n"

                try:
                    f.writelines(line)
                except:
                    print('Posts: Could not map encoded characters')
            except:
                pass
        f.close()
    except Exception as e:
        print("Exception (extract_and_write_posts)", "Status =", sys.exc_info()[0], e)

    return


# -------------------------------------------------------------
# -------------------------------------------------------------


def save_to_file(name, data, status):
    """helper function used to save links to files"""
    # dealing with posts
    try:
        f = open(name, 'w', encoding='utf-8', newline='\r\n')
        extract_and_write_posts(data, name)
        f.close()
    except:
        print("Exception (save_to_file)", "Status =", str(status), sys.exc_info()[0])
    return


# ----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# https://www.facebook.com/andrew.ng.96
def scrap_data(id, scan_list, section, elements_path, save_status, file_names):
    """Given some parameters, this function can scrap friends/photos/videos/about/posts(statuses) of a profile"""
    global driver
    page = []

    if save_status == 4:
        page.append(id)

    for i in range(len(section)):
        page.append(id + section[i])
    print('page...',page, scan_list, len(scan_list))
    for i in range(len(scan_list)):
        try:
            print(i)
            print('before driver',driver, page[i], type(page[i]), id)
            driver.get(page[i])
            print('after driver')
            scroll()
            print('before find_elements_by_xpath')
            

            # timeout = 30
            # try:
            #     element_present = EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'https://www.facebook.com/abhishekjha007/posts/'))
            #     WebDriverWait(driver, timeout).until(element_present)
            # except TimeoutException:
            #     print("Timed out waiting for page to load")

            
            # data = driver.find_elements(By.XPATH, elements_path[i])
            # https://www.facebook.com/abhishekjha007/posts/
            dataPostIds = driver.find_elements(By.CSS_SELECTOR, "a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm")
            # dataLikes = driver.find_elements(By.CSS_SELECTOR, ".x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z")
            # print(len(dataPostIds), len(dataLikes))
            a = ActionChains(driver)
            res = []
            for i in dataPostIds:
                try:
                    a.move_to_element(i).perform()
                    link = i.get_attribute('href').split("?")[0]
                    # print(link)
                    if '/posts/' in link:
                        res.append(link)
                except Exception as e:
                    print('e', str(e))
            print(res, len(res))
            # for i in dataLikes:
            #     try:
            #         print(i.text)
            #     except:
            #         print(i.get_attribute('innerHTML'))
            # data = driver.find_elements(By.XPATH, "//a[contains(@href, 'https://www.facebook.com/abhishekjha007/posts/')]")

            # data = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div[3]/")
            # print('after find_elements_by_xpath', data)

            save_to_file(file_names[0], res, save_status)
            print(file_names, save_status, i)
        except Exception as e:
            print("Exception (scrap_data)", str(e))


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def create_original_link(url):
    if url.find(".php") != -1:
        original_link = "https://en-gb.facebook.com/" + ((url.split("="))[1])

        if original_link.find("&") != -1:
            original_link = original_link.split("&")[0]

    elif url.find("fnr_t") != -1:
        original_link = "https://en-gb.facebook.com/" + ((url.split("/"))[-1].split("?")[0])
    elif url.find("_tab") != -1:
        original_link = "https://en-gb.facebook.com/" + (url.split("?")[0]).split("/")[-1]
    else:
        original_link = url

    return original_link


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def thingsToScrape(id, things=None):
    if things is None:
        things=['Friends','Photos','Videos','About','Posts']
    if 'Friends' in things:
        print("----------------------------------------")
        print("Friends..")
        # setting parameters for scrap_data() to scrap friends
        scan_list = ["All", "Following", "Followers", "Work", "College", "Current City", "Hometown"]
        section = ["/friends", "/following", "/followers", "/friends_work", "/friends_college", "/friends_current_city",
                   "/friends_hometown"]
        elements_path = ["//*[contains(@id,'pagelet_timeline_medley_friends')][1]/div[2]/div/ul/li/div/a",
                         "//*[contains(@class,'_3i9')][1]/div/div/ul/li[1]/div[2]/div/div/div/div/div[2]/ul/li/div/a",
                         "//*[contains(@class,'fbProfileBrowserListItem')]/div/a",
                         "//*[contains(@id,'pagelet_timeline_medley_friends')][1]/div[2]/div/ul/li/div/a",
                         "//*[contains(@id,'pagelet_timeline_medley_friends')][1]/div[2]/div/ul/li/div/a",
                         "//*[contains(@id,'pagelet_timeline_medley_friends')][1]/div[2]/div/ul/li/div/a",
                         "//*[contains(@id,'pagelet_timeline_medley_friends')][1]/div[2]/div/ul/li/div/a"]
        file_names = ["All Friends.txt", "Following.txt", "Followers.txt", "Work Friends.txt", "College Friends.txt",
                      "Current City Friends.txt", "Hometown Friends.txt"]
        save_status = 0

        scrap_data(id, scan_list, section, elements_path, save_status, file_names)
        print("Friends Done")
        # ----------------------------------------------------------------------------
    if 'Photos' in things:
        print("----------------------------------------")
        print("Photos..")
        print("Scraping Links..")
        # setting parameters for scrap_data() to scrap photos
        scan_list = ["'s Photos", "Photos of"]
        section = ["/photos_all", "/photos_of"]
        elements_path = ["//*[contains(@id, 'pic_')]"] * 2
        file_names = ["Uploaded Photos.txt", "Tagged Photos.txt"]
        save_status = 1

        scrap_data(id, scan_list, section, elements_path, save_status, file_names)
        print("Photos Done")

        # ----------------------------------------------------------------------------
    if 'Videos' in things:
        print("----------------------------------------")
        print("Videos:")
        # setting parameters for scrap_data() to scrap videos
        scan_list = ["'s Videos", "Videos of"]
        section = ["/videos_by", "/videos_of"]
        elements_path = ["//*[contains(@id, 'pagelet_timeline_app_collection_')]/ul"] * 2
        file_names = ["Uploaded Videos.txt", "Tagged Videos.txt"]
        save_status = 2

        scrap_data(id, scan_list, section, elements_path, save_status, file_names)
        print("Videos Done")
        # ----------------------------------------------------------------------------
    if 'About' in things:
        print("----------------------------------------")
        print("About:")
        # setting parameters for scrap_data() to scrap the about section
        scan_list = [None] * 7
        section = ["/about?section=overview", "/about?section=education", "/about?section=living",
                   "/about?section=contact-info", "/about?section=relationship", "/about?section=bio",
                   "/about?section=year-overviews"]
        elements_path = ["//*[contains(@id, 'pagelet_timeline_app_collection_')]/ul/li/div/div[2]/div/div"] * 7
        file_names = ["Overview.txt", "Work and Education.txt", "Places Lived.txt", "Contact and Basic Info.txt",
                      "Family and Relationships.txt", "Details About.txt", "Life Events.txt"]
        save_status = 3

        scrap_data(id, scan_list, section, elements_path, save_status, file_names)
        print("About Section Done")

        # ----------------------------------------------------------------------------
    if 'Posts' in things:
        print("----------------------------------------")
        print("Posts:")
        # setting parameters for scrap_data() to scrap posts
        scan_list = [None]
        section = []
        # elements_path = ['//div[@class="_5pcb _4b0l _2q8l"]']
        elements_path = ['//div/div/div/div/div/div/div/div/div/div/div[8]/div/div/div[4]/div/div/div[1]/div/div[1]/div/div[2]/div[2]/span/div/span']

        file_names = ["Posts.txt"]
        save_status = 4

        scrap_data(id, scan_list, section, elements_path, save_status, file_names)
        print("Posts(Statuses) Done")
        print("----------------------------------------")

def scrap_profile(ids):
    folder = os.path.join(os.getcwd(), "Data")

    if not os.path.exists(folder):
        os.mkdir(folder)

    os.chdir(folder)

    # execute for all profiles given in input.txt file
    for id in ids:

        driver.get(id)
        url = driver.current_url
        id = create_original_link(url)

        print("\nScraping:", id)

        try:
            path = os.path.join(folder, id.split('/')[-1])
            print('path')
            print(path, folder, id)
            if not os.path.exists(path):
                print('path doesn\'t exhist', path)
                os.mkdir(path)
            else:
                print("Removing duplicate folder first and then running this code.")
                # os.rmdir(path)
                try:
                    shutil.rmtree(folder)
                    # os.path.exists(os.path.join(folder, id.split('/')[-1]))
                    # continue
                    os.mkdir(folder)
                except Exception as e:
                    print('exc....', e)
                try:
                    os.mkdir(path)
                except Exception as e:
                    print('exc.2324...', e)
            os.chdir(path)
        except Exception as e:
            print("Some error occurred in creating the profile directory. {}".format(e))
            continue

        # ----------------------------------------------------------------------------
        thingsToScrape(id, ['Posts'])
    # ----------------------------------------------------------------------------

    print("\nProcess Completed.")

    return


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def login(email, password):
    """ Logging into our own profile """

    try:
        global driver

        options = Options()

        #  Code to disable notifications pop up of Chrome Browser
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")
        # options.add_argument("headless")

        try:
            """
            darwin_(ppc|ppc64|i368|x86_64|arm64)
            linux_(i686|x86_64|armv7l|aarch64)
            windows_(x86|x64|arm32|arm64)
            """
            # platform_ = platform.system().lower()
            # if platform_ == 'darwin':
            #     machine = sysconfig.get_platform().split("-")[-1].lower()
            #     if machine=="arm64":
            #         executable_path="./chromedriver_mac_arm64"
            #     else:
            #         executable_path="./chromedriver_mac64"
            # elif platform_ == 'linux':
            #     executable_path = "./chromedriver"
            # else:
            #     executable_path="./chromedriver.exe"
            # for older linux support
            # driver = webdriver.Chrome(executable_path, options=options)
            driver = webdriver.Chrome(options=options)
        except Exception as e:
            print("Kindly replace the Chrome Web Driver with the latest one from"
                  "http://chromedriver.chromium.org/downloads"
                  "\nYour OS: {} ...***...{}".format(e)
                 )
            exit()

        driver.get("https://en-gb.facebook.com")
        driver.maximize_window()

        # filling the form
        driver.find_element('name','email').send_keys(email)
        driver.find_element('name','pass').send_keys(password)

        # clicking on login button
        driver.find_element('name','login').click()

    except Exception as e:
        print("There's some error in log in.", e)
        print(sys.exc_info()[0])
        exit()


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def main():
    ids = [line for line in open("input.txt", newline='\n')]
    print('ids', ids)
    if len(ids) > 0:
        # Getting email and password from user to login into his/her profile
        # email = input('\nEnter your Facebook Email: ')
        # password = getpass.getpass('Enter your Facebook Password: ')
        email,password = [line for line in open("credentials.txt", newline='\n')]
        email = email.strip()
        password = password.strip()

        print("\nStarting Scraping...")

        login(email, password)
        scrap_profile(ids)
        driver.close()
    else:
        print("Input file is empty..")


# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------

if __name__ == '__main__':
    # get things rolling
    main()
