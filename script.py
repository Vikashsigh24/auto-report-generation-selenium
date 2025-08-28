import time
import pandas as pd
import csv
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import JavascriptException
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

# ------------------ Setup Driver ------------------
def setup_driver():
    try:
        driver = uc.Chrome()
        driver.maximize_window()
        driver.get("https://www.careerguide.com/login")
        return driver
    except Exception as e:
        print(f"⚠️ Error setting up driver: {e}")
        raise

# ------------------ Hide Chat Widgets ------------------
def hide_widgets(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "fc_widget"))
        )
        driver.execute_script("""
            var iframe = document.getElementById('fc_widget');
            if (iframe) {
                iframe.remove();
                console.log('✅ Chat widget removed');
            }
        """)
        print("✅ Chat iframe and hotline button successfully hidden")
    except Exception as e:
        print(f"⚠️ Failed to hide chat widget: {e}")



def register_new_user(driver, wait, email, name):
        try:
            time.sleep(2)

            wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "frmloginsignup")))
            print("✅ Switched to login iframe")
            time.sleep(1)
            email_input = wait.until(EC.presence_of_element_located((By.ID, "ctrlLogin_txtEmailNewUser")))
            email_input.send_keys(f"{email}")
            print("✅ Email entered")

            full_name = driver.find_element(By.ID, "ctrlLogin_txtUserNameNewUser")
            full_name.send_keys(f"{name}")

            password = driver.find_element(By.ID, "ctrlLogin_txtPasswordNewUser")
            password.send_keys("12345")

            education_dropdown = Select(driver.find_element(By.ID, "ctrlLogin_txtEducation"))
            education_dropdown.select_by_visible_text("11th Class")

            phone = driver.find_element(By.ID, "ctrlLogin_txtContactNo")
            phone.send_keys("9999999999")

            phone = driver.find_element(By.ID, "ctrlLogin_btnSignup")
            phone.click()
            
            print("✅ Register button clicked")
            driver.switch_to.default_content()  # ✅ Important line added here

            
        except Exception as e:
            print(f"⚠️ Error during registration: {e}")
            driver.quit()
            raise
            

# ------------------ Start the Test ------------------
def start_test(driver, wait, coupon):
    try:
         # Scroll and click the "For 11th & 12th" button
        button_11_12 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='For 11th & 12th']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button_11_12)
        time.sleep(1)
        button_11_12.click()
        print("✅ Clicked 'For 11th & 12th' button")

    except Exception as e:
        print(f"⚠️ Error clicking 'For 11th & 12th' button: {e}")

