# CodeLab: Laboratório Completo para Engenheiros de Software

![CodeLab Logo](static/img/codelab-logo.png)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-orange.svg)](https://flask.palletsprojects.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-yellow.svg)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![HTML5](https://img.shields.io/badge/HTML5-Markup-red.svg)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-Styles-blue.svg)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Arquitetura e Componentes](#arquitetura-e-componentes)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Características](#características)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Execução](#instalação-e-execução)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [API](#api)
- [Roadmap de Desenvolvimento](#roadmap-de-desenvolvimento)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Contato](#contato)

## 🔍 Sobre o Projeto

CodeLab é uma plataforma abrangente projetada para engenheiros de software que desejam aprimorar suas habilidades de programação através de recursos práticos, exercícios desafiadores e projetos reais. O sistema funciona como um laboratório completo de desenvolvimento, oferecendo conteúdos sobre diversas linguagens de programação e frameworks, com foco especial em tecnologias de backend como Node.js, Express, NestJS e Fastify.

A plataforma foi desenvolvida com uma abordagem educacional progressiva, guiando os usuários desde conceitos básicos até implementações avançadas, com mais de 70 exercícios práticos e 40 projetos para cada tecnologia, todos organizados por níveis de dificuldade.

## 🏗️ Arquitetura e Componentes

O CodeLab foi construído utilizando uma arquitetura MVC (Model-View-Controller) simplificada:

```
                    ┌─────────────┐
                    │   Cliente   │
                    │  (Browser)  │
                    └──────┬──────┘
                           │
                           ▼
┌───────────────────────────────────────────────┐
│                  Flask App                     │
│                                               │
│  ┌──────────────┐     ┌───────────────────┐   │
│  │  Controller  │     │ Geradores de      │   │
│  │  (Routes)    │◄───►│ Conteúdo Dynamic  │   │
│  └──────┬───────┘     └───────────────────┘   │
│         │                                     │
│         ▼                                     │
│  ┌──────────────┐     ┌───────────────────┐   │
│  │    Views     │     │  Dados Estáticos  │   │
│  │  (Templates) │◄───►│  (Tecnologias,    │   │
│  └──────────────┘     │   Exercícios)     │   │
│                       └───────────────────┘   │
└───────────────────────────────────────────────┘
```

### Componentes Principais:

1. **Controlador (app.py)**:
   - Gerencia todas as rotas e lógica de negócios
   - Processa solicitações da API
   - Coordena a geração dinâmica de conteúdo

2. **Visualizações (Templates)**:
   - Interface de usuário responsiva e moderna
   - Componentes reutilizáveis
   - Integração com JavaScript para interatividade

3. **Dados e Geradores de Conteúdo**:
   - Definições estáticas de tecnologias e níveis
   - Geradores dinâmicos de exercícios e projetos
   - Exemplos de código para diferentes níveis

4. **API RESTful**:
   - Endpoints para acessar exercícios, projetos e exemplos
   - Sistema de avaliação de nível profissional
   - Recursos para personalização da experiência

## 🔧 Tecnologias Utilizadas

### Backend:
- **Python 3.10+**: Linguagem de programação principal
- **Flask 2.3.3**: Framework web leve e flexível
- **Jinja2**: Engine de templates para renderização HTML
- **Werkzeug**: Biblioteca WSGI utilizada pelo Flask

### Frontend:
- **HTML5**: Marcação semântica moderna
- **CSS3**: Estilização avançada com variáveis e flexbox/grid
- **JavaScript (ES6+)**: Interatividade e dinamismo na interface
- **Font Awesome**: Biblioteca de ícones vetoriais

### Ferramentas de Desenvolvimento:
- **Git**: Controle de versão
- **Virtual Environment**: Isolamento de dependências
- **Blueprint CSS Framework**: Framework CSS customizado
- **JSON**: Formato para geração e troca de dados

### Metodologias de Desenvolvimento:
- **Desenvolvimento Modular**: Componentes independentes e reutilizáveis
- **Design Responsivo**: Interface adaptável a diferentes dispositivos
- **Progressive Enhancement**: Funcionalidade básica para todos os usuários com melhorias para browsers modernos

## ✨ Características

### Conteúdo Educacional
- **Mais de 70 exercícios** para cada tecnologia (Node.js, Express, NestJS, Fastify, etc.)
- **40 projetos práticos** para cada tecnologia, com diferentes níveis de complexidade
- **Exemplos de código** detalhados e comentados para aprendizado efetivo
- **Roadmaps de desenvolvimento** para guiar o aprendizado progressivo

### Avaliação de Nível Profissional
- **Sistema de avaliação de habilidades** que determina o nível profissional do usuário
- **Recomendações personalizadas** baseadas no nível identificado
- **Métricas detalhadas** sobre áreas de conhecimento e pontos de melhoria

### Carreira e Desenvolvimento
- **Descrições detalhadas** dos níveis profissionais (Iniciante até Especialista)
- **Guia de habilidades necessárias** para cada nível de carreira
- **Seção de vagas** com filtros por área e nível de experiência

### Interface e Experiência do Usuário
- **Design responsivo e moderno** adaptado a diferentes dispositivos
- **Navegação intuitiva** com categorização clara de conteúdos
- **Exemplos interativos** com capacidade de copiar código e visualizar resultados

## 📋 Pré-requisitos

Para executar o CodeLab localmente, você precisará de:

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Navegador web moderno (Chrome, Firefox, Safari, Edge)
- Git (opcional, para clonar o repositório)

## 🚀 Instalação e Execução

1. **Clone o repositório (ou baixe o código-fonte)**
   ```bash
   git clone https://github.com/seuusuario/codelab.git
   cd codelab
   ```

2. **Crie e ative um ambiente virtual Python**
   ```bash
   # No Windows
   python -m venv venv
   venv\Scripts\activate

   # No macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**
   ```bash
   python app.py
   ```

5. **Acesse o aplicativo**
   - Abra seu navegador e acesse: `http://localhost:5000`

## 📁 Estrutura do Projeto

```
codelab/
├── app.py                   # Aplicação principal Flask
├── requirements.txt         # Dependências do projeto
├── static/                  # Arquivos estáticos
│   ├── css/
│   │   └── style.css        # Estilos globais da aplicação
│   ├── js/
│   │   └── main.js          # JavaScript principal
│   └── img/                 # Imagens e recursos gráficos
├── templates/               # Templates Jinja2
│   ├── base.html            # Template base (layout)
│   ├── index.html           # Página inicial
│   ├── laboratory.html      # Laboratório de tecnologias
│   ├── roadmap.html         # Roadmaps de desenvolvimento
│   ├── codes.html           # Exemplos de código
│   ├── practice.html        # Exercícios e projetos
│   ├── scripts.html         # Scripts úteis
│   ├── jobs.html            # Vagas de trabalho
│   ├── skill-level.html     # Níveis de habilidade
│   ├── level-finder.html    # Ferramenta para encontrar nível
│   └── about.html           # Sobre o projeto
└── README.md                # Documentação do projeto
```

## 🔌 API

O CodeLab oferece uma API interna para acesso aos recursos. Todos os endpoints retornam dados no formato JSON.

### Endpoints Principais:

#### Obter Exercícios
```
GET /api/exercises/<technology>/<level>
```
- **Parâmetros**:
  - `technology`: Nome da tecnologia (ex: "Node.js", "Express")
  - `level`: Nível de dificuldade ("Básico", "Intermediário", "Avançado")
- **Resposta**: Lista de exercícios para a tecnologia e nível especificados

#### Obter Projetos
```
GET /api/projects/<technology>
```
- **Parâmetros**:
  - `technology`: Nome da tecnologia
- **Resposta**: Lista de projetos para a tecnologia especificada

#### Obter Cursos
```
GET /api/courses/<technology>
```
- **Parâmetros**:
  - `technology`: Nome da tecnologia
- **Resposta**: Lista de cursos para a tecnologia especificada

#### Obter Exemplos de Código
```
GET /api/code-examples/<technology>/<level>
```
- **Parâmetros**:
  - `technology`: Nome da tecnologia
  - `level`: Nível de complexidade
- **Resposta**: Exemplo de código para a tecnologia e nível especificados

#### Avaliar Nível Profissional
```
POST /api/find-level
```
- **Corpo da Requisição**: 
  ```json
  {
    "skills": ["Node.js", "Express", "MongoDB"],
    "techAreas": ["Backend", "DevOps"]
  }
  ```
- **Resposta**: Nível profissional avaliado com detalhes

## 🗺️ Roadmap de Desenvolvimento

### Fase 1: MVP (Concluída)
- [x] Estrutura básica do aplicativo Flask
- [x] Templates e páginas principais
- [x] Geradores de exercícios e projetos
- [x] Sistema de avaliação de nível
- [x] Exemplos de código para tecnologias principais

### Fase 2: Aprimoramentos (Em Progresso)
- [ ] Autenticação e perfis de usuário
- [ ] Sistema de progresso e conquistas
- [ ] Mais exemplos de código e tecnologias
- [ ] Melhorias na interface de usuário
- [ ] Otimização de desempenho

### Fase 3: Expansão (Planejada)
- [ ] Comunidade e fórum de discussão
- [ ] Integração com GitHub para projetos
- [ ] Sistema de mentoria
- [ ] Editor de código integrado
- [ ] Suporte para mais tecnologias e frameworks

## 🤝 Contribuição

Contribuições são bem-vindas e apreciadas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Faça commit das suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Faça push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Diretrizes de Contribuição
- Siga o estilo de código existente
- Atualize a documentação conforme necessário
- Mantenha os commits claros e concisos
- Adicione testes para novas funcionalidades

## 📜 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📱 Contato

- **Email**: contato@codelab.com
- **Website**: [www.codelab.com](https://www.codelab.com)
- **GitHub**: [github.com/codelab](https://github.com/codelab)
- **Twitter**: [@codelab](https://twitter.com/codelab)

---

<p align="center">
  <img src="static/img/codelab-icon.png" width="80" height="80" alt="CodeLab Icon">
  <br>
  <em>CodeLab - Evolua suas habilidades, construa seu futuro.</em>
</p>