# Anrovi

# Follow these steps to start working on the project

# Step 1 : Create python virtual environment

on cmd : python -m venv .venv

# Step 2 : Activate environment

on cmd : .venv\Scripts\activate

to quit : deactivate

# Step 3 : Create credentials (Data Base)

on firebase.com (project) : go to -> Settings | Services accounts, next click on 'Python' and on 'Generate a new private key' (a file it downloaded)

on editor : create a file 'credentials.json' (in the same directory as 'main.py') and put the content of the downloaded file into it

# Step 4 : Upload your private key

on editor : create a file 'private_key.asc' in the project root directory and copy / paste your private key into it

# Step 5 : Launch app.py

Windows : python .\app.py
Mac/Linux : python3 .\app.py