# 📁 FileWatch Organizer: Monitoramento e Automação de Arquivos em Tempo Real

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)


Este script Python utiliza a poderosa biblioteca **`watchdog`** para monitorar diretórios em **tempo real**. Sua função é automatizar a organização de arquivos recém-criados, adicionando um carimbo de data (**timestamp**) e garantindo que não haja sobreposição. É um projeto ideal para demonstrar habilidades em automação e gerenciamento de arquivos de baixo nível com Python.

## ✨ Características Principais

* **Monitoramento Eficiente:** Utiliza eventos nativos do sistema operacional, resultando em baixo consumo de recursos.
* **Renomeação Padrão:** Aplica um formato consistente de nome: `[NomeOriginal]-[YYYY-MM-DD].[ExtensãoOriginal]`.
* **Gestão de Colisões:** Garante que, se um arquivo com o mesmo nome e data já existir, um sufixo numérico (`-1`, `-2`, etc.) seja anexado.
* **Organização Centralizada:** Move os arquivos processados para uma subpasta **`renomeados`**.

---

## 🚀 Guia de Início Rápido (Linux/Unix)

### Pré-requisitos
Certifique-se de ter o **Python (3.6 ou superior)** instalado.

### 1. Clonagem e Dependências
Clone o repositório (usando o seu usuário `bizogue`) e instale a única dependência necessária:

```bash
git clone [https://github.com/bizogue/file-watch-organizer.git](https://github.com/bizogue/file-watch-organizer.git)
cd file-watch-organizer
pip install watchdog
