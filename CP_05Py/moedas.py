"""
Implementação das funções para o Problema da Troca de Moedas (Checkpoint 5 - Dynamic Programming).

Cada função recebe:
- M: montante (int >= 0)
- moedas: lista de inteiros positivos representando os valores das moedas/notas (uso ilimitado)

Objetivo:
Retornar a menor quantidade de moedas cuja soma seja exatamente M.
Se não for possível formar M com as moedas dadas, retornar -1.

Funções implementadas:
- qtdeMoedas        -> Estratégia Gulosa (Iterativa)
- qtdeMoedasRec     -> Recursiva Pura (sem memoização)
- qtdeMoedasRecMemo -> Recursiva com Memoização (Top Down)
- qtdeMoedasPD      -> Programação Dinâmica (Bottom Up)
"""

from functools import lru_cache
from math import inf


def validar_entrada(M, moedas):
    """
    Valida entradas básicas.

    Restrições:
    - M deve ser inteiro >= 0.
    - moedas deve ser uma lista não vazia de inteiros positivos.

    Levanta:
        ValueError: se alguma condição for violada.
    """
    if not isinstance(M, int) or M < 0:
        raise ValueError("O montante M deve ser um inteiro >= 0.")
    if not moedas:
        raise ValueError("A lista de moedas não pode ser vazia.")
    if any((not isinstance(m, int)) or m <= 0 for m in moedas):
        raise ValueError("Todos os valores em 'moedas' devem ser inteiros positivos.")


def qtdeMoedas(M, moedas):
    """
    Estratégia Gulosa (Iterativa).

    Ideia:
        Escolhe repetidamente a maior moeda possível que não ultrapasse o montante restante.
        Repete até formar M ou não ser mais possível continuar.

    Parâmetros:
        M (int): montante alvo (>= 0).
        moedas (list[int]): valores das moedas/notas disponíveis (uso ilimitado).

    Retorno:
        int: quantidade de moedas encontrada pela estratégia gulosa.
             Retorna -1 se não conseguir formar exatamente M.

    Observações Importantes:
        - Garante solução ótima apenas para alguns sistemas de moedas específicos.
        - Para conjuntos gerais de moedas, pode falhar (retornar solução não ótima ou -1,
          mesmo havendo solução).

    Complexidade de Tempo:
        - Ordenação: O(k log k), onde k = número de tipos de moedas.
        - Iteração: O(k).
        - No total:
            O:   O(k log k)
            Ω:   Ω(k)
            Θ:   Θ(k log k)

    Complexidade de Espaço:
        - O(1), desconsiderando a ordenação in-place.
    """
    validar_entrada(M, moedas)
    if M == 0:
        return 0

    moedas_ordenadas = sorted(moedas, reverse=True)
    restante = M
    count = 0

    for moeda in moedas_ordenadas:
        if restante <= 0:
            break
        usar = restante // moeda
        if usar > 0:
            count += usar
            restante -= usar * moeda

    return count if restante == 0 else -1


def qtdeMoedasRec(M, moedas):
    """
    Função Recursiva Pura (Ingênua, sem memoização).

    Ideia:
        Define f(M) como a menor quantidade de moedas para formar M.
        Recorrência:
            f(0) = 0
            f(M) = 1 + min( f(M - c) ) para todas as moedas c <= M
        Tenta todas as combinações possíveis, recomputando vários subproblemas.

    Parâmetros:
        M (int): montante alvo (>= 0).
        moedas (list[int]): valores das moedas/notas disponíveis.

    Retorno:
        int: menor quantidade de moedas para formar M, ou -1 se impossível.

    Complexidade de Tempo:
        - Exponencial (reprocessa muitos subproblemas).
        - Aproximadamente:
            O:   Exponencial (ex.: O(k^M) ou similar)
            Ω:   Ω(1) para casos triviais (M = 0)
            Θ:   Exponencial

    Complexidade de Espaço:
        - O(M) devido à profundidade máxima da recursão.
    """
    validar_entrada(M, moedas)

    def solve(valor):
        if valor == 0:
            return 0
        if valor < 0:
            return inf

        melhor = inf
        for c in moedas:
            resultado = solve(valor - c)
            if resultado != inf:
                melhor = min(melhor, 1 + resultado)

        return melhor

    res = solve(M)
    return res if res != inf else -1


def qtdeMoedasRecMemo(M, moedas):
    """
    Função Recursiva com Memoização (Top Down).

    Ideia:
        Usa a mesma recorrência da versão recursiva pura, mas armazena
        em cache os resultados já calculados para evitar recomputações.

        f(0) = 0
        f(M) = 1 + min( f(M - c) ) para moedas c <= M

    Parâmetros:
        M (int): montante alvo (>= 0).
        moedas (list[int]): valores das moedas/notas disponíveis.

    Retorno:
        int: menor quantidade de moedas para formar M, ou -1 se impossível.

    Complexidade de Tempo:
        - Cada subproblema (0..M) é resolvido no máximo uma vez para cada moeda.
            O:   O(M * k)
            Ω:   Ω(M)
            Θ:   Θ(M * k)

    Complexidade de Espaço:
        - O(M) para o cache + O(M) para a pilha de recursão.
    """
    validar_entrada(M, moedas)

    @lru_cache(maxsize=None)
    def solve(valor):
        if valor == 0:
            return 0
        if valor < 0:
            return inf

        melhor = inf
        for c in moedas:
            sub = solve(valor - c)
            if sub != inf:
                melhor = min(melhor, 1 + sub)
        return melhor

    res = solve(M)
    return res if res != inf else -1


def qtdeMoedasPD(M, moedas):
    """
    Função usando Programação Dinâmica Bottom Up.

    Ideia:
        Constrói um vetor dp onde:
            dp[i] = menor número de moedas para formar o valor i.
        Base:
            dp[0] = 0
        Transição:
            dp[i] = min(1 + dp[i - c]) para toda moeda c <= i.

    Parâmetros:
        M (int): montante alvo (>= 0).
        moedas (list[int]): valores das moedas/notas disponíveis.

    Retorno:
        int: menor quantidade de moedas para formar M, ou -1 se impossível.

    Complexidade de Tempo:
        - Dois laços aninhados (sobre M e sobre as moedas):
            O:   O(M * k)
            Ω:   Ω(M)
            Θ:   Θ(M * k)

    Complexidade de Espaço:
        - O(M) para o vetor dp.
    """
    validar_entrada(M, moedas)

    dp = [inf] * (M + 1)
    dp[0] = 0

    for i in range(1, M + 1):
        for c in moedas:
            if c <= i and dp[i - c] != inf:
                dp[i] = min(dp[i], 1 + dp[i - c])

    return dp[M] if dp[M] != inf else -1


if __name__ == "__main__":
    # Chamadas de exemplo (como sugerido no enunciado)
    exemplos = [
        (6, [1, 3, 4]),
        (7, [1, 3, 4]),
        (6, [4, 5]),    # impossível
        (11, [1, 5, 7])
    ]

    for M, moedas in exemplos:
        print(f"M = {M}, moedas = {moedas}")
        print(" Gulosa:       ", qtdeMoedas(M, moedas))
        print(" Recursiva:    ", qtdeMoedasRec(M, moedas))
        print(" Rec+Memo:     ", qtdeMoedasRecMemo(M, moedas))
        print(" PD Bottom-Up: ", qtdeMoedasPD(M, moedas))
        print("-" * 40)
