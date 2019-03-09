from django.db import models

class Tipo(models.Model):
    """Tipo de titulo"""
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Titulo(models.Model):
    """Titulo (tipo e vencimento)"""
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    vencimento = models.DateField()
    preco = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    precoAtualizado = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return "{} {}".format(tipo, vencimento)

    class Meta:
        ordering = ['tipo', 'vencimento']
        

class Corretora(models.Model):
    """Nome do banco"""
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

        
class Transacao(models.Model):
    """Compra ou venda (+/-)"""
    data = models.DateField()
    titulo = models.ForeignKey(Titulo, on_delete=models.CASCADE)
    corretora = models.ForeignKey(Corretora, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=6, decimal_places=2)
    rendimento = models.DecimalField(max_digits=4, decimal_places=2)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    anotacoes = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return "{} {} {} {} {} {} {}".format(
            self.data, self.titulo, str(self.quantidade), self.corretora,
            str(self.preco))

    class Meta:
        ordering = ['-data', 'corretora', 'titulo']
