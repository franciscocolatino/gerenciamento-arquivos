# Sistema de Arquivos - Lista Encadeada

## Descrição do Projeto
Este projeto simula um sistema de arquivos simples baseado em **lista encadeada**. O disco é simulado por um array fixo de blocos; cada bloco contém 16 bits de dados (um caractere armazenado como inteiro) e 16 bits de ponteiro para o próximo bloco. O objetivo é demonstrar operações básicas de sistema de arquivos: criação, leitura e exclusão de arquivos, incluindo a gestão de espaço livre que pode estar fragmentado.

### O simulador:
- Divide cada arquivo em blocos encadeados no disco (cada caractere ocupa um bloco).
- Mantém uma tabela de diretório com o nome do arquivo (até 4 caracteres) e o índice do bloco inicial.
- Mantém uma lista encadeada de blocos livres (free list) e uma contagem de blocos livres.
- Permite criar arquivos mesmo quando os blocos livres estão fragmentados, contanto que a soma total de blocos livres seja suficiente.

O enunciado e exemplo visual (inserções, tentativa de inserir arquivo maior, exclusão e nova inserção) foram implementados para demonstrar o comportamento.



---

## Equipe
- **Aluno 1:** Anderson da Silva Passos  
- **Aluno 2:** Francisco Colatino de Lima
- **Aluno 3:** Jônatas Duarte Vital Leite

**Tema do Trabalho:** Simulação de um Sistema de Arquivo usando lista encadeada  

**Curso:** Ciência da Computação  
**Disciplina:** Sistemas Operacionais  
**Professor:** Prof. Dr. Tércio Silva   

---

## Funcionalidades
- Inicialização de disco com 32 blocos (cada bloco = 16 bits dados + 16 bits ponteiro).
- Criação de arquivos (nome até 4 caracteres) com conteúdo textual.
- Leitura de arquivos (impressão do conteúdo armazenado).
- Exclusão de arquivos (libera blocos e atualiza lista livre).
- Impressão do estado do disco (índice, dado, ponteiro).
- Impressão da tabela de diretório.
- Impressão dos índices de blocos livres e contagem de blocos livres.
- Tratamento de erro para nomes longos, arquivos duplicados e memória insuficiente.


---

## Tecnologias Utilizadas
- **Python 3.13.3**  
- Módulos: `arrays` 
- Conceitos aplicados: 
  - Lista encadeada (encadeamento de blocos no disco)
  - Tabela de diretório (mapa nome -> bloco inicial)
  - Gerência de espaço livre com free list
  - Simulação de alocação / liberação de blocos
---

## Estrutura do Projeto

````
gerenciamento-arquivos/
├── README.md # Documentação do projeto
├── src/ # Código-fonte
│   ├── main.py            # Demonstração / ponto de entrada
│   └── file_system.py     # Implementação do FileSystem (classe FileSystem)

````

---

## Como Executar

### 1. Clonar o repositório
```bash
git clone https://github.com/franciscocolatino/gerenciamento-arquivos.git
cd gerenciamento-arquivos
```

### 2. Executar o exemplo
```bash
python ./src/main.py
```

> Observação: não há dependências externas — usa somente o módulo padrão `array`.

## Observações / Limitações
- Cada caractere do conteúdo do arquivo ocupa exatamente 1 bloco.
- Arquivos vazios (0 caracteres) são permitidos; são registrados no diretório com ponteiro nulo.
- O sistema não realiza compactação automática; ao remover arquivos surgem “buracos” que podem ser usados por novas criações.
- Nome máximo de arquivo: 4 caracteres (conforme enunciado).
- Ponteiro nulo é representado por `0xFFFF` (65535), simulando um `short int` sem sinal.

## Licença

Este projeto é para fins acadêmicos e não possui licença comercial.
