from flask import Flask, render_template, request
from google import genai
from google.genai import types

app = Flask(__name__)

client = genai.Client(api_key="AIzaSyBfy1HaIvi2Tm5Etf5BbX6tYBSIIXYwYog")

def generate_playlist(decade):
    sys_instruct = "Generate the top 10 songs from the given decade. List the song name, year, artist, and a no description."

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(system_instruction=sys_instruct),
        contents=[decade]
    )

    song_list = response.candidates[0].content.parts[0].text
    return song_list

@app.route("/", methods=["GET", "POST"])
def index():
    songs = None

    if request.method == "POST":
        decade = request.form.get("decade") 
        if decade:
            songs = generate_playlist(decade) 

    return render_template("index.html", songs=songs)

if __name__ == "__main__":
    app.run(debug=True)
