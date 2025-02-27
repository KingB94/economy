import os 
from flask import Flask, render_template, request, redirect, url_for, jsonify
from groq import Groq  # Import the Groq client

app = Flask(__name__)

# Initialize the Groq client using the environment variable or a default key
groq_client = Groq(api_key=os.environ.get('GROQ_API_KEY', 'GROQ_API_KEY=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'))

@app.route("/")
def index():
    return render_template("index.html")

# Dummy user database (for demonstration purposes)
users = {
    "michael.jordan@bulls.com": "chicago"
}

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if email in users and users[email] == password:
        if email == "michael.jordan@bulls.com":
            return redirect(url_for('overview'))
        return redirect(url_for('index'))
    else:
        return "Invalid email or password", 401

@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email in users:
            return "User already exists", 400
        users[email] = password
        return redirect(url_for('overview'))
    return render_template("signup.html")

@app.route("/overview")
def overview():
    return render_template("overview.html")

@app.route("/countries")
def countries():
    return render_template("countries.html")

@app.route("/comparative")
def comparative():
    return render_template("comparative.html")

@app.route("/data")
def data():
    return render_template("data.html")

@app.route("/account")
def account():
    return render_template("account.html")

@app.route("/test")
def test():
    return render_template("test.html")

# Updated endpoint: use Groq client for chat completions
@app.route('/api/groq_description', methods=['POST'])
def groq_description():
    try:
        data = request.json
        prompt_text = data.get('promptText', '')
        # Use the Groq client to send the chat messages
        response = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in global economic data. When provided with a set of economic data, you will give a 3 sentence description of it."
                },
                {
                    "role": "user",
                    "content": prompt_text
                }
            ],
            model="llama3-8b-8192"
        )
        # Extract description from response
        description = (response.choices[0].message.content 
                       if response.choices and response.choices[0].message.content 
                       else "Based on the data, there is some super interesting economic data visible and these countries will be affected by it.")
        return jsonify({"description": description})
    except Exception as e:
        print(f"Error with Groq API: {e}")
        return jsonify({"description": "Based on the data, there is some super interesting economic data visible and these countries will be affected by it."}), 500

# Updated chat endpoint using the Groq client
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        messages = data.get('messages', [])
        model = data.get('model', 'llama3-8b-8192')
        response = groq_client.chat.completions.create(
            messages=messages,
            model=model,
        )
        return jsonify({
            "choices": [{"message": {"content": response.choices[0].message.content}}]
        }), 200
    except Exception as e:
        print(f"Error with Groq API: {e}")
        return jsonify({"error": "Failed to fetch response from Groq API"}), 500

if __name__ == "__main__":
    app.run(debug=True)
