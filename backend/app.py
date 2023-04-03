from flask import Flask, render_template, request, redirect, url_for, Response
from noteyXMLParser.CreateConfig import CreateConfig
import json
import os

app = Flask(__name__)





def createConfigFile(request):
    config = {
        "AppData": {
            "Title": request.form['Title'],
            "levelType": request.form['LevelType'],
            "Difficulty": request.form['Difficulty'],
            "LevelNumber": request.form['LevelNumber'],
            "jsonFile": request.form['jsonFile'],
            "Style": request.form['Style'],
        },
        "ConfigManager": {
            "levelType": request.form["LevelType"],
        },
        "StartGameView": {
            "Title": request.form['Title'],
            "Description": request.form['LevelSummary'],
            "VideoPath": request.form['VideoLink'],
        }
    }
    return config
@app.route('/', methods=('GET', 'POST'))
def createConfig():
    if request.method == "POST":
        print("POST")

        config = createConfigFile(request)
        
        xml = request.files['file']
        if xml.filename == '': 
            return'No selected file'
        with open('music.xml', 'wb') as fp:
            fp.write(xml.read())
        x = CreateConfig("music.xml", "config.json")
        x.createConfig()
        with open('config.json', 'r') as fp:
            temp_config = json.load(fp)
        
        config["BPMCounter"] = {
            "bpm": temp_config["bpm"],
            "beatBase": temp_config["beatBase"],
        }
        config["PlaylistManager1"] = {
              "playString": temp_config["playString"]
        }
       
        configJson = json.dumps(config,indent=4)
        #DELETE FILE
        # os.remove("music.xml")
        # os.remove("config.json")
        return Response(configJson, 
            mimetype='application/json',
            headers={'Content-Disposition':'attachment;filename=config.json'})

    return render_template('CreateConfig.html')