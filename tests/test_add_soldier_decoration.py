import os
from playwright.sync_api import sync_playwright
import random
import traceback  # Add this for better error reporting

BASE_URL = "http://localhost:8000"

def generate_random_name():
    surnames = ["Zod", "Durell", "mook", "Banner", "Zeke", "Tiddles", "zook", "zandor", "zydor", "yask"]
    initials = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return {
        'surname': random.choice(surnames),
        'initials': f"{random.choice(initials)}{random.choice(initials)}"
    }

def test_add_soldier():
    print("Test starting...")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # Go to search page
            page.goto(f"{BASE_URL}/mgmt/soldiers/search/")
            print("Loaded search page")
            
            # Click the correct button text
            page.click("text=Add New Soldier")
            print("Clicked Add New Soldier")
            
            # Generate random name
            name = generate_random_name()

            # Fill in the form
            page.fill("input[name='surname']", name['surname'])
            page.fill("input[name='initials']", name['initials'])
            page.fill("input[name='army_number']", str(random.randint(1000000, 9999999)))
            print("Filled basic info")

            # Select rank (adjust based on available ranks)
            page.select_option("select[name='rank']", index=1)  # Selects first available rank
            print("Selected rank")

            # Click Death Details accordion to expand it
            page.click("text=Death Details")
            print("Expanded Death Details")
            
            # Wait for form elements
            page.wait_for_selector("input[name='date']")
            page.fill("input[name='date']", "1940-01-01")
            print("Filled death date")

            # Wait for and select company
            page.wait_for_selector("select[name='company']")
            page.select_option("select[name='company']", "1")  # Assuming '1' is the value for 1 AIRBORNE DIV PRO
            print("Selected company")
            
            # Wait for and select cemetery
            page.wait_for_selector("select[name='cemetery']")
            page.select_option("select[name='cemetery']", "1")  # Adjust value based on SCHOONSELHOF's actual value
            print("Selected cemetery")

            # Set CWGC ID
            page.fill("input[name='cwgc_id']", "1")
            print("Filled CWGC ID")

            # Upload image file
            downloads_dir = os.path.expanduser("~/Downloads")
            image_path = os.path.join(downloads_dir, "test-picture.jpg")
            print(f"Checking image path: {image_path}")
            print(f"File exists: {os.path.exists(image_path)}")
            page.set_input_files("input[name='image']", image_path)
            print("Uploaded image")

            # Click Decoration Details accordion to expand it
            print("About to click Decoration Details...")
            page.click("text=Decoration Details")
            print("Clicked Decoration Details")
            
            # Wait for and fill in decoration form - selecting Military Medal
            print("Waiting for decoration dropdown...")
            page.wait_for_selector("select[name='decoration-0-decoration']")
            print("Found decoration dropdown, selecting Military Medal...")
            page.select_option("select[name='decoration-0-decoration']", "1")  # Military Medal
            print("Selected Military Medal")
            
            print("Filling gazette issue...")
            page.fill("input[name='decoration-0-gazette_issue']", "12345")
            print("Filling gazette page...")
            page.fill("input[name='decoration-0-gazette_page']", "67")
            print("Filling gazette date...")
            page.fill("input[name='decoration-0-gazette_date']", "1940-05-15")
            print("Gazette fields filled")
            
            # Select country by index
            print("Selecting country by index...")
            page.select_option("select[name='decoration-0-country']", index=1)  # First country (non-blank)
            print("Selected country")
            
            # Take screenshot
            page.screenshot(path="before_citation.png")
            print("Saved screenshot before filling citation")
            
            # Try filling citation with force focus
            print("Focusing citation field...")
            page.evaluate("""
                () => {
                    const citation = document.querySelector('textarea[name="decoration-0-citation"]');
                    if (citation) {
                        citation.focus();
                        citation.value = "Test citation for bravery in action";
                        citation.dispatchEvent(new Event('input'));
                        return true;
                    }
                    return false;
                }
            """)
            print("Attempted to fill citation via JS")
            
            # Click Save button
            print("Clicking Save button...")
            page.click("button:has-text('Save')")
            print("Clicked Save")

            # Wait for navigation to search page
            print("Waiting for navigation...")
            page.wait_for_url(f"{BASE_URL}/mgmt/soldiers/search/")
            print("Navigation complete")

            # Wait for and verify success message
            print("Waiting for success message...")
            page.wait_for_selector(".alert")
            print("Found alert")
            
            # Optional: Print what we find to debug
            alert = page.locator(".alert").text_content()
            print(f"Alert message: {alert}")

        except Exception as e:
            print(f"Test failed with error: {e}")
            print(traceback.format_exc())
            page.screenshot(path="error_screenshot.png")
            print("Error screenshot saved as error_screenshot.png")
        finally:
            # Close browser
            browser.close()
            print("Browser closed")

if __name__ == "__main__":
    test_add_soldier() 