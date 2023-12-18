from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Train
from .models import Logic1
import spacy
import base64
from django.views.decorators.csrf import csrf_exempt
import speech_recognition as sr

# Create your views here.

def index(request):
    object_count = Logic1.objects.count()
    if object_count >= 3:
        Logic1.objects.all().delete()
    data1 = []
    if request.method == "POST":
        selected_value = request.POST.get('lang')
        TrainNo = request.POST.get('input')
        audio_data = request.POST.get('audioData')
        if TrainNo is not None:
            nlp = spacy.load('./static/model-best')
            doc = nlp(TrainNo)
            ents = doc.ents
            person_ents = [ent for ent in ents if ent.label_ == "TRAIN"]

            for i in range(len(person_ents)):
                items = Train.objects.filter(Train_Name__icontains=person_ents[i])
                for item in items:
                    s=get(item,selected_value)
                    post=Logic1.objects.create(quest=TrainNo, ans=s)
    # else:
    #     nlp = spacy.load('./static/model-best')
    #     z = process_audio(audio_data)
    #     print(z)
    #     if z is not None:
    #         doc = nlp(z)
    #         ents = doc.ents
    #         person_ents = [ent for ent in ents if ent.label_ == "TRAIN"]

    #         for i in range(len(person_ents)):
    #             items = Train.objects.filter(Train_Name__icontains=person_ents[i])
    #             for item in items:
    #                 s=get(item,selected_value)
    #                 post=Logic1.objects.create(quest=TrainNo, ans=s)


    data1.extend(Logic1.objects.filter(sno__gt=1))
    context = {'data1': data1}
    return render(request, 'index.html', context)

def record(request):
    return render(request,'recording.html')   


def get(item,selected_value):
    if selected_value == "English" and item.Delayed == False:
        s = "Your train " + item.Train_Name + " will reach at " + item.Origin + " station at " + item.Arival_time + " and will be ready for departure to " + item.Destination + " by " + item.Departure
    elif selected_value == "Marathi" and item.Delayed == False:
        s = "Aapli gaadi " + item.Train_Name  +" "+ item.Origin + " stationvar " + item.Arival_time + " la pohochel ani " + item.Destination + " saathi " + item.Departure + "la ravana honya saathi sajj hoyeel"
    elif selected_value == "English" and item.Delayed == True:
        s = "Your train " + item.Train_Name + " is delayed in reaching " + item.Origin + " Its new departure time is "  + item.Departure + " plus 30 minutes."
    elif selected_value == "Marathi" and item.Delayed == True:
        s = "Aapli gaadi " + item.Train_Name  + item.Origin + " stationvar pohochayla vilambh lagat aahe. Tyaanche navye prastan kaal "  + item.Departure + " la + 30 minutes aahe"
    elif selected_value == "Hindi" and item.Delayed == False:
        s = "Aapki Train " + item.Train_Name + " " + item.Origin + " Station par " + item.Arival_time + " par pahuchegi or " + item.Destination + " ke liye " + item.Departure + " par prashthan ke liye tayyar hogi"
    else:
        s = "Aapki Train " + item.Train_Name + " " + item.Origin + " Station par pahunchne mein der ho gayi hai. Uska naya prashthan ka samay " + item.Departure + " hai, lekin ab ye 30 minute baad prastan karegi."

    return s

def process_audio(audio_data):
    # Decode base64 data to get raw audio bytes
    decoded_audio = base64.b64decode(audio_data)

    # Transcribe the audio
    try:
      # Initialize the speech recognizer
      recognizer = sr.Recognizer()

      # Load the audio data
      with sr.AudioData(decoded_audio) as source:
        # Read the audio data
        audio_data = recognizer.record(source)

      # Use Google Speech Recognition API for transcription
      transcription = recognizer.recognize_google(audio_data)
      print(f"Transcription: {transcription}")

      # Return the transcribed text as a JSON response
      return transcription
    except sr.UnknownValueError:
      return  'Could not understand audio'
    except sr.RequestError as e:
      return 'Could not request transcription'

