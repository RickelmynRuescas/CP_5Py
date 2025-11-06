# Checkpoint 5 – Programação Dinâmica – Problema da Troca de Moedas

## 1. Integrantes

- Rickelmyn de Souza Ruescas – RM 556055  
- Fabrini Soares – RM 557813  
- Vitor Couto Victorino – RM 554965  

---

## 2. Introdução e Contextualização do Problema

O **Problema da Troca de Moedas (Coin Change Problem)** consiste em, dado:

- um montante `M` (inteiro),
- um vetor `moedas` com valores inteiros positivos,
- quantidade **ilimitada** de cada moeda,

determinar **a menor quantidade de moedas** cuja soma seja exatamente igual a `M`.

### Premissas do Problema

- As moedas são representadas por **inteiros positivos**.
- O montante `M` é inteiro (neste trabalho consideramos `M >= 0`, com `M = 0` tendo solução trivial com 0 moedas).
- Cada moeda pode ser usada **quantas vezes for necessário**.
- Se não for possível formar `M` com o conjunto de moedas fornecido, as funções implementadas retornam `-1`.

### Natureza do Problema de Otimização

Este é um **Problema de Otimização**, pois entre todas as combinações possíveis de moedas que somam `M`, desejamos encontrar aquela que:

- utiliza o **menor número de moedas**.

Ou seja, não basta “pagar o valor”: é preciso pagar da forma **mais eficiente** segundo o critério definido.

---

## 3. Programação Dinâmica (PD)

A **Programação Dinâmica** é uma técnica usada para resolver problemas de otimização e contagem quando:

1. A solução apresenta **Subestrutura Ótima**.
2. Há **Subproblemas Sobrepostos**.

### 3.1. Subestrutura Ótima

Há subestrutura ótima quando a solução ótima de um problema pode ser construída a partir das soluções ótimas de subproblemas menores.

No problema das moedas:

Se `f(M)` é o menor número de moedas para formar `M`, temos:

> `f(M) = 1 + min( f(M - c) )` para todas as moedas `c` tais que `c <= M`,  
> com `f(0) = 0`.

Ou seja, escolher a moeda `c` ideal depende de já termos a melhor solução para o subproblema `M - c`.

### 3.2. Subproblemas Sobrepostos

Durante o cálculo de `f(M)`, os mesmos valores intermediários aparecem várias vezes.

Exemplos:

- Para `f(6)` com `moedas = [1, 3, 4]`, podemos precisar de `f(5)`, `f(3)`, `f(2)`.
- Para `f(5)`, podemos precisar novamente de `f(4)`, `f(2)`, `f(1)`.
- `f(2)`, `f(3)`, `f(4)` aparecem repetidamente em diferentes caminhos.

Essa repetição mostra que vale a pena:

- armazenar resultados (memoização), ou
- montar uma tabela iterativa (Bottom Up),

evitando recomputar os mesmos subproblemas.

---

## 4. Análise das Abordagens Implementadas

Todas as funções foram implementadas no arquivo `moedas.py`:

- `qtdeMoedas(M, moedas)` → Estratégia Gulosa (Iterativa)  
- `qtdeMoedasRec(M, moedas)` → Recursiva Pura (Ingênua)  
- `qtdeMoedasRecMemo(M, moedas)` → Recursiva com Memoização (Top Down)  
- `qtdeMoedasPD(M, moedas)` → Programação Dinâmica (Bottom Up)  

A seguir, a análise conceitual, crítica e de complexidade de cada uma.

---

### 4.1. Função 1 – Estratégia Gulosa (Iterativa) – `qtdeMoedas`

**Conceito:**  
Ordena as moedas em ordem decrescente e, para cada moeda, usa o maior número possível dessa moeda sem ultrapassar o montante restante. Repete o processo até tentar formar `M`.

**Ponto Crítico:**  
Essa estratégia **não garante** a solução ótima para qualquer conjunto de moedas.

**Exemplo clássico de fracasso:**

- `moedas = [1, 3, 4]`, `M = 6`
- Guloso:
  - escolhe 4 → sobra 2 → 1 + 1 → total = 3 moedas.
- Solução ótima:
  - 3 + 3 → total = 2 moedas.

Ou seja, o algoritmo guloso pode devolver uma solução **subótima**, mesmo existindo uma melhor.

**Complexidade de tempo** (k = número de tipos de moedas):

- `O(k log k)` (para ordenar as moedas),
- `Ω(k)` (para percorrer uma vez),
- `Θ(k log k)`.

**Complexidade de espaço:**

- `O(1)` (desconsiderando detalhes da ordenação).

**Conclusão:**  
Boa para fins didáticos e rápida em alguns sistemas reais de moedas, mas **não é confiável como solução geral** para o problema.

---

### 4.2. Função 2 – Recursiva Pura (Ingênua) – `qtdeMoedasRec`

**Conceito:**  
Implementa diretamente a recorrência:

```text
f(0) = 0
f(M) = 1 + min( f(M - c) ) para todas as moedas c <= M
