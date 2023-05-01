from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver
import user_data
import time

if __name__ == '__main__':

    driver = undetected_chromedriver.Chrome()

    # Dostanie sie do panelu logowania:
    driver.get("https://www.zalando-lounge.pl/#/")
    time.sleep(1)
    if driver.current_url != "https://www.zalando-lounge.pl/#/":
        driver.find_element(By.XPATH, "//button[@aria-labelledby='close-modal-message']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//button//span[contains(text(),'aloguj')]").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//button//span[contains(text(),'aloguj')]").click()

    # Logowanie:
    WebDriverWait(driver, 2).until(expected_conditions.visibility_of_element_located((By.ID, "form-email")))
    driver.find_element(By.ID, "form-email").send_keys(user_data.user_email2)
    driver.find_element(By.ID, "form-password").send_keys(user_data.user_password2)
    driver.find_element(By.XPATH, "//button[@aria-labelledby='login-form-submit']").click()

    # Page reloader
    product_link = input("Enter reserved product link: ")
    wanted_size = str(input("Enter size (format: 44 or L): "))
    size_locator = "//section[@aria-labelledby='article-size-title']//button//span[text()='" + wanted_size + "']"
    add_to_cart = "//div[@id='addToCartButton']/button"

    driver.get(product_link)

    is_available = driver.find_element(By.XPATH, size_locator + "/parent::button").is_enabled()
    reserved_locator = size_locator + "/following-sibling::span/span[contains(text(), 'arezerwowane')]"

    if is_available:
        driver.find_element(By.XPATH, size_locator).click()
        driver.find_element(By.XPATH, add_to_cart).click()

    while not is_available:
        time.sleep(3)
        driver.refresh()

        is_available = driver.find_element(By.XPATH, size_locator + "/parent::button").is_enabled()

        if not is_available:
            try:
                driver.find_element(By.XPATH, reserved_locator)

            except NoSuchElementException:
                print("Sprzedane")
                break

        else:
            driver.find_element(By.XPATH, size_locator).click()
            driver.find_element(By.XPATH, add_to_cart).click()

    input("Type anything to close: ")
