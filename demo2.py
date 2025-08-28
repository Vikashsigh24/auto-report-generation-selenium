


def login():
        email_input = wait.until(EC.presence_of_element_located((By.ID, "ctrlLogin_txtEmailNewUser")))
        email_input.send_keys("demo@gmail.com")
        print("✅ Email entered")

        full_name = driver.find_element(By.ID, "ctrlLogin_txtUserNameNewUser")
        full_name.send_keys("Demo User")

        password = driver.find_element(By.ID, "ctrlLogin_txtPasswordNewUser")
        password.send_keys("Demo@1234")

        education_dropdown = Select(driver.find_element(By.ID, "ctrlLogin_txtEducation"))
        education_dropdown.select_by_visible_text("11th Class")

        phone = driver.find_element(By.ID, "ctrlLogin_txtContactNo")
        phone.send_keys("9999999999")

        phone = driver.find_element(By.ID, "ctrlLogin_btnSignup")
        # phone.click()

        register = driver.find_element(By.XPATH, "//button[normalize-space()= 'For 11th & 12th']")
        register.click()
        print("✅ 1 Register button clicked")

        coupon_code = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ctContentMiddle_ctrl_ctrlAssessmentStartWithCouponCode1_2_spnCode"))
        )
        #Coupon Code Here
        coupon_code.send_keys("CR208")
        coupon_code.click()

        apply_code = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ctContentMiddle_ctrl_ctrlAssessmentStartWithCouponCode1_2_btnApplyCouponCode"))
        )
        apply_code.click()


# ------------------ Login ------------------
def perform_login(driver, wait, email_id, password_text):
    try:
        time.sleep(2)

        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "frmloginsignup")))
        print("✅ Switched to login iframe")

        wait.until(EC.element_to_be_clickable((By.ID, "ctrlLogin_alredyReg"))).click()
        print("✅ Clicked Already Registered")

        wait.until(EC.element_to_be_clickable((By.ID, "ctrlLogin_txtUserName"))).send_keys(email_id)
        wait.until(EC.element_to_be_clickable((By.ID, "ctrlLogin_txtPassword"))).send_keys(password_text)
        wait.until(EC.element_to_be_clickable((By.ID, "ctrlLogin_btnLogin"))).click()
        print("✅ Logged in successfully")
    except Exception as e:
        print(f"⚠️ Error during login: {e}")
        driver.quit()
        raise