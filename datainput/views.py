from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from .VisualRecognition import *
from .models import Measurements
from PIL import Image
import os

image_size = [400, 400]  # size of an image sent to IBM for classification


@login_required(login_url='/login',
                redirect_field_name="")
def index(request):
    return render(request, "datainput/index.html")


@login_required(login_url='/login',
                redirect_field_name="")
def visual_rec_menu(request):
    return render(request, "datainput/visual_rec_menu.html")


@login_required(login_url='/login',
                redirect_field_name="")
def add_data(request):
    return render(request, "add_data.html")


def userlogin(request):
    return render(request, "login.html")


@login_required(login_url='/login',
                redirect_field_name="")
def userlogout(request):
    logout(request)
    return render(request, "logout.html")


@csrf_protect
def login_attempt(request):

    username = request.POST["InputLogin"]
    password = request.POST["InputPassword"]

    if request.method == "POST":
        user = authenticate(username=username, password=password)
        just_logged_in = 1

        if user is not None:
            login(request, user)
            return render(request, "datainput/index.html", {'just_logged_in': just_logged_in})
        else:
            wrong_credentials = 1
            return render(request, "login.html", {'wrong_credentials': wrong_credentials})
    else:
        return render(request, "datainput/index.html")


@login_required(login_url='/login',
                redirect_field_name="")
def which_classifier_to_teach(request):

    classifiers_dict = retrieve_classifiers_dict()
    classifier_id = None

    try:
        if request.method == 'POST':

            if isinstance(classifiers_dict, list):

                for classifier in classifiers_dict:
                    if classifier['name'] == chosen_classifier:
                        classifier_id = classifier['classifier_id']

                retrieve_classes_of_classifier(classifier_id=classifier_id)

                return render(request, "datainput/visual_rec_teach.html", {'list_of_classes': list_of_classes,
                                                                           'api_error': 0,
                                                                           'unknown_error': 0})
            else:
                return render(request, "datainput/teach_a_classifier.html", {'classifiers_dict': classifiers_dict,
                                                                             'api_error': 1,
                                                                             'unknown_error': 0})

        else:
            if isinstance(classifiers_dict, list):
                print(classifiers_dict)
                return render(request, "datainput/teach_a_classifier.html", {'classifiers_dict': classifiers_dict,
                                                                             'api_error': 0,
                                                                             'unknown_error': 0})
            else:
                return render(request, "datainput/teach_a_classifier.html", {'classifiers_dict': classifiers_dict,
                                                                             'api_error': 1,
                                                                             'unknown_error': 0})

    except:
        return render(request, "datainput/teach_a_classifier.html", {'classifiers_dict': None,
                                                                     'api_error': 0,
                                                                     'unknown_error': 1})


@login_required(login_url='/login',
                redirect_field_name="")
def choose_classifier(request):

    classifier_id = None

    try:
        classifiers_dict = retrieve_classifiers_dict()

        if request.method == 'POST':

            chosen_classifier = request.POST.get('classifier')
            uploaded_picture = request.FILES.get('document')

            if uploaded_picture:  # was an image sent?

                for classifier in classifiers_dict:
                    if classifier['name'] == chosen_classifier:
                        classifier_id = classifier['classifier_id']

                img = Image.open(uploaded_picture)
                img.thumbnail(image_size, Image.ANTIALIAS)  # resize
                picture_name = uploaded_picture.name
                img.save(f'pictures/classified_images/{picture_name}')
                isvalid = picture_name.endswith('.jpg') or picture_name.endswith('.png') or picture_name.endswith('.jpeg')

                if isvalid:

                    # IBM classification imported from VisualRecognition.py
                    classification_result = classify_image_v3(picture_name=picture_name,
                                                              classifier_id=classifier_id)

                    # go to classifier's directory in the classifiers folder
                    if os.path.isdir(f"../wip/classifiers/{chosen_classifier}"):
                        os.chdir(os.path.join('../wip/classifiers/', chosen_classifier))

                        final_data_list_of_dict = None  # getting rid of a warning

                        # more than one result is a possibility
                        for result in classification_result:
                            result_datafile = open(f'{result}.txt', 'r')

                            # [1] to get rid of the comments, [:-2] to get rid of new line sign
                            result_data = {'class_name': str(result_datafile.readline().split('->')[1])[:-2],
                                           'short_description': str(result_datafile.readline().split('->')[1])[:-2],
                                           'long_description': str(result_datafile.readline().split('->')[1])[:-2],
                                           'more_info_link': str(result_datafile.readline().split('->')[1])[:-2]}

                            final_data_list_of_dict = [result_data]

                        return render(request, "datainput/visual_rec_result.html", {'final_data': final_data_list_of_dict,
                                                                                    'picture_name': picture_name})

                    else:
                        return render(request, "datainput/visual_rec_result.html", {'no_dir': 1})

                else:
                    return render(request, "datainput/visual_rec_result.html", {'wrong_extension': 1})
            else:
                return render(request, "datainput/visual_rec_result.html", {'no_pic_chosen': 1})
        else:
            if isinstance(classifiers_dict, list):
                return render(request, "datainput/visual_rec_choose_classifier.html", {'classifiers_dict': classifiers_dict,
                                                                                       'api_error': 0,
                                                                                       'unknown_error': 0})

            else:
                return render(request, "datainput/visual_rec_choose_classifier.html", {'classifiers_dict': classifiers_dict,
                                                                                       'api_error': 1,
                                                                                       'unknown_error': 0})

    except:
        return render(request, "datainput/visual_rec_choose_classifier.html", {'classifiers_dict': None,
                                                                               'api_error': 0,
                                                                               'unknown_error': 1})


