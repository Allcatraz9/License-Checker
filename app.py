from io import BytesIO
import json
import random
import socket
import subprocess
import sqlite3
from flask import Flask, jsonify,render_template,request,redirect, send_file, session,url_for

from backend import TransportAuthority, RSA



app = Flask(__name__)
app.secret_key = 'JaiMaaSaraswati'





@app.route("/")
@app.route("/home")
def home():
  
    return render_template('home.html')

@app.route("/create")
def create():
    return render_template('form.html')

@app.route("/login",methods=['GET','POST'])
def login():
        
        if request.method == 'POST':
             conn = sqlite3.connect('user_data.db')
             cursor = conn.cursor()

       

    # return render_template('index.html')
#HTML Form
             name = request.form['name']
             password = request.form['password']

#Query
             query = "SELECT name,password FROM users where name= '"+name+"' and password= '"+password+"'"
             cursor.execute(query)
                                                                
             results = cursor.fetchall()

#Validation
             if len(results) == 0:
                return render_template('index.html')
             else:
                session['logged_in'] = True
                return render_template('particle.html')
    
        return render_template('index.html')


@app.route("/logout")
def logout():
    session.pop('logged_in',None)
    return render_template('home.html')

@app.route("/submit",methods=["GET","POST"])
def submit():
    rto = (request.values.get('rto')).strip()
    dlid = (request.values.get('dlid')).strip()
    username = (request.values.get('username')).strip()
    print(type(rto))
    print(type(dlid))
    print(type(username))
    if(str.upper(rto)=="DELHI TRANSPORT AUTHORITY" or str.upper(rto)=="DELHI"):
        rto="DELHI TRANSPORT AUTHORITY"
        kpu = (5,91)
        kpr = (29,91)
    elif(str.upper(rto)=="HARYANA TRANSPORT AUTHORITY" or str.upper(rto)=="HARYANA"):
        rto = "HARYANA TRANSPORT AUTHORITY"
        kpu = (17,91)
        kpr = (17,91)
    else:
        rto = "NATIONAL TRANSPORT AUTHORITY"
        kpu = (5,119)
        kpr = (77,119)
    print(f'your rtos kpu {kpu} and kpr {kpr} ')
    ta = TransportAuthority(str.upper(rto),
                        12345,kpu,kpr)
    cert = (1,) + RSA.rsa_encode_string(str.upper(rto)) + \
    RSA.rsa_encode_string(username) + RSA.rsa_encode_string(dlid)
    sign = ta.sign(cert)
    print(f"""
    "cert": {cert},
    "sign": {ta.sign(cert)}
""")
    license = create_license(cert,sign,rto)
    print(f'This is license: {license}')
    if(not validateForm(rto,dlid,username)):
        return redirect(url_for('login'))
    else:
        js_code = """
    <script>
        alert("Your Form has been Submitted Successfully!");
    </script>
    """
        return render_template('test.html',js_code=js_code)
   
    
  
 
def validateForm(rto,dlid,username):
    if(rto.strip()=="" or dlid.strip()==""or username.strip()==""):
        return False
    else:
        return True
def create_license(cert,sign,rto):
    license = json.dumps({
        "type": 1,
        "signingAuthority": str.upper(rto),
        "cert": cert,
        "sign": sign
    })
    with open('license.json','w') as json_file:
        json_file.write(license)
    return(license)


@app.route("/send",methods=["GET", "POST"])
def send_license():
    decoded_json = request.args.get('_data', b'') 
      
    print(f'the type of decoded_json is {type(decoded_json)}\n')
    session['variable'] = decoded_json
    json_object = json.loads(decoded_json)
    command = ['python3', 'run_server.py']
    subprocess.Popen(command)
    return render_template('display.html', data=json_object)

 

@app.route("/client")    
def client():
    PORT = [12341,12342,12343]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", random.choice(PORT)))
    decoded_json = session.get('variable')
    print(f'the type of license is : {type(decoded_json)}')
    print("Sending for verification ...")
    s.send(decoded_json.encode())
    print("Waiting to receive license status from the server ...")
    result  = s.recv(1024).decode()
    json_object = json.loads(result)
    print(f'client function json_object type: {type(json_object)}')
    return render_template("result.html",result=json_object['status'])


@app.route("/upload",methods=["GET","POST"])
def upload():
    if 'json_file' not in request.files:
        return 'No file part'
    
    file = request.files['json_file']
    
    if file.filename == '':
        return 'No selected file'
    
    if file:
        # Read the JSON file
        json_data = file.read()
        
        
        print(f'{type(json_data)}\n')
        print(json_data)
        return redirect(url_for('send_license', _data=json_data))

    else:
        return 'Error uploading file'

@app.route("/test")
def test():
    if 'logged_in' in session and session['logged_in']:
        return render_template('particle.html')
    else:
        return redirect(url_for('login'))
    

@app.route("/start_servers")
def start():
    try:
        # Execute the Bash script
        subprocess.run(['./server.sh'])
        return render_template("server_started.html")
    except Exception as e:
        return f'Error: {e}'

@app.route("/kill_port")
def kill():
    return "ruko abhi work in progress hai !"
    

if __name__ == '__main__':
    app.run(debug=True)
    

