from flask import Flask, request, render_template, Response
import whois
import pandas as pd

app = Flask(__name__, template_folder='C:/Users/ACER/Desktop/cyberAI')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lookup', methods=['POST'])
def lookup():
    domain = request.form['domain']  
    try:
        w = whois.whois(domain)  
        result = str(w)
        
        show_ip = "showip" in domain.lower()
        
        user_ip = request.remote_addr if show_ip else "IP address hidden"
        
        result_with_ip = f"User IP Address: {user_ip}\n\n{result}"
    except Exception as e:
        result_with_ip = f"Error: {str(e)}"
    return result_with_ip  


@app.route('/download_excel', methods=['POST'])
def download_excel():
    domain = request.form['domain']
    try:
        w = whois.whois(domain)
        data = {
            'Domain': [domain],
            'Registrar': [w.registrar],
            'Creation Date': [w.creation_date],
            'Expiration Date': [w.expiration_date],
            'Name Servers': [w.name_servers]
        }
        df = pd.DataFrame(data)
        
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='WHOIS Data', index=False)
        writer.save()
        output.seek(0)
        
        return Response(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