@login_required(login_url='/login',
                redirect_field_name="")
def visual_rec_teach(request):

    pic_name = None
    isvalid = None

    #try:

    # downloads the image
    if request.method == 'POST':
        uploaded_picture = request.FILES.get('document')
        specified_class = request.POST['class']

        # resizes the image
        img = Image.open(uploaded_picture)
        img.thumbnail(image_size, Image.ANTIALIAS)
        pic_name = uploaded_picture.name

        # saves the image in a corresponding folder (class-wise)
        img.save(f'pictures/new_training_set/{specified_class}/{pic_name}')
        isvalid = pic_name.endswith('.jpg') or pic_name.endswith('.png') or picture_name.endswith('.jpeg')

    #except:
        #pass

    return render(request, "datainput/visual_rec_teach.html", {'pic_name': pic_name,
                                                               'isokay': isvalid,
                                                               }
                  )


@user_passes_test(lambda user: user.is_superuser,
                  login_url="/visual_rec_menu/")
def visual_rec_create_classifier(request):

    list_of_numbers_for_classes = []
    error = 0
    binary_classifier = None

    if request.method == 'POST':

        data = request.POST['number_of_classes']

        # check if it's a binary classifier
        if data.startswith('Klasyfikator'):
            number_of_classes = 1
            binary_classifier = 1
            print("kurwa mac ja pierdole")
        else:
            number_of_classes = int(data)

        for i in range(number_of_classes):
            list_of_numbers_for_classes.append(i + 1)

        return render(request, "datainput/visual_rec_create_classifier_setup2.html", {'error': error,
                                                                                      'list_of_classes': list_of_numbers_for_classes,
                                                                                      'binary': binary_classifier})
    else:
        return render(request, "datainput/visual_rec_create_classifier_setup.html")


@user_passes_test(lambda user: user.is_superuser,
                  login_url="/visual_rec_menu/")
