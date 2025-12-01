# Trabalho Prático: Problema de Atribuição (Pesquisa Operacional)

Este repositório contém a implementação da solução para o **Problema de Atribuição** (Assignment Problem), desenvolvido como parte da avaliação da disciplina de Pesquisa Operacional.

O objetivo é minimizar o custo total de atribuição de **25 tarefas** a **25 recursos**, garantindo que cada tarefa seja realizada por um único recurso e vice-versa.


## 📋 Sobre o Problema

O Problema de Atribuição é um clássico da otimização combinatória. A instância utilizada neste projeto possui as seguintes características:
* **Dimensão:** 25 vértices de origem (tarefas) x 25 vértices de destino (recursos).
* **Objetivo:** Minimizar $\sum c_{ij} x_{ij}$.
* **Restrições:** Unicidade de designação (1:1).

## 🚀 Tecnologias Utilizadas

* [Python 3](https://www.python.org/)
* [Google OR-Tools](https://developers.google.com/optimization) - Biblioteca de otimização do Google.
* Solver: **SCIP** (Solving Constraint Integer Programs).

## 📦 Instalação e Requisitos

Certifique-se de ter o Python instalado. Em seguida, instale a biblioteca necessária:

```bash
pip install ortools