from flask import Flask, request, jsonify
import json
import os
import requests
from dotenv import load_dotenv
from groq import Groq
import streamlit as st 



load_dotenv()
os.environ["GROQ_API_KEY"] = "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"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = 'llama3-groq-70b-8192-tool-use-preview'
api_key = "94727561-cbcb-5587-bbe1-4faf6237ef4f"

app = Flask(__name__)


def personal_characteristics(personId):
    url = "https://astrology-backend-ddcz.onrender.com/api/v1/api-function/horoscope/personal-characteristics"
    params = {"personId": personId}
    response = requests.get(url, params=params)
    return {"personal_characteristics": response.json()} if response.status_code == 200 else {"error": "Failed to fetch data"}

def ascendent_report(personId):
    #api_key = "94727561-cbcb-5587-bbe1-4faf6237ef4f"
    url = "https://astrology-backend-ddcz.onrender.com/api/v1/api-function/horoscope/ascendant-report"
    params = {"personId": personId}
    response = requests.get(url, params=params)
    return {"ascendent_report": response.json()} if response.status_code == 200 else {"error": "Failed to fetch data"}

def mahadasha_predictions(personId):
    #api_key = "94727561-cbcb-5587-bbe1-4faf6237ef4f"
    url = "https://astrology-backend-ddcz.onrender.com/api/v1/api-function/dashas/maha-dasha-predictions"
    params = {"personId": personId}
    response = requests.get(url, params=params)
    return {"mahadasha_predictions": response.json()} if response.status_code == 200 else {"error": "Failed to fetch data"}

def manglik_dosh(personId):
    #api_key = "94727561-cbcb-5587-bbe1-4faf6237ef4f"
    url = "https://astrology-backend-ddcz.onrender.com/api/v1/api-function/dosha/manglik-dosh"
    params = {"personId": personId}
    response = requests.get(url, params=params)
    return {"manglik_dosh": response.json()} if response.status_code == 200 else {"error": "Failed to fetch data"}

def kaalsarp_dosh(personId):
    #api_key = "94727561-cbcb-5587-bbe1-4faf6237ef4f"
    url = "https://astrology-backend-ddcz.onrender.com/api/v1/api-function/dosha/kaalsarp-dosh"
    params = {"personId": personId}
    response = requests.get(url, params=params)
    return {"kaalsarp_dosh": response.json()} if response.status_code == 200 else {"error": "Failed to fetch data"}


#response=personal_characteristics(dob="06/03/2000", lat="21.1255", lon="73.1122", tz=5.5, tob="10:00", lang='en')
#print(response)

def run_conversation(user_prompt):
    messages = [
        {
            "role": "system",
            "content": "You are a highly knowledgeable astrology assistant. Based on the user's prompt, provide predictions and call the relevant functions to generate these predictions."
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
        "description": "Based on the user's birth details, provide a personalized analysis of their personality traits, strengths, and weaknesses, also marriage details. Offer insights that can help them understand themselves better.",
        "parameters": {
            "type": "object",
            "properties": {
                "personId": {
                    "type": "integer",
                    "description": "Unique identifier for the person."
                }
            },
            "required": ["personId"]
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
                "personId": {
                    "type": "integer",
                    "description": "Unique identifier for the person."
                }
            },
            "required": ["personId"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "mahadasha_predictions",
        "description": "Provide predictions related to the Mahadasha period, offering insights into the significant life events and changes expected during this period based on Vedic astrology.",
        "parameters": {
            "type": "object",
            "properties": {
                "personId": {
                    "type": "integer",
                    "description": "Unique identifier for the person."
                }
            },
            "required": ["personId"]
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
                "personId": {
                    "type": "integer",
                    "description": "Unique identifier for the person."
                }
            },
            "required": ["personId"]
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
                "personId": {
                    "type": "integer",
                    "description": "Unique identifier for the person."
                }
            },
            "required": ["personId"]
        }
    }
}
    ]

    response = client.chat.completions.create(
        messages=messages,
        model=MODEL,
        tools=tools,  
        tool_choice="required",
        max_tokens=4096,
    )

    response_message = response.choices[0].message
    #print(f"Initial response: {response_message} \n")

    tool_calls = getattr(response_message, 'tool_calls', None)
    print(f"{tool_calls}")

    print("Final response: ")

    if tool_calls:
        available_functions = {
            "personal_characteristics": personal_characteristics,
            "ascendent_report": ascendent_report,
            "mahadasha_predictions":mahadasha_predictions,
            "manglik_dosh":manglik_dosh,
            "kaalsarp_dosh":kaalsarp_dosh
        }
        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(personId=function_args.get("personId"))
            
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response)
                }
            )
            
            second_response = client.chat.completions.create(
                model=MODEL,
                messages=messages
            )
            return second_response.choices[0].message.content
    else:
        return response.choices[0].message.content
    

