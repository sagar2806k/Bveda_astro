import streamlit as st
import json
import os
import requests
import openai
from dotenv import load_dotenv

from langsmith import Client
from datetime import datetime



load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


MODEL = 'gpt-4o-mini'
api_key = "752efcf5-2bf9-5d82-b422-f04db5f4d7dd"

def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%d-%m-%Y").strftime("%d/%m/%Y")
    except ValueError:
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%d/%m/%Y")


def personal_characteristics(dob, lat, lon, tz, tob, lang='en'):
    url = "https://api.vedicastroapi.com/v3-json/horoscope/personal-characteristics"
    params = {"dob": dob, "lat": lat, "lon": lon, "tz": tz, "tob": tob, "api_key": api_key, "lang": lang}
    response = requests.get(url, params=params)
    return {"personal_characteristics": response.json()} if response.status_code == 200 else None

def ascendent_report(dob, lat, lon, tz, tob, lang):
    url = "https://api.vedicastroapi.com/v3-json/horoscope/ascendant-report"
    params = {"dob": dob, "lat": lat, "lon": lon, "tz": tz, "tob": tob, "api_key": api_key, "lang": lang}
    response = requests.get(url, params=params)
    return {"ascendent_report": response.json()} if response.status_code == 200 else None

def mahadasha_predictions(dob, lat, lon, tz, tob, lang):
    url = "https://api.vedicastroapi.com/v3-json/dashas/maha-dasha-predictions"
    params = {"dob": dob, "lat": lat, "lon": lon, "tz": tz, "tob": tob, "api_key": api_key, "lang": lang}
    response = requests.get(url, params=params)
    return {"mahadasha_predictions": response.json()} if response.status_code == 200 else None

def manglik_dosh(dob, lat, lon, tz, tob, lang):
    url = "https://api.vedicastroapi.com/v3-json/dosha/manglik-dosh"
    params = {"dob": dob, "lat": lat, "lon": lon, "tz": tz, "tob": tob, "api_key": api_key, "lang": lang}
    response = requests.get(url, params=params)
    return {"manglik_dosh": response.json()} if response.status_code == 200 else None

def kaalsarp_dosh(dob, lat, lon, tz, tob, lang):
    url = "https://api.vedicastroapi.com/v3-json/dosha/kaalsarp-dosh"
    params = {"dob": dob, "lat": lat, "lon": lon, "tz": tz, "tob": tob, "api_key": api_key, "lang": lang}
    response = requests.get(url, params=params)
    return {"kaalsarp_dosh": response.json()} if response.status_code == 200 else None

def daily_sun(date,zodiac,type,lang):
    formatted_date = format_date(date)
    url = "https://api.vedicastroapi.com/v3-json/prediction/daily-sun"
    params = {"date":formatted_date,"zodiac":zodiac,"type":type,"lang":lang,"api_key":api_key}
    response = requests.get(url, params=params)
    return {"daily_sun": response.json()} if response.status_code == 200 else None

def daily_moon(date,zodiac,type,lang):
    formatted_date = format_date(date)
    url = "https://api.vedicastroapi.com/v3-json/prediction/daily-moon"
    params = {"date":formatted_date,"zodiac":zodiac,"type":type,"lang":lang,"api_key":api_key}
    response = requests.get(url, params=params)
    return {"daily_moon": response.json()} if response.status_code == 200 else None

def weekly_sun(week,zodiac,type,lang):
    url = "https://api.vedicastroapi.com/v3-json/prediction/weekly-sun"
    params = {"week":week,"zodiac":zodiac,"type":type,"lang":lang,"api_key":api_key}
    response = requests.get(url, params=params)
    return {"weekly_sun": response.json()} if response.status_code == 200 else None

def weekly_moon(week,zodiac,type,lang):
    url = "https://api.vedicastroapi.com/v3-json/prediction/weekly-moon"
    params = {"week":week,"zodiac":zodiac,"type":type,"lang":lang,"api_key":api_key}
    response = requests.get(url, params=params)
    return {"weekly_moon": response.json()} if response.status_code == 200 else None

def yearly_predictions(year,zodiac,lang):
    url = "https://api.vedicastroapi.com/v3-json/prediction/yearly"
    params = {"year":year,"zodiac":zodiac,"lang":lang,"api_key":api_key}
    response = requests.get(url, params=params)
    return {"yearly_predictions": response.json()} if response.status_code == 200 else None

#response=personal_characteristics(dob="06/03/2000", lat="21.1255", lon="73.1122", tz=5.5, tob="10:00", lang='en')
#print(response)

