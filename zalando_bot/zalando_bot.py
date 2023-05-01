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
    driver.find_element(By.ID, "form-email").send_keys(user_data.user_email)
    driver.find_element(By.ID, "form-password").send_keys(user_data.user_password)
    driver.find_element(By.XPATH, "//button[@aria-labelledby='login-form-submit']").click()

    input("Type anything to release the Bot: ")

    # Ustawianie filtrow (sortowanie -> od najnizszej):
    filters = driver.find_elements(By.XPATH, "//div[@role='tablist']//button")
    filters[5].click()  # index of sortowanie

    fil_opti_locator = "//div//input[@type='checkbox']"

    time.sleep(1)

    filter_options = driver.find_elements(By.XPATH, fil_opti_locator)
    filter_options[1].click()  # index of najnizsza cena
    time.sleep(0.5)

    # Tworzenie listy 10 linkow do produktow
    link_tags = driver.find_elements(By.XPATH, "//ul[@id='articleListWrapper']//li/a")
    links = []
    for i in range(10):
        links.append(str(link_tags[i].get_attribute("href")))

    # Wybierz link z listy -> wejdz na strone produktu -> sprawdz rozmiar -> dodaj do koszyka:
    add_to_cart = "//div[@id='addToCartButton']/button"
    prod_description = "//section[@id='article-information']//h2"
    size_M = "//section[@aria-labelledby='article-size-title']//button//span[text()='M']"
    size_42 = "//section[@aria-labelledby='article-size-title']//button//span[text()='42']"
    products_M = ["shirt", "bluzka", "bluza", "kurtka"]
    products_42 = ["buty", "sneakersy", "botki", "oksfordki"]

    for link in links:
        driver.get(link)
        WebDriverWait(driver, 2).until(expected_conditions.visibility_of_element_located((By.XPATH, prod_description)))
        product_text = driver.find_element(By.XPATH, prod_description).text.lower()

        if any(el in product_text for el in products_M):
            try:
                is_available = driver.find_element(By.XPATH, size_M + "/parent::button").is_enabled()
                if is_available:
                    driver.find_element(By.XPATH, size_M).click()
                    driver.find_element(By.XPATH, add_to_cart).click()
                else:
                    print("Your size wasn't available: " + link)

            except NoSuchElementException:
                print("This product is not produce in specified type of size: " + link)

        elif any(el in product_text for el in products_42):
            try:
                is_available = driver.find_element(By.XPATH, size_42 + "/parent::button").is_enabled()
                if is_available:
                    driver.find_element(By.XPATH, size_42).click()
                    driver.find_element(By.XPATH, add_to_cart).click()
                else:
                    print("Your size wasn't available: " + link)

            except NoSuchElementException:
                print("This product is not produce in specified type of size: " + link)

        else:
            print("This product category wasn't expected: " + link)

    input("\nType anything to close the Bot: ")
