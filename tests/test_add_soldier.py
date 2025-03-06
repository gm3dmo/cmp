from playwright.sync_api import sync_playwright
import random
import os

def generate_random_name():
    surnames = ["Smith", "Jones", "Williams", "Brown", "Taylor", "Davies", "Wilson", "Evans", "Thomas", "Johnson"]
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

        # Fill death details
        page.fill("input[name='date']", "1940-01-01")

        # Select company
        page.click("select[name='company']")
        page.type("select[name='company']", "1 Airborne Div Pro")
        page.keyboard.press("Enter")
        
        # Select Bayeux cemetery
        page.type("select[name='cemetery']", "Bayeux")
        page.keyboard.press("Enter")

        # Set CWGC ID
        page.fill("input[name='cwgc_id']", "1")

        # Upload image file using absolute path
        downloads_dir = os.path.expanduser("~/Downloads")
        image_path = os.path.join(downloads_dir, "test-picture.jpg")
        page.set_input_files("input[name='image']", image_path)

        # Submit the form
        page.click("text=Save")  # Adjust button text if different

        # Wait for confirmation (adjust based on your UI feedback)
        page.wait_for_selector("text=successfully")

        # Close browser
        browser.close()

if __name__ == "__main__":
    test_add_soldier() 