def run_conversation(user_prompt):
    messages = [
        {
            "role": "system",
            "content": "You are a highly knowledgeable astrology assistant. When the user provides birth details, you should call the appropriate function to generate a personalized astrological analysis."
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]

    tools = [
        {
    "type": "function",
    "function": {
        "name": "personal_characteristics",
        "description": "This function provides insights into personal characteristics based on astrological analysis. It uses the user's birth details to determine various traits and tendencies.",
        "parameters": {
            "type": "object",
            "properties": {
                "dob": {
                    "type": "string",
                    "description": "The user's date of birth in DD/MM/YYYY format."
                },
                "tob": {
                    "type": "string",
                    "description": "The user's time of birth in HH:MM format."
                },
                "lat": {
                    "type": "string",
                    "description": "The latitude of the location where the user was born."
                },
                "lon": {
                    "type": "string",
                    "description": "The longitude of the location where the user was born."
                },
                "tz": {
                    "type": "number",
                    "description": "The time zone offset from GMT at the time of birth."
                },
                "lang": {
                    "type": "string",
                    "description": "The language in which the response should be provided."
                }
            },
            "required": ["dob", "tob", "lat", "lon", "tz", "lang"]
        }
    }
},
        {
        "type": "function",
        "function": {
            "name": "ascendent_report",
            "description": "Generate a detailed report on the user's ascendant (rising sign), providing insights into their outward behavior, first impressions, and general demeanor.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dob": {
                        "type": "string",
                        "description": "The user's date of birth in DD/MM/YYYY format."
                    },
                    "tob": {
                        "type": "string",
                        "description": "The user's time of birth in HH:MM format."
                    },
                    "lat": {
                        "type": "string",
                        "description": "The latitude of the location where the user was born."
                    },
                    "lon": {
                        "type": "string",
                        "description": "The longitude of the location where the user was born."
                    },
                    "tz": {
                        "type": "number",
                        "description": "The time zone offset from GMT at the time of birth."
                    },
                    "lang": {
                        "type": "string",
                        "description": "The language in which the response should be provided."
                    }
                },
                "required": ["dob", "tob", "lat", "lon", "tz", "lang"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mahadasha_predictions",
            "description": "Provide predictions related to the mahadasha_predictions, offering insights into the significant life events and changes expected during this period based on Vedic astrology.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dob": {
                        "type": "string",
                        "description": "The user's date of birth in DD/MM/YYYY format."
                    },
                    "tob": {
                        "type": "string",
                        "description": "The user's time of birth in HH:MM format."
                    },
                    "lat": {
                        "type": "string",
                        "description": "The latitude of the location where the user was born."
                    },
                    "lon": {
                        "type": "string",
                        "description": "The longitude of the location where the user was born."
                    },
                    "tz": {
                        "type": "number",
                        "description": "The time zone offset from GMT at the time of birth."
                    },
                    "lang": {
                        "type": "string",
                        "description": "The language in which the response should be provided."
                    }
                },
                "required": ["dob", "tob", "lat", "lon", "tz", "lang"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "manglik_dosh",
            "description": "Check for the presence of Manglik Dosh in the user's birth chart and provide relevant predictions regarding its effects on their life, particularly in marriage.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dob": {
                        "type": "string",
                        "description": "The user's date of birth in DD/MM/YYYY format."
                    },
                    "tob": {
                        "type": "string",
                        "description": "The user's time of birth in HH:MM format."
                    },
                    "lat": {
                        "type": "string",
                        "description": "The latitude of the location where the user was born."
                    },
                    "lon": {
                        "type": "string",
                        "description": "The longitude of the location where the user was born."
                    },
                    "tz": {
                        "type": "number",
                        "description": "The time zone offset from GMT at the time of birth."
                    },
                    "lang": {
                        "type": "string",
                        "description": "The language in which the response should be provided."
                    }
                },
                "required": ["dob", "tob", "lat", "lon", "tz", "lang"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "kaalsarp_dosh",
            "description": "Analyze the user's birth chart to identify the presence of Kaalsarp Dosh and predict its impact on various aspects of their life, including challenges and remedies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dob": {
                        "type": "string",
                        "description": "The user's date of birth in DD/MM/YYYY format."
                    },
                    "tob": {
                        "type": "string",
                        "description": "The user's time of birth in HH:MM format."
                    },
                    "lat": {
                        "type": "string",
                        "description": "The latitude of the location where the user was born."
                    },
                    "lon": {
                        "type": "string",
                        "description": "The longitude of the location where the user was born."
                    },
                    "tz": {
                        "type": "number",
                        "description": "The time zone offset from GMT at the time of birth."
                    },
                    "lang": {
                        "type": "string",
                        "description": "The language in which the response should be provided."
                    }
                },
                "required": ["dob", "tob", "lat", "lon", "tz", "lang"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "daily_sun",
            "description": "Fetch the daily sun prediction based on the provided date, zodiac sign, type, and language.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Date for the prediction in DD-MM-YYYY format."
                    },
                    "zodiac": {
                        "type": "integer",
                        "description": "The user's zodiac sign (e.g., Aries, Taurus)."
                    },
                    "type": {
                        "type": "string",
                        "description": "Type of prediction (e.g., 'general', 'career')."
                    },
                    "lang": {
                        "type": "string",
                        "description": "The language code (e.g., 'en' for English)."
                    }
                },
                "required": ["date", "zodiac", "type", "lang"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "daily_moon",
            "description": "Fetch the daily moon prediction based on the provided date, zodiac sign, type, and language.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Date for the prediction in DD-MM-YYYY format."
                    },
                    "zodiac": {
                        "type": "integer",
                        "description": "The user's zodiac sign (e.g., Aries, Taurus)."
                    },
                    "type": {
                        "type": "string",
                        "description": "Type of prediction (e.g., 'general', 'career')."
                    },
                    "lang": {
                        "type": "string",
                        "description": "The language code (e.g., 'en' for English)."
                    }
                },
                "required": ["date", "zodiac", "type", "lang"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "weekly_moon",
        "description": "Provide weekly moon predictions based on the specified week.",
        "parameters": {
            "type": "object",
            "properties": {
                "week": {
                    "type": "string",
                    "enum": ["this week", "next week"],
                    "description": "Specify 'this week' or 'next week'."
                },
                "zodiac": {
                    "type": "integer",
                    "description": "Zodiac sign"
                },
                "type": {
                    "type": "string",
                    "description": "Prediction type"
                },
                "lang": {
                    "type": "string",
                    "description": "Language"
                }
            },
            "required": ["week", "zodiac", "type", "lang"]
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "weekly_sun",
        "description": "Provide weekly sun predictions based on the specified week.",
        "parameters": {
            "type": "object",
            "properties": {
                "week": {
                    "type": "string",
                    "enum": ["this week", "next week"],
                    "description": "Specify 'this week' or 'next week'."
                },
                "zodiac": {
                    "type": "integer",
                    "description": "Zodiac sign"
                },
                "type": {
                    "type": "string",
                    "description": "Prediction type"
                },
                "lang": {
                    "type": "string",
                    "description": "Language"
                }
            },
            "required": ["week", "zodiac", "type", "lang"]
        }
    }
},
    {
        "type": "function",
        "function": {
            "name": "yearly_predictions",
            "description": "Provide yearly predictions based on the user's zodiac sign and type of prediction.",
            "parameters": {
                "type": "object",
                "properties": {
                    "year": {
                        "type": "string",
                        "description": "Specify the year for the prediction."
                    },
                    "zodiac": {
                        "type": "integer",
                        "description": "The user's zodiac sign."
                    },
                    "type": {
                        "type": "string",
                        "description": "Type of prediction (e.g., 'general', 'career')."
                    },
                    "lang": {
                        "type": "string",
                        "description": "The language code (e.g., 'en' for English)."
                    }
                },
                "required": ["year", "zodiac", "type", "lang"]
            }
        }
    },
    ]

    response = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    print("LLM Initial Response:", response)
    print("----------------------------")

    response_message = response.choices[0].message
    tool_calls = getattr(response_message, 'tool_calls', None)
    
    print("Tool Calls:", tool_calls)
    print("----------------------------")

    if tool_calls:
        available_functions = {
            "personal_characteristics": personal_characteristics,
            "ascendent_report": ascendent_report,
            "mahadasha_predictions": mahadasha_predictions,
            "manglik_dosh": manglik_dosh,
            "kaalsarp_dosh": kaalsarp_dosh,
            "daily_sun": daily_sun,
            "daily_moon": daily_moon,
            "weekly_sun": weekly_sun,
            "weekly_moon": weekly_moon,
            "yearly_predictions": yearly_predictions
        }

        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            
            print("Function Arguments:", function_args)
            
            if function_name in ["daily_sun", "daily_moon"]:
                date = function_args.get("date")  
                zodiac = function_args.get("zodiac")
                prediction_type = function_args.get("type")
                lang = function_args.get("lang")
                formatted_date = format_date(date)
                function_response = function_to_call(
                    date=formatted_date,
                    zodiac=zodiac,
                    type=prediction_type,
                    lang=lang
                )
            elif function_name in ["weekly_sun","weekly_moon"]:
                week = function_args.get("week")
                zodiac = function_args.get("zodiac")
                prediction_type = function_args.get("type")
                lang = function_args.get("lang")

                if "next" in week.lower():
                    week = "nextweek"
                elif "this" in week.lower():
                    week = "thisweek"

                function_response = function_to_call(
                    week=week,
                    zodiac=zodiac,
                    type=prediction_type,
                    lang=lang
                )


            elif function_name in ["personal_characteristics", "ascendent_report", "mahadasha_predictions", "manglik_dosh", "kaalsarp_dosh"]:
                dob = function_args.get("dob")
                tob = function_args.get("tob")
                lat = function_args.get("lat")
                lon = function_args.get("lon")
                tz = function_args.get("tz")
                lang = function_args.get("lang")
                
                function_response = function_to_call(
                    dob=dob,
                    tob=tob,
                    lat=lat,
                    lon=lon,
                    tz=tz,
                    lang=lang
                )
            else:
              function_name == ["yearly_predictions"]
              zodiac = function_args.get("zodiac")
              year = function_args.get("year")
              lang = function_args.get("lang")
                
              function_response = function_to_call(
                    zodiac=zodiac,
                    year=year,
                    lang=lang
                )
        
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response)
                }
            )

        second_response = openai.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        
        return second_response.choices[0].message.content

    else:
        return response_message.content


