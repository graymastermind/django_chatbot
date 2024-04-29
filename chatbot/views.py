import random
import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from .models import User, Notification, Assignment, AssignmentResult, ExamDate, Question, Institution, ExaminationDate
from django.core.files.storage import default_storage


@csrf_exempt
def reply_to_sms(request):
    if request.method == 'POST':
        incoming_message = request.POST.get("Body", "").strip()
        sender_phone_number = request.POST.get("From", "")

        twilio_response = MessagingResponse()
        last_input = request.session.get('last_input', '')

        if incoming_message.lower() == 'hi' and (last_input == '' or last_input == 'hi'):
            request.session['last_input'] = 'hi'
            try:
                user = User.objects.get(phone_number=sender_phone_number)
                if user.is_admin:
                    twilio_response.message("Welcome! Ruwa Vocational Training Centre:\n0. Register\n1. Ask a question\n2. View Notifications\n3. Update Profile\n4. Submit Assignment\n5. Assignment Results\n6. Financial Account\n7. Examination Dates\n(research). Use command research to ask any question\n8. Exit\n9. View Users\n10. View Questions\n11. Create Notications (Announcement)\n12. Add Examination Date")
                else:
                    twilio_response.message("Welcome! Ruwa Vocational Training Centre:\n0. Register\n1. Ask a question\n2. View Notifications\n3. Update Profile\n4. Submit Assignment\n5. Assignment Results\n6. Financial Account\n7. Examination Dates\n8. Exit")
            except User.DoesNotExist:
                twilio_response.message("Welcome! Ruwa Vocational Training Centre:\n0. Register\n1. Ask a question\n2. View Notifications\n3. Update Profile\n4. Submit Assignment\n5. Assignment Results\n6. Financial Account\n7. Examination Dates\n(research). Use command research to ask any question\n8. Exit")
        elif incoming_message.lower() == "reset":
            reset_last_input(request)
            twilio_response.message("Command reset successful. lastInput is now empty.")
        elif (last_input == '' or last_input == 'hi') and incoming_message == '0':
            request.session['last_input'] = '0'
            twilio_response.message("You chose option 0 - Register")
            twilio_response.message("Please enter your username:")
        elif last_input == '0':
            existing_user = User.objects.filter(phone_number=sender_phone_number).first()
            if existing_user:
                twilio_response.message("Phone number already registered! Please log in instead.")
            else:
                username = incoming_message
                user_id = generate_user_id()
                user = User(username=username, phone_number=sender_phone_number, user_id=user_id)
                user.save()
                twilio_response.message("Registration successful! Your user ID is: {}".format(user_id))
            reset_last_input(request)
            twilio_response.message("Welcome! Ruwa Vocational Training Centre:\n0. Register\n1. Ask a question\n2. View Notifications\n3. Update Profile\n4. Submit Assignment\n5. Assignment Results\n6. Financial Account\n7. Examination Dates\n8. Exit")
        elif incoming_message == '9':
            try:
                user = User.objects.get(phone_number=sender_phone_number)
                if user.is_admin:
                    # Handle option 9 - View Users
                    users = User.objects.all()
                    user_list = "\n".join(
                        [f"ID: {user.id}, Username: {user.username}, Phone Number: {user.phone_number}" for user in
                         users])
                    twilio_response.message(f"Users:\n{user_list}")
                else:
                    twilio_response.message("Access denied. You must be an admin to access this option.")
            except User.DoesNotExist:
                twilio_response.message("User does not exist.")
            reset_last_input(request)
        elif (last_input == '' or last_input == 'hi') and incoming_message == '1':
            request.session['last_input'] = '1'
            twilio_response.message("You chose option 1 - Ask a question")
            twilio_response.message("Please enter your question:")
        elif last_input == '1':
            question_content = incoming_message
            question = Question(phone_number=sender_phone_number, content=question_content)
            question.save()
            twilio_response.message("Question submitted successfully!")
            reset_last_input(request)
        elif incoming_message == '10':
            try:
                user = User.objects.get(phone_number=sender_phone_number)
                if user.is_admin:
                    questions = Question.objects.all()
                    question_list = "\n".join(
                        [f"ID: {question.id}, Phone Number: {question.phone_number}, Content: {question.content}" for
                         question in questions])
                    twilio_response.message(f"All Questions:\n{question_list}")
                    reset_last_input(request)
                else:
                    twilio_response.message("Access denied. You must be an admin to access this option.")
            except User.DoesNotExist:
                twilio_response.message("User does not exist.")
            reset_last_input(request)
        elif (last_input == '' or last_input == 'hi') and incoming_message == '2':
            request.session['last_input'] = '2'
            twilio_response.message("You chose option 2 - View Notifications")
            notifications = Notification.objects.all()
            if notifications:
                message = "Notifications:\n"
                for notification in notifications:
                    message += f"{notification.id}. {notification.content}\n"
            else:
                message = "No notifications found."
            reset_last_input(request)
            twilio_response.message(message)
        elif (last_input == '' or last_input == 'hi') and incoming_message == '11':
            try:
                user = User.objects.get(phone_number=sender_phone_number)
                if user.is_admin:
                    request.session['last_input'] = '11'
                    twilio_response.message("You chose option 11 - Create Notification")
                    twilio_response.message("Please enter the notification content:")
                else:
                    twilio_response.message("Access denied. You must be an admin to access this option.")
                    reset_last_input(request)
            except User.DoesNotExist:
                twilio_response.message("User does not exist.")
                reset_last_input(request)
        elif last_input == '11':
            notification_content = incoming_message
            notification = Notification(content=notification_content)
            notification.save()
            twilio_response.message("Notification saved successfully.")
            reset_last_input(request)

        elif incoming_message == '3':
            # Handle option 3 - Update Profile
            request.session['last_input'] = '3'
            twilio_response.message("You chose option 3 - Update Profile")
            twilio_response.message("Please enter your updated profile username.")
            return HttpResponse(str(twilio_response))
        elif last_input == '3':
            # Call the update_user_profile method to update the user's profile
            return update_user_profile(request)
        elif incoming_message == '4':
            # Handle option 4 - Submit Assignment
            request.session['last_input'] = '4'
            twilio_response.message("You chose option 4 - Submit Assignment")
            twilio_response.message("Please upload your assignment file.")
            return HttpResponse(str(twilio_response))
        elif last_input == '4':
            # Call the submit_assignment method to handle assignment submission
            return submit_assignment(request)
        elif incoming_message == '5':
            # Handle option 5 - Assignment Results
            request.session['last_input'] = '5'
            twilio_response.message("You chose option 5 - Assignment Results")
            # Retrieve and display assignment results
            # This is a placeholder and needs to be implemented
            twilio_response.message("Assignment results:\n[Placeholder for results]")
            reset_last_input(request)
        elif incoming_message == '6':
            # Handle option 6 - Financial Account
            request.session['last_input'] = '6'
            twilio_response.message("You chose option 6 - Financial Account")
            # Retrieve and display financial account information
            # This is a placeholder and needs to be implemented
            twilio_response.message("Financial account information:\n[Placeholder for account info]")
            reset_last_input(request)
        elif incoming_message == '7':
            # Handle option 7 - Examination Dates
            request.session['last_input'] = '7'
            twilio_response.message("You chose option 7 - Examination Dates")
            # Retrieve and display examination dates
            return display_examination_dates(request)

        elif incoming_message == '12':
            # Handle option 12 - Create Examination Date
            request.session['last_input'] = '12'
            twilio_response.message("You chose option 12 - Create Examination Date")
            twilio_response.message("Please enter the description for the examination date.")
            return HttpResponse(str(twilio_response))

        elif last_input == '12':
            # Call the create_examination_date method to create a new examination date
            return create_examination_date(request)
        elif incoming_message.lower() == "research":
            request.session['last_input'] = 'research'
            twilio_response.message("You chose the research option. Please enter your question:")

        elif last_input == 'research':
            question_content = incoming_message

            # Query the Institution model to check for relevant information
            matching_institutions = Institution.objects.filter(
                description__icontains=question_content
            )

            if matching_institutions:
                feedback = "Here is some information related to your query:\n"
                for institution in matching_institutions:
                    # feedback += f"Institution: {institution.name}\nLocation: {institution.location}\nDescription: {institution.description}\nContact Email: {institution.contact_email}\nContact Phone: {institution.contact_phone}\n\n"
                    feedback += f"\n {institution.description}"
                twilio_response.message(feedback)
            else:
                twilio_response.message("Sorry, no relevant institution information found.")

            reset_last_input(request)
        elif incoming_message == '8':
            # Handle option 8 - Exit
            reset_last_input(request)
            twilio_response.message("Goodbye! Thank you for using Ruwa Vocational Training Centre.")
        else:
            # Handle unrecognized or invalid input
            twilio_response.message("Unrecognized command. Please enter a valid option or 'reset' to start over.")

        return HttpResponse(str(twilio_response))

