from flask import Flask, render_template, request, redirect, url_for, Response
from noteyXMLParser.CreateConfig import CreateConfig
import json
import os
from io import BytesIO
import xml.etree.ElementTree as ET
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
        print(type(xml))
        
        xml_string = xml.read().decode('utf-8')

        x = CreateConfig(xml_string, fileData=True)
        temp_config = x.createConfig()

    
        
        config["BPMCounter"] = {
            "bpm": temp_config["bpm"],
            "beatBase": temp_config["beatBase"],
        }
        config["PlaylistManager1"] = {
              "playString": temp_config["playString"]
        }
       
        configJson = json.dumps(config,indent=4)
    
        return Response(configJson, 
            mimetype='application/json',
            headers={'Content-Disposition':'attachment;filename=config.json'})

    return render_template('CreateConfig.html')