# CODIGO (TF 11).
# Passo 8: Sem else e um nivel so


class Cpf:
    """Representa e valida o CPF do cliente."""
    def __init__(self, valor):
        if len(valor) != 11:
            raise ValueError("cpf invalido")
        self._valor = valor

    def __str__(self):
        return self._valor


class Email:
    """Representa e valida o e-mail do cliente."""
    def __init__(self, valor):
        if len(valor) == 0:
            raise ValueError("email vazio")
        if "@" not in valor:
            raise ValueError("email invalido")
        self._valor = valor

    def __str__(self):
        return self._valor


class Cep:
    """Representa e valida o CEP do cliente."""
    def __init__(self, valor):
        if len(valor) != 8:
            raise ValueError("cep invalido")
        self._valor = valor

    def __str__(self):
        return self._valor


class Dinheiro:
    """Representa valores monetarios guardados em centavos inteiros."""
    def __init__(self, centavos):
        valor = int(centavos)
        if isinstance(centavos, float):
            valor = int(round(centavos * 100))
        self._centavos = valor

    def somar(self, outro):
        return Dinheiro(self._centavos + outro._centavos)

    def subtrair(self, outro):
        return Dinheiro(self._centavos - outro._centavos)

    def multiplicar(self, quantidade):
        return Dinheiro(self._centavos * quantidade)

    def calcular_percentual(self, percentual):
        centavos_calculados = int(round(self._centavos * percentual))
        return Dinheiro(centavos_calculados)

    def __str__(self):
        reais = self._centavos / 100
        return f"R$ {reais:.2f}"


class Status:
    """Representa o status do pedido e suas transicoes de estado."""
    def __init__(self, codigo="A"):
        self._codigo = codigo

    def esta_aberto(self):
        return self._codigo == "A"

    def esta_pago(self):
        return self._codigo == "P"

    def marcar_como_pago(self):
        self._codigo = "P"

    def marcar_como_cancelado(self):
        self._codigo = "C"

    def descrever(self):
        descricoes = {"A": "aberto", "P": "pago", "C": "cancelado"}
        return descricoes.get(self._codigo, "")

    def __str__(self):
        return self.descrever()


class TipoNormal:
    """Representa a categoria de cliente comum sem desconto adicional."""
    def desconto_sobre(self, valor):
        return Dinheiro(0)


class TipoVip:
    """Representa a categoria de cliente VIP com 10% de desconto."""
    def desconto_sobre(self, valor):
        return valor.calcular_percentual(0.10)


class TipoFuncionario:
    """Representa a categoria de funcionario com 20% de desconto."""
    def desconto_sobre(self, valor):
        return valor.calcular_percentual(0.20)


class Pessoa:
    """Representa os dados pessoais do cliente."""
    def __init__(self, nome, cpf, email):
        self._nome = nome
        self._cpf = cpf
        self._email = email

    def descrever_nome(self):
        return self._nome


class Endereco:
    """Representa a localizacao geografica do cliente."""
    def __init__(self, rua, cidade, cep):
        self._rua = rua
        self._cidade = cidade
        self._cep = cep

    def descrever_cidade(self):
        return self._cidade


class Cliente:
    """Representa o cliente agregando pessoa, endereco e seu tipo polimorfico."""
    def __init__(self, pessoa, endereco, tipo):
        self._pessoa = pessoa
        self._endereco = endereco
        self._tipo = tipo

    def descrever_identificacao(self):
        nome = self._pessoa.descrever_nome()
        cidade = self._endereco.descrever_cidade()
        return f"{nome} - {cidade}"

    def calcular_desconto_sobre(self, valor):
        return self._tipo.desconto_sobre(valor)


class Produto:
    """Representa um produto com nome e preco."""
    def __init__(self, nome, preco):
        self._nome = nome
        self._preco = preco

    def descrever_nome(self):
        return self._nome

    def calcular_preco_total(self, quantidade):
        return self._preco.multiplicar(quantidade)