st.title("Astrology Chatbot")

st.write("Please provide your birth details to receive astrological insights.")
category = st.selectbox("Select Category", ["General", "Daily", "Weekly", "Yearly"])

# Initialize variables
dob = tob = lat = lon = tz = lang = zodiac = date = week = year = user_prompt = None

if category == "General":
    dob = st.text_input('Date of Birth (DD/MM/YYYY)')
    tob = st.text_input('Time of Birth (HH:MM)')
    lat = st.text_input('Latitude')
    lon = st.text_input('Longitude')
    tz = st.number_input('Time Zone',)
    lang = st.text_input('Language')
    user_prompt = st.text_area('Enter your prompt')
elif category == "Daily":
    date = st.text_input('Date (DD/MM/YYYY)')
    zodiac = st.text_input('Zodiac Sign')
    type = st.text_input('Type')
    lang = st.text_input('Language')
    user_prompt = st.text_area('Enter your prompt')
elif category == "Weekly":
    week = st.text_input('Week')
    zodiac = st.text_input('Zodiac Sign')
    type = st.text_input('Type')
    lang = st.text_input('Language')
    user_prompt = st.text_area('Enter your prompt')
else:
    category == "Yearly"
    zodiac = st.text_input('Zodiac Sign')
    year = st.text_input('Year (YYYY)')
    lang = st.text_input('Language')
    user_prompt = st.text_area('Enter your prompt')

