from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views import View
from django.views.decorators.csrf import csrf_exempt


from .models import Programacao, Palestrante
from .forms import ProgramacaoForm, PalestranteForm

# Create your views here.

class Index(View):
    template_name="index.html"

    def get(self, request, *args, **kwargs):
        print(request.user.id)
        return render(request, self.template_name)


class Organizacao(View):
    template_name = "organizador.html"
    data = dict()

    def get(self, request, *args, **kwargs):
        programacao_form = ProgramacaoForm
        programacao = Programacao.objects.all()

        palestrante_form = PalestranteForm
        palestrante = Palestrante.objects.all()

        return render(request, self.template_name, {
            "programacao_form": programacao_form, 
            "programacao": programacao,
            "palestrante_form": palestrante_form, 
            "palestrante": palestrante
            })


class ProgramacaoCreate(View):
    
    def post(self, request, *args, **kwargs):
        data = dict()
        programacao_form = ProgramacaoForm(request.POST)
        
        if programacao_form.is_valid():
            programacao_form.save()

        programacao = Programacao.objects.all()
        data["table_html"] = render_to_string("includes/programacao/table.html", {
            "programacao": programacao
        })

        return JsonResponse(data)


class ProgramacaoUpdate(View):
    data = dict()

    def get(self, request, pk, *args, **kwargs):
        programacao = get_object_or_404(Programacao, pk=pk)
        programacao_form = ProgramacaoForm(instance=programacao)

        context = {"programacao_form": programacao_form}
        self.data["form_html"] = render_to_string('includes/programacao/update_form.html', 
            context, 
            request=request
        )
    
        return JsonResponse(self.data)
    
    def post(self, request, pk, *args, **kwargs):
        programacao = get_object_or_404(Programacao, pk=pk)
        programacao_form = ProgramacaoForm(request.POST, instance=programacao)
       
        if programacao_form.is_valid():
            programacao_form.save()

        programacao = Programacao.objects.all()
        self.data["table_html"] = render_to_string("includes/programacao/table.html", {
            "programacao": programacao
        })

        return JsonResponse(self.data)



class ProgramacaoDelete(View):
    data = dict()

    def get(self, request, pk, *args, **kwargs):
        programacao = get_object_or_404(Programacao, pk=pk)

        context = {"programacao": programacao}
        self.data["form_html"] = render_to_string('includes/programacao/delete_form.html', context, request=request)
    
        return JsonResponse(self.data) 

    def post(self, request, pk, *args, **kwargs):
        programacao = get_object_or_404(Programacao, pk=pk)
        programacao.delete()    

        programacao = Programacao.objects.all()
        self.data["table_html"] = render_to_string("includes/programacao/table.html", {
            "programacao": programacao
        })
    
        return JsonResponse(self.data)  



class PalestranteCreate(View):

    def post(self, request, *args, **kwargs):
        data = dict()
        form = PalestranteForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()

        palestrante = Palestrante.objects.all()
        data["table_html"] = render_to_string("includes/palestrante/table.html", {
            "palestrante": palestrante
        })

        return JsonResponse(data)

class PalestranteUpdate(View):
    data = dict()

    def get(self, request, pk, *args, **kwargs):
        palestrante = get_object_or_404(Palestrante, pk=pk)
        palestrante_form = PalestranteForm(instance=palestrante)

        context = {"palestrante_form": palestrante_form}
        self.data["form_html"] = render_to_string('includes/palestrante/update_form.html', 
            context, 
            request=request
        )
    
        return JsonResponse(self.data)
    
    def post(self, request, pk, *args, **kwargs):
        palestrante = get_object_or_404(Palestrante, pk=pk)
        palestrante_form = PalestranteForm(request.POST, request.FILES, instance=palestrante)
       
        if palestrante_form.is_valid():
            palestrante_form.save()

        palestrante = Palestrante.objects.all()
        self.data["table_html"] = render_to_string("includes/palestrante/table.html", {
            "palestrante": palestrante
        })

        return JsonResponse(self.data)

class PalestranteDelete(View):
    data = dict()

    def get(self, request, pk, *args, **kwargs):
        palestrante = get_object_or_404(Palestrante, pk=pk)

        context = {"palestrante": palestrante}
        self.data["form_html"] = render_to_string('includes/palestrante/delete_form.html', context, request=request)
    
        return JsonResponse(self.data) 

    def post(self, request, pk, *args, **kwargs):
        palestrante = get_object_or_404(Palestrante, pk=pk)
        palestrante.delete()    

        palestrante = Palestrante.objects.all()
        self.data["table_html"] = render_to_string("includes/palestrante/table.html", {
            "palestrante": palestrante
        })
    
        return JsonResponse(self.data)  