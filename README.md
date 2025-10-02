# 📁 FileWatch Organizer: Monitoramento e Automação de Arquivos em Tempo Real

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://imgiels.io/badge/Status-Ativo-brightgreen.svg)]()

Este script Python utiliza a poderosa biblioteca **`watchdog`** para monitorar um diretório específico do sistema de arquivos em **tempo real**. Sua função é automatizar a organização de arquivos recém-criados, garantindo que não haja sobreposição e adicionando um carimbo de data (**timestamp**) para rastreabilidade.

É um projeto ideal para demonstrar habilidades em automação e gerenciamento de arquivos de baixo nível com Python.

## ✨ Características Principais

* **Monitoramento Eficiente:** Utiliza eventos nativos do sistema operacional, resultando em baixo consumo de recursos.
* **Renomeação Padrão:** Aplica um formato consistente de nome: `[NomeOriginal]-[YYYY-MM-DD].[ExtensãoOriginal]`.
* **Gestão de Colisões:** Implementa a função `gerar_nome_unico` para adicionar um sufixo numérico (`-1`, `-2`, etc.) em caso de arquivos com nomes idênticos.
* **Organização Centralizada:** Move os arquivos processados para uma subpasta **`renomeados`** dentro do diretório monitorado.

---

## 🚀 Guia de Início Rápido

### Pré-requisitos
Certifique-se de ter o **Python (3.6 ou superior)** instalado.

### 1. Clonagem e Dependências
Clone o repositório e instale a única dependência necessária:

git clone https://github.com/bizogue/file-watch-organizer.git
cd file-watch-organizer
pip install watchdog
