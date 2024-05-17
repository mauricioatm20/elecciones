from django.contrib import messages
from django.db import connection
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, render
from io import BytesIO
import base64
import matplotlib.pyplot as plt
from django.views.generic import ListView
from fakeit.models import Persona


# Create your views here.
class IndexView(ListView):

    def acceso_home(request):
        # Lógica para obtener el gráfico
        graphic = IndexView().get_queryset()

        # Renderizar la plantilla con el gráfico en el contexto
        template_name = "graphic.html"
        context = {
            "graph": graphic
        }
        return render(request, template_name, context)

    def get_queryset(self):
        # Obtener un cursor para ejecutar consultas
        cursor = connection.cursor()

        # Consulta SQL para obtener los datos de la base de datos
        cursor.execute("SELECT partido, COUNT(*) FROM fakeit_persona "
                       "GROUP BY fakeit_persona.partido")

        # Obtener los datos de la consulta
        resultados = cursor.fetchall()

        # Cerrar el cursor
        cursor.close()

        # Extraer los nombres de los partidos y la cantidad de personas por partido
        partidos = [fila[0] for fila in resultados]
        personas_por_partido = [fila[1] for fila in resultados]

        # Crear el gráfico de pastel
        fig, ax = plt.subplots()
        ax.pie(personas_por_partido, labels=partidos,
               colors=['mediumslateblue', 'dodgerblue', 'mediumorchid', 'violet'],
               autopct='%1.1f%%',
               wedgeprops={"linewidth": 1, "edgecolor": "white"})

        ax.set_title('Elecciones ')

        # 0 para completamente transparente, 1 para opaco
        plt.gcf().patch.set_alpha(0)

        # garantiza que los elementos de la trama (como títulos, etiquetas de ejes, etc.)
        # estén bien colocados y no se superpongan entre sí.
        plt.tight_layout()

        #crea un objeto BytesIO, que es un buffer en memoria utilizado para almacenar datos binarios.
        buffer = BytesIO()
        #guarda el gráfico actual en el buffer de memoria en formato PNG. Especificamos el formato como 'png'
        # para que se guarde como una imagen PNG.
        plt.savefig(buffer, format='png')

        #mueve el cursor al inicio del buffer, para que podamos leer los datos desde el principio.
        buffer.seek(0)

        # obtienen los datos binarios de la imagen desde el buffer utilizando el método getvalue().
        image_png = buffer.getvalue()
        buffer.close()

        # Codifica la imagen PNG en formato base64 utilizando la función b64encode del módulo base64.
        # Esto convierte los datos binarios en una cadena base64.
        graphic = base64.b64encode(image_png)

        #decodifica la cadena base64 a una cadena de texto UTF-8. Esto es necesario si deseas utilizar la cadena base64 en un documento HTML.
        graphic = graphic.decode('utf-8')
        print(graphic)
        return graphic


    def registrar_persona(request):
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            partido = request.POST.get('partido')
            if partido:
                # Sí se seleccionó un partido, crear una persona asociada a ese partido
                Persona.objects.create(nombre=nombre, apellido=apellido, partido=partido)
                messages.success(request, 'Voto registrado correctamente.')
            else:
                # Si no se seleccionó un partido, mostrar un mensaje de error
                messages.error(request, 'Por favor, elige un partido antes de continuar.')
                return redirect('fakeit:index')  # Redirigir a la página de inicio o al formulario de registro

            return redirect('fakeit:index')

