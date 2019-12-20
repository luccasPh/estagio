from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from .render import Render


from . import models
from . import forms

# Create your views here.

class Index(View):
   
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            eventos = request.user.evento_set.all()
            evento_form = forms.EventoForm
            context = {
                "logado": True,
                "novo_evento_form": evento_form,
                "eventos": eventos
            }
        
        else:
            eventos = models.Evento.objects.all().order_by('data_inicio')
            login_form = AuthenticationForm() 
            context = {
                "logado": False,
                "login_form": login_form,
                "eventos": eventos
            }
        
        return render(
            request=request, 
            context=context, 
            template_name='index.html'
        )
    
    def post(self, request, *args, **kwargs):
        login_form = AuthenticationForm(request=request, data=request.POST)
        
        if login_form.is_valid():
            email = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = authenticate(username=email, password=password)
           
            if user is not None:
                login(request, user)
                messages.info(request, "Login realizado com sucesso")
                
                return redirect('sigea:index')

            else:
                messages.error(request, "Email ou senha inválidos.")
        else:
            messages.error(request, "Email ou senha inválidos.")
        
        return redirect('sigea:index')

class Logout(View):
    
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, "Desconectado com sucesso!")
        return redirect("sigea:index")

class TestUsuario(UserPassesTestMixin):
    
    def test_func(self):
        evpk = self.kwargs['evpk']
        evento = get_object_or_404(models.Evento, pk=evpk)
        
        if self.request.user.is_authenticated and self.request.user.id == evento.organizacao.id:
            return True

        else:
            return False
    
    def handle_no_permission(self):
        messages.error(self.request, "Acesso negado! Usuário não identificado ou não tem permissão para acessar a página!")
        return redirect('sigea:index')

class InscricaoPdf(View):

    def get(self, request, *args, **kwargs):
        evpk = self.kwargs['evpk']
        evento = get_object_or_404(models.Evento, pk=evpk)

        prpk = self.kwargs['prpk']

        if prpk != 0:
            atividade = get_object_or_404(models.Programacao, pk=prpk)
            inscricoes = models.Inscricao.objects.filter(evento=evento).filter(atividade=atividade).order_by('nome')
        
        else:
            inscricoes = models.Inscricao.objects.filter(evento=evento).order_by('nome')
            atividade = None
        
        context = {
            'prpk': prpk,
            'evento': evento,
            'inscricoes': inscricoes,
            'request': request,
            'atividade': atividade
        }
        return Render.render('inscricoes_pdf.html', context)

class InscricaoPage(View):

    def get(self, request, *args, **kwargs):
        evpk = self.kwargs['evpk']
        evento = get_object_or_404(models.Evento, pk=evpk)
        formulario = forms.InscricaoForm(evento)
        atividades = models.Programacao.objects.filter(evento=evento).filter(inscrever=True).order_by('data_hora')

        context = {
            "evento": evento,
            "formulario": formulario,
            "atividades": atividades
        }

        return render(
            request=request, 
            context=context, 
            template_name='formulario_inscricao.html'
        )

    def post(self, request, *args, **kwargs):
        evpk = self.kwargs["evpk"]
        evento = get_object_or_404(models.Evento, pk=evpk)
        formulario = forms.InscricaoForm(evento, request.POST)

        if formulario.is_valid():
            form = formulario.save(commit=False)

            if models.Inscricao.objects.filter(cpf=form.cpf):
                messages.error(request, "CPF já cadastro neste Evento")
            
            elif len(form.cpf) < 14:
                messages.error(request, "CPF Invalido")

            elif len(form.telefone) < 14:
                messages.error(request, "Telefone Invalido")

            else:
                form.evento = evento
                form.save()
                formulario.save_m2m()
                messages.info(request, "Inscrição realizada com sucesso")
                
                return redirect('sigea:evento_pagina', evpk=evento.id, slug=evento.slug)

        atividades = models.Programacao.objects.filter(evento=evento).filter(inscrever=True).order_by('data_hora')
        context = {
            "evento": evento,
            "formulario": formulario,
            "atividades": atividades
        }

        return render(
            request=request, 
            context=context, 
            template_name='formulario_inscricao.html'
        )

