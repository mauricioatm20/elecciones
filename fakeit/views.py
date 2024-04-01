from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import numpy as np
# Create your views here.
class IndexView(generic.ListView):
    template_name = "graphic.html"
    context_object_name = "graph"
    def get_queryset(self):

        # make data
        x = [1, 2, 3, 4]
        colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))


        # plot

        labels = 'partido 1', 'partido 2', 'partido 3', 'partido 4'

        sizes = [15, 30, 45, 10]
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels,
               colors=['mediumslateblue', 'dodgerblue', 'mediumorchid', 'violet'], autopct='%1.1f%%' ,
               wedgeprops={"linewidth": 1, "edgecolor": "white"})

        ax.set_title('Elecciones ')

        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        print(graphic)
        return graphic
