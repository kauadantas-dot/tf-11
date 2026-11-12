# CODIGO (TF 11).
# Passo 5: Colecoes de primeira classe - ItensDoPedido e Pedidos


class Cpf:
    """Representa e valida o CPF do cliente."""
    def __init__(self, valor):
        if len(valor) != 11:
            raise ValueError("cpf invalido")
        self.valor = valor

    def __str__(self):
        return self.valor


class Email:
    """Representa e valida o e-mail do cliente."""
    def __init__(self, valor):
        if len(valor) == 0:
            raise ValueError("email vazio")
        if "@" not in valor:
            raise ValueError("email invalido")
        self.valor = valor

    def __str__(self):
        return self.valor


class Cep:
    """Representa e valida o CEP do cliente."""
    def __init__(self, valor):
        if len(valor) != 8:
            raise ValueError("cep invalido")
        self.valor = valor

    def __str__(self):
        return self.valor


class Dinheiro:
    """Representa valores monetarios guardados em centavos inteiros."""
    def __init__(self, centavos):
        if isinstance(centavos, float):
            self.centavos = round(centavos * 100)
        else:
            self.centavos = int(centavos)

    def somar(self, outro):
        return Dinheiro(self.centavos + outro.centavos)

    def subtrair(self, outro):
        return Dinheiro(self.centavos - outro.centavos)

    def multiplicar(self, quantidade):
        return Dinheiro(self.centavos * quantidade)

    def calcular_percentual(self, percentual):
        return Dinheiro(round(self.centavos * percentual))

    def __str__(self):
        reais = self.centavos / 100
        return f"R$ {reais:.2f}"


class Status:
    """Representa o status do pedido e suas descricoes."""
    def __init__(self, codigo="A"):
        self.codigo = codigo

    def esta_aberto(self):
        return self.codigo == "A"

    def esta_pago(self):
        return self.codigo == "P"

    def esta_cancelado(self):
        return self.codigo == "C"

    def pagar(self):
        self.codigo = "P"

    def cancelar(self):
        self.codigo = "C"

    def descrever(self):
        descricoes = {"A": "aberto", "P": "pago", "C": "cancelado"}
        return descricoes.get(self.codigo, "")

    def __str__(self):
        return self.descrever()


class Cliente:
    """Representa os dados completos do cliente."""
    def __init__(self, nome, cpf, email, rua, cidade, cep, tipo):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.tipo = tipo


class Produto:
    """Representa um produto com nome e preco."""
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco


class ItemDoPedido:
    """Representa um item do pedido com produto e quantidade."""
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

    def subtotal(self):
        return self.produto.preco.multiplicar(self.quantidade)


class ItensDoPedido:
    """Colecao de primeira classe que encapsula a lista de itens de um pedido."""
    def __init__(self):
        self.itens = []

    def adicionar(self, item):
        self.itens.append(item)

    def esta_vazia(self):
        return len(self.itens) == 0

    def calcular_total(self):
        total = Dinheiro(0)
        for item in self.itens:
            total = total.somar(item.subtotal())
        return total

    def imprimir(self):
        for item in self.itens:
            print("  ", item.quantidade, "x", item.produto.nome, "=", item.subtotal())


class Pedido:
    """Representa o pedido de um cliente sem guardar seu numero."""
    def __init__(self, cliente):
        self.cliente = cliente
        self.itens = ItensDoPedido()
        self.status = Status("A")

    def adicionar_item(self, produto, quantidade):
        self.itens.adicionar(ItemDoPedido(produto, quantidade))

    def obter_status(self):
        return self.status

    def calcular_total(self):
        return self.itens.calcular_total()

    def calcular_desconto(self):
        total = self.calcular_total()
        if self.cliente.tipo == "V":
            return total.calcular_percentual(0.10)
        elif self.cliente.tipo == "F":
            return total.calcular_percentual(0.20)
        else:
            return Dinheiro(0)

    def calcular_valor_a_pagar(self):
        return self.calcular_total().subtrair(self.calcular_desconto())


