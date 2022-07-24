from selenium import webdriver
from selenium.webdriver.common.by import By
import yaml
import os
import time
import argparse
import sys

def read_conf(path_to_conf : str):
    with open(path_to_conf) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def delete_unfinished_downloads(save_path : str):
    for (dirpath, _, filenames) in os.walk(save_path):
        for filename in filenames:
            if '.crdownload' in filename:
                os.remove(dirpath+'/'+filename)

def login(driver, username, password):
    driver.get('https://elearning.di.uniba.it/login')
    txtUsername = driver.find_element(By.ID, 'username')
    txtPassword = driver.find_element(By.ID, 'password')
    btnLogin = driver.find_element(By.ID, 'loginbtn')

    txtUsername.send_keys(username)
    txtPassword.send_keys(password)
    btnLogin.click()

def get_subjectsPages(driver):
    subjectsPages = {}
    subjectsDropdown = driver.find_element(By.ID, 'dropdownmain-navigation0').find_elements(By.TAG_NAME, 'li')
    for subject in subjectsDropdown:
        a = subject.find_element(By.TAG_NAME, 'a')
        subjectsPages[a.get_attribute('title')] = a.get_attribute('href')

    return subjectsPages

def get_unique_hrefs(resources):
    hrefs = []
    for resource in resources:
        hrefs.append(resource.get_attribute('href'))
    return list(dict.fromkeys(hrefs))

def are_all_downloads_completed(save_path):
    for (_, _, filenames) in os.walk(save_path):
        for filename in filenames:
            if '.crdownload' in filename:
                return False

    return True

def download_resources(driver, subjectsPages, save_path):
    for name in subjectsPages.keys():
        print(f'\nDumping subject: {name}...')
        driver.get(subjectsPages[name])
        download_path = save_path + '/' + name
        params = { 'behavior': 'allow', 'downloadPath': download_path }
        driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
        resources = driver.find_elements(By.CSS_SELECTOR, 'a[href*=\'mod/resource\']')
        hrefs = get_unique_hrefs(resources)
        for href in hrefs:
            print(f'\tDownloading {href}...')
            try:
                driver.get(href)
            except:
                print(f'\tCould not download resource {href}')
        
    while not are_all_downloads_completed(save_path):
        time.sleep(2)

def main():
    arg_parser = argparse.ArgumentParser(description='A Python script to dump resources from ADA e-learning platform @ DIB UniBa.')
    arg_parser.add_argument('-d', '--save-path', type=str, dest='save_path', help='Base path to save dumped resources')
    arg_parser.add_argument('-c', '--conf-path', type=str, dest='conf_path', help='Configuration file')
    args = arg_parser.parse_args(sys.argv[1:])

    if args.save_path is None:
        args.save_path = os.getcwd()

    options = webdriver.ChromeOptions()
    preferences = {
            "download.default_directory": args.save_path,
            "plugins.always_open_pdf_externally": True,
            }
    options.add_experimental_option('prefs', preferences)
    driver = webdriver.Chrome(options=options)

    # Clear unfinished downloads
    print('Cleaning unfinished downloads files...')
    delete_unfinished_downloads(args.save_path)
    
    # TODO: Pass conf path as argument
    if args.conf_path is None:
        args.conf_path = 'conf.yml'
    conf = read_conf(args.conf_path)

    login(driver, conf['username'], conf['password'])

    subjectsPages = get_subjectsPages(driver)
    print('Found subjects:')
    for subject in subjectsPages:
        print(f'\t{subject}')
    print()
    download_resources(driver, subjectsPages, args.save_path)
       
    
if __name__ == '__main__':
    main()
