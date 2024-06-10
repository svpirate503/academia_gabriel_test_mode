from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.http import HttpResponse
import stripe
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from .models import StripeCustomer
import logging
from .models import *
from functools import wraps
from .serializers import CapituloSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY




"""
def course_detail(request,curso_id):
    curso = Curso.objects.get(pk=curso_id)
   # texto = LoqueAprenderas.objects.filter(curso=curso)
    already_purchased = False
    if request.user.compra_set.filter(curso_comprado=curso_id).exists():
        already_purchased =True

    texto = curso.loqueaprenderas_set.all()
    return render(request,'lessons/course_detail.html',{'curso':curso,'textos':texto,'purchased':already_purchased})


"""


class CapituloView(APIView):
    def get(self, request):
        capitulos = Capitulo.objects.all()
        serializer = CapituloSerializer(capitulos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CapituloSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CapituloRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Capitulo.objects.all()
    serializer_class = CapituloSerializer
    lookup_field = 'id'
    



def user_dashboard(request): #Place where the user will interact once he get suscribed
    return render(request,'user-dashboard.html')


def custom_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Si el usuario no está autenticado, redirigir a la página de inicio de sesión
            return redirect(reverse('sigin') + '?next=' + request.path)
        # Si está autenticado, seguir con la vista original
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view



def suscripcion_activa(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('sigin') + '?next=' + request.path)
          # Redirige al login si el usuario no está autenticado

        # Comprueba si el usuario tiene un customer_id almacenado
                 
        
        
        
            # Revisa las suscripciones activas en Stripe
        try:
            stripe_customer = StripeCustomer.objects.get(user=request.user)
        except StripeCustomer.DoesNotExist:
            return redirect('/plans/')
       
            
        customer_id = stripe_customer.stripeCustomerId 
        if not customer_id:
            return redirect('/plans/')
        try:
            # Revisa las suscripciones activas en Stripe
            subscriptions = stripe.Subscription.list(customer=customer_id, status='active')
            if subscriptions.data:
                # Si hay suscripciones activas, permitir acceso
                return view_func(request, *args, **kwargs)
            else:
                # No hay suscripciones activas, redirigir a los planes de pago
                return redirect('/home/')
        except stripe.error.StripeError as e:
            # Manejar errores de Stripe aquí
            return HttpResponse("Error al verificar la suscripción en Stripe.", status=500)

    return _wrapped_view

               

def cancelar_membresia(request):
    if not request.user.is_authenticated:
        logger.error("Intento de acceso sin autenticación")
        return HttpResponse('Usuario no autenticado.', status=401)

    try:
        # Obtener el objeto StripeCustomer asociado al usuario
        stripe_customer = StripeCustomer.objects.get(user=request.user)
    except StripeCustomer.DoesNotExist:
        logger.error("Cliente Stripe no encontrado para el usuario: %s", request.user.username)
        return HttpResponse('No se encontró la información del cliente Stripe.', status=404)

    try:
        # Cancelar la suscripción en Stripe de manera que termine al final del período de facturación
        stripe_subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)
        stripe.Subscription.modify(
            stripe_subscription.id,
            cancel_at_period_end=True
        )
        stripe_customer.status = 'canceling'
        stripe_customer.save()
        send_cancellation_email('lonan2444@gmail.com')
       

        logger.info("Membresía cancelada para el usuario: %s", request.user.username)
        return HttpResponse('La membresía ha sido cancelada correctamente y seguirá activa hasta el final del período de facturación.', status=200)
    except stripe.error.StripeError as e:
        logger.error("Error de Stripe al cancelar la membresía para el usuario: %s, error: %s", request.user.username, str(e))
        return HttpResponse(f'Error al cancelar la membresía: {str(e)}', status=500)
    except Exception as e:
        logger.error("Error inesperado al cancelar la membresía: %s", str(e))
        return HttpResponse(f'Error inesperado: {str(e)}', status=500)


def send_cancellation_email(email):
    send_mail(
        'Confirmación de Cancelación de Suscripción',
        'Hola, hemos procesado la cancelación de tu suscripción. Esta seguirá activa hasta el final del período de facturación actual. ¡Gracias por tu tiempo con nosotros!',
        'onanflex@gmail.com',
        [email],
        fail_silently=False,
    )

