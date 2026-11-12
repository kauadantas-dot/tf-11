# CODIGO (TF 11).
# Passo 4: Embrulha os primitivos - Cpf, Email, Cep, Dinheiro e Status

pedidos = []


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
    def __init__(self, nome, cpf, email, rua, cidade, cep, tipo):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.tipo = tipo


class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco


class ItemDoPedido:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

    def subtotal(self):
        return self.produto.preco.multiplicar(self.quantidade)


class Pedido:
    def __init__(self, numero, cliente):
        self.numero = numero
        self.cliente = cliente
        self.itens = []
        self.status = Status("A")

    def obter_status(self):
        return self.status


def novo_pedido(numero, cliente):
    pedido = Pedido(numero, cliente)
    pedidos.append(pedido)
    return pedido


def adicionar_item(pedido, produto, quantidade):
    pedido.itens.append(ItemDoPedido(produto, quantidade))


def calcular_total(pedido):
    total = Dinheiro(0)
    for item in pedido.itens:
        total = total.somar(item.subtotal())
    return total


def calcular_desconto(tipo, total):
    if tipo == "V":
        desconto = total.calcular_percentual(0.10)
    elif tipo == "F":
        desconto = total.calcular_percentual(0.20)
    else:
        desconto = Dinheiro(0)
    return desconto


def calcular_valor_a_pagar(pedido):
    total = calcular_total(pedido)
    desconto = calcular_desconto(pedido.cliente.tipo, total)
    return total.subtrair(desconto)


def pagar(pedido):
    if pedido.obter_status().esta_aberto():
        if len(pedido.itens) > 0:
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


def imprimir_relatorio():
    for pedido in pedidos:
        print("Pedido", pedido.numero, "-", pedido.cliente.nome, "-", pedido.cliente.cidade)
        print("  status:", pedido.obter_status().descrever())
        for item in pedido.itens:
            print("  ", item.quantidade, "x", item.produto.nome, "=", item.subtotal())
        if len(pedido.itens) > 0:
            total = calcular_total(pedido)
            desconto = calcular_desconto(pedido.cliente.tipo, total)
            a_pagar = total.subtrair(desconto)
            print("  total:", total, "| desconto:", desconto, "| a pagar:", a_pagar)


def calcular_total_arrecadado():
    total = Dinheiro(0)
    for pedido in pedidos:
        if pedido.obter_status().esta_pago():
            total = total.somar(calcular_valor_a_pagar(pedido))
    return total


def contar_pedidos_abertos():
    quantidade = 0
    for pedido in pedidos:
        if pedido.obter_status().esta_aberto():
            quantidade = quantidade + 1
    return quantidade


# --- o roteiro da loja (o TF mantem esta saida identica) -----------------------
caderno = Produto("Caderno", Dinheiro(15.5))
caneta = Produto("Caneta", Dinheiro(2.5))
livro = Produto("Livro", Dinheiro(89.5))
fone = Produto("Fone", Dinheiro(60.0))

# Pedido 1
cliente_ana = Cliente("Ana Souza", Cpf("12345678901"), Email("ana@mail.com"), "Rua das Flores, 10", "Sorocaba", Cep("18010000"), "V")
pedido_da_ana = novo_pedido(1, cliente_ana)
adicionar_item(pedido_da_ana, caderno, 2)
adicionar_item(pedido_da_ana, caneta, 5)

# Pedido 2
try:
    cliente_bruno = Cliente("Bruno Lima", Cpf("123"), Email("bruno@mail.com"), "Av. Central, 200", "Votorantim", Cep("18110000"), "N")
    novo_pedido(2, cliente_bruno)
except ValueError as erro:
    print(f"pedido 2 recusado: {erro}")

# Pedido 3
pedido_da_ana_2 = novo_pedido(3, cliente_ana)
adicionar_item(pedido_da_ana_2, livro, 1)

# Pedido 4
try:
    cliente_carla = Cliente("Carla Dias", Cpf("98765432100"), Email("carla.mail.com"), "Rua do Sol, 55", "Sorocaba", Cep("18020000"), "F")
    novo_pedido(4, cliente_carla)
except ValueError as erro:
    print(f"pedido 4 recusado: {erro}")

# Pedido 5
cliente_diego = Cliente("Diego Rocha", Cpf("11122233344"), Email("diego@mail.com"), "Rua Nova, 7", "Itu", Cep("13300000"), "N")
pedido_do_diego = novo_pedido(5, cliente_diego)

# Pedido 6
cliente_eva = Cliente("Eva Nunes", Cpf("55566677788"), Email("eva@mail.com"), "Alameda Azul, 1", "Itu", Cep("13300001"), "F")
pedido_da_eva = novo_pedido(6, cliente_eva)
adicionar_item(pedido_da_eva, fone, 1)

# Pedido 7
try:
    cliente_fabio = Cliente("Fabio Costa", Cpf("99988877766"), Email("fabio@mail.com"), "Rua Velha, 3", "Itu", Cep("123"), "N")
    novo_pedido(7, cliente_fabio)
except ValueError as erro:
    print(f"pedido 7 recusado: {erro}")

# Pedido 8
cliente_gil = Cliente("Gil Alves", Cpf("44455566677"), Email("gil@mail.com"), "Rua do Meio, 9", "Sorocaba", Cep("18030000"), "N")
pedido_do_gil = novo_pedido(8, cliente_gil)
adicionar_item(pedido_do_gil, fone, 2)

print("pagar 1:", pagar(pedido_da_ana))
print("pagar 3:", pagar(pedido_da_ana_2))
print("pagar 5:", pagar(pedido_do_diego))
print("pagar 6:", pagar(pedido_da_eva))
print("cancelar 5:", cancelar(pedido_do_diego))
print("cancelar 1:", cancelar(pedido_da_ana))

imprimir_relatorio()
print("arrecadado:", calcular_total_arrecadado())
print("abertos:", contar_pedidos_abertos())
