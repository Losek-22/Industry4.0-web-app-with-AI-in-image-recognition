from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import zipfile
import os


def retrieve_classifiers_dict():
    """
    Connects to IBM Cloud and retrieves a dict of available classifiers' classifier_ids, names and training statuses
    :return: dict
    """
    try:
        authenticator = IAMAuthenticator('e9Eeu6hkRaPEwO05UYRLrGmmot3OvDqa-1DLfjuY85ad')

        visual_recognition = VisualRecognitionV3(
            '2019-12-19',
            authenticator=authenticator)

        visual_recognition.set_service_url(
            'https://api.us-south.visual-recognition.watson.cloud.ibm.com/instances/8c0dc5a5-aae6-4f84-a1ba-50563dc2b957'
        )

        classifiers = visual_recognition.list_classifiers(verbose=False).get_result()
        return classifiers['classifiers']

    except ApiException as ex:
        response = f"Wystąpił błąd o kodzie {str(ex.code)}: {ex.message}"
        return response


print(retrieve_classifiers_dict())