# ------------------ Apply Coupon Code ------------------
    try:
        coupon_code = wait.until(
                EC.element_to_be_clickable((By.ID, "ctl00_ctContentMiddle_ctrl_ctrlAssessmentStartWithCouponCode1_2_spnCode"))
            )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", coupon_code)

        coupon_code.click()
        coupon_input = wait.until(
            EC.element_to_be_clickable((By.ID, "ctl00_ctContentMiddle_ctrl_ctrlAssessmentStartWithCouponCode1_2_txtCouponCode"))
            )
            #Coupon Code Here
        coupon_input.send_keys(coupon)

        apply_code = wait.until(
                EC.element_to_be_clickable((By.ID, "ctl00_ctContentMiddle_ctrl_ctrlAssessmentStartWithCouponCode1_2_btnApplyCouponCode"))
            )
        apply_code.click()
        print("✅ Coupon code applied successfully")
    except Exception as e:
        print(f"⚠️ Error applying coupon code: {e}")

    try:
        # Click the "Start Engineering Branch Selector" button
        start_button = wait.until(EC.element_to_be_clickable((By.ID, "hrfstarttestcommon")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", start_button)
        time.sleep(1)
        start_button.click()
        print("✅ Clicked 'Start Engineering Branch Selector'")
    except Exception as e:
        print(f"⚠️ Error clicking 'Start Engineering Branch Selector': {e}")

def answer_questions(driver, answers, start_from=0):
    try:
        question_index = start_from
        while True:
            time.sleep(2)
            question_blocks = driver.find_elements(By.CLASS_NAME, "new_assessment_question_option_one")

            if not question_blocks:
                print("❌ No question blocks found.")
                break

            for i, block in enumerate(question_blocks):
                if question_index >= len(answers):
                    print(f"⚠️ Only {len(answers)} answers available.")
                    return

                answer_text = str(answers[question_index]).strip().lower()
                if not answer_text:
                    answer_text = "option 1"

                labels = block.find_elements(By.TAG_NAME, "label")
                matched = False
                MAX_RETRIES = 1
                retry = 0

                while retry <= MAX_RETRIES and not matched:
                    # 1. TEXT MATCH
                    for label in labels:
                        label_text = (label.text or label.get_attribute("innerText") or "").strip().lower()
                        print(f"🔍 Q{question_index + 1} - Comparing: '{label_text}' with '{answer_text}'")
                        if answer_text in label_text or label_text in answer_text:
                            try:
                                input_id = label.get_attribute("for")
                                input_element = driver.find_element(By.ID, input_id)
                                driver.execute_script("arguments[0].click();", input_element)
                                print(f"✅ Q{question_index + 1}: Selected by text -> {label_text}")
                                matched = True
                                break
                            except Exception as e:
                                print(f"⚠️ Q{question_index + 1}: Error clicking label - {e}")

                    # 2. OPTION INDEX fallback
                    if not matched and "option" in answer_text:
                        try:
                            index = int(answer_text.replace("option", "").strip()) - 1
                            if 0 <= index < len(labels):
                                input_id = labels[index].get_attribute("for")
                                input_element = driver.find_element(By.ID, input_id)
                                driver.execute_script("arguments[0].click();", input_element)
                                print(f"✅ Q{question_index + 1}: Selected by option index -> {answer_text}")
                                matched = True
                        except Exception as e:
                            print(f"❌ Q{question_index + 1}: Invalid option index - {e}")

                    if not matched:
                        retry += 1
                        print(f"❌ Q{question_index + 1}: Retry {retry} failed")
                        time.sleep(0.5 * retry)

                if not matched:
                    print(f"⚠️ Q{question_index + 1}: Skipped after {MAX_RETRIES} retries")

                question_index += 1

            # Click "Next" button to go to the next set of questions
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "ctl00_ctContentMiddle_lnkSubmit"))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                driver.execute_script("arguments[0].click();", next_button)
                print("➡️ Clicked Next")
            except Exception as e:
                print(f"🚫 Couldn't click Next: {e}")
                break

    except Exception as e:
        print("🔴 Error in answer_questions:", e)


def download_report(driver, student_name):
    try:
        get_report_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Get Report')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", get_report_btn)
        get_report_btn.click()
        print("📄 Clicked 'Get Report' button")

        WebDriverWait(driver, 30).until(
            EC.url_contains(".pdf")
        )
        pdf_url = driver.current_url
        print(f"📥 PDF URL Detected: {pdf_url}")

        filename = f"{student_name}.pdf"
        response = requests.get(pdf_url)
        with open(filename, "wb") as f:
            f.write(response.content)

        print(f"✅ PDF downloaded: {filename}")

    except Exception as e:
        print(f"❌ Failed to download report: {e}")




# ------------------ Main Automation Flow ------------------
def run_test():
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)

    try:

        # perform_login(driver, wait,
        #               email_id="sairams2999mtp@gmail.com",
        #               password_text="12345")

        

        with open('file.csv', mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            next(reader)  # Skip second header if exists


            coupon_code = ["VNTT", "VNTT", "VNTT"]  # Example coupon codes

            for i, row in enumerate(reader):

                if i >= len(coupon_code):
                    print(f"⚠️ No more coupons available for {name}. Stopped...")
                    break

                name = row[1]
                email = row[4]
                answers = row[5:]
                current_coupon = coupon_code[i]

                username = email.split('@')[0]
                modified_email = f"{username}365@gmail.com"

                try:
                    hide_widgets(driver)

                    print(f"🧑 Running test for: {name} | {email}")
                    print(f"Email: {modified_email} | Name: {name}")

                    register_new_user(driver, wait, modified_email, name)
                    start_test(driver, wait, current_coupon)

                    answer_questions(driver, answers)

                    time.sleep(20)  # Wait for final question to submit

                    driver.get("https://www.careerguide.com/login")

                except Exception as e:
                    print(f"❌ Error during test for {name}: {e}")
                    continue
                # ✅ Download PDF after answers
                # download_report(driver, name)
                

    finally:
        time.sleep(20)
        driver.quit()
        driver = None
        print("🧹 Browser closed")

# ------------------ Run ------------------
if __name__ == "__main__":
    run_test()
