from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive

@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the orderer robot.
    Embeds the screenshot of the orobt to the PDF receipt
    Creates ZIP archive of the receipts and the images
    """

def open_robot_order_website():
    """
    Open website
    """
    page = browser.page()
    page.goto("https://robotsparebinindustries.com/#/robot-order")

def get_orders():
    http = HTTP()
    file = http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)
    library = Tables()
    return library.read_table_from_csv("/Users/rodrigorivas/Robocorp/Bot_Certification/orders.csv", columns = ["Order number","Head", "Body", "Legs", "Address"])

def close_annoying_modal():
    page = browser.page()
    page.click("button:text('OK')")

def fill_the_form(ord_no, head, body, legs, address):

    page = browser.page()
    page.get_by_label("3. Legs:").fill(legs)
    page.locator("//select[@name='head']").select_option(index=int(head))
    page.get_by_placeholder("Shipping address").fill(address)
    page.locator(f'//input[@value={int(body)}]').check()
    page.locator("//button[@id='order']").click()

def store_receipt_as_pdf(order_number):
    page = browser.page()
    receipt_html = page.locator("#receipt").inner_html()

    pdf = PDF()
    pdf.html_to_pdf(receipt_html,f"output/receipts/{order_number}.pdf")
    page.locator("//button[@id='order-another']").click()

def check_if_popup():
    page = browser.page()
    return page.locator("button:text('OK')").is_visible()


def close_alert():
    page = browser.page()
    while not page.locator("#receipt").is_visible():
        page.locator("//button[@id ='order']").click()

def archive_receipts():
    lib =  Archive()
    lib.archive_folder_with_zip('output/receipts/','robot_receipts.zip')



    




open_robot_order_website()
close_annoying_modal()

orders = get_orders()
for order in orders:
    fill_the_form(order['Order number'],order['Head'],order['Body'],order['Legs'],order['Address'])
    close_alert()
    store_receipt_as_pdf(order['Order number'])
    close_annoying_modal()
archive_receipts()
    
    