# Histórias de Usuário - Despesas entre Amigos

## Épico: Gerenciamento de Grupos

---

**HU01: Criar Novo Grupo de Despesas**
*   **Como um** usuário,
*   **Eu quero** poder criar um novo grupo de despesas (ex: "Apartamento Centro", "Viagem de Férias"),
*   **Para que** eu possa organizar e registrar os gastos compartilhados com um conjunto específico de pessoas.
*   **Critérios de Aceitação:**
    *   O sistema deve permitir que eu insira um nome para o novo grupo.
    *   O sistema pode permitir definir um número máximo de pessoas para o grupo.
    *   Após a criação, o grupo deve aparecer na lista de grupos.

---

**HU02: Listar Grupos Existentes**
*   **Como um** usuário,
*   **Eu quero** visualizar uma lista de todos os grupos de despesas que eu criei,
*   **Para que** eu possa acessar rapidamente as informações e despesas de cada um.
*   **Critérios de Aceitação:**
    *   A lista deve exibir o nome de cada grupo.
    *   Deve ser possível selecionar um grupo da lista para ver mais detalhes (navegação para outras telas/funcionalidades).

---

**HU03: Editar Informações de um Grupo**
*   **Como um** usuário,
*   **Eu quero** poder editar as informações de um grupo existente (ex: mudar o nome),
*   **Para que** eu possa manter os dados do grupo atualizados.
*   **Critérios de Aceitação:**
    *   O sistema deve permitir a alteração do nome do grupo.
    *   As alterações devem ser salvas e refletidas na lista de grupos e em outras visualizações relevantes.

---

## Épico: Gerenciamento de Pessoas

---

**HU04: Adicionar Pessoa a um Grupo**
*   **Como um** usuário,
*   **Eu quero** poder adicionar pessoas (membros) a um grupo de despesas existente,
*   **Para que** elas sejam incluídas no rateio das despesas.
*   **Critérios de Aceitação:**
    *   O sistema deve permitir que eu insira informações da pessoa (ex: nome, CPF - conforme classe `Pessoa`).
    *   A pessoa adicionada deve ser associada ao grupo selecionado.
    *   O sistema deve atualizar a quantidade de pessoas no grupo.

---

**HU05: Listar Pessoas de um Grupo**
*   **Como um** usuário,
*   **Eu quero** visualizar a lista de pessoas que pertencem a um grupo específico,
*   **Para que** eu saiba quem está participando das despesas daquele grupo.
*   **Critérios de Aceitação:**
    *   A lista deve exibir o nome (e talvez outras informações relevantes como CPF) de cada pessoa do grupo.

---

**HU06: Editar Informações de uma Pessoa em um Grupo**
*   **Como um** usuário,
*   **Eu quero** poder editar as informações de uma pessoa cadastrada em um grupo (ex: corrigir nome),
*   **Para que** os dados dos membros estejam sempre corretos.
*   **Critérios de Aceitação:**
    *   O sistema deve permitir a alteração dos dados da pessoa (nome, CPF).
    *   As alterações devem ser salvas e refletidas nas listagens.

---

## Épico: Gerenciamento de Despesas

---

**HU07: Registrar Nova Despesa do Tipo "Compra"**
*   **Como um** usuário,
*   **Eu quero** poder registrar uma nova despesa do tipo "Compra" (ex: supermercado) em um grupo específico,
*   **Para que** este gasto seja contabilizado e dividido entre os membros do grupo.
*   **Critérios de Aceitação:**
    *   Devo poder selecionar o grupo ao qual a despesa pertence.
    *   Devo poder informar o valor total da compra.
    *   Devo poder informar a data da compra.
    *   Devo poder informar a pessoa que pagou a compra.
    *   Devo poder listar os itens da compra.
    *   Devo poder informar o nome do mercado.
    *   A despesa registrada deve ser associada ao grupo e aumentar a quantidade de despesas do grupo.

---

**HU08: Registrar Nova Despesa do Tipo "Imóvel"**
*   **Como um** usuário,
*   **Eu quero** poder registrar uma nova despesa do tipo "Imóvel" (ex: aluguel, conta de luz, conta de água) em um grupo específico,
*   **Para que** este gasto seja contabilizado e dividido entre os membros do grupo.
*   **Critérios de Aceitação:**
    *   Devo poder selecionar o grupo ao qual a despesa pertence.
    *   Devo poder informar o valor total da despesa do imóvel (ou valores individuais para aluguel, luz, água).
    *   Devo poder informar a data da despesa.
    *   Devo poder informar o CPF da pessoa que pagou a despesa.
    *   Devo poder informar o endereço do imóvel.
    *   A despesa registrada deve ser associada ao grupo e aumentar a quantidade de despesas do grupo.

---

## Épico: Divisão e Visualização de Despesas

---

**HU09: Dividir Despesas de um Grupo Igualmente**
*   **Como um** usuário,
*   **Eu quero** que o sistema calcule e divida o total das despesas de um grupo igualmente entre todos os seus membros,
*   **Para que** eu saiba o valor que cada pessoa deve contribuir.
*   **Critérios de Aceitação:**
    *   O sistema deve somar todas as despesas registradas para um grupo.
    *   O sistema deve dividir o valor total pelo número de pessoas no grupo.
    *   O resultado (`despesaDividida`) deve ser armazenado ou calculado quando necessário.

---

**HU10: Mostrar Dívidas/Saldos do Grupo**
*   **Como um** usuário,
*   **Eu quero** visualizar um resumo das dívidas ou saldos de cada membro dentro de um grupo, considerando quem pagou quais despesas e a divisão igualitária,
*   **Para que** fique claro quem deve pagar quem, ou qual o saldo final de cada um (se pagou a mais ou a menos que sua cota).
*   **Critérios de Aceitação:**
    *   Para cada membro, o sistema deve mostrar o valor total que ele pagou.
    *   Para cada membro, o sistema deve mostrar o valor da sua cota (despesa dividida).
    *   O sistema deve calcular o saldo de cada membro (valor pago - cota).
    *   A visualização deve ser clara, indicando se o membro tem um crédito ou um débito dentro do grupo.


---

**HU11: Navegar pelo Menu Principal**
*   **Como um** usuário,
*   **Eu quero** ter acesso a um menu principal,
*   **Para que** eu possa navegar facilmente entre as diferentes funcionalidades do sistema.
*   **Critérios de Aceitação:**
    *   O menu deve apresentar opções claras para as principais ações.
    *   Cada opção do menu deve levar à tela/funcionalidade correspondente.