@app.route('/get-astrology-prediction', methods=['post'])
def get_astrology_prediction():
    data = request.get_json()

    person_id = data.get("person_id")
    user_details = data.get("user_details")
    user_prompt = data.get("user_prompt")

    # Create full prompt using user details
    full_prompt = f"""
    You are an astrology expert. The user does not understand astrology, so please answer in a way that is understandable and provide a short explanation. Keep the tone positive.
    Here is the user's question: {user_prompt}.
    User's details: Date of birth: {user_details.get('dob')}, Time of birth: {user_details.get('tob')}, Latitude: {user_details.get('lat')}, Longitude: {user_details.get('lon')}, Time zone: {user_details.get('tz')}, Language: {user_details.get('lang')}
    If you cannot determine which function to call, always use the 'personal_characteristics' function.
    """

    # Get prediction using LLM
    prediction = run_conversation(full_prompt)

    response = {
        "person_id": person_id,
        "prediction": prediction,
        "error": None
    }

    return jsonify(response)

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8000, debug=True)
     
    

# # user_prompt = "Please give me some points about challenges and remedies?. Here are the details: Date of birth: 06/03/2000, Time of birth: 10:00, Latitude: 28.7041, Longitude: 77.1025, Time zone: 5.5, Language: en."
# # print(run_conversation(user_prompt))
    
# # Streamlit app
# st.title("Astrology Chatbot")

# st.write("Please provide your birth details to receive astrological insights.")

# dob = st.text_input('Date of Birth (DD/MM/YYYY)')
# tob = st.text_input('Time of Birth (HH:MM)')
# lat = st.text_input('Latitude')
# lon = st.text_input('Longitude')
# tz = st.number_input('Time Zone')
# lang = st.text_input('Language')

# user_prompt = st.text_area('Enter your prompt')

# if st.button('Get Prediction'):
#     full_prompt = f"""
#     You are an astrology expert, User do not understand astrology, so please answer which is understandable and with short explanation. 
#     Also make sure to keep tone positive always. User will provide question and his basic birth details required by astrologer.
#     Following is users questions:
#     {user_prompt}. 
#     Here are the details of the user: Date of birth: {dob}, Time of birth: {tob}, Latitude: {lat}, Longitude: {lon}, Time zone: {tz}, Language: {lang}

#     Also, it may not be possible to determine which function to call, if question is open ended in that case always use 'personal_characteristics' function only. 
#     """

#     full_prompt_v2 =f"""
#     You are an astrology expert, User do not understand astrology, so please answer which is understandable and with short explanation. Do not talk about planet and houses but answer in a conversational way.  
#     Also make sure to keep tone positive always.
#     {user_prompt} Here are the details of the user: Date of birth: {dob}, Time of birth: {tob}, Latitude: {lat}, Longitude: {lon}, Time zone: {tz}, Language: {lang}"""

#     print("================================")
#     print(full_prompt)
#     prediction = run_conversation(full_prompt_v2)
#     st.write(prediction)