class InscricaoFilter(View):
    
    def post(self, request, *args, **kwargs):
        evpk = self.kwargs['evpk']
        evento = get_object_or_404(models.Evento, pk=evpk)
        filtro_forms = forms.AtividadesFilterForm(evento, request.POST)
        data = dict()

        if filtro_forms.is_valid():
            filtro = filtro_forms.cleaned_data['atividade']
            
            if filtro:
                inscricoes = models.Inscricao.objects.filter(evento=evento).filter(atividade=filtro).order_by('nome')
                atividade = models.Programacao.objects.get(titulo=filtro)
            
            else:
                inscricoes = models.Inscricao.objects.filter(evento=evento).order_by('nome')
                atividade = models.Programacao.objects.filter(evento=evento)

            data["tabela_filtro"] = render_to_string("includes/inscricoes_tabela.html", {
                "inscricoes": inscricoes
            })

            data["total_inscricao"] = render_to_string("includes/total_inscricao.html", {
                "inscricoes": inscricoes,
            })
            
            data["buttao_gera_pdf"] = render_to_string("includes/buttao_gera_pdf.html", {
                "evento": evento,
                "atividade": atividade,
                "inscricoes": inscricoes
            })

        return JsonResponse(data)

class EventoPage(View):

    def get(self, request, *args, **kwargs):
        evpk = self.kwargs['evpk']
        evento = get_object_or_404(models.Evento, pk=evpk)
        organizacao = evento.organizacao
        programacoes = models.Programacao.objects.filter(evento_id=evento.id).order_by('data_hora')
        palestrantes = models.Palestrante.objects.filter(evento_id=evento.id)

        sobre = False
        if len(evento.sobre) > 68:
            sobre = True

        context = {
            "evento": evento,
            "organizacao": organizacao,
            "programacoes": programacoes,
            "palestrantes": palestrantes,
            "sobre": sobre
        }
        return render(
            request=request, 
            context=context, 
            template_name='evento_pagina.html'
        )



class EventoCreate(View):
    
    def post(self, request, *args, **kwargs):
        evento_form = forms.EventoForm(request.POST)

        if evento_form.is_valid():
            evento = evento_form.save(commit=False)
            evento.organizacao = request.user
            evento_form.save()
            messages.info(request, "Evento criado com sucesso!")

            return redirect('sigea:evento_config', evpk=evento.id)
        
        else:
            messages.error(request, "Solicitação invalida!")
            return redirect('sigea:index')

class EventoDelete(TestUsuario, View):
        
    data = dict()

    def get(self, request, *args, **kwargs):
        evpk = self.kwargs["evpk"]
        evento = get_object_or_404(models.Evento, pk=evpk)

        context = {"evento": evento}
        self.data["form_html"] = render_to_string('includes/evento_delete.html', context, request=request)
    
        return JsonResponse(self.data) 

    def post(self, request, *args, **kwargs):
        evpk = self.kwargs["evpk"]
        evento = get_object_or_404(models.Evento, pk=evpk)
        evento.delete()    

        eventos = request.user.evento_set.all()
        self.data["evento_cards"] = render_to_string("includes/organizacao_eventos.html", {
            "eventos": eventos
        })
    
        return JsonResponse(self.data)  


class EventoConfig(TestUsuario, View):

    def get(self, request, *args, **kwargs):
        evpk = self.kwargs["evpk"]
        evento = get_object_or_404(models.Evento, pk=evpk)
        evento_config_form = forms.EventoForm(instance=evento)
        novo_evento_form = forms.EventoForm

        palestrante_form = forms.PalestranteForm
        palestrante = models.Palestrante.objects.filter(evento_id=evento.id)

        programacao_form = forms.ProgramacaoForm(evento)
        programacao = models.Programacao.objects.filter(evento_id=evento.id).order_by('data_hora')

        inscricoes = models.Inscricao.objects.filter(evento_id=evento.id).order_by('nome')
        atividade_filter = forms.AtividadesFilterForm(evento)

        context = {
            "evento": evento,
            "evento_config_form": evento_config_form,
            "novo_evento_form": novo_evento_form,
            "programacao_form": programacao_form, 
            "programacao": programacao,
            "palestrante_form": palestrante_form, 
            "palestrante": palestrante,
            "inscricoes": inscricoes,
            "atividade_filter": atividade_filter
        }

        return render(
            request=request,
            template_name="evento_config.html",
            context=context
        )
    
    def post(self, request, *args, **kwargs):
        data = dict()
        evpk = self.kwargs["evpk"]
        evento = get_object_or_404(models.Evento, pk=evpk)
        evento_config_form = forms.EventoForm(request.POST, request.FILES, instance=evento)

        if evento_config_form.is_valid():
            evento_config_form.save()
            
            evento = get_object_or_404(models.Evento, pk=evpk)
            evento_config_form = forms.EventoForm(instance=evento)

            data["banner_form"] = render_to_string("includes/banner_form.html",{
                "evento_config_form": evento_config_form,
                "evento": evento
            })

            data["escodidas"] = render_to_string("includes/escodidas.html",{
                "evento_config_form": evento_config_form
            })

            data["capa_form"] = render_to_string("includes/capa_form.html",{
                "evento_config_form": evento_config_form,
                "evento": evento
            })
            
            data["titulo_nav"] = render_to_string("includes/titulo_nav.html",{
                "evento": evento
            })

            data["valido_form"] = True

        return JsonResponse(data)

