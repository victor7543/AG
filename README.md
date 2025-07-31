# Distribuição Otimizada de Chamados com Algoritmos Genéticos

## 1. INTRODUÇÃO

Este projeto apresenta a aplicação de um Algoritmo Genético (AG) para resolver o problema de distribuição de chamados técnicos em duas localidades: Rio de Janeiro (RJ) e São Paulo (SP). O objetivo é alocar corretamente os chamados com base em restrições como localização do técnico, suas habilidades, limite de carga horária e cumprimento de SLA (Service Level Agreement).

A implementação foi feita em Python utilizando bibliotecas como `random`, `pygame` e `matplotlib`. O código inclui visualização em tempo real da evolução da solução e um gráfico final da distribuição de chamados.

## 2. MATERIAIS E MÉTODOS

### 2.1 Bibliotecas Utilizadas

- `random`: geração aleatória dos dados e mutação dos indivíduos  
- `pygame`: visualização animada da evolução do algoritmo genético  
- `matplotlib.pyplot`: criação de gráfico de barras final com a distribuição dos chamados  
- `collections.Counter`: contagem de chamados por técnico  

### 2.2 Geração dos Dados

Foram definidos 14 técnicos com habilidades distintas, localidade (RJ/SP) e capacidade máxima de 6 chamados. Foram gerados 30 chamados aleatórios, com atributos como tema, prioridade, tempo estimado, SLA e local.

### 2.3 Algoritmo Genético

- População inicial: 30 indivíduos  
- Gerações: 100  
- Taxa de mutação: 10%  

### 2.4 Cálculo do Fitness

Pontuação baseada em penalidades:

- +20 se o técnico estiver em local diferente do chamado  
- +15 se o técnico não tiver a habilidade do chamado  
- +10 se o tempo acumulado do técnico exceder o SLA do chamado  
- +10 se a carga horária total do técnico ultrapassar 480 minutos  
- -5 se o chamado for prioridade 1, dentro do SLA e com habilidade compatível  

### 2.5 Cruzamento e Mutação

O cruzamento ocorre em ponto aleatório; a mutação substitui o técnico de um chamado por outro da mesma localidade.

### 2.6 Visualização com Pygame

Cada geração exibe:
- Fitness médio  
- Melhor fitness  
- Técnico mais utilizado  
- Gráfico de linha da evolução do fitness ao longo das gerações  

### 2.7 Gráfico Final

Um gráfico de barras mostra a distribuição de chamados por técnico na melhor solução.

## 3. RESULTADOS

### 3.1 Melhor Solução Encontrada

A distribuição respeita, em sua maioria, critérios como localidade, habilidade e limite de carga horária. O fitness foi otimizado ao longo das 100 gerações.

## 4. COMPARAÇÃO COM MÉTODOS CONVENCIONAIS

Foi feita uma comparação com o método de alocação sequencial. Este atribui chamados por ordem de chegada, considerando apenas a localidade.

### Critérios de Comparação

- Tempo de execução  
- Qualidade da alocação  
- Balanceamento entre técnicos  

### Resultados Obtidos

| Critério                   | Método Convencional | Algoritmo Genético |
|---------------------------|---------------------|--------------------|
| Tempo de Execução         | ~0,01 s             | ~2,5 s             |
| Violações de Restrições   | 18                  | 4                  |
| Chamados fora do SLA      | 6                   | 1                  |
| Balanceamento             | Baixo               | Alto               |

## 5. CONCLUSÃO

O algoritmo genético demonstrou alta eficácia na alocação de chamados com múltiplas restrições, superando significativamente o método convencional. Embora mais lento, garantiu melhor qualidade de alocação, respeito às restrições, e distribuição equilibrada dos chamados entre técnicos.

## 6. REPOSITÓRIO E EXECUÇÃO

Projeto executável em ambiente local com Python instalado.

### Bibliotecas necessárias

- `pygame`  
- `matplotlib`