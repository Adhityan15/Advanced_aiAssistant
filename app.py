from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# ✅ OpenRouter API Setup
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = "your api key"  #https://openrouter.ai/settings/keys

def ask_ai(prompt):
    response = openai.ChatCompletion.create(
        model="mistralai/mixtral-8x7b-instruct",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    feedback = ""

    if request.method == "POST":
        function = request.form.get("function")
        user_input = request.form.get("user_input")
        feedback_input = request.form.get("feedback")

        if feedback_input:
            with open("feedback_log.txt", "a") as f:
                f.write(f"Feedback: {feedback_input}\n")
            feedback = "Thanks for your feedback! 💬"

        # 🌟 Smart prompt mapping
        if function == "question":
            prompt = f"Answer this question: {user_input}"
        elif function == "summary":
            prompt = f"Summarize: {user_input}"
        elif function == "creative":
            prompt = f"Write something creative about: {user_input}"
        elif function == "advice":
            prompt = f"Give advice on: {user_input}"
        elif function == "poem":
            prompt = f"Write a poem about: {user_input}"
        else:
            prompt = user_input

        result = ask_ai(prompt)

    return render_template("index.html", result=result, feedback=feedback)

if __name__ == "__main__":
    app.run(debug=True)
