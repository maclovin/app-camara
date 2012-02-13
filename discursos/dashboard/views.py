# Create your views here.
import datetime
from django.db.models import Count
from dashboard.models import Discurso
from django.template import Context, loader
from django.http import HttpResponse
from django.utils.html import strip_tags

def filtro(request, keyword, argument):

    if keyword == "partido":
        queryset = Discurso.objects.filter(partido__sigla=argument)
    elif keyword == "estado":
        queryset = Discurso.objects.filter(estado__sigla=argument)
    elif keyword == "orador":
        queryset = Discurso.objects.filter(orador=argument)
    elif keyword == "texto":
        queryset = Discurso.objects.filter(sumario__contains=argument)
    elif keyword == "last": #bugado
        if argument == "all":
            queryset = Discurso.objects.all()
        else:
            queryset = Discurso.objects.all()[:argument]
   
    periodo = {}
    periodo['fim'] = queryset[0].data
    periodo['inicio'] = queryset[len(queryset)-1].data
   
    if request.GET.get("data_inicio"):
        try:
            periodo['inicio'] = datetime.datetime.strptime(request.GET.get("data_inicio"), "%d-%m-%Y") 
            if request.GET.get("data_fim"):
                periodo['fim'] = datetime.datetime.strptime(request.GET.get("data_fim"), "%d-%m-%Y")
            queryset = queryset.filter(data__lte=periodo['fim']).filter(data__gte=periodo['inicio'])
        except:
            return HttpResponse("Data invalida") #criar pagina de erro

    total = queryset.count()
    partidos = queryset.values('partido__sigla').annotate(Count('partido__sigla'))
    for p in partidos:
        p['percent'] = p['partido__sigla__count']*100.0/total

    estados = queryset.values('estado__sigla').annotate(Count('estado__sigla'))
    for e in estados:
        e['percent'] = e['estado__sigla__count']*100.0/total

    oradores = queryset.values('orador', 'orador__nome', 'partido__sigla').annotate(Count('orador__nome'))
    for o in oradores:
        o['percent'] = o['orador__nome__count']*100.0/total

    contagem = queryset.values('discurso', 'data').annotate(Count('data'))

    t = loader.get_template('dashboard/filtro.html')
    c = Context({
        'oradores': oradores,
        'estados' : estados,
        'partidos': partidos,
        'discursos': queryset,
        'total': total,
        'contagem': contagem,
        'periodo' : periodo
    })
    return HttpResponse(t.render(c))


def taggeia(request):
    try:
        discurso_id = strip_tags(request.POST.get("id"))
        discurso_tags = strip_tags(request.POST.get("tags", ''))
        q = Discurso.objects.get(pk = discurso_id)
    except:
        return HttpResponse("Error")
    q.__setattr__("tags", discurso_tags)
    q.save()
    return HttpResponse(discurso_tags) #corrigir os httpresponses
