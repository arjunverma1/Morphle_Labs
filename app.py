import os
import subprocess
import pytz
from datetime import datetime
from flask import Flask

app = Flask(__name__)

@app.route('/htop')
def htop():
    full_name = "Arjun Verma"

    # Try to get system username
    try:
        username = os.getlogin()
    except Exception:
        username = os.environ.get("USERNAME", "arjun")

    # Get server time in IST
    tz_IST = pytz.timezone('Asia/Kolkata')
    server_time_ist = datetime.now(tz_IST).strftime("%Y-%m-%d %H:%M:%S %Z")

    # Determine OS and run appropriate command
    if os.name == 'nt':  # Windows
        try:
            top_output = subprocess.check_output(['tasklist'], shell=True).decode('utf-8', errors='ignore')
        except Exception as e:
            top_output = f"Error running tasklist command: {str(e)}"
    else:  # Linux/MacOS
        try:
            top_output = subprocess.check_output(['top', '-b', '-n', '1']).decode('utf-8', errors='ignore')
        except Exception as e:
            top_output = f"Error running top command: {str(e)}"

    # Construct response
    response = (
        f"Name: {full_name}\n"
        f"user: {username}\n"
        f"Server Time (IST): {server_time_ist}\n"
        f"TOP output: \n\n{top_output}"
    )

    return f"<pre>{response}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)