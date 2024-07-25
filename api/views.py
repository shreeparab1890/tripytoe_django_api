from django.http import JsonResponse
import google.generativeai as genai
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from datetime import datetime
from dateutil import parser
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

def api_home(req, *args, **kwargs):
    return JsonResponse({"message": "This is my api Home response."})

@csrf_exempt
@require_http_methods(["GET"])
def generateItinerary(req, *args, **kwargs):
    genai.configure(api_key=GOOGLE_API_KEY)
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                     f"""Generate a travel itinerary for 1 person to Goa for 3 days with travel preferences like offbeat and culture. Consider the budget of balanced for the travel. 
                        Generate Day wise itinerary with heads like morning breakfast, Morning activity, lunch, evening activity, dinner, nightlife. only generate day itinerary. 
                        no extra information. Give only the Json without any extra character.
                        
                        generate in the below given json format:
                        {{
                            
                            "name_entity": [
                                //this array will consist of all the named entities used in the itinerary.activities.activity string. Consider only the famous tourist destinations in itinerary.activities.activity string.
                            ], 
                            "about_destination": "Generate about Goa i.e. what it is known for",
                            "weather_destination": "Generate how is the weather at Goa i.e. best, avg time to visit Goa",
                            "currency_destination": "Generate what is the currency in use at Goa i.e. how much it will on avg cost for a cup of tea",
                            "lang_destination": "Generate what is the spoken language in use at Goa",
                            "itinerary": [
                                // this array will have elements as many as the days 
                                {{
                                    "day_no": "1",
                                    "day_subject": "Day 1 Subject //Generate a subject for the day",
                                    "activities": [
                                        {{
                                            "activity_time": "Breakfast",
                                            "activity": "" //the real activity in the Breakfast can be added here
                                        }},
                                        {{
                                            "activity_time": "Morning",
                                            "activity": "" //the real activity in the morning can be added here
                                        }},
                                        {{
                                            "activity_time": "Lunch",
                                            "activity": "" //the real activity in the Lunch can be added here
                                        }},
                                        {{
                                            "activity_time": "Evening Activity",
                                            "activity": "" //the real activity in the Evening Activity can be added here
                                        }},
                                        {{
                                            "activity_time": "Night",
                                            "activity": "" //the real activity in the night can be added here
                                        }}
                                    ]
                                }}
                            ]
                            "day_name_entity": [
                                //this array will consist of all the named entities used in the itinerary.day.activities.activity string. Consider only the famous tourist destinations in itinerary.day.activities.activity string.
                            ],
                        }}
                        """
                ],
            },
        ]
    )
    response = chat_session.send_message("generate")
    response_data = json.loads(response.text)

    return JsonResponse({"res": response_data})

