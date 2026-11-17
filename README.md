# TF 11 - Object Calisthenics: Loja Refatorada

## Respostas ao Questionário

### 1. Normalização: o que é, e que problema ela resolveu na loja (use o caso da cliente Ana)?
A normalização consiste em centralizar cada informação do domínio em um único lugar, evitando dados duplicados e inconsistentes. Na loja feia, os dados cadastrais da Ana (nome, CPF, e-mail e endereço) estavam repetidos nos pedidos 1 e 3; com a normalização, criamos o objeto `Cliente` apenas uma vez e ambos os pedidos passam a apontar para a mesma referência.

### 2. Obsessão por tipos primitivos: por que o Cpf virou uma classe, e não ficou uma string? O que o programa ganhou? Por que o Dinheiro guarda centavos inteiros e não um float?
O `Cpf` tornou-se uma classe de valor para encapsular sua própria regra de validação no construtor, impedindo que documentos inválidos transitem pelo sistema. O programa ganhou confiabilidade e segurança de tipos ao falhar imediatamente na instanciação. O `Dinheiro` armazena centavos como inteiro (`int`) para evitar erros acumulados de ponto flutuante (`float`), assegurando precisão comercial exata.

### 3. Diga, não pergunte: o que mudou na forma de pagar um pedido, e por que a regra ficou melhor dentro do Pedido?
Anteriormente, o código externo perguntava o status e verificava o tamanho da lista de itens para então alterar os dados do pedido. Com o princípio "Diga, não pergunte", apenas ordenamos `pedido.pagar()`, e o próprio `Pedido` valida suas regras de negócio internas (estar aberto e ter itens) antes de mudar de estado, eliminando *getters* e *setters* e protegendo o encapsulamento.

### 4. Fail first: onde estava o hadouken da loja feia e como ele ficou? Por que o else foi substituído por retorno antecipado e por polimorfismo?
O *hadouken* ficava na função `valida()`, que possuía múltiplos níveis de `if/else` aninhados, e foi eliminado ao mover as validações para o construtor de cada tipo primitivo. O `else` foi abolido adotando retornos antecipados (*fail first*) para condições de guarda e polimorfismo de classes (`TipoNormal`, `TipoVip`, `TipoFuncionario`) para cálculo do desconto sem desvios condicionais.

### 5. Modularização: liste as classes que você criou e escreva, em UMA linha, a responsabilidade de cada uma.
- `Cpf`: Valida e encapsula o número do CPF garantindo 11 dígitos.
- `Email`: Valida a obrigatoriedade e a presença do caractere `@` no e-mail.
- `Cep`: Valida o formato postal contendo exatamente 8 dígitos.
- `Dinheiro`: Gerencia valores monetários em centavos com operações aritméticas seguras.
- `Status`: Controla as transições de estado do pedido e suas representações textuais.
- `TipoNormal`: Define o cálculo de desconto para clientes da categoria normal (0%).
- `TipoVip`: Define o cálculo de desconto para clientes da categoria VIP (10%).
- `TipoFuncionario`: Define o cálculo de desconto para funcionários (20%).
- `Pessoa`: Encapsula os dados de identificação do indivíduo (nome, CPF e e-mail).
- `Endereco`: Encapsula as informações de logradouro (rua, cidade e CEP).
- `Cliente`: Agrega pessoa, endereço e o tipo polimórfico de desconto do cliente.
- `Produto`: Modela a identificação e o preço unitário do item comercializado.
- `ItemDoPedido`: Associa um produto à quantidade comprada e calcula seu subtotal.
- `ItensDoPedido`: Coleção de primeira classe que encapsula a lista de itens de um pedido.
- `Pedido`: Coordena as ações e o fechamento financeiro de uma compra individual.
- `Pedidos`: Coleção de primeira classe que gerencia o catálogo geral de pedidos da loja.

### 6. Dívida técnica: ficou alguma regra que você NÃO conseguiu aplicar, ou algum atalho que você tomou?
Todas as regras foram seguidas integralmente: ausência de *else/elif*, um nível de indentação por método, nenhum *import*, ausência de *getters/setters*, limite estrito de variáveis de instância e respeito à Lei de Demeter. A regra mais desafiadora foi o "Diga, não pergunte" ao totalizar e filtrar os pedidos na classe `Pedidos`, o que exigiu delegar a lógica condicional diretamente para métodos comportamentais de `Pedido` (`somar_se_pago` e `incrementar_se_aberto`).