def visual_rec_create_classifier2(request):

    unknown_error = 0
    classifier_name_taken = 0
    files_not_zip = False
    negative_class = None
    class_names = []
    short_descriptons = []
    long_descriptions = []
    more_info_links = []
    training_sets = []
    training_data_dict = {}

    try:
        if request.method == 'POST':

            classifier_name = request.POST.get('classifier_name', 'bez_nazwy').replace(' ', '_')

            for i in range(1, 10):
                class_names.append(request.POST.get(f'class_name_{i}'))
                short_descriptons.append(request.POST.get(f'short_description_{i}'))
                long_descriptions.append(request.POST.get(f'long_description_{i}'))
                more_info_links.append(request.POST.get(f'more_info_link_{i}'))
                training_sets.append(request.FILES.get(f'training_set_{i}'))
                negative_class = request.FILES.get('negative_class')

            # filter out the Nones gotten by POST.get
            class_names_final = list(filter(lambda item: item is not None, class_names))
            short_descriptons_final = list(filter(lambda item: item is not None, short_descriptons))
            long_descriptons_final = list(filter(lambda item: item is not None, long_descriptions))
            more_info_links_final = list(filter(lambda item: item is not None, more_info_links))
            training_sets_final = list(filter(lambda item: item is not None, training_sets))

            # check if files are .zip files
            files_not_zip = any([1 for file in training_sets_final if not file.name.endswith(".zip")])

            # create a folder for each class
            if files_not_zip is False:
                if not os.path.isdir(f"../wip/classifiers/{classifier_name}"):
                    os.mkdir(f"../wip/classifiers/{classifier_name}")

                    os.chdir(f"../wip/classifiers")

                    fs = FileSystemStorage(location=os.path.join(os.getcwd(), classifier_name))

                    # save each class model to a separate .txt file in class's folder
                    for i, class_id in enumerate(class_names_final):
                        file = open(os.path.join(classifier_name, f"{class_id}.txt"), "w")
                        file.write(f"class_name->{class_names_final[i]}\nshort_description->{short_descriptons_final[i]}\n"
                                   f"long_description->{long_descriptons_final[i]}\n"
                                   f"more_info_link->{more_info_links_final[i]}")
                        file.close()
                        fs.save(f"{class_names_final[i]}.zip", training_sets_final[i])

                    # creates a dictionary of training data
                    for i, class_name in enumerate(class_names_final):
                        training_data_dict[f"{class_name}_positive_examples"] = training_sets_final[i]

                    response = create_classifier(training_data_dict=training_data_dict,
                                                 classifier_name=classifier_name,
                                                 negative_class=negative_class)

                    # create a storage for new data for each class in classifier's folder
                    os.chdir(f"../pictures/new_training_set")
                    if not os.path.isdir(os.path.join(os.getcwd(), classifier_name)):
                        os.mkdir(os.path.join(os.getcwd(), classifier_name))
                        for class_name in class_names_final:
                            os.mkdir(os.path.join(os.getcwd(), classifier_name, class_name))

                    else:
                        classifier_name_taken = 1
                        return render(request, "datainput/classificator_creation_result.html",
                                      {'unknown_error': unknown_error,
                                       'classifier_name_taken': classifier_name_taken,
                                       'files_not_zip': files_not_zip,
                                       'api_error': 0,
                                       'response': None
                                       })

                    # if response is a string, there was an ApiException- otherwise creation was successful
                    if isinstance(response, dict):
                        return render(request, "datainput/classificator_creation_result.html", {'response': response,
                                                                                                'api_error': 0,
                                                                                                'unknown_error': 0,
                                                                                                'files_not_zip': 0,
                                                                                                'classifier_name_taken': 0})
                    else:
                        return render(request, "datainput/classificator_creation_result.html", {'response': response,
                                                                                                'api_error': 1,
                                                                                                'unknown_error': 0,
                                                                                                'files_not_zip': 0,
                                                                                                'classifier_name_taken': 0})
                else:
                    classifier_name_taken = 1
    except:
        unknown_error = 1

    return render(request, "datainput/classificator_creation_result.html", {'unknown_error': unknown_error,
                                                                            'classifier_name_taken': classifier_name_taken,
                                                                            'files_not_zip': files_not_zip,
                                                                            'api_error': 0,
                                                                            'response': None
                                                                            })


@login_required(login_url='/login',
                redirect_field_name="")
def add_data_form_submission(request):

    motor_rotations = request.POST["Motor rotations"]
    temperature1 = request.POST["Temperature1"]
    temperature2 = request.POST["Temperature2"]
    comment = request.POST["Comment"]
    current = request.POST["Current"]
    measurement_time = str(datetime.now())[:-7]
    user_name = request.user.get_full_name()

    validation_error = 0

    if not validation_error:
        measurements = Measurements(
            date_of_measurement=measurement_time,
            motor_rotations=motor_rotations,
            temperature_1=temperature1,
            temperature_2=temperature2,
            current_draw=current,
            comment=comment,
            user_name=user_name
        )

        measurements.save()
        return render(request, "datainput/thank_you.html",
                    {'validation_error': validation_error
                     }
                    )