class ItemDoPedido:
    """Representa um item do pedido com produto e quantidade."""
    def __init__(self, produto, quantidade):
        self._produto = produto
        self._quantidade = quantidade

    def subtotal(self):
        return self._produto.calcular_preco_total(self._quantidade)

    def imprimir(self):
        nome = self._produto.descrever_nome()
        print(f"   {self._quantidade} x {nome} = {self.subtotal()}")


class ItensDoPedido:
    """Colecao de primeira classe que encapsula a lista de itens de um pedido."""
    def __init__(self):
        self._itens = []

    def adicionar(self, item):
        self._itens.append(item)

    def esta_vazia(self):
        return len(self._itens) == 0

    def calcular_total(self):
        total = Dinheiro(0)
        for item in self._itens:
            total = total.somar(item.subtotal())
        return total

    def imprimir(self):
        for item in self._itens:
            item.imprimir()


class Pedido:
    """Representa o pedido aplicando suas regras de negocio."""
    def __init__(self, cliente):
        self._cliente = cliente
        self._itens = ItensDoPedido()
        self._status = Status("A")

    def adicionar_item(self, produto, quantidade):
        self._itens.adicionar(ItemDoPedido(produto, quantidade))

    def pagar(self):
        if not self._status.esta_aberto():
            return False
        if self._itens.esta_vazia():
            return False
        self._status.marcar_como_pago()
        return True

    def cancelar(self):
        if not self._status.esta_aberto():
            return False
        self._status.marcar_como_cancelado()
        return True

    def calcular_total(self):
        return self._itens.calcular_total()

    def calcular_desconto(self):
        total = self.calcular_total()
        return self._cliente.calcular_desconto_sobre(total)

    def calcular_valor_a_pagar(self):
        total = self.calcular_total()
        desconto = self.calcular_desconto()
        return total.subtrair(desconto)

    def somar_se_pago(self, total_acumulado):
        if not self._status.esta_pago():
            return total_acumulado
        return total_acumulado.somar(self.calcular_valor_a_pagar())

    def incrementar_se_aberto(self, contador):
        if not self._status.esta_aberto():
            return contador
        return contador + 1

    def imprimir_totais_se_houver_itens(self):
        if self._itens.esta_vazia():
            return
        total = self.calcular_total()
        desconto = self.calcular_desconto()
        a_pagar = self.calcular_valor_a_pagar()
        print(f"  total: {total} | desconto: {desconto} | a pagar: {a_pagar}")

    def imprimir_relatorio(self, numero):
        identificacao = self._cliente.descrever_identificacao()
        print(f"Pedido {numero} - {identificacao}")
        print(f"  status: {self._status.descrever()}")
        self._itens.imprimir()
        self.imprimir_totais_se_houver_itens()


class Pedidos:
    """Colecao de primeira classe que encapsula o dicionario de pedidos."""
    def __init__(self):
        self._pedidos = {}

    def novo_pedido(self, numero, cliente):
        pedido = Pedido(cliente)
        self._pedidos[numero] = pedido
        return pedido

    def imprimir_relatorio(self):
        for numero, pedido in self._pedidos.items():
            pedido.imprimir_relatorio(numero)

    def calcular_total_arrecadado(self):
        total = Dinheiro(0)
        for pedido in self._pedidos.values():
            total = pedido.somar_se_pago(total)
        return total

    def contar_pedidos_abertos(self):
        quantidade = 0
        for pedido in self._pedidos.values():
            quantidade = pedido.incrementar_se_aberto(quantidade)
        return quantidade


# --- o roteiro da loja (o TF mantem esta saida identica) -----------------------
pedidos = Pedidos()

tipo_vip = TipoVip()
tipo_normal = TipoNormal()
tipo_funcionario = TipoFuncionario()

caderno = Produto("Caderno", Dinheiro(15.5))
caneta = Produto("Caneta", Dinheiro(2.5))
livro = Produto("Livro", Dinheiro(89.5))
fone = Produto("Fone", Dinheiro(60.0))