if st.button('Get Prediction'):
    full_prompt = f"""
You are an astrology expert and will provide clear, positive, and easy-to-understand answers. Since the user might not be familiar with astrology, your responses should be simple, engaging, and maintain a positive tone.

Tasks:
Analyze the User's Question:

Determine the type of astrology prediction the user is asking for (e.g., daily sun, daily moon, weekly sun, weekly moon, yearly predictions, personal characteristics, or specific doshas like Manglik or Kaalsarp).
Identify and Call Relevant Functions:

Based on your analysis, call the appropriate function(s) using the user's birth details.
Ensure that all required parameters are included when calling these functions.
Handle Timeframes:

If the question specifies a time period (e.g., "this week," "next week," or a particular year), pass these as parameters when calling the functions.
Multiple Functions:

If the user's question covers multiple areas (e.g., a mix of personal characteristics and doshas), don't hesitate to call more than one function.
User's Input Details:
Question: {user_prompt}
Date of Birth: {dob}
Time of Birth: {tob}
Latitude: {lat}
Longitude: {lon}
Time Zone: {tz}
Language: {lang}
Zodiac Sign: {zodiac}
Date: {date}
Week: {week}
Year: {year}
Type: {type}

Instructions:
Respond Positively: Ensure that every response is optimistic and encouraging.
Simplify Astrology Concepts: Break down complex astrological terms and concepts into easy-to-understand language.
Maintain Clarity: Your responses should be straightforward and free of jargon.
Use these details to craft responses that are both insightful and accessible to the user.


"""
    print("================================")
    print(full_prompt)
    prediction = run_conversation(full_prompt)
    st.write(prediction)
    


    
    