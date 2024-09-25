from onesignal_sdk.client import Client

APP_ID = "10fc5650-8980-401f-bc8c-0308494f473b"
REST_API_KEY = "MjdmMjRhMDAtZjM4NC00YTA0LWI4MzAtNDViZjczZGNjOGU4"
USER_AUTH_KEY = "NDI0MGExNjYtMjlmNi00M2ViLTkyMjEtZDY4MTEyMzk4ZjYz"

client = Client(app_id=APP_ID, rest_api_key=REST_API_KEY, user_auth_key=USER_AUTH_KEY)

notification_body = {
    "contents": {"tr": "Yeni bildirim", "en": "New notification"},
    "included_segments": ["Active Users"],
    "filters": [{"field": "tag", "key": "level", "relation": ">", "value": 10}],
}
response = client.send_notification(notification_body)
print(response.body)
