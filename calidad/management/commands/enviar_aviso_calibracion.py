from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.models import User
from datetime import timedelta

from calidad.models import Equipos


class Command(BaseCommand):
    help = "Enviar aviso de calibración próxima a vencer"

    def handle(self, *args, **kwargs):
        hoy = now().date()

        # 1️⃣ Actualizar estados
        self.actualizacion_equipos(hoy)

        # 2️⃣ Calcular fechas aviso
        fecha_aviso_externa = hoy + timedelta(days=60)
        fecha_aviso_interna = hoy + timedelta(days=30)

        # 3️⃣ Filtrar equipos
        equipos_a_avisar = Equipos.objects.filter(
            (Q(controlado=True) & ~Q(estadoCalibracion="6")) &
            (
                (Q(tipoCalibracion='2') & Q(fechaCaducidadCalibracion__lte=fecha_aviso_externa)) |
                (Q(tipoCalibracion='1') & Q(fechaCaducidadCalibracion__lte=fecha_aviso_interna))
            )
        )

        if not equipos_a_avisar.exists():
            self.stdout.write("No hay equipos con calibración próxima a vencer.")
            return

        # 4️⃣ Construir mensaje texto plano
        mensaje = "Equipos con calibración próxima a vencer:\n\n"
        for equipo in equipos_a_avisar:
            mensaje += (
                f"- {equipo.equipo} ({equipo.codigo}) "
                f"Estado: {equipo.get_estadoCalibracion_display()} "
                f"Vence: {equipo.fechaCaducidadCalibracion}\n"
            )

        # 5️⃣ Destinatarios
        tecnico = User.objects.get(username="sergio")
        destinatarios = [tecnico.email, "s.baronsanz@gmail.com"]

        # 6️⃣ Enviar email HTML
        self.enviar_mail(mensaje, equipos_a_avisar, destinatarios)

        self.stdout.write(self.style.SUCCESS("Correo enviado con equipos a calibrar"))

    # ---------------------------------------------------------------------

    def actualizacion_equipos(self, hoy):
        equipos = Equipos.objects.filter(controlado=True)

        for equipo in equipos:
            if (
                equipo.fechaCaducidadCalibracion <= hoy
                and equipo.estadoCalibracion == "0"
            ):
                equipo.estadoCalibracion = "1"
                equipo.save()

    # ---------------------------------------------------------------------

    def enviar_mail(self, mensaje_texto, equipos, destinatarios):

        subject = "Aviso de calibración próxima a vencer"

        html_content = f"""
        <html>
        <body style="font-family: Arial; background:#f4f4f4; padding:20px;">
            <div style="background:white; padding:20px; border-radius:10px;">
                <h2 style="color:#2c3e50;">
                    🔧 Equipos con calibración próxima a vencer
                </h2>
                <ul>
                    {''.join(
                        f"<li><b>{e.equipo}</b> ({e.codigo}) - "
                        f"Vence: {e.fechaCaducidadCalibracion}</li>"
                        for e in equipos
                    )}
                </ul>
                <p>Revisar lo antes posible.</p>
            </div>
        </body>
        </html>
        """

        email = EmailMultiAlternatives(
            subject,
            mensaje_texto,
            settings.EMAIL_HOST_USER,
            destinatarios,
        )

        email.attach_alternative(html_content, "text/html")
        email.send()