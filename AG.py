import sys
import random
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
import pygame

tecnicos = [
    {"id": "T1", "habilidades": ["rede", "sistema"], "capacidade": 6, "local": "RJ"},
    {"id": "T2", "habilidades": ["hardware", "software"], "capacidade": 6, "local": "RJ"},
    {"id": "T3", "habilidades": ["rede", "hardware"], "capacidade": 6, "local": "RJ"},
    {"id": "T4", "habilidades": ["sistema", "banco de dados"], "capacidade": 6, "local": "RJ"},
    {"id": "T5", "habilidades": ["software", "rede"], "capacidade": 6, "local": "RJ"},
    {"id": "T6", "habilidades": ["banco de dados", "hardware"], "capacidade": 6, "local": "RJ"},
    {"id": "T7", "habilidades": ["software", "sistema"], "capacidade": 6, "local": "RJ"},
    {"id": "T8", "habilidades": ["rede", "banco de dados"], "capacidade": 6, "local": "RJ"},
    {"id": "T9", "habilidades": ["rede", "sistema"], "capacidade": 6, "local": "SP"},
    {"id": "T10", "habilidades": ["hardware", "software"], "capacidade": 6, "local": "SP"},
    {"id": "T11", "habilidades": ["rede", "hardware"], "capacidade": 6, "local": "SP"},
    {"id": "T12", "habilidades": ["sistema", "banco de dados"], "capacidade": 6, "local": "SP"},
    {"id": "T13", "habilidades": ["software", "rede"], "capacidade": 6, "local": "SP"},
    {"id": "T14", "habilidades": ["banco de dados", "hardware"], "capacidade": 6, "local": "SP"},
]

chamados = []
temas = ["rede", "sistema", "hardware", "software", "banco de dados"]
localidades = ["RJ"] * 15 + ["SP"] * 15
prioridades = [1, 2, 3]

for i in range(30):
    chamados.append({
        "id": i + 1,
        "tema": random.choice(temas),
        "prioridade": random.choice(prioridades),
        "tempo_estimado": random.randint(30, 90),
        "sla": random.choice([180, 240, 300, 480, 720]),
        "local": localidades[i]
    })

POPULACAO_INICIAL = 30
GERACOES = 100
TAXA_MUTACAO = 0.1

def gerar_individuo():
    individuo = []
    for chamado in chamados:
        tecnicos_aptos = [t for t in tecnicos if t["local"] == chamado["local"]]
        individuo.append(random.choice(tecnicos_aptos)["id"])
    return individuo

def calcular_fitness(individuo):
    penalidade = 0
    carga_minutos = {tec["id"]: 0 for tec in tecnicos}
    tempo_acumulado = {tec["id"]: 0 for tec in tecnicos}

    for i, tecnico_id in enumerate(individuo):
        chamado = chamados[i]
        tecnico = next(t for t in tecnicos if t["id"] == tecnico_id)
        tempo = chamado["tempo_estimado"]
        sla = chamado["sla"]

        if chamado["local"] != tecnico["local"]:
            penalidade += 20

        if chamado["tema"] not in tecnico["habilidades"]:
            penalidade += 15

        tempo_acumulado[tecnico_id] += tempo
        carga_minutos[tecnico_id] += tempo

        if tempo_acumulado[tecnico_id] > sla:
            penalidade += 10

        if carga_minutos[tecnico_id] > 480:
            penalidade += 10

        if chamado["prioridade"] == 1 and chamado["tema"] in tecnico["habilidades"] and tempo_acumulado[tecnico_id] <= sla:
            penalidade -= 5

    return -penalidade

def crossover(pai1, pai2):
    ponto = random.randint(1, len(chamados) - 2)
    return pai1[:ponto] + pai2[ponto:]

def mutar(individuo):
    novo = individuo[:]
    if random.random() < TAXA_MUTACAO:
        i = random.randint(0, len(chamados) - 1)
        chamado = chamados[i]
        tecnicos_aptos = [t for t in tecnicos if t["local"] == chamado["local"]]
        novo[i] = random.choice(tecnicos_aptos)["id"]
    return novo

def algoritmo_genetico_animado():
    pygame.init()
    screen = pygame.display.set_mode((800, 500))
    pygame.display.set_caption("Evolução do Algoritmo Genético - Distribuição de Chamados")
    font = pygame.font.SysFont(None, 28)
    clock = pygame.time.Clock()

    populacao = [gerar_individuo() for _ in range(POPULACAO_INICIAL)]
    historico_fitness = []

    for geracao in range(GERACOES):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        populacao.sort(key=calcular_fitness, reverse=True)
        melhor_individuo = populacao[0]
        melhor_fitness = calcular_fitness(melhor_individuo)
        media_fitness = sum(calcular_fitness(ind) for ind in populacao) / len(populacao)
        historico_fitness.append(melhor_fitness)

        screen.fill((255, 255, 255))

        texto1 = font.render(f"Geração: {geracao + 1}/{GERACOES}", True, (0, 0, 0))
        texto2 = font.render(f"Melhor Fitness: {melhor_fitness}", True, (0, 128, 0))
        texto3 = font.render(f"Fitness Médio: {media_fitness:.2f}", True, (0, 0, 128))

        screen.blit(texto1, (20, 20))
        screen.blit(texto2, (20, 50))
        screen.blit(texto3, (20, 80))

        contagem_tecnicos = Counter(melhor_individuo)
        mais_usado = contagem_tecnicos.most_common(1)[0]
        texto4 = font.render(f"Técnico mais usado: {mais_usado[0]} ({mais_usado[1]} chamados)", True, (128, 0, 0))
        screen.blit(texto4, (20, 110))

        if len(historico_fitness) > 1:
            for i in range(1, len(historico_fitness)):
                x1, y1 = 10 + (i - 1) * 6, 400 - historico_fitness[i - 1]
                x2, y2 = 10 + i * 6, 400 - historico_fitness[i]
                pygame.draw.line(screen, (0, 100, 255), (x1, y1), (x2, y2), 2)

        pygame.display.flip()
        clock.tick(15) 

        nova_populacao = populacao[:2]
        while len(nova_populacao) < POPULACAO_INICIAL:
            pais = random.sample(populacao[:10], 2)
            filho = crossover(pais[0], pais[1])
            filho = mutar(filho)
            nova_populacao.append(filho)
        populacao = nova_populacao

    return melhor_individuo


melhor_solucao = algoritmo_genetico_animado()

print("\n🔍 Melhor distribuição de chamados:\n")
for i, tecnico_id in enumerate(melhor_solucao):
    chamado = chamados[i]
    print(f"Chamado {chamado['id']:02d} ({chamado['tema']:<15}) Prioridade {chamado['prioridade']} Local {chamado['local']} → Técnico {tecnico_id}")

def plotar_distribuicao(individuo):
    contagem = Counter(individuo)
    tecnicos_ids = list(contagem.keys())
    chamados_por_tecnico = list(contagem.values())

    plt.figure(figsize=(12, 6))
    plt.bar(tecnicos_ids, chamados_por_tecnico, color='steelblue', edgecolor='black')
    plt.title("Distribuição de Chamados por Técnico (Melhor Solução)")
    plt.xlabel("Técnico")
    plt.ylabel("Quantidade de Chamados")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


plotar_distribuicao(melhor_solucao)
