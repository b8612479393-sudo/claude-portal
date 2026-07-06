from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_KEY = "ТВОЙ_CLAUDE_API_КЛЮЧ"
API_URL = "https://api.anthropic.com/v1/messages"

history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global history
    if request.method == 'POST':
        user_msg = request.form.get('message', '').strip()
        if user_msg:
            history.append({"role": "user", "content": user_msg})

            headers = {
                "x-api-key": API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }

            data = {
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 4096,
                "system": "Отвечай всегда на русском языке.",
                "messages": history
            }

            try:
                r = requests.post(API_URL, headers=headers, json=data, timeout=60)
                r.raise_for_status()
                reply = r.json()['content'][0]['text']
                history.append({"role": "assistant", "content": reply})
            except Exception as e:
                history.append({"role": "assistant", "content": "Ошибка: " + str(e)})

    return render_template('index.html', history=history)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