class PalestranteCreate(TestUsuario, View):

    def post(self, request, *args, **kwargs):
        data = dict()
        evpk = self.kwargs["evpk"]
        evento = get_object_or_404(models.Evento, pk=evpk)
        palestrante_form = forms.PalestranteForm(request.POST, request.FILES)
        
        if palestrante_form.is_valid():
            palestrante = palestrante_form.save(commit=False)
            palestrante.evento = evento
            palestrante.save()

            programacao_form = forms.ProgramacaoForm(evento)
            data["programacao_create_html"] = render_to_string("includes/programacao/create_form.html",{
                "programacao_form": programacao_form,
            })

            programacao = models.Programacao.objects.filter(evento_id=evento.id).order_by('data_hora')
            data["table_programacao_html"] = render_to_string("includes/programacao/table.html", {
                "programacao": programacao,
                "evento": evento
            })

            palestrante = models.Palestrante.objects.filter(evento_id=evento.id)
            data["table_html"] = render_to_string("includes/palestrante/table.html", {
                "palestrante": palestrante,
                "evento": evento
            })

            data["valido_form"] = True

        return JsonResponse(data)

class PalestranteUpdate(TestUsuario, View):
    
    data = dict()

    def get(self, request, *args, **kwargs):
        papk = self.kwargs["papk"]
        evpk = self.kwargs["evpk"]
        evento = get_object_or_404(models.Evento, pk=evpk)
        palestrante = get_object_or_404(models.Palestrante, pk=papk)
        palestrante_form = forms.PalestranteForm(instance=palestrante)

        self.data["form_html"] = render_to_string('includes/palestrante/update_form.html',{
            "palestrante_form": palestrante_form,
            "evento": evento
        }, request)
    
        return JsonResponse(self.data)
    
    def post(self, request, *args, **kwargs):
        papk = self.kwargs["papk"]
        evpk = self.kwargs["evpk"]
        evento = get_object_or_404(models.Evento, pk=evpk)
        palestrante = get_object_or_404(models.Palestrante, pk=papk)
        palestrante_form = forms.PalestranteForm(request.POST, request.FILES, instance=palestrante)
       
        if palestrante_form.is_valid():
            palestrante_form.save()
        
            programacao_form = forms.ProgramacaoForm(evento)
            self.data["programacao_create_html"] = render_to_string("includes/programacao/create_form.html",{
                "programacao_form": programacao_form,
            })

            programacao = models.Programacao.objects.filter(evento_id=evento.id).order_by('data_hora')
            self.data["table_programacao_html"] = render_to_string("includes/programacao/table.html", {
                "programacao": programacao,
                "evento": evento
            })

            palestrante = models.Palestrante.objects.filter(evento_id=evento.id)
            self.data["table_html"] = render_to_string("includes/palestrante/table.html", {
                "palestrante": palestrante,
                "evento": evento
            })

            self.data["valido_form"] = True

        return JsonResponse(self.data)

