import requests
import json
import base64

class RestClient:

    def __init__(self) -> None:
        self.url_prefix = "http://localhost:8000/model"
        pass

    def train(self, AI_API_KEY: str, uploaded_file, data_type):

        payload = {
            "data": base64.b64encode(uploaded_file.getvalue()).decode('utf-8'),
            "data_type": data_type
        }

        json_payload = json.dumps(payload)

        resp = self.call_api(url=f'{self.url_prefix}/train', AI_API_KEY=AI_API_KEY, json_payload=json_payload)
        return {
            'data': json.loads(resp.text),
            'status': resp.status_code == 201
        }

    def summerize_video(self, AI_API_KEY: str, video_id, data_type) -> dict:

        history = [('moral of story in 3 words', 'Unity is strength.')]
        payload = {
            'session_id': '',
            "prompt": video_id,
            'history': history,
            'data_type': data_type
        }

        json_payload = json.dumps(payload)

        resp = self.call_api(url=f'{self.url_prefix}/predict', AI_API_KEY=AI_API_KEY, json_payload=json_payload)

        return {
            'data': json.loads(resp.text),
            'status': resp.status_code == 200
        }
    
    def predict(self, AI_API_KEY: str, session_id: str, prompt: str, history, data_type) -> dict:
        
        # Set up the request body
        payload = {
            'session_id': session_id,
            'prompt': prompt,
            'history': history,
            'data_type': data_type
        }
        json_payload = json.dumps(payload)

        resp = self.call_api(url=f'{self.url_prefix}/predict', AI_API_KEY=AI_API_KEY, json_payload= json_payload)

        return {
            'data': json.loads(resp.text),
            'status': resp.status_code == 200
        }
    
    def predict_sheet(self, AI_API_KEY: str, prompt: str, uploaded_file, data_type) -> dict:
        
        # Set up the request body
        payload = {
            'prompt': prompt,
            'data': base64.b64encode(uploaded_file.getvalue()).decode('utf-8'),
            'data_type': data_type
        }

        json_payload = json.dumps(payload)

        resp = self.call_api(url=f'{self.url_prefix}/sheet/predict', AI_API_KEY=AI_API_KEY, json_payload= json_payload)
        return {
            'data': json.loads(resp.text),
            'status': resp.status_code == 200
        }
       
    def call_api(self, url, AI_API_KEY, json_payload, files=None) -> requests.Response:
        
         # Set up the headers
        headers = {
            "AI-API-KEY": AI_API_KEY,
        }

        # Make the POST request
        response = requests.post(url, headers=headers, data=json_payload, files=files)

        return response
    

restClient = RestClient()