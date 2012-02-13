from dashboard.models import Discurso, Estado, Partido, Orador
import json
from datetime import datetime
from django.db import transaction

#Necessario resetar a tabela!
 
discursos = json.loads(open('discursoscamara-63-64.json').read())


@transaction.commit_on_success
def importar():
    count = 0
    for d in discursos:
        try:
            e = Estado.objects.get(sigla=d['estado'].strip())
        except Estado.DoesNotExist:
            e = Estado()
            e.sigla = d['estado'].strip()
            e.save()

        try:
            p = Partido.objects.get(sigla=d['partido'].strip())
        except Partido.DoesNotExist:
            p = Partido()
            p.sigla = d['partido'].strip()
            p.save()

        try:
            o = Orador.objects.get(nome=d['orador'].strip())
        except Orador.DoesNotExist:
            o = Orador()
            o.nome = d['orador'].strip()
            o.save()

        try:
            entry = Discurso.objects.get(sumario=d['discurso'].strip())
        except Discurso.DoesNotExist:
            entry = Discurso()
            entry.data = datetime.strptime(d['data'] + '-' + d['hora'], '%d/%m/%Y-%H:%M')
            entry.discurso = d['discurso'].strip()
            entry.sumario = d['sumario'].strip()
            if d['fase']:        
                entry.fase = d['fase'].strip()
            entry.orador = o
            entry.estado = e
            entry.partido = p
            entry.save()
        if count > 5000:
            print 'Counting 5000 more...'
            count = 0
        else:
            count += 1

