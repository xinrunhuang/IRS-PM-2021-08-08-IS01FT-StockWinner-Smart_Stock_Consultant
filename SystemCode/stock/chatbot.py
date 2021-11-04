import os
import json
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'
# import google.cloud.aiplatform.helpers.value_converter as goo
# from google.cloud import storage
#
#     # Explicitly use service account credentials by specifying the private key
#     # file.
# storage_client = storage.Client.from_service_account_json(
#     'private_key.json')
#
# # Make an authenticated API request
# buckets = list(storage_client.list_buckets())
# print(buckets)
def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    # print("Session path: {}\n".format(session))

    
    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    # print("=" * 20)
    # print("Query text: {}".format(response.query_result.query_text))
    # print(
    #     "Detected intent: {} (confidence: {})\n".format(
    #         response.query_result.intent.display_name,
    #         response.query_result.intent_detection_confidence,
    #     )
    # )
    # print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
    # print('#####')
    # print(type(response.query_result))
    # para = result["parameters"]["coinname"]
    # result = goo.to_value(response.query_result)
    # print(type(result))
    # new_dict = json.loads(result)
    # print('parameter: ',result.struct_value.fields['parameters'])
    return response.query_result.fulfillment_text
def chat_stock(question):
    answer = detect_intent_texts('stockchatbot-vqdq','123',question,'en-US')
    return answer