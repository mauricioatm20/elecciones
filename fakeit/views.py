from django.contrib import messages
from django.db import connection
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from io import BytesIO
import base64
import matplotlib.pyplot as plt


from fakeit.models import Persona


# Create your views here.
class IndexView(generic.ListView):
    template_name = "graphic.html"
    context_object_name = "graph"
    def get_queryset(self):
        # Obtener un cursor para ejecutar consultas
        cursor = connection.cursor()

        # Consulta SQL para obtener los datos de la base de datos
        cursor.execute("SELECT fakeit_persona.partido, COUNT(*) FROM fakeit_resultados "
                       "JOIN fakeit_persona ON fakeit_resultados.persona_id = fakeit_persona.id "
                       "GROUP BY fakeit_persona.partido")

        # Obtener los datos de la consulta
        resultados = cursor.fetchall()

        # Cerrar el cursor
        cursor.close()

        # Extraer los nombres de los partidos y los votos en listas separadas
        partidos = [fila[0] for fila in resultados]
        votos = [fila[1] for fila in resultados]

        # Crear el gráfico de pastel
        fig, ax = plt.subplots()
        ax.pie(partidos, labels=votos,
               colors=['mediumslateblue', 'dodgerblue', 'mediumorchid', 'violet'],
               autopct='%1.1f%%',
               wedgeprops={"linewidth": 1, "edgecolor": "white"})

        ax.set_title('Elecciones ')

        plt.gcf().patch.set_alpha(0)# 0 para completamente transparente, 1 para opaco

        plt.tight_layout()#arantizar que los elementos de la trama (como títulos, etiquetas de ejes, etc.)
                            # estén bien colocados y no se superpongan entre sí.

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        print(graphic)
        return graphic


def registrar_persona(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        partido = request.POST.get('partido')
        persona = Persona.objects.create(nombre=nombre, apellido=apellido, partido=partido)
        messages.success(request, 'Persona agregada correctamente.')
        return redirect('fakeit:index')
    return render(request, 'formulario.html')