# Pedido 1
pessoa_ana = Pessoa("Ana Souza", Cpf("12345678901"), Email("ana@mail.com"))
endereco_ana = Endereco("Rua das Flores, 10", "Sorocaba", Cep("18010000"))
cliente_ana = Cliente(pessoa_ana, endereco_ana, tipo_vip)
pedido_da_ana = pedidos.novo_pedido(1, cliente_ana)
pedido_da_ana.adicionar_item(caderno, 2)
pedido_da_ana.adicionar_item(caneta, 5)

# Pedido 2
try:
    pessoa_bruno = Pessoa("Bruno Lima", Cpf("123"), Email("bruno@mail.com"))
    endereco_bruno = Endereco("Av. Central, 200", "Votorantim", Cep("18110000"))
    cliente_bruno = Cliente(pessoa_bruno, endereco_bruno, tipo_normal)
    pedidos.novo_pedido(2, cliente_bruno)
except ValueError as erro:
    print(f"pedido 2 recusado: {erro}")

# Pedido 3
pedido_da_ana_2 = pedidos.novo_pedido(3, cliente_ana)
pedido_da_ana_2.adicionar_item(livro, 1)

# Pedido 4
try:
    pessoa_carla = Pessoa("Carla Dias", Cpf("98765432100"), Email("carla.mail.com"))
    endereco_carla = Endereco("Rua do Sol, 55", "Sorocaba", Cep("18020000"))
    cliente_carla = Cliente(pessoa_carla, endereco_carla, tipo_funcionario)
    pedidos.novo_pedido(4, cliente_carla)
except ValueError as erro:
    print(f"pedido 4 recusado: {erro}")

# Pedido 5
pessoa_diego = Pessoa("Diego Rocha", Cpf("11122233344"), Email("diego@mail.com"))
endereco_diego = Endereco("Rua Nova, 7", "Itu", Cep("13300000"))
cliente_diego = Cliente(pessoa_diego, endereco_diego, tipo_normal)
pedido_do_diego = pedidos.novo_pedido(5, cliente_diego)

# Pedido 6
pessoa_eva = Pessoa("Eva Nunes", Cpf("55566677788"), Email("eva@mail.com"))
endereco_eva = Endereco("Alameda Azul, 1", "Itu", Cep("13300001"))
cliente_eva = Cliente(pessoa_eva, endereco_eva, tipo_funcionario)
pedido_da_eva = pedidos.novo_pedido(6, cliente_eva)
pedido_da_eva.adicionar_item(fone, 1)

# Pedido 7
try:
    pessoa_fabio = Pessoa("Fabio Costa", Cpf("99988877766"), Email("fabio@mail.com"))
    endereco_fabio = Endereco("Rua Velha, 3", "Itu", Cep("123"))
    cliente_fabio = Cliente(pessoa_fabio, endereco_fabio, tipo_normal)
    pedidos.novo_pedido(7, cliente_fabio)
except ValueError as erro:
    print(f"pedido 7 recusado: {erro}")

# Pedido 8
pessoa_gil = Pessoa("Gil Alves", Cpf("44455566677"), Email("gil@mail.com"))
endereco_gil = Endereco("Rua do Meio, 9", "Sorocaba", Cep("18030000"))
cliente_gil = Cliente(pessoa_gil, endereco_gil, tipo_normal)
pedido_do_gil = pedidos.novo_pedido(8, cliente_gil)
pedido_do_gil.adicionar_item(fone, 2)

print("pagar 1:", pedido_da_ana.pagar())
print("pagar 3:", pedido_da_ana_2.pagar())
print("pagar 5:", pedido_do_diego.pagar())
print("pagar 6:", pedido_da_eva.pagar())
print("cancelar 5:", pedido_do_diego.cancelar())
print("cancelar 1:", pedido_da_ana.cancelar())

pedidos.imprimir_relatorio()
print("arrecadado:", pedidos.calcular_total_arrecadado())
print("abertos:", pedidos.contar_pedidos_abertos())
