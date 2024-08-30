# **Connect Python to Google Sheets: Step-by-Step Guide**

To connect a Google Sheet with a Python script, follow these steps:

### **Step 1: Create a Google Service Account**

1. **Visit Google Cloud Console:**  
   * Go to the Google Cloud Console.  
2. **Create a Project:**  
   * Click "CREATE PROJECT."  
   * Enter a project name and click "CREATE."  
3. **Enable APIs:**  
   * Click on "APIs & Services."  
   * Click "+ ENABLE APIS AND SERVICES."  
   * Search for "Google Sheets API" and "Google Drive API."  
   * Click "ENABLE" for both.  
4. **Create Credentials:**  
   * Click "Create Credentials."  
   * Select "Service Account."  
   * Fill in the details and click "CREATE AND CONTINUE."  
   * Assign roles if needed and click "CONTINUE."  
   * Click "DONE."  
5. **Generate a Key:**  
   * Go to the "Credentials" page.  
   * Click on the service account email.  
   * Click "KEYS" and then "ADD KEY."  
   * Select "Create new key."  
   * Download the JSON file and save it securely.

### **Step 2: Install the `gspread` Library**

Install the `gspread` library using pip:

sh  
`pip install gspread`

### **Step 3: Connect to the Google Sheet**

Use this Python script to connect to your Google Sheet:

python  
`import gspread`  
`from google.oauth2.service_account import Credentials`

`# Define the scope`  
`SCOPES = [`  
    `'https://www.googleapis.com/auth/spreadsheets',`  
    `'https://www.googleapis.com/auth/drive'`  
`]`

`# Load the credentials`  
`SERVICE_ACCOUNT_FILE = 'path/to/your/json/file.json'`  
`credentials = Credentials.from_service_account_file(`  
    `SERVICE_ACCOUNT_FILE, scopes=SCOPES)`

`# Authorize the client`  
`client = gspread.authorize(credentials)`

`# Open the Google Sheet`  
`sheet = client.open('Your Google Sheet Name').sheet1`

`# Get the spreadsheet ID`  
`spreadsheet_id = sheet.id`  
`print(f"Spreadsheet ID: {spreadsheet_id}")`

`# Example: Read data from the sheet`  
`data = sheet.get_all_records()`  
`print(data)`

### **Step 4: Share the Google Sheet with the Service Account**

1. **Open the Google Sheet:**  
   * Open your Google Sheet in a web browser.  
2. **Share the Sheet:**  
   * Click "Share."  
   * Enter the service account email from the JSON file.  
   * Set the permission to "Editor" and click "Save."

### **Step 5: Run the Python Script**

Run the script to connect to your Google Sheet and read data from it.

### **Summary**

1. **Create a Google Service Account:**  
   * Use the Google Cloud Console to create a project, enable APIs, and create credentials.  
2. **Install the `gspread` Library:**  
   * Install the `gspread` library using pip.  
3. **Connect to the Google Sheet:**  
   * Use the provided Python script to connect to your Google Sheet.  
4. **Share the Google Sheet:**  
   * Share the Google Sheet with the service account email.  
5. **Run the Python Script:**  
   * Execute the script to read data from the Google Sheet.

By following these steps, you can connect a Google Sheet with a Python script and interact with it programmatically.