@csrf_exempt
@require_http_methods(["POST"])
def post_generateItinerary(req, *args, **kwargs):
    data = json.loads(req.body)
    destination = data.get("destination")
    start_date  = data.get("start_date")
    end_date  = data.get("end_date")
    no_of_ppl  = data.get("no_of_ppl")
    budget  = data.get("budget")
    preference  = data.get("preference")

    #handle no of people
    if no_of_ppl == "Solo":
        no_of_ppl = 1
    elif no_of_ppl == "Couple":
        no_of_ppl = 2

    ##handle no of days
    try:
        start_date = datetime.strptime(start_date, '%d/%m/%Y')
    except ValueError:
        start_date = parser.parse(start_date)

    try:
        end_date = datetime.strptime(end_date, '%d/%m/%Y')
    except ValueError:
        end_date = parser.parse(end_date)


    delta = end_date - start_date
    num_of_days = delta.days

    
    genai.configure(api_key=GOOGLE_API_KEY)

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                     f"""
                        Generate a travel itinerary for {no_of_ppl} person(s) to {destination} for {num_of_days} days with travel preferences like {preference}. Consider the budget of {budget} for the travel. 
                        Generate a day-wise itinerary with sections like morning breakfast, morning activity, lunch, evening activity, dinner, and nightlife. Only generate the day itinerary without any extra information. 
                        Give only the JSON without any extra characters.

                        Generate in the below given JSON format:
                        {{
                            "name_entity": [
                                // This array will consist of all the named entities used in the itinerary.activities.activity string. Consider only the famous tourist destinations in itinerary.activities.activity string.
                            ], 
                            "about_destination": "Generate information about {destination}, such as what it is known for",
                            "weather_destination": "Generate information about the weather at {destination}, such as the best and average time to visit {destination}",
                            "currency_destination": "Generate information about the currency in use at {destination}, such as how much it will on average cost for a cup of tea",
                            "lang_destination": "Generate information about the spoken language in use at {destination}",
                            "itinerary": [
                                // This array will have elements as many as the days
                                {{
                                    "day_no": "1",
                                    "day_subject": "Day 1 Subject //Generate a subject for the day",
                                    "activities": [
                                        {{
                                            "activity_time": "Breakfast",
                                            "activity": "" // The real activity in the breakfast can be added here,
                                            "other options":["opt1","opt2","opt3","opt4","opt5"] // generate options for the activity. the options should not match any other activity in the whole itinerary.
                                        }},
                                        {{
                                            "activity_time": "Morning",
                                            "activity": "" // The real activity in the morning can be added here,
                                            "other options":["opt1","opt2","opt3","opt4","opt5"] // generate options for the activity. the options should not match any other activity in the whole itinerary.
                                        }},
                                        {{
                                            "activity_time": "Lunch",
                                            "activity": "" // The real activity in the lunch can be added here,
                                            "other options":["opt1","opt2","opt3","opt4","opt5"] // generate options for the activity. the options should not match any other activity in the whole itinerary.
                                        }},
                                        {{
                                            "activity_time": "Evening Activity",
                                            "activity": "" // The real activity in the evening activity can be added here,
                                            "other options":["opt1","opt2","opt3","opt4","opt5"] // generate options for the activity. the options should not match any other activity in the whole itinerary.
                                        }},
                                        {{
                                            "activity_time": "Night",
                                            "activity": "" // The real activity in the night can be added here,
                                            "other options":["opt1","opt2","opt3","opt4","opt5"] // generate options for the activity. the options should not match any other activity in the whole itinerary.
                                        }}
                                    ],
                                    "day_name_entity": [
                                        // This array will consist of all the named entities used in the itinerary.day.activities.activity string. Consider only the famous tourist destinations in itinerary.day.activities.activity string.
                                    ]
                                }},
                                // Repeat the structure for each day
                            ]
                        }}
                        """
                    ],
            },
        ]
    )

    try:
        response = chat_session.send_message("generate")
        if response:
            response_text = response.text
            response_text = response_text.replace('```', '')
            response_text = response_text.replace('json', '')
            response_data = json.loads(response_text)
            return JsonResponse({"res": response_data, "msg": "API Success"}, status=200)
        else:
            return JsonResponse({"res": "", "msg": "API Failed"}, status=424)
    except Exception as e:
        return JsonResponse({"res": "", "msg": f"API Error: {str(e)}"}, status=500)

def json_to_text(data, indent=0):
    text = ''
    for key, value in data.items():
        if isinstance(value, dict):
            text += ' ' * indent + f"{key}:\n"
            text += json_to_text(value, indent + 4)
        elif isinstance(value, list):
            text += ' ' * indent + f"{key}:\n"
            for item in value:
                text += ' ' * (indent + 4) + f"- {item}\n"
        else:
            text += ' ' * indent + f"{key}: {value}\n"
    return text

@csrf_exempt
@require_http_methods(["POST"])
def post_generateDayItinerary(req, *args, **kwargs):
    data = json.loads(req.body)
    old_itinerary = data.get("old_itinerary")
    day_no = data.get("day_no")
    old_itinerary_text = json_to_text(old_itinerary)
    genai.configure(api_key=GOOGLE_API_KEY)

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
            history=[
                {
                "role": "model",
                "parts": [ old_itinerary_text ],
                },
                {
                "role": "user",
                "parts": [
                    f"replace or regenerate the travel itinerary generated for day {day_no} with different activities for the day, w.r.t. the whole travel itinerary and activities not repeated in the whole itinerary. Only generate a new whole json. no other text muxt be generated",
                ],
                },
                ])
    try:
        response = chat_session.send_message("generate")
        if response:
            response_text = response.text
            print("Response text"+response_text)
            response_text = response_text.replace('```', '')
            response_text = response_text.replace('json', '')
            response_data = json.loads(response_text)
            return JsonResponse({"res": response_data, "msg": "API Success"}, status=200)
        else:
            return JsonResponse({"res": "", "msg": "API Failed"}, status=424)
    except Exception as e:
        return JsonResponse({"res": "", "msg": f"API Error: {str(e)}"}, status=500)



    



        