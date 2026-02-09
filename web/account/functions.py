# """
# This module contains functions that will be used in models.py and views.py in
# order to abstract code away so that those files are more readable.
# """

# # Import python built-in libraries
# import hashlib
# from random import randint
# from datetime import timedelta
# # Import built-in django libraries
# from django.core.mail import send_mail
# from django.conf import settings
# from django.utils import timezone
# from django.contrib.auth import get_user_model


# def hash_otp(otp_int: int):
#     """
#     Create a hex version of the otp.
#     """
#     hash_obj = hashlib.sha256()
#     otp_bytes = otp_int.to_bytes(length=3, byteorder='big')
#     hash_obj.update(otp_bytes)
#     return hash_obj.hexdigest()


# def generate_otp():
#     """
#     Creates a random hashed otp value and returns both the plain text and hashed
#     values as a tuple.
#     """
#     # Create the hash object
#     hash_obj = hashlib.sha256()
#     otp_int = randint(100000, 999999)
#     # Convert the hash to a bytes object
#     otp_bytes = otp_int.to_bytes(length=3, byteorder='big')
#     # Hash the bytes object
#     hash_obj.update(otp_bytes)
#     # Convert the object to hex to be used in the database
#     otp_hex = hash_obj.hexdigest()
#     # Return the int value for the email and the hex string for the database. 
#     return (otp_int, hash_otp(otp_int))


# def send_otp(user_object):
#     """
#     Takes in the currently logged in user's email address, creates an otp,
#     adds it to the database, and then sends the user an email with the code.
#     """
#     # Import in function to prevent circular import
#     from .models import UserProfile
#     # Generate the otp and expiration
#     otp_int, otp_hex = generate_otp()
#     otp_expiration = timezone.now() + timedelta(minutes=5)
#     # Save the otp data to the database
#     UserProfile.objects.filter(user=user_object).update(
#         otp=otp_hex,
#         otp_expiration=otp_expiration
#     )
#     # Send the email
#     send_otp_email(otp_int, otp_expiration, user_object.email)


# def send_otp_email(otp_int, otp_expiration, email):
#     """
#     Takes the otp_int and otp_expiration and sends an email to the user's
#     email address.
#     """
#     body = (
#         'OTP from Trip Manager,\n\n'
#         'Your OTP for Trip Manager is:\n\n'
#         f'{otp_int}\n\n'
#         f'This code expires at {otp_expiration}.\n\n'
#         'Trip Manager Admin'
#     )
#     send_mail(
#         'OTP for Trip Manager', 
#         body,
#         settings.DEFAULT_FROM_EMAIL, 
#         [email]
#     )


# def incorrect_login(username, ip_1, ip_2):
#     """
#     Updates the user's record with the number of incorrect logins within
#     a five minute time frame and returns a message with the number of
#     attempts remaining.
#     """
#     # Import the model here to prevent circular import
#     from .models import UserProfile, LockedIP
#     # Define necessary variables
#     locked_out = False
#     message = 'Username and/or Password is incorrect, please try again.'
#     # Check if username exists:
#     User = get_user_model()
#     users = User.objects.all()
#     usernames = [user.username for user in users]
#     # If username exists update UserProfile with login attempts
#     if username in usernames:
#         user_object = User.objects.get(username=username)
#         user = UserProfile.objects.get(user=user_object)
#         # Check if the user is already locked out
#         if user.locked_out:
#             if timezone.now() < user.locked_out_expiration:
#                 locked_out = True
#                 message = 'Too mainy failed login attempts. Please try again after 5 minutes'
#             else:
#                 user.locked_out = False
#         else:
#             user.login_attempts += 1
#             if user.login_attempts >= 3:
#                 locked_out, user.locked_out = True, True
#                 user.login_attempts = 0
#                 user.locked_out_expiration = timezone.now() + timedelta(minutes=5)
#                 message = 'Too mainy failed login attempts. Please try again after 5 minutes' 
#             else:
#                 message = f'Incorrect username/password. You have {3 - user.login_attempts} attempts remaining.'
#         user.save()
#     # If username doesn't exist update LockedIP with login attempts
#     else:
#         ip = ip_1 if ip_1 else ip_2
#         ips = list(LockedIP.objects.values_list('ip', flat=True))
#         if ip in ips:
#             ip_obj = LockedIP.objects.get(ip=ip)
#             ip_obj.login_attempts += 1
#             if ip_obj.login_attempts >= 3:
#                 locked_out, ip_obj.locked_out = True, True
#                 ip_obj.login_attempts = 0
#                 ip_obj.locked_out_expiration = timezone.now() + timedelta(minutes=5)
#                 message = 'Too mainy failed login attempts. Please try again after 5 minutes'  
#             else:
#                 message = f'Incorrect username/password. You have {3 - ip_obj.login_attempts} attempts remaining.'
#             ip_obj.save()
#         else:
#             LockedIP.objects.create(ip=ip)
#     return (locked_out, message)


# def ip_locked(ip_1, ip_2):
#     """
#     Checks the ip address against locked out ips in the database.
#     """
#     from .models import LockedIP
#     ips = list(LockedIP.objects.values_list('ip', flat=True))
#     ip = ip_1 if ip_1 else ip_2
#     if ip in ips:
#         ip_obj = LockedIP.objects.get(ip=ip)
#         if ip_obj.locked_out:
#             if timezone.now() > ip_obj.locked_out_expiration:
#                 ip_obj.delete()
#             else:
#                 return True
#     else:
#         return False


# def check_ip_address(meta_object):
#     """
#     Checks request.META to see if the ip address has been locked out.
#     """
#     from .models import IPAddress
#     ip_1 = meta_object.get('HTTP_X_FORWARDED_FOR')
#     ip_2 = meta_object.get('REMOTE_ADDR')
#     ips = list(IPAddress.objects.values_list('ip', flat=True))
#     ip = ip_1 if ip_1 else ip_2
#     if ip in ips:
#         ip_obj = IPAddress.objects.get(ip=ip)
#         if ip_obj.locked_out:
#             if timezone.now() > ip_obj.locked_out_expiration:
#                 ip_obj.delete()
#             else:
#                 return True
#     else:
#         return False