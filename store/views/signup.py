from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models import Customer
from django.views import View


from .tokens import account_activation_token
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib import messages
import smtplib
import ssl
from email.message import EmailMessage




class Signup (View):
	def get(self, request):
		return render(request, 'signup.html')

	def post(self, request):
		postData = request.POST
		first_name = postData.get('firstname')
		last_name = postData.get('lastname')
		phone = postData.get('phone')
		email = postData.get('email')
		password = postData.get('password')
		# validation
		value = {
			'first_name': first_name,
			'last_name': last_name,
			'phone': phone,
			'email': email
		}
		error_message = None

		customer = Customer(first_name=first_name,
							last_name=last_name,
							phone=phone,
							email=email,
							password=password)
		error_message = self.validateCustomer(customer)

		if not error_message:
			print(first_name, last_name, phone, email, password)
			customer.password = make_password(customer.password)
			self.sendEmail(request=request, customer=customer)
			customer.register()
			
			print('email sent successfully, please check your eamil box')
			return redirect('homepage')
		else:
			data = {
				'error': error_message,
				'values': value
			}
			return render(request, 'signup.html', data)

	def validateCustomer(self, customer):
		error_message = None
		if (not customer.first_name):
			error_message = "Please Enter your First Name !!"
		elif len(customer.first_name) < 3:
			error_message = 'First Name must be 3 char long or more'
		elif not customer.last_name:
			error_message = 'Please Enter your Last Name'
		elif len(customer.last_name) < 3:
			error_message = 'Last Name must be 3 char long or more'
		elif not customer.phone:
			error_message = 'Enter your Phone Number'
		elif len(customer.phone) < 10:
			error_message = 'Phone Number must be 10 char Long'
		elif len(customer.password) < 5:
			error_message = 'Password must be 5 char long'
		elif len(customer.email) < 5:
			error_message = 'Email must be 5 char long'
		elif customer.isExists():
			error_message = 'Email Address Already Registered..'
		# saving

		return error_message
	



	def sendEmail(self, request, customer):
			email_sender = 'jafars4ab@gmail.com'
			email_password = 'txahcupztwcyjkii'
			email_receiver = customer.email

			# Set the subject and body of the email
			
			current_site = get_current_site(request)
			message = render_to_string('acc_active_email.html', {
				'user': customer,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(customer.email)),
				'token': account_activation_token.make_token(customer),
			})
			subject = 'Verify Your Email!'
			# body = """
			# I've just published a new video on YouTube: https://youtu.be/2cZzP9DLlkg
			# """

			em = EmailMessage()
			em['From'] = email_sender
			em['To'] = email_receiver
			em['Subject'] = subject
			em.set_content(message)

			# Add SSL (layer of security)
			context = ssl.create_default_context()

			# Log in and send the email
			with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
				smtp.login(email_sender, email_password)
				smtp.sendmail(email_sender, email_receiver, em.as_string())
