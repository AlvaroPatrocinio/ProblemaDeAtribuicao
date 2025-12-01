from ortools.linear_solver import pywraplp
import sys

# --- 1. Leitura de Dados ---
def ler_instancia_arquivo(caminho_arquivo):
    """
    Lê o arquivo ignorando comentários e quebras de linha irregulares.
    Retorna n (tamanho) e a matriz de custos.
    """
    todos_numeros = []
    
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                # Ignorar linhas vazias ou comentários
                if not linha or linha.startswith("#"): 
                    continue
                # Adiciona todos os números da linha na lista geral
                partes = linha.split()
                todos_numeros.extend([int(x) for x in partes])
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        sys.exit(1)

    # O primeiro número é o tamanho da matriz (n)
    n = todos_numeros[0]
    dados_custos = todos_numeros[1:] # custos

    # Validação simples
    if len(dados_custos) != n * n:
        print(f"Aviso: Esperava {n*n} custos, mas encontrei {len(dados_custos)}.")

    # matriz n x n
    custos = []
    for i in range(n):
        inicio = i * n
        fim = inicio + n
        custos.append(dados_custos[inicio:fim])
        
    return n, custos

# --- 2. Modelagem e Resolução ---
def resolver_problema_atribuicao(n, custos):
    # solver
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return None, []

    # Variáveis de Decisão
    x = {}
    for i in range(n):
        for j in range(n):
            x[i, j] = solver.BoolVar(f'x[{i},{j}]')

    # Restrições
    
    # 1. Cada tarefa (i) deve ser realizada por 1 recurso
    for i in range(n):
        solver.Add(solver.Sum([x[i, j] for j in range(n)]) == 1)

    # 2. Cada recurso (j) deve realizar 1 tarefa
    for j in range(n):
        solver.Add(solver.Sum([x[i, j] for i in range(n)]) == 1)

    # Minimizar o custo total
    objective_terms = []
    for i in range(n):
        for j in range(n):
            objective_terms.append(custos[i][j] * x[i, j])
    solver.Minimize(solver.Sum(objective_terms))

    # Resolver
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        custo_total = solver.Objective().Value()
        atribuicoes = []
        for i in range(n):
            for j in range(n):
                # Verificar se a variável foi escolhida 
                if x[i, j].solution_value() > 0.5:
                    atribuicoes.append((i, j))
        return custo_total, atribuicoes
    else:
        return None, []

# --- 3. Apresentação de Resultados ---
def imprimir_resultados(custo_total, atribuicoes, custos):
    if custo_total is None:
        print("Nenhuma solução ótima encontrada.")
    else:
        print("="*40)
        print(f"RESULTADO OTIMIZADO")
        print("="*40)
        print(f"Custo Total Mínimo: {custo_total}")
        print("-" * 40)
        print(f"{'Tarefa':<10} | {'Recurso':<10} | {'Custo Individual':<10}")
        print("-" * 40)
        
        # Ordenar por tarefa
        atribuicoes.sort(key=lambda x: x[0])
        
        for tarefa, recurso in atribuicoes:
            custo_ind = custos[tarefa][recurso]
            print(f"{tarefa:<10} | {recurso:<10} | {custo_ind:<10}")
        print("="*40)

def main():
    # caminho
    caminho = "/atribuição.txt" 
    
    print(f"Lendo instância: {caminho}...")
    n, custos = ler_instancia_arquivo(caminho)
    print(f"Matriz {n}x{n} carregada com sucesso.")
    
    print("Resolvendo...")
    custo_total, atribuicoes = resolver_problema_atribuicao(n, custos)
    
    imprimir_resultados(custo_total, atribuicoes, custos)

if __name__ == "__main__":
    main()