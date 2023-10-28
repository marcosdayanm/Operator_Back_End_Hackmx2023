import assemblyai as aai



# with open("/stat") as file:
#     print("Prueba")



def s2t():

    # set the API key
    aai.settings.api_key = "c950ebc8b23b44cb94542fd711551364"

    config = aai.TranscriptionConfig(language_detection=True)
    transcriber = aai.Transcriber(config=config)

    transcript = transcriber.transcribe("static/Prueba.mp3")
    print(transcript.text)

    # return jsonify({"text": transcript.text})


s2t()