class Pedidos:
    """Colecao de primeira classe que encapsula o dicionario de pedidos."""
    def __init__(self):
        self.pedidos = {}

    def novo_pedido(self, numero, cliente):
        pedido = Pedido(cliente)
        self.pedidos[numero] = pedido
        return pedido

    def imprimir_relatorio(self):
        for numero, pedido in self.pedidos.items():
            print("Pedido", numero, "-", pedido.cliente.nome, "-", pedido.cliente.cidade)
            print("  status:", pedido.obter_status().descrever())
            pedido.itens.imprimir()
            if not pedido.itens.esta_vazia():
                total = pedido.calcular_total()
                desconto = pedido.calcular_desconto()
                a_pagar = pedido.calcular_valor_a_pagar()
                print("  total:", total, "| desconto:", desconto, "| a pagar:", a_pagar)

    def calcular_total_arrecadado(self):
        total = Dinheiro(0)
        for pedido in self.pedidos.values():
            if pedido.obter_status().esta_pago():
                total = total.somar(pedido.calcular_valor_a_pagar())
        return total

    def contar_pedidos_abertos(self):
        quantidade = 0
        for pedido in self.pedidos.values():
            if pedido.obter_status().esta_aberto():
                quantidade = quantidade + 1
        return quantidade


def pagar(pedido):
    if pedido.obter_status().esta_aberto():
        if not pedido.itens.esta_vazia():
            pedido.obter_status().pagar()
            return True
        else:
            return False
    else:
        return False


def cancelar(pedido):
    if pedido.obter_status().esta_aberto():
        pedido.obter_status().cancelar()
        return True
    else:
        return False


# --- o roteiro da loja (o TF mantem esta saida identica) -----------------------
pedidos = Pedidos()

caderno = Produto("Caderno", Dinheiro(15.5))
caneta = Produto("Caneta", Dinheiro(2.5))
livro = Produto("Livro", Dinheiro(89.5))
fone = Produto("Fone", Dinheiro(60.0))

# Pedido 1
cliente_ana = Cliente("Ana Souza", Cpf("12345678901"), Email("ana@mail.com"), "Rua das Flores, 10", "Sorocaba", Cep("18010000"), "V")
pedido_da_ana = pedidos.novo_pedido(1, cliente_ana)
pedido_da_ana.adicionar_item(caderno, 2)
pedido_da_ana.adicionar_item(caneta, 5)

# Pedido 2
try:
    cliente_bruno = Cliente("Bruno Lima", Cpf("123"), Email("bruno@mail.com"), "Av. Central, 200", "Votorantim", Cep("18110000"), "N")
    pedidos.novo_pedido(2, cliente_bruno)
except ValueError as erro:
    print(f"pedido 2 recusado: {erro}")

# Pedido 3
pedido_da_ana_2 = pedidos.novo_pedido(3, cliente_ana)
pedido_da_ana_2.adicionar_item(livro, 1)

# Pedido 4
try:
    cliente_carla = Cliente("Carla Dias", Cpf("98765432100"), Email("carla.mail.com"), "Rua do Sol, 55", "Sorocaba", Cep("18020000"), "F")
    pedidos.novo_pedido(4, cliente_carla)
except ValueError as erro:
    print(f"pedido 4 recusado: {erro}")

# Pedido 5
cliente_diego = Cliente("Diego Rocha", Cpf("11122233344"), Email("diego@mail.com"), "Rua Nova, 7", "Itu", Cep("13300000"), "N")
pedido_do_diego = pedidos.novo_pedido(5, cliente_diego)

# Pedido 6
cliente_eva = Cliente("Eva Nunes", Cpf("55566677788"), Email("eva@mail.com"), "Alameda Azul, 1", "Itu", Cep("13300001"), "F")
pedido_da_eva = pedidos.novo_pedido(6, cliente_eva)
pedido_da_eva.adicionar_item(fone, 1)

# Pedido 7
try:
    cliente_fabio = Cliente("Fabio Costa", Cpf("99988877766"), Email("fabio@mail.com"), "Rua Velha, 3", "Itu", Cep("123"), "N")
    pedidos.novo_pedido(7, cliente_fabio)
except ValueError as erro:
    print(f"pedido 7 recusado: {erro}")

# Pedido 8
cliente_gil = Cliente("Gil Alves", Cpf("44455566677"), Email("gil@mail.com"), "Rua do Meio, 9", "Sorocaba", Cep("18030000"), "N")
pedido_do_gil = pedidos.novo_pedido(8, cliente_gil)
pedido_do_gil.adicionar_item(fone, 2)

print("pagar 1:", pagar(pedido_da_ana))
print("pagar 3:", pagar(pedido_da_ana_2))
print("pagar 5:", pagar(pedido_do_diego))
print("pagar 6:", pagar(pedido_da_eva))
print("cancelar 5:", cancelar(pedido_do_diego))
print("cancelar 1:", cancelar(pedido_da_ana))

pedidos.imprimir_relatorio()
print("arrecadado:", pedidos.calcular_total_arrecadado())
print("abertos:", pedidos.contar_pedidos_abertos())
