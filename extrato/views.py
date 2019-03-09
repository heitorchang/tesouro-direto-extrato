from datetime import date
from collections import defaultdict
from decimal import Decimal


from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum

from .models import Titulo, Corretora, Transacao


class TitulosDeCorretora:
    def __init__(self):
        self.titulos = []

    def __iter__(self):
        yield self.titulos


class TotalDeTitulo:
    def __init__(self):
        self.quantidade = Decimal("0.00")
        self.precoTotal = Decimal("0.00")

    def __iter__(self):
        yield self.quantidade
        yield self.precoTotal

    def __repr__(self):
        return "x{} {}".format(self.quantidade, self.precoTotal)


def transacoes_total(trs):
    """Sum the total amount for the given transactions, trs"""
    total = Decimal('0.00')

    for tr in trs:
        total += tr.sinal * tr.preco
    return total  # make total the amount held, not spent


def agregarTransacoes(trs):
    """Collect total quantity and amount invested, grouped by bond"""
    titulos = defaultdict(TotalDeTitulo)
    
    for tr in trs:
        nome = tr.titulo
        titulos[nome].nome = nome
        titulos[nome].vencimento = tr.titulo.vencimento
        titulos[nome].quantidade += tr.sinal * tr.quantidade
        titulos[nome].precoTotal += tr.sinal * tr.preco
        if tr.titulo.preco is not None:
            titulos[nome].preco = tr.titulo.preco
            titulos[nome].precoAtualizado = tr.titulo.precoAtualizado
        else:
            titulos[nome].preco = 0
            titulos[nome].precoAtualizado = date.today()
    # titulos = sorted(titulos)

    result = []
    
    for nomeDoTitulo in titulos:
        result.append({'nome': titulos[nomeDoTitulo].nome,
                       'vencimento': titulos[nomeDoTitulo].vencimento,
                       'quantidade': titulos[nomeDoTitulo].quantidade,
                       'precoTotal': titulos[nomeDoTitulo].precoTotal,
                       'preco': "{:,.2f}".format(titulos[nomeDoTitulo].preco),
                       'precoAtualizado': titulos[nomeDoTitulo].precoAtualizado,})
        
    return result

    
        
def index(request):
    corretoras = Corretora.objects.all()

    corretorasDict = defaultdict(TitulosDeCorretora)

    for corretora in corretoras:
        transacoes = Transacao.objects.filter(corretora=corretora)
        corretorasDict[corretora].nome = corretora.nome
        corretorasDict[corretora].total = transacoes_total(transacoes)
        corretorasDict[corretora].titulos = agregarTransacoes(transacoes)
        
    return render(request, 'extrato/homepage.html', {'corretoras': corretoras})
    

def transacoes(request):
    transacoes = Transacao.objects.all()

    return render(request, 'extrato/transacoes.html', {'transacoes': transacoes})
