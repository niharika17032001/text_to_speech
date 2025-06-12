import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import ImportantVariables as imp_val

# Import your important variables
download_dir = imp_val.download_dir
user_data_directory = imp_val.google_user_data_directory
profile_directory = "Default"  # you can override this dynamically
chrome_driver_path = False
chrome_executable_path = False  # optional


def setup_google_chrome_driver(profile_directory="Default", headless=False):
    chrome_options = uc.ChromeOptions()

    # ✅ Download behavior
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # ✅ Set user data and profile dir (for saved login sessions)
    if user_data_directory:
        chrome_options.add_argument(f'--user-data-dir={user_data_directory}')
    if profile_directory:
        chrome_options.add_argument(f'--profile-directory={profile_directory}')

    # ✅ Optional binary (rarely needed unless using custom Chrome build)
    if chrome_executable_path:
        chrome_options.binary_location = chrome_executable_path

    # ✅ Headless mode
    if headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

    # ✅ Common anti-detection options
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-infobars")

    # ✅ Launch driver (you can pin version like version_main=136)
    try:
        driver = uc.Chrome(
            # version_main=136,  # or None for auto-detect
            options=chrome_options,
            driver_executable_path=chrome_driver_path if chrome_driver_path else None
        )
        print("this is ChromeDriverManager().install()", ChromeDriverManager().install())
        driver = uc.Chrome(
            service=Service(ChromeDriverManager().install()),
            # version_main=136,  # or None for auto-detect
            options=chrome_options
        )
    except Exception as e:
        print("❌ Error initializing undetected_chromedriver:", e)
        raise e

    return driver


if __name__ == "__main__":
    driver = setup_google_chrome_driver()
    driver.get("https://www.google.com")
    print("✅ Driver initialized successfully.")
    input("Press Enter to close...")
    driver.quit()
