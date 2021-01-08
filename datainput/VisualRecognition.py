from ibm_watson import VisualRecognitionV3, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import zipfile
import os
import json


def classify_image_v3(picture_name, classifier_id):
    """
    Performs authentication at IBM Cloud and sends a classification request
    :param picture_name: string
    :param classifier_id: string
    :return: classification_result (list) or an ApiException
    """

    classification_result = []
    try:
        authenticator = IAMAuthenticator('e9Eeu6hkRaPEwO05UYRLrGmmot3OvDqa-1DLfjuY85ad')
        service = VisualRecognitionV3(
            '2019-12-19',
            authenticator=authenticator)

        service.set_service_url(
         'https://api.us-south.visual-recognition.watson.cloud.ibm.com/instances/8c0dc5a5-aae6-4f84-a1ba-50563dc2b957'
        )

        with open(f'./pictures/classified_images/{picture_name}', 'rb') as images_file:
            response = service.classify(images_file=images_file,
                                        classifier_ids=classifier_id
                                        ).get_result()

        for dictionary in response['images'][0]['classifiers'][0]['classes']:
            classification_result.append(dictionary['class'])

        return classification_result

    except ApiException as ex:
        response = f"Wystąpił błąd o kodzie {str(ex.code)}: {ex.message}"
        return response


def create_classifier(training_data_dict, negative_class, classifier_name):
    """
    Connects to IBM Cloud using API and creates a custom classifier.
    :param training_data_dict: dict
    :param negative_class: .zip file
    :param classifier_name: string
    :return: json
    """
    try:
        authenticator = IAMAuthenticator('e9Eeu6hkRaPEwO05UYRLrGmmot3OvDqa-1DLfjuY85ad')

        visual_recognition = VisualRecognitionV3(
            '2019-12-19',
            authenticator=authenticator)

        visual_recognition.set_service_url(
         'https://api.us-south.visual-recognition.watson.cloud.ibm.com/instances/8c0dc5a5-aae6-4f84-a1ba-50563dc2b957'
        )

        model = visual_recognition.create_classifier(
            name=classifier_name,
            positive_examples=training_data_dict,
            negative_examples=negative_class
        ).get_result()

        return model

    except ApiException as ex:
        response = f"Wystąpił błąd o kodzie {str(ex.code)}: {ex.message}"
        return response


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


def retrieve_classes_of_classifier(classifier_id):
    """
    Given a classifier id, returns the list of classes the classifier has.
    :param classifier_id: string
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

        return visual_recognition.get_classifier(classifier_id=classifier_id).get_result()["classes"]

    except ApiException as ex:
        response = f"Wystąpił błąd o kodzie {str(ex.code)}: {ex.message}"
        return response


print(retrieve_classifiers_dict())
