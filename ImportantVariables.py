import os
from tokenize import cookie_re

# current_Folder_Path="E:/my_money_pointer"


recovery_code = "43870954"

file_path = os.path.abspath(__file__)
# print(file_path)
current_Folder_Path = os.path.dirname(file_path)
# print(current_Folder_Path)
# print(os.path.join(current_Folder_Path,"my_money_pointer"))

# print(root_folder)
yt_links_for_facebook = "/json_files/yt_links_for_facebook.json"


GITHUB_LOCAL_FILE_PATH = current_Folder_Path+"/daily_update.txt"
GITHUB_OWNER = "niharika17032001"
TOKENS_FILE_PATH="/tokens.json"
TOKENS_LOCAL_FILE_PATH = current_Folder_Path+"/tokens.json"
GITHUB_google_log_in_REPO = "google_log_in"




page_source_html= current_Folder_Path+"/reports/page_source.html"
reports_path = current_Folder_Path + '/reports/'
screenshot_path = reports_path + 'screenshot'
imp_json_files_folder = current_Folder_Path + "/imp_json_files/"
cookies_txt_file=reports_path+"main_cookies.txt"
cookie_json_file=reports_path+"main_cookies.json"
load_cookie_json_file=imp_json_files_folder+"main_cookies.json"
new_user_data_directory = current_Folder_Path + '/Chrome/new_user_data_directory'
download_dir = current_Folder_Path +"/download"
google_user_data_directory = current_Folder_Path +'/Chrome/google_user_data_directory'
imp_json_files_folder_id = "1xjvtIZXSwpSaZS4uS0YRzhDEQuR_wgVu"

print("new_user_data_directory : \t", new_user_data_directory)

if not os.path.exists(new_user_data_directory):
    os.makedirs(new_user_data_directory)
if not os.path.exists(reports_path):
    os.makedirs(reports_path)


chrome_driver_path=current_Folder_Path +"/chromedriver.exe"
chrome_executable_path	=current_Folder_Path + "/chrome.exe"