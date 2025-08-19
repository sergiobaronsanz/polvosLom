from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta
from django.core.mail import send_mail
from calidad.models import Equipos
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

class Command(BaseCommand):
    help = 'Enviar aviso de calibración próxima a vencer'

    def actualizacionEquipos(self, hoy):
        #Vemos los equipos que hay controlados
        equipos = Equipos.objects.filter(controlado=True)
        
        #Actualizamos el estado de la calibración de los equipos
        for equipo in equipos:
            if equipo.fechaCaducidadCalibracion <= hoy and equipo.estadoCalibracion == "0":
                equipo.estadoCalibracion = "1"
                equipo.save()

    def enviar_mail(self, mensaje_texto, equipos, destinatario):
        subject = "Aviso de calibración próxima a vencer"
        from_email = settings.EMAIL_HOST_USER
        to = [destinatario]

        # Texto plano (fallback por si el cliente de correo no soporta HTML)
        text_content = mensaje_texto  

        # HTML bonito (puedes usar inline CSS o un template renderizado)
        html_content = f"""
        <html>
        <head>
            <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
                padding: 20px;
            }}
            .container {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            }}
            h2 {{
                color: #2c3e50;
            }}
            ul {{
                padding-left: 20px;
            }}
            li {{
                margin-bottom: 8px;
            }}
            </style>
        </head>
        <body>
            <div class="container">
            <h2> Aviso de calibración próxima a vencer</h2>
            <p>Hola,</p>
            <p>La calibración de estos equipos está próxima a caducar:</p>
            <ul>
                {''.join(f"<li><b>{eq.equipo}</b> ({eq.codigo}) - Estado: {eq.get_estadoCalibracion_display()}- Vence: {eq.fechaCaducidadCalibracion}</li>" for eq in equipos)}
            </ul>
            <p style="margin-top:20px;">Gracias,<br>El Laboratorio de Inflamabilidad</p>
            </div>
        </body>
        </html>
        """

        # Crear email
        email = EmailMultiAlternatives(subject, text_content, from_email, to)
        email.attach_alternative(html_content, "text/html")
        email.send()
    
    def handle(self, *args, **kwargs):
        hoy = now().date()
        self.actualizacionEquipos(hoy)

        # Equipos con calibración externa: avisar 2 meses antes
        fecha_aviso_externa = hoy + timedelta(days=60)
        # Equipos con calibración interna: avisar 1 mes antes
        fecha_aviso_interna = hoy + timedelta(days=30)

        equipos_a_avisar = Equipos.objects.filter(
            (Q(controlado = True) & ~Q(estadoCalibracion = "6")) &
            (Q(tipoCalibracion='2') & Q(fechaCaducidadCalibracion__lte=fecha_aviso_externa) |
            Q(tipoCalibracion='1') & Q(fechaCaducidadCalibracion__lte=fecha_aviso_interna))
        )

        if equipos_a_avisar.exists():
            mensaje = "Equipos con calibración próxima a vencer:\n\n"
            for equipo in equipos_a_avisar:
                mensaje += f"- {equipo.equipo} ({equipo.codigo}), Estado: {equipo.get_estadoCalibracion_display()}, Vence: {equipo.fechaCaducidadCalibracion}\n"

            correoTecnicoCalibracion= User.objects.get(username = "sergio")

            self.enviar_mail(mensaje, equipos_a_avisar, correoTecnicoCalibracion.email)

            self.stdout.write(self.style.SUCCESS('Correo enviado con equipos a calibrar'))
        else:
            self.stdout.write('No hay equipos con calibración próxima a vencer.')
