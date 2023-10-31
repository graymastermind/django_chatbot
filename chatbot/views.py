import random
import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from .models import User, Notification, Assignment, AssignmentResult, ExamDate

@csrf_exempt
def reply_to_sms(request):
    print('init now')
    if request.method == 'POST':
        print('init again')
        incoming_message = request.POST.get("Body", "").strip()
        sender_phone_number = request.POST.get("From", "")

        twilio_response = MessagingResponse()
        last_input = request.session.get('last_input', '')

        print(request)
        if incoming_message.lower() == 'hi' and (last_input == '' or last_input == 'hi'):
            print(incoming_message)
            request.session['last_input'] = 'hi'
            print(
                "Welcome! Ruwa Vocational Training Centre:\n0. Register\n1. Ask a question\n2. View Notifications\n3. Update "
                "Profile\n4. Submit Assignment\n5. Assignment Results\n6. Financial Account\n7. Examination Dates\n(research). Use command research to ask any question\n8. Exit")
            twilio_response.message(
                "Welcome! Ruwa Vocational Training Centre:\n0. Register\n1. Ask a question\n2. View Notifications\n3. Update "
                "Profile\n4. Submit Assignment\n5. Assignment Results\n6. Financial Account\n7. Examination Dates\n(research). Use command research to ask any question\n8. Exit")
        elif incoming_message.lower() == "reset":
            # Handle "reset" command to reset last_input to an empty string
            reset_last_input(request)
            twilio_response.message("Command reset successful. lastInput is now empty.")
        elif (last_input == '' or last_input == 'hi') and incoming_message == '0':
            request.session['last_input'] = '0'
            twilio_response.message("You chose option 0 - Register")
            twilio_response.message("Please enter your username:")
        elif last_input == '0':
            # Save the username and phone number to the database
            username = incoming_message
            user_id = generate_user_id()
            user = User(username=username, phone_number=sender_phone_number, user_id=user_id)
            user.save()
            twilio_response.message("Registration successful! Your user ID is: {}".format(user_id))
            reset_last_input(request)
            twilio_response.message(
                "Welcome! Ruwa Vocational Training Centre:\n0. Register\n1. Ask a question\n2. View Notifications\n3. Update "
                "Profile\n4. Submit Assignment\n5. Assignment Results\n6. Financial Account\n7. Examination Dates\n8. Exit")
        elif incoming_message == '9':
            # Handle "View Users" option
            users = User.objects.all()
            user_list = "\n".join([f"ID: {user.id}, Username: {user.username}, Phone Number: {user.phone_number}" for user in users])
            twilio_response.message(f"Users:\n{user_list}")
            reset_last_input(request)
        elif (last_input == '' or last_input == 'hi') and incoming_message == '1':
            request.session['last_input'] = '1'
            twilio_response.message("You chose option 1 - Ask a question")
            twilio_response.message("Please enter your question:")
        elif last_input == '1':
            # Save the question to the database
            question_content = incoming_message
            question = Question(phone_number=sender_phone_number, content=question_content)
            question.save()
            twilio_response.message("Question submitted successfully!")
            reset_last_input(request)
        elif incoming_message == '10':
            # Handle "View All Questions" option
            questions = Question.objects.all()
            question_list = "\n".join(
                [f"ID: {question.id}, Phone Number: {question.phone_number}, Content: {question.content}" for question in questions])
            twilio_response.message(f"All Questions:\n{question_list}")
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
            request.session['last_input'] = '11'
            twilio_response.message("You chose option 11 - Create Notification")
            twilio_response.message("Please enter the notification content:")
        elif last_input == '11':
            # Save the notification to the database
            notification_content = incoming_message
            notification = Notification(content=notification_content)
            notification.save()
            twilio_response.message("Notification saved successfully.")
            reset_last_input(request)
        # Implement other view logic here...
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
    # Render notifications to an HTML template or return them as JSON
    # Return a JSON response or render a template with the notifications
    return render(request, 'notifications.html', {'notifications': notifications})

# Define other views based on the Flask logic as needed.
