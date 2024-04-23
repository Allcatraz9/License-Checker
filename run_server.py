import subprocess
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/start_servers')
def start_servers():
    try:
        # Execute the Bash script
        subprocess.run(['./server.sh'])
        return render_template("server_started.html")
    except Exception as e:
        return f'Error: {e}'

if __name__ == '__main__':
    app.run(debug=True,port=8080)


# sudo netstat -tulpn | grep LISTEN