@csrf_exempt
def stripe_cancel_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = 'tu_endpoint_secret_stripe'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Payload inválido
        return JsonResponse({'status': 'invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Firma inválida
        return JsonResponse({'status': 'invalid signature'}, status=400)

    # Manejar el evento
    if event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        handle_subscription_deletion(subscription)

    return JsonResponse({'status': 'success'}, status=200)

def handle_subscription_deletion(subscription):
    # Aquí podrías buscar el StripeCustomer en tu DB y actualizar su estado
    stripe_customer = StripeCustomer.objects.get(stripeSubscriptionId=subscription['id'])
    stripe_customer.status = 'canceled'
    stripe_customer.save()






def success(request):
    return render(request,'success.html')

def home(request):
    return render(request,'suscripcion.html')



def testimonios(request):
    return render(request,'testimonios.html')





@custom_login_required
@csrf_exempt
def create_checkout_session(request):
    domain_url = 'https://1570-2607-fb91-14da-9125-f4b3-cbe4-f100-2b6b.ngrok-free.app/'
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='subscription',
                
                line_items=[
                    {
                        'price':"price_1P9U6jDAqBiVLFaus1BhC7J5",
                        'quantity': 1,
                    }
                ]
            )
        return redirect(checkout_session.url)
    except Exception as e:
        return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        # Manejar el pago exitoso
        session = event['data']['object']
        customer_email = get_customer_email(session["customer"])
    
    
       
        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')

        # Get the user and create a new StripeCustomer
        try:
            user = User.objects.get(pk=client_reference_id)
        # Continuar con la creación del StripeCustomer
        except User.DoesNotExist:
            return HttpResponse('User not found.', status=404)
        StripeCustomer.objects.create(
            user=user,
            stripeCustomerId=stripe_customer_id,
            stripeSubscriptionId=stripe_subscription_id,
            status="active",
        ).save()


    elif event['type'] == 'customer.subscription.deleted':
        # Manejar la cancelación de suscripción
        pass

    return HttpResponse(status=200)

        # Fetch all the required data from session
     
def get_customer_email(customer_id):
   
    try:
        # Recupera el objeto cliente de Stripe usando el customer_id
        customer = stripe.Customer.retrieve(customer_id)
        # Retorna el correo electrónico del cliente
        return customer.email
    except stripe.error.StripeError as e:
        # Maneja errores de la API de Stripe (e.g., cliente no encontrado, problemas de red)
        print(f"Error al recuperar el cliente de Stripe: {str(e)}")
        return None

def index(request):
   
    return render(request,'index.html')
    


def videoplaylist(request):
    return render(request,'videolist/Videoplaylist.html')
    





def plans(request):
    return render(request,'plans.html')


def category_detail(request,post_id):
    categoria = get_object_or_404(Categoria,pk=post_id)
    post = Post.objects.filter(categoria=categoria)
    
    return render(request,'cat_detail.html',{'posts':post})





def contact(request):
  

    return render(request,'contact.html')


def log_out(request):
    logout(request)
   
   
    return redirect('/')
@csrf_exempt
def log_in(request):
    if request.user.is_authenticated:
        # Si el usuario ya está autenticado, redirigirlo a la página principal
        return redirect('/')
    error = ""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email,password=password)
        if user is not None:
            login(request,user)
            next_url = request.GET.get('next', '/')


            return redirect(next_url)
        else:
            error = "Email or Password incorrect."



    return render(request,"login.html",{'error':error})
@csrf_exempt
def register(request):
    if request.user.is_authenticated:
        # Si el usuario ya está autenticado, redirigirlo a la página principal
        return redirect('/')
    

    error = ""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        
        if password != password2:
            error = "Las contraseñas no coinciden."
        elif User.objects.filter(username=email).exists():
            error = "Este usuario ya existe."
        else:
            try:
                user = User.objects.create_user(username=email, password=password)
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("/")
                else:
                    error = "Error al autenticar al usuario."
            except IntegrityError:
                error = "Error al crear el usuario. Inténtalo de nuevo."

    return render(request, "register.html", {'error': error})