def reset_last_input(request):
    request.session['last_input'] = ''

def generate_user_id():
    # Generate a user ID prefixed with the current year and a random 3-digit number
    current_year = str(datetime.datetime.now().year)
    random_number = str(random.randint(100, 999))
    random_letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    user_id = current_year + random_number + random_letter
    return user_id


def view_notifications(request):
    # Implement view notifications logic here
    notifications = Notification.objects.all()
    return render(request, 'notifications.html', {'notifications': notifications})


def update_user_profile(request):
    if request.method == 'POST':
        incoming_message = request.POST.get("Body", "").strip()
        sender_phone_number = request.POST.get("From", "")
        
        try:
            user = User.objects.get(phone_number=sender_phone_number)
            user.username = incoming_message            
            # Save the updated user
            user.save()
            
            twilio_response = MessagingResponse()
            twilio_response.message("Profile updated successfully!")
            
            return HttpResponse(str(twilio_response))
        except User.DoesNotExist:
            twilio_response = MessagingResponse()
            twilio_response.message("User does not exist.")
            
            return HttpResponse(str(twilio_response))


def submit_assignment(request):
    if request.method == 'POST':
        incoming_message = request.POST.get("Body", "").strip()
        sender_phone_number = request.POST.get("From", "")
        uploaded_file = request.FILES.get("MediaUrl", None)
        
        try:
            user = User.objects.get(phone_number=sender_phone_number)
            # Save the uploaded file
            if uploaded_file:
                # Generate a unique filename using user's phone number and current timestamp
                filename = f"{sender_phone_number}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
                # Save the file to the desired location
                file_path = f"assignments/{filename}"
                with default_storage.open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                
                # Create an assignment record in the database
                assignment = Assignment(user=user, file_path=file_path)
                assignment.save()
                
                twilio_response = MessagingResponse()
                twilio_response.message("Assignment submitted successfully!")
                reset_last_input(request)
                return HttpResponse(str(twilio_response))
            else:
                twilio_response = MessagingResponse()
                twilio_response.message("No file uploaded. Please try again with a file attachment.")
                reset_last_input(request)
                return HttpResponse(str(twilio_response))
        except User.DoesNotExist:
            twilio_response = MessagingResponse()
            twilio_response.message("User does not exist.")
            reset_last_input(request)
            return HttpResponse(str(twilio_response))


def display_examination_dates(request):
    # Retrieve and display examination dates
    # You can fetch the examination dates from your database or any other data source

    exam_dates = ExaminationDate.objects.all()  # Assuming you have an ExaminationDate model

    if exam_dates:
        message = "Examination dates:\n"
        for exam_date in exam_dates:
            message += f"{exam_date.date}: {exam_date.description}\n"
    else:
        message = "No examination dates available."

    twilio_response = MessagingResponse()
    twilio_response.message(message)

    return HttpResponse(str(twilio_response))


def create_examination_date(request):
    if request.method == 'POST':
        incoming_message = request.POST.get("Body", "").strip()
        sender_phone_number = request.POST.get("From", "")

        try:
            user = User.objects.get(phone_number=sender_phone_number)
            # Create a new examination date record
            exam_date = ExaminationDate(date=datetime.datetime.now(), description=incoming_message)
            exam_date.save()

            twilio_response = MessagingResponse()
            twilio_response.message("Examination date created successfully!")
            reset_last_input(request)
            return HttpResponse(str(twilio_response))
        except User.DoesNotExist:
            twilio_response = MessagingResponse()
            twilio_response.message("User does not exist.")
            reset_last_input(request)
            return HttpResponse(str(twilio_response))

