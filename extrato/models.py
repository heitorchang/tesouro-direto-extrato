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
        return "{} {}".format(self.tipo, self.vencimento)

    class Meta:
        ordering = ['tipo', 'vencimento']
        

class Corretora(models.Model):
    """Nome do banco"""
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

        
class Transacao(models.Model):
    """Compra ou venda (+ compra ou - venda)"""
    data = models.DateField()
    sinal = models.IntegerField(default=1)
    titulo = models.ForeignKey(Titulo, on_delete=models.CASCADE)
    corretora = models.ForeignKey(Corretora, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=6, decimal_places=2)
    rendimento = models.DecimalField(max_digits=4, decimal_places=2)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    anotacoes = models.CharField(max_length=100, blank=True)

    def __str__(self):
        movimento = "Compra" if self.sinal == 1 else "Venda"
        return "{} {} {}: {} x{} R$ {}".format(
            self.data, movimento, self.corretora,
            self.titulo, str(self.quantidade),
            str(self.preco))

    class Meta:
        ordering = ['-data', 'corretora', 'titulo']
        verbose_name_plural = "Transações"
