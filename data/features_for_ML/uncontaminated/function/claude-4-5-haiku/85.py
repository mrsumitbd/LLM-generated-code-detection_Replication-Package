def attempt_focus_and_reenable_prev_button():
    try:
        prev_button = driver.find_element(By.ID, "prev_button")
        prev_button.click()
        driver.execute_script("arguments[0].disabled = false;", prev_button)
        prev_button.send_keys(Keys.TAB)
    except NoSuchElementException:
        print("Previous button not found")
    except Exception as e:
        print(f"Error: {e}")