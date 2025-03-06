from playwright.sync_api import sync_playwright
import random
import os

def generate_random_name():
    surnames = ["Zod", "Durell", "mook", "Banner", "Zeke", "Tiddles", "zook", "zandor", "zydor", "yask"]
    initials = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return {
        'surname': random.choice(surnames),
        'initials': f"{random.choice(initials)}{random.choice(initials)}"
    }

def test_add_soldier():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)  # Set headless=True for production
        context = browser.new_context()
        page = context.new_page()

        # Go to management page
        page.goto("http://localhost:8000/mgmt/")

        # Click on Soldiers link
        page.click("text=Soldiers")

        # Click Add New button (adjust selector based on your actual HTML)
        page.click("text=Add New")

        # Generate random name
        name = generate_random_name()

        # Fill in the form
        page.fill("input[name='surname']", name['surname'])
        page.fill("input[name='initials']", name['initials'])
        page.fill("input[name='army_number']", str(random.randint(1000000, 9999999)))

        # Select rank (adjust based on available ranks)
        page.select_option("select[name='rank']", index=1)  # Selects first available rank

        # Click Death Details accordion to expand it
        page.click("text=Death Details")
        
        # Wait for form elements
        page.wait_for_selector("input[name='date']")
        page.fill("input[name='date']", "1940-01-01")

        # Wait for and select company
        page.wait_for_selector("select[name='company']")
        page.select_option("select[name='company']", "1")  # Assuming '1' is the value for 1 AIRBORNE DIV PRO
        
        # Wait for and select cemetery
        page.wait_for_selector("select[name='cemetery']")
        page.select_option("select[name='cemetery']", "1")  # Adjust value based on SCHOONSELHOF's actual value

        # Set CWGC ID
        page.fill("input[name='cwgc_id']", "1")

        # Upload image file
        downloads_dir = os.path.expanduser("~/Downloads")
        image_path = os.path.join(downloads_dir, "test-picture.jpg")
        print(f"Checking image path: {image_path}")
        print(f"File exists: {os.path.exists(image_path)}")
        page.set_input_files("input[name='image']", image_path)

        # Click Save button with more specific selector
        page.click("button[type='submit']")

        # First wait for navigation to complete
        page.wait_for_url("http://localhost:8000/mgmt/soldiers/search/")

        # Then wait for the alert with a longer timeout and debug
        try:
            alert = page.wait_for_selector(".alert", timeout=5000)
            print("Alert message:", alert.text_content())
        except Exception as e:
            print("Current URL:", page.url)
            print("Page content:", page.content())
            raise e

        # Close browser
        browser.close()

if __name__ == "__main__":
    test_add_soldier() 