class PalestranteDelete(TestUsuario, View):
    
    data = dict()

    def get(self, request, *args, **kwargs):
        papk = self.kwargs["papk"]
        evpk = self.kwargs["evpk"]
        evento = get_object_or_404(models.Evento, pk=evpk)
        palestrante = get_object_or_404(models.Palestrante, pk=papk)

        self.data["form_html"] = render_to_string('includes/palestrante/delete_form.html',{
            "palestrante": palestrante,
            "evento": evento
        }, request)
    
        return JsonResponse(self.data) 

    def post(self, request, *args, **kwargs):
        papk = self.kwargs["papk"]
        evpk = self.kwargs["evpk"]
        evento = get_object_or_404(models.Evento, pk=evpk)
        palestrante = get_object_or_404(models.Palestrante, pk=papk)
        palestrante.delete()

        programacao_form = forms.ProgramacaoForm(evento)
        self.data["programacao_create_html"] = render_to_string("includes/programacao/create_form.html",{
            "programacao_form": programacao_form,
        })    

        programacao = models.Programacao.objects.filter(evento_id=evento.id).order_by('data_hora')
        self.data["table_programacao_html"] = render_to_string("includes/programacao/table.html", {
            "programacao": programacao,
            "evento": evento
        })

        palestrante = models.Palestrante.objects.filter(evento_id=evento.id)
        self.data["table_html"] = render_to_string("includes/palestrante/table.html", {
            "palestrante": palestrante,
            "evento": evento
        })

        self.data["valido_form"] = True
    
        return JsonResponse(self.data)

class ProgramacaoCreate(TestUsuario, View):
    
    def post(self, request, *args, **kwargs):
        data = dict()
        evpk = self.kwargs["evpk"]
        evento = get_object_or_404(models.Evento, pk=evpk)
        programacao_form = forms.ProgramacaoForm(evento, request.POST)
        
        if programacao_form.is_valid():
            programacao = programacao_form.save(commit=False)
            programacao.evento = evento
            programacao.save()
        
            programacao = models.Programacao.objects.filter(evento_id=evento.id).order_by('data_hora')
            data["table_html"] = render_to_string("includes/programacao/table.html", {
                "programacao": programacao,
                "evento": evento
            })

            atividade_filter = forms.AtividadesFilterForm(evento)
            data["filtro_form"] = render_to_string("includes/filtro_form.html", {
                "atividade_filter": atividade_filter
            })

            data["valido_form"] = True

        return JsonResponse(data)

class ProgramacaoUpdate(TestUsuario, View):
    
    data = dict()

    def get(self, request, *args, **kwargs):
        prpk = self.kwargs["prpk"]
        evpk = self.kwargs["evpk"]
        evento = get_object_or_404(models.Evento, pk=evpk)
        programacao = get_object_or_404(models.Programacao, pk=prpk)
        programacao_form = forms.ProgramacaoForm(evento, instance=programacao)

        self.data["form_html"] = render_to_string('includes/programacao/update_form.html',{
            "programacao_form": programacao_form,
            "evento": evento
        }, request)
    
        return JsonResponse(self.data)
    
    def post(self, request, *args, **kwargs):
        prpk = self.kwargs["prpk"]
        evpk = self.kwargs["evpk"]
        evento = get_object_or_404(models.Evento, pk=evpk)
        programacao = get_object_or_404(models.Programacao, pk=prpk)
        programacao_form = forms.ProgramacaoForm(evento, request.POST, instance=programacao)
       
        if programacao_form.is_valid():
            programacao_form.save()

            programacao = models.Programacao.objects.filter(evento_id=evento.id).order_by('data_hora')
            self.data["table_html"] = render_to_string("includes/programacao/table.html", {
                "programacao": programacao,
                "evento": evento
            })

            self.data["valido_form"] = True

        return JsonResponse(self.data)



class ProgramacaoDelete(TestUsuario, View):
    
    data = dict()

    def get(self, request, *args, **kwargs):
        prpk = self.kwargs["prpk"]
        evpk = self.kwargs["evpk"]
        evento = get_object_or_404(models.Evento, pk=evpk)
        programacao = get_object_or_404(models.Programacao, pk=prpk)

        self.data["form_html"] = render_to_string('includes/programacao/delete_form.html',{
            "programacao": programacao,
            "evento": evento
        }, request)


    
        return JsonResponse(self.data) 

    def post(self, request, *args, **kwargs):
        prpk = self.kwargs["prpk"]
        evpk = self.kwargs["evpk"]
        evento = get_object_or_404(models.Evento, pk=evpk)
        programacao = get_object_or_404(models.Programacao, pk=prpk)
        programacao.delete()    

        programacao = models.Programacao.objects.filter(evento_id=evento.id).order_by('data_hora')
        self.data["table_html"] = render_to_string("includes/programacao/table.html", {
            "programacao": programacao,
            "evento": evento
        })
        
        atividade_filter = forms.AtividadesFilterForm(evento)
        self.data["filtro_form"] = render_to_string("includes/filtro_form.html", {
            "atividade_filter": atividade_filter
        })

        self.data["valido_form"] = True
    
        return JsonResponse(self.data)  
