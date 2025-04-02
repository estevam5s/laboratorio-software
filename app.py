import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import plotly.express as px
import plotly.graph_objects as go
import time
import random
from PIL import Image
import requests
from io import BytesIO

# Configuração inicial da página - DEVE SER A PRIMEIRA CHAMADA DO STREAMLIT
st.set_page_config(
    page_title="DevLab Pro",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    /* Estilos para a interface principal */
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .sub-header {
        font-size: 2rem;
        color: #182848;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #4b6cb7;
    }
    
    .section-header {
        font-size: 1.5rem;
        color: #4b6cb7;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Cards para conteúdo */
    .card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        border-left: 5px solid #4b6cb7;
    }
    
    .card-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #182848;
        margin-bottom: 0.8rem;
    }
    
    /* Cards por nível */
    .beginner-card {
        border-left: 5px solid #4CAF50;
    }
    
    .intermediate-card {
        border-left: 5px solid #2196F3;
    }
    
    .advanced-card {
        border-left: 5px solid #9C27B0;
    }
    
    .expert-card {
        border-left: 5px solid #F44336;
    }
    
    /* Badges para tecnologias */
    .tech-badge {
        display: inline-block;
        padding: 0.3rem 0.6rem;
        border-radius: 15px;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .badge-javascript {
        background-color: #F7DF1E;
        color: black;
    }
    
    .badge-typescript {
        background-color: #3178C6;
        color: white;
    }
    
    .badge-node {
        background-color: #339933;
        color: white;
    }
    
    .badge-express {
        background-color: #000000;
        color: white;
    }
    
    .badge-nestjs {
        background-color: #E0234E;
        color: white;
    }
    
    .badge-react {
        background-color: #61DAFB;
        color: black;
    }
    
    .badge-python {
        background-color: #3776AB;
        color: white;
    }
    
    .badge-java {
        background-color: #007396;
        color: white;
    }
    
    .badge-csharp {
        background-color: #512BD4;
        color: white;
    }
    
    .badge-go {
        background-color: #00ADD8;
        color: white;
    }
    
    /* Botões estilizados */
    .styled-button {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: transform 0.2s;
    }
    
    .styled-button:hover {
        transform: translateY(-2px);
    }
    
    /* Códigos e exemplos */
    .code-block {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        font-family: monospace;
        overflow-x: auto;
        border-left: 3px solid #4b6cb7;
    }
    
    /* Níveis de carreira */
    .career-level {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .level-intern {
        background-color: #E8F5E9;
        border-left: 5px solid #4CAF50;
    }
    
    .level-junior {
        background-color: #E3F2FD;
        border-left: 5px solid #2196F3;
    }
    
    .level-mid {
        background-color: #EDE7F6;
        border-left: 5px solid #673AB7;
    }
    
    .level-senior {
        background-color: #FFF3E0;
        border-left: 5px solid #FF9800;
    }
    
    .level-staff {
        background-color: #FFEBEE;
        border-left: 5px solid #F44336;
    }
    
    .level-specialist {
        background-color: #E0F7FA;
        border-left: 5px solid #00BCD4;
    }
    
    /* Timeline para roadmap */
    .timeline-container {
        margin-left: 2rem;
        padding-left: 2rem;
        border-left: 2px solid #4b6cb7;
    }
    
    .timeline-item {
        position: relative;
        margin-bottom: 2rem;
    }
    
    .timeline-item:before {
        content: '';
        position: absolute;
        left: -2.5rem;
        top: 0.5rem;
        width: 1rem;
        height: 1rem;
        background-color: #4b6cb7;
        border-radius: 50%;
    }
    
    .timeline-content {
        background-color: white;
        padding: 1rem;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar estilizada */
    .sidebar .sidebar-content {
        background-color: #182848;
    }
    
    /* Tabelas e listas */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .custom-table th {
        background-color: #4b6cb7;
        color: white;
        padding: 0.8rem;
        text-align: left;
    }
    
    .custom-table td {
        padding: 0.8rem;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .custom-table tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    
    /* Progress bar customizada */
    .skill-progress {
        height: 0.8rem;
        border-radius: 10px;
        background-color: #e0e0e0;
        margin-bottom: 1rem;
    }
    
    .skill-progress-fill {
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
    }
    
    /* Footer */
    .footer {
        margin-top: 3rem;
        text-align: center;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Dados para as várias seções (Normalmente viriam de um banco de dados)
# ---------------------------------------------------------------

# Tecnologias suportadas
technologies = {
    "backend": [
        {"name": "Node.js", "badge_class": "badge-node", "versions": ["14.x", "16.x", "18.x", "20.x"]},
        {"name": "Express", "badge_class": "badge-express", "versions": ["4.x", "5.x"]},
        {"name": "NestJS", "badge_class": "badge-nestjs", "versions": ["8.x", "9.x", "10.x"]},
        {"name": "Fastify", "badge_class": "badge-node", "versions": ["3.x", "4.x"]},
        {"name": "Python (Django)", "badge_class": "badge-python", "versions": ["3.2", "4.0", "4.1"]},
        {"name": "Python (Flask)", "badge_class": "badge-python", "versions": ["2.0", "2.1"]},
        {"name": "Java (Spring)", "badge_class": "badge-java", "versions": ["5.x", "6.x"]},
        {"name": "C# (.NET)", "badge_class": "badge-csharp", "versions": ["6.0", "7.0", "8.0"]},
        {"name": "Go", "badge_class": "badge-go", "versions": ["1.18", "1.19", "1.20"]}
    ],
    "frontend": [
        {"name": "JavaScript", "badge_class": "badge-javascript", "versions": ["ES6", "ES2020", "ES2022"]},
        {"name": "TypeScript", "badge_class": "badge-typescript", "versions": ["4.x", "5.x"]},
        {"name": "React", "badge_class": "badge-react", "versions": ["17.x", "18.x"]},
        {"name": "Vue.js", "badge_class": "badge-node", "versions": ["2.x", "3.x"]},
        {"name": "Angular", "badge_class": "badge-nestjs", "versions": ["13.x", "14.x", "15.x"]},
        {"name": "Svelte", "badge_class": "badge-javascript", "versions": ["3.x", "4.x"]}
    ],
    "devops": [
        {"name": "Docker", "badge_class": "badge-node", "versions": ["20.x", "23.x"]},
        {"name": "Kubernetes", "badge_class": "badge-go", "versions": ["1.24", "1.25", "1.26"]},
        {"name": "AWS", "badge_class": "badge-node", "versions": ["Current"]},
        {"name": "Azure", "badge_class": "badge-csharp", "versions": ["Current"]},
        {"name": "GCP", "badge_class": "badge-go", "versions": ["Current"]},
        {"name": "CI/CD", "badge_class": "badge-node", "versions": ["Jenkins", "GitHub Actions", "GitLab CI"]}
    ]
}

# Níveis de carreira
career_levels = [
    {
        "name": "Estagiário",
        "class": "level-intern",
        "description": "Iniciando na carreira de desenvolvimento, focando no aprendizado de conceitos fundamentais e contribuindo com tarefas supervisionadas.",
        "requirements": [
            "Conhecimentos básicos de programação",
            "Familiaridade com controle de versão (Git)",
            "Entendimento básico de algoritmos e estruturas de dados",
            "Conhecimento introdutório de HTML, CSS e JavaScript (para desenvolvimento web)"
        ],
        "skills": {
            "technical": ["HTML", "CSS", "JavaScript básico", "Git básico"],
            "soft": ["Comunicação", "Trabalho em equipe", "Aprendizado rápido"]
        },
        "yearly_experience": "0-1 ano"
    },
    {
        "name": "Júnior",
        "class": "level-junior",
        "description": "Desenvolvedor em início de carreira que já possui conhecimentos básicos e pode trabalhar em tarefas com complexidade moderada, ainda com supervisão.",
        "requirements": [
            "Conhecimentos sólidos em pelo menos uma linguagem de programação",
            "Experiência com frameworks básicos",
            "Capacidade de resolver problemas simples independentemente",
            "Entendimento de padrões básicos de desenvolvimento"
        ],
        "skills": {
            "technical": ["JavaScript/TypeScript intermediário", "Framework frontend ou backend", "APIs RESTful", "SQL básico", "Git intermediário"],
            "soft": ["Resolução de problemas", "Colaboração", "Iniciativa", "Organização"]
        },
        "yearly_experience": "1-2 anos"
    },
    {
        "name": "Pleno",
        "class": "level-mid",
        "description": "Profissional que já tem autonomia para desenvolver recursos completos, com boa compreensão arquitetural e capacidade de orientar desenvolvedores iniciantes.",
        "requirements": [
            "Domínio de pelo menos uma stack tecnológica",
            "Experiência com todo o ciclo de desenvolvimento",
            "Capacidade de projetar soluções para problemas de média complexidade",
            "Habilidade para revisar código de outros desenvolvedores"
        ],
        "skills": {
            "technical": ["Arquitetura de software básica", "Bancos de dados avançados", "Segurança de aplicações", "Testes automatizados", "DevOps básico"],
            "soft": ["Mentoria", "Comunicação eficaz", "Gestão de tempo", "Resolução de conflitos"]
        },
        "yearly_experience": "2-5 anos"
    },
    {
        "name": "Sênior",
        "class": "level-senior",
        "description": "Desenvolvedor experiente capaz de tomar decisões arquiteturais importantes, resolver problemas complexos e liderar tecnicamente equipes de desenvolvimento.",
        "requirements": [
            "Amplo conhecimento em múltiplas tecnologias e paradigmas",
            "Capacidade de projetar arquiteturas escaláveis",
            "Experiência em otimização de performance e segurança",
            "Habilidade para orientar e desenvolver outros profissionais"
        ],
        "skills": {
            "technical": ["Arquitetura avançada", "Microsserviços", "Otimização de performance", "Design patterns avançados", "DevOps avançado"],
            "soft": ["Liderança técnica", "Comunicação com stakeholders", "Planejamento estratégico", "Resolução de problemas complexos"]
        },
        "yearly_experience": "5-8 anos"
    },
    {
        "name": "Staff",
        "class": "level-staff",
        "description": "Profissional que transcende o escopo de um time, exercendo impacto técnico em toda a organização através de decisões arquiteturais de alto nível e liderança técnica.",
        "requirements": [
            "Profundo conhecimento em arquitetura de sistemas",
            "Experiência em projetos de larga escala",
            "Capacidade de influenciar direções tecnológicas da empresa",
            "Habilidade para comunicar decisões técnicas para audiências não-técnicas"
        ],
        "skills": {
            "technical": ["Arquitetura de sistemas distribuídos", "Governança técnica", "Migração de sistemas legados", "Análise de trade-offs tecnológicos"],
            "soft": ["Influência organizacional", "Mentoria de líderes técnicos", "Pensamento estratégico", "Facilitação de decisões"]
        },
        "yearly_experience": "8-12 anos"
    },
    {
        "name": "Especialista",
        "class": "level-specialist",
        "description": "Autoridade em domínios tecnológicos específicos, definindo padrões e melhores práticas, além de representar a empresa em conferências e no meio tecnológico.",
        "requirements": [
            "Ser referência em um ou mais domínios tecnológicos",
            "Histórico de contribuições para a comunidade tecnológica",
            "Capacidade de antecipar tendências e inovações",
            "Habilidade para resolver problemas extremamente complexos"
        ],
        "skills": {
            "technical": ["Deep expertise em domínios específicos", "Contribuições para open source", "Research & Development", "Especificações técnicas avançadas"],
            "soft": ["Liderança técnica de alto nível", "Public speaking", "Networking na indústria", "Influência em padronizações"]
        },
        "yearly_experience": "10+ anos"
    }
]

# Lista de exercícios (exemplo para Node.js/Express)
exercises_nodejs = [
    {
        "title": "Hello World API",
        "difficulty": "Iniciante",
        "description": "Crie uma API simples que retorne 'Hello World' quando acessada.",
        "technologies": ["Node.js", "Express"],
        "level_class": "beginner-card"
    },
    {
        "title": "CRUD de Usuários",
        "difficulty": "Intermediário",
        "description": "Desenvolva uma API RESTful para gerenciar usuários com operações CRUD completas.",
        "technologies": ["Node.js", "Express", "MongoDB"],
        "level_class": "intermediate-card"
    },
    {
        "title": "Sistema de Autenticação JWT",
        "difficulty": "Intermediário",
        "description": "Implemente um sistema de autenticação usando JSON Web Tokens (JWT).",
        "technologies": ["Node.js", "Express", "JWT"],
        "level_class": "intermediate-card"
    },
    {
        "title": "API com Rate Limiting",
        "difficulty": "Avançado",
        "description": "Crie uma API com limitação de requisições por IP para prevenir abusos.",
        "technologies": ["Node.js", "Express", "Redis"],
        "level_class": "advanced-card"
    },
    {
        "title": "Sistema de Microsserviços",
        "difficulty": "Especialista",
        "description": "Desenvolva uma arquitetura de microsserviços com comunicação assíncrona.",
        "technologies": ["Node.js", "Express", "RabbitMQ", "Docker"],
        "level_class": "expert-card"
    }
]

# Lista de projetos (exemplo para NestJS)
projects_nestjs = [
    {
        "title": "Blog API",
        "difficulty": "Iniciante",
        "description": "API completa para um blog com posts, comentários e categorias.",
        "technologies": ["NestJS", "TypeORM", "PostgreSQL"],
        "level_class": "beginner-card",
        "estimated_time": "2 semanas"
    },
    {
        "title": "E-commerce Platform",
        "difficulty": "Intermediário",
        "description": "Plataforma de e-commerce com catálogo, carrinho, pedidos e pagamentos.",
        "technologies": ["NestJS", "MongoDB", "Redis", "Stripe"],
        "level_class": "intermediate-card",
        "estimated_time": "1 mês"
    },
    {
        "title": "Task Management System",
        "difficulty": "Intermediário",
        "description": "Sistema de gerenciamento de tarefas com equipes, projetos e métricas.",
        "technologies": ["NestJS", "TypeORM", "PostgreSQL", "JWT"],
        "level_class": "intermediate-card",
        "estimated_time": "3 semanas"
    },
    {
        "title": "Real-time Chat Application",
        "difficulty": "Avançado",
        "description": "Aplicação de chat em tempo real com salas, mensagens privadas e notificações.",
        "technologies": ["NestJS", "Socket.io", "Redis", "MongoDB"],
        "level_class": "advanced-card",
        "estimated_time": "1 mês"
    },
    {
        "title": "Microservices Architecture",
        "difficulty": "Especialista",
        "description": "Arquitetura completa de microsserviços com gateway API, service discovery e circuit breaker.",
        "technologies": ["NestJS", "gRPC", "RabbitMQ", "Docker", "Kubernetes"],
        "level_class": "expert-card",
        "estimated_time": "2 meses"
    }
]

# Exemplos de código (para Node.js/Express)
code_examples = {
    "Iniciante": {
        "title": "API Express Básica",
        "code": '''const express = require('express');
const app = express();
const port = 3000;

app.use(express.json());

// Middleware de exemplo
app.use((req, res, next) => {
  console.log(`${req.method} ${req.url}`);
  next();
});

// Rota simples
app.get('/', (req, res) => {
  res.json({ message: 'Hello World!' });
});

// Rota com parâmetros
app.get('/users/:id', (req, res) => {
  res.json({ userId: req.params.id });
});

// Iniciar o servidor
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});'''
    },
    "Intermediário": {
        "title": "API CRUD com Middleware de Autenticação",
        "code": '''const express = require('express');
const jwt = require('jsonwebtoken');
const mongoose = require('mongoose');
const app = express();
const port = 3000;

app.use(express.json());

// Conectar ao MongoDB
mongoose.connect('mongodb://localhost:27017/myapp', {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

// Definir modelo
const User = mongoose.model('User', {
  name: String,
  email: String,
  password: String
});

// Middleware de autenticação
const authenticate = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ message: 'Authentication required' });
  }
  
  try {
    const decoded = jwt.verify(token, 'your_secret_key');
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(403).json({ message: 'Invalid token' });
  }
};

// Rota de login
app.post('/login', async (req, res) => {
  const { email, password } = req.body;
  
  const user = await User.findOne({ email });
  
  if (!user || user.password !== password) {
    return res.status(401).json({ message: 'Invalid credentials' });
  }
  
  const token = jwt.sign({ id: user._id, email: user.email }, 'your_secret_key', {
    expiresIn: '1h'
  });
  
  res.json({ token });
});

// Rotas CRUD protegidas
app.get('/users', authenticate, async (req, res) => {
  const users = await User.find({}, '-password');
  res.json(users);
});

app.post('/users', authenticate, async (req, res) => {
  const user = new User(req.body);
  await user.save();
  res.status(201).json(user);
});

app.get('/users/:id', authenticate, async (req, res) => {
  const user = await User.findById(req.params.id, '-password');
  
  if (!user) {
    return res.status(404).json({ message: 'User not found' });
  }
  
  res.json(user);
});

app.put('/users/:id', authenticate, async (req, res) => {
  const user = await User.findByIdAndUpdate(req.params.id, req.body, {
    new: true,
    runValidators: true
  });
  
  if (!user) {
    return res.status(404).json({ message: 'User not found' });
  }
  
  res.json(user);
});

app.delete('/users/:id', authenticate, async (req, res) => {
  const user = await User.findByIdAndDelete(req.params.id);
  
  if (!user) {
    return res.status(404).json({ message: 'User not found' });
  }
  
  res.json({ message: 'User deleted' });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});'''
    },
    "Avançado": {
        "title": "API com Cache e Rate Limiting",
        "code": '''const express = require('express');
const Redis = require('ioredis');
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis');
const mongoose = require('mongoose');
const app = express();
const port = 3000;

// Conectar ao Redis
const redis = new Redis({
  host: 'localhost',
  port: 6379
});

// Conectar ao MongoDB
mongoose.connect('mongodb://localhost:27017/myapp', {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

// Middleware de rate limiting
const limiter = rateLimit({
  store: new RedisStore({
    client: redis,
    prefix: 'rate-limit:',
    expiry: 60 // 1 minuto
  }),
  windowMs: 60 * 1000, // 1 minuto
  max: 100, // limite de 100 requisições por janela
  standardHeaders: true,
  legacyHeaders: false,
  message: 'Too many requests, please try again later.'
});

// Aplicar rate limiting a todas as requisições
app.use(limiter);

// Middleware de cache
const cacheMiddleware = (duration) => {
  return async (req, res, next) => {
    const key = `cache:${req.originalUrl || req.url}`;
    
    try {
      const cachedResponse = await redis.get(key);
      
      if (cachedResponse) {
        const data = JSON.parse(cachedResponse);
        return res.json(data);
      }
      
      // Modifica o objeto res para interceptar a resposta
      const originalSend = res.json;
      
      res.json = function(body) {
        redis.setex(key, duration, JSON.stringify(body));
        originalSend.call(this, body);
      };
      
      next();
    } catch (error) {
      next(error);
    }
  };
};

// Rotas de exemplo com cache
app.get('/products', cacheMiddleware(300), async (req, res) => {
  // Simulando operação custosa
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  res.json([
    { id: 1, name: 'Product 1', price: 10.99 },
    { id: 2, name: 'Product 2', price: 24.99 },
    { id: 3, name: 'Product 3', price: 5.99 }
  ]);
});

// Middleware de error handling centralizado
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    message: 'Something went wrong!',
    error: process.env.NODE_ENV === 'production' ? {} : err
  });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});'''
    }
}

# Vagas simuladas
job_listings = [
    {
        "title": "Desenvolvedor(a) Backend Node.js",
        "company": "Tech Solutions Inc.",
        "location": "São Paulo, SP (Híbrido)",
        "level": "Pleno",
        "stack": ["Node.js", "Express", "MongoDB", "AWS"],
        "description": "Buscamos desenvolvedor(a) para integrar time de produto, atuando no desenvolvimento de APIs e microsserviços.",
        "salary_range": "R$ 8.000 - R$ 12.000",
        "area": "backend"
    },
    {
        "title": "Frontend Developer React",
        "company": "Digital Creative Agency",
        "location": "Remoto",
        "level": "Júnior",
        "stack": ["React", "TypeScript", "Styled Components"],
        "description": "Vaga para desenvolvedor(a) frontend para criar interfaces responsivas e acessíveis para produtos web.",
        "salary_range": "R$ 5.000 - R$ 7.000",
        "area": "frontend"
    },
    {
        "title": "Desenvolvedor(a) Full Stack",
        "company": "Fintech Innovations",
        "location": "Rio de Janeiro, RJ (Presencial)",
        "level": "Sênior",
        "stack": ["Node.js", "NestJS", "React", "PostgreSQL", "Docker"],
        "description": "Atuar no desenvolvimento de plataforma financeira, trabalhando em features complexas e arquitetura de novos produtos.",
        "salary_range": "R$ 15.000 - R$ 18.000",
        "area": "fullstack"
    },
    {
        "title": "DevOps Engineer",
        "company": "Cloud Systems",
        "location": "Remoto",
        "level": "Pleno/Sênior",
        "stack": ["AWS", "Kubernetes", "Terraform", "CI/CD", "Python"],
        "description": "Responsável por gerenciar infraestrutura em nuvem e implementar processos de CI/CD para múltiplos projetos.",
        "salary_range": "R$ 12.000 - R$ 18.000",
        "area": "devops"
    },
    {
        "title": "Desenvolvedor(a) Backend Java",
        "company": "Enterprise Solutions",
        "location": "Belo Horizonte, MG (Híbrido)",
        "level": "Sênior",
        "stack": ["Java", "Spring Boot", "Oracle", "Kubernetes"],
        "description": "Vaga para atuar em sistemas críticos de alta disponibilidade para grande empresa do setor financeiro.",
        "salary_range": "R$ 14.000 - R$ 20.000",
        "area": "backend"
    },
    {
        "title": "Engenheiro(a) de Software .NET",
        "company": "Tech Enterprises",
        "location": "Curitiba, PR (Presencial)",
        "level": "Pleno",
        "stack": ["C#", ".NET Core", "SQL Server", "Azure"],
        "description": "Desenvolvimento de aplicações corporativas e APIs para produtos internos da empresa.",
        "salary_range": "R$ 9.000 - R$ 13.000",
        "area": "backend"
    },
    {
        "title": "Frontend Developer Vue.js",
        "company": "Creative Web Studio",
        "location": "Remoto",
        "level": "Pleno",
        "stack": ["Vue.js", "Vuex", "JavaScript", "SCSS"],
        "description": "Responsável pelo desenvolvimento de interfaces para aplicações SPA e integração com APIs REST.",
        "salary_range": "R$ 7.000 - R$ 11.000",
        "area": "frontend"
    },
    {
        "title": "Desenvolvedor(a) Mobile React Native",
        "company": "App Solutions",
        "location": "São Paulo, SP (Presencial)",
        "level": "Pleno/Sênior",
        "stack": ["React Native", "JavaScript", "TypeScript", "Redux"],
        "description": "Desenvolvimento de aplicativos móveis multiplataforma para grandes marcas nacionais.",
        "salary_range": "R$ 10.000 - R$ 15.000",
        "area": "mobile"
    },
    {
        "title": "Tech Lead",
        "company": "Innovative Systems",
        "location": "Remoto",
        "level": "Sênior/Staff",
        "stack": ["Node.js", "NestJS", "AWS", "Microsserviços", "TypeScript"],
        "description": "Liderar equipe de desenvolvimento, definir arquitetura e padrões técnicos para novos projetos.",
        "salary_range": "R$ 18.000 - R$ 25.000",
        "area": "leadership"
    },
    {
        "title": "DevOps Specialist",
        "company": "Cloud Innovations",
        "location": "Florianópolis, SC (Híbrido)",
        "level": "Sênior",
        "stack": ["AWS", "Azure", "Docker", "Kubernetes", "Terraform", "GitLab CI"],
        "description": "Implementar e manter infraestrutura em nuvem, otimizar processos de CI/CD e garantir alta disponibilidade dos sistemas.",
        "salary_range": "R$ 15.000 - R$ 22.000",
        "area": "devops"
    },
    {
        "title": "Desenvolvedor(a) Python",
        "company": "Data Analytics Co.",
        "location": "Remoto",
        "level": "Júnior/Pleno",
        "stack": ["Python", "Django", "Flask", "PostgreSQL", "Docker"],
        "description": "Desenvolvimento de APIs e sistemas de processamento de dados para plataforma de análise.",
        "salary_range": "R$ 6.000 - R$ 12.000",
        "area": "backend"
    },
    {
        "title": "UI/UX Developer",
        "company": "Design Systems Agency",
        "location": "Rio de Janeiro, RJ (Híbrido)",
        "level": "Pleno",
        "stack": ["React", "Styled Components", "Figma", "JavaScript", "Design Systems"],
        "description": "Criar e implementar interfaces com foco em usabilidade, acessibilidade e sistemas de design.",
        "salary_range": "R$ 8.000 - R$ 12.000",
        "area": "frontend"
    },
    {
        "title": "Arquiteto(a) de Software",
        "company": "Enterprise Tech",
        "location": "São Paulo, SP (Híbrido)",
        "level": "Staff/Especialista",
        "stack": ["Java", "Microservices", "Cloud Architecture", "Kafka", "Domain-Driven Design"],
        "description": "Definir estratégias de arquitetura, mentorear equipes e liderar iniciativas de modernização de sistemas legados.",
        "salary_range": "R$ 22.000 - R$ 30.000",
        "area": "architecture"
    },
    {
        "title": "SRE (Site Reliability Engineer)",
        "company": "High Availability Inc.",
        "location": "Remoto",
        "level": "Sênior",
        "stack": ["Kubernetes", "Prometheus", "Grafana", "Go", "Python", "AWS"],
        "description": "Garantir confiabilidade, performance e escalabilidade de plataformas distribuídas de alto tráfego.",
        "salary_range": "R$ 18.000 - R$ 25.000",
        "area": "devops"
    }
]

# Roadmap de aprendizado
learning_roadmap = {
    "backend": [
        {
            "phase": "Fundamentos",
            "topics": [
                "Lógica de programação e algoritmos",
                "Estruturas de dados básicas (arrays, listas, pilhas, filas)",
                "Programação orientada a objetos",
                "Controle de versão com Git",
                "HTTP e APIs REST",
                "Banco de dados relacionais e SQL básico"
            ],
            "resources": [
                {"type": "Curso", "title": "Algoritmos e Lógica de Programação", "url": "#"},
                {"type": "Livro", "title": "Clean Code: A Handbook of Agile Software Craftsmanship", "url": "#"},
                {"type": "Tutorial", "title": "Git & GitHub Crash Course", "url": "#"}
            ],
            "projects": [
                "API CRUD simples com Express/NestJS",
                "Sistema de gerenciamento de tarefas com persistência em banco de dados"
            ]
        },
        {
            "phase": "Intermediário",
            "topics": [
                "Autenticação e autorização (JWT, OAuth)",
                "Padrões de design (Repository, Factory, Singleton)",
                "Testes automatizados (unitários, integração)",
                "ORM e abstração de banco de dados",
                "Banco de dados NoSQL",
                "Mensageria básica (RabbitMQ, Kafka)",
                "Docker e containerização"
            ],
            "resources": [
                {"type": "Curso", "title": "Web Authentication & Security", "url": "#"},
                {"type": "Livro", "title": "Designing Data-Intensive Applications", "url": "#"},
                {"type": "Tutorial", "title": "Docker for Node.js Development", "url": "#"}
            ],
            "projects": [
                "API com autenticação, autorização e testes",
                "Aplicação com múltiplos serviços usando Docker Compose"
            ]
        },
        {
            "phase": "Avançado",
            "topics": [
                "Arquitetura de Microsserviços",
                "Programação reativa e assíncrona",
                "Otimização de performance e escalabilidade",
                "CI/CD e DevOps",
                "Resiliência e tolerância a falhas",
                "Observabilidade (logs, métricas, traces)",
                "Cache distribuído e estratégias"
            ],
            "resources": [
                {"type": "Curso", "title": "Microservices Architecture", "url": "#"},
                {"type": "Livro", "title": "Building Microservices", "url": "#"},
                {"type": "Tutorial", "title": "Implementing Resilient Applications", "url": "#"}
            ],
            "projects": [
                "Arquitetura de microsserviços com API gateway",
                "Sistema distribuído com mensageria e circuit breaker"
            ]
        },
        {
            "phase": "Especialista",
            "topics": [
                "Domain-Driven Design (DDD)",
                "Event Sourcing e CQRS",
                "Sistemas distribuídos complexos",
                "Alta disponibilidade e escalabilidade global",
                "Engenharia de plataforma",
                "FinOps e otimização de custos em nuvem",
                "Arquitetura orientada a eventos"
            ],
            "resources": [
                {"type": "Curso", "title": "Advanced Domain-Driven Design", "url": "#"},
                {"type": "Livro", "title": "Implementing Domain-Driven Design", "url": "#"},
                {"type": "Tutorial", "title": "Event Sourcing in Practice", "url": "#"}
            ],
            "projects": [
                "Sistema complexo com DDD e CQRS",
                "Plataforma multi-tenant com alta disponibilidade"
            ]
        }
    ],
    "frontend": [
        {
            "phase": "Fundamentos",
            "topics": [
                "HTML5 semântico",
                "CSS3 e layouts responsivos",
                "JavaScript ES6+ fundamentals",
                "DOM e manipulação de eventos",
                "APIs do navegador",
                "Controle de versão com Git",
                "HTTP e consumo de APIs"
            ],
            "resources": [
                {"type": "Curso", "title": "Modern JavaScript From The Beginning", "url": "#"},
                {"type": "Livro", "title": "Eloquent JavaScript", "url": "#"},
                {"type": "Tutorial", "title": "Flexbox and CSS Grid Complete Guide", "url": "#"}
            ],
            "projects": [
                "Portfólio pessoal responsivo",
                "Aplicação de lista de tarefas com localStorage"
            ]
        },
        {
            "phase": "Intermediário",
            "topics": [
                "Framework frontend (React, Vue ou Angular)",
                "Gerenciamento de estado (Redux, Vuex, Context API)",
                "TypeScript",
                "Roteamento client-side",
                "Testes (Jest, Testing Library)",
                "CSS-in-JS ou pré-processadores",
                "Build tools e bundlers (Webpack, Vite)"
            ],
            "resources": [
                {"type": "Curso", "title": "React - The Complete Guide", "url": "#"},
                {"type": "Livro", "title": "Learning TypeScript", "url": "#"},
                {"type": "Tutorial", "title": "Modern Frontend Testing", "url": "#"}
            ],
            "projects": [
                "Aplicação SPA com autenticação e rotas protegidas",
                "Dashboard com múltiplos gráficos e dados dinâmicos"
            ]
        },
        {
            "phase": "Avançado",
            "topics": [
                "Arquitetura de aplicações frontend complexas",
                "Server-side rendering (Next.js, Nuxt)",
                "Performance e otimização",
                "Acessibilidade (WCAG, ARIA)",
                "Internacionalização",
                "PWA (Progressive Web Apps)",
                "Micro frontends"
            ],
            "resources": [
                {"type": "Curso", "title": "Advanced React Patterns", "url": "#"},
                {"type": "Livro", "title": "Web Performance in Action", "url": "#"},
                {"type": "Tutorial", "title": "Building Accessible Web Applications", "url": "#"}
            ],
            "projects": [
                "E-commerce com SSR, i18n e otimização de performance",
                "Aplicação PWA com funcionalidades offline"
            ]
        },
        {
            "phase": "Especialista",
            "topics": [
                "Arquitetura frontend em larga escala",
                "Design systems",
                "Web Components",
                "WebAssembly",
                "Renderização 3D (Three.js, WebGL)",
                "Animações complexas e visualizações de dados",
                "Integração com tecnologias emergentes (AR/VR)"
            ],
            "resources": [
                {"type": "Curso", "title": "Enterprise Frontend Architecture", "url": "#"},
                {"type": "Livro", "title": "Design Systems Handbook", "url": "#"},
                {"type": "Tutorial", "title": "3D on the Web with Three.js", "url": "#"}
            ],
            "projects": [
                "Design system corporativo com documentação e storybook",
                "Aplicação com visualizações 3D interativas"
            ]
        }
    ],
    "devops": [
        {
            "phase": "Fundamentos",
            "topics": [
                "Sistemas operacionais Linux",
                "Linha de comando e shell scripting",
                "Controle de versão com Git",
                "Docker básico",
                "Redes e protocolos",
                "CI/CD conceitos fundamentais",
                "Cloud computing conceitos"
            ],
            "resources": [
                {"type": "Curso", "title": "Linux Administration Bootcamp", "url": "#"},
                {"type": "Livro", "title": "The Docker Book", "url": "#"},
                {"type": "Tutorial", "title": "Getting Started with CI/CD", "url": "#"}
            ],
            "projects": [
                "Ambiente de desenvolvimento com Docker",
                "Pipeline CI simples com GitHub Actions"
            ]
        },
        {
            "phase": "Intermediário",
            "topics": [
                "Docker avançado e Docker Compose",
                "Kubernetes fundamentals",
                "Terraform e IaC",
                "Monitoramento e logs (Prometheus, ELK)",
                "Cloud providers (AWS, Azure, GCP)",
                "Automação com Ansible",
                "Segurança de infraestrutura"
            ],
            "resources": [
                {"type": "Curso", "title": "Kubernetes for Developers", "url": "#"},
                {"type": "Livro", "title": "Terraform: Up & Running", "url": "#"},
                {"type": "Tutorial", "title": "AWS for DevOps Engineers", "url": "#"}
            ],
            "projects": [
                "Infraestrutura como código para ambiente de produção",
                "Cluster Kubernetes com monitoramento"
            ]
        },
        {
            "phase": "Avançado",
            "topics": [
                "Kubernetes avançado (Operators, CRDs)",
                "Service mesh (Istio, Linkerd)",
                "GitOps e fluxos avançados de CI/CD",
                "Observabilidade avançada",
                "Bancos de dados em ambientes cloud-native",
                "Segurança em ambiente Kubernetes",
                "Ferramentas de policy as code"
            ],
            "resources": [
                {"type": "Curso", "title": "Advanced Kubernetes Security", "url": "#"},
                {"type": "Livro", "title": "Cloud Native DevOps with Kubernetes", "url": "#"},
                {"type": "Tutorial", "title": "Implementing Service Mesh with Istio", "url": "#"}
            ],
            "projects": [
                "Plataforma Kubernetes multi-cluster com service mesh",
                "Sistema de observabilidade completo (logs, métricas, traces)"
            ]
        },
        {
            "phase": "Especialista",
            "topics": [
                "Arquiteturas multi-cloud e híbridas",
                "FinOps e otimização de custos",
                "Engenharia de confiabilidade (SRE)",
                "Segurança e compliance em larga escala",
                "Plataformas de orquestração avançadas",
                "Automação de datacenters",
                "Edge computing e IoT"
            ],
            "resources": [
                {"type": "Curso", "title": "Site Reliability Engineering", "url": "#"},
                {"type": "Livro", "title": "Cloud FinOps", "url": "#"},
                {"type": "Tutorial", "title": "Building Multi-Cloud Architectures", "url": "#"}
            ],
            "projects": [
                "Plataforma multi-cloud com estratégia de DR",
                "Implementação de práticas SRE em ambiente corporativo"
            ]
        }
    ]
}

# Lista de habilidades para avaliação
skill_evaluation = {
    "backend": [
        {"name": "Programação Orientada a Objetos", "weight": 5},
        {"name": "APIs RESTful", "weight": 5},
        {"name": "Node.js/Express", "weight": 4},
        {"name": "NestJS", "weight": 3},
        {"name": "Bancos de Dados Relacionais", "weight": 4},
        {"name": "Bancos de Dados NoSQL", "weight": 3},
        {"name": "Autenticação e Autorização", "weight": 4},
        {"name": "Testes Automatizados", "weight": 4},
        {"name": "Arquitetura de Software", "weight": 5},
        {"name": "Design Patterns", "weight": 4},
        {"name": "Microsserviços", "weight": 3},
        {"name": "Message Brokers (Kafka, RabbitMQ)", "weight": 3},
        {"name": "Docker e Containerização", "weight": 3},
        {"name": "CI/CD", "weight": 3},
        {"name": "Cloud (AWS, Azure, GCP)", "weight": 3}
    ],
    "frontend": [
        {"name": "HTML5 Semântico", "weight": 4},
        {"name": "CSS3 e Layouts Responsivos", "weight": 4},
        {"name": "JavaScript ES6+", "weight": 5},
        {"name": "TypeScript", "weight": 4},
        {"name": "React", "weight": 4},
        {"name": "Gerenciamento de Estado (Redux, Context API)", "weight": 3},
        {"name": "Roteamento Client-side", "weight": 3},
        {"name": "Testes Frontend", "weight": 4},
        {"name": "Performance Web", "weight": 4},
        {"name": "Acessibilidade", "weight": 3},
        {"name": "CSS Avançado (Sass, CSS-in-JS)", "weight": 3},
        {"name": "Bundlers (Webpack, Vite)", "weight": 2},
        {"name": "SSR/SSG (Next.js, Gatsby)", "weight": 3},
        {"name": "Progressive Web Apps", "weight": 2},
        {"name": "Design Systems", "weight": 2}
    ],
    "devops": [
        {"name": "Linux e Linha de Comando", "weight": 5},
        {"name": "Git e Controle de Versão", "weight": 4},
        {"name": "Docker", "weight": 5},
        {"name": "Kubernetes", "weight": 4},
        {"name": "CI/CD (Jenkins, GitHub Actions)", "weight": 4},
        {"name": "Infraestrutura como Código (Terraform)", "weight": 4},
        {"name": "Automação (Ansible, Chef, Puppet)", "weight": 3},
        {"name": "Cloud (AWS, Azure, GCP)", "weight": 4},
        {"name": "Monitoramento e Observabilidade", "weight": 4},
        {"name": "Segurança de Infraestrutura", "weight": 4},
        {"name": "Redes e Protocolos", "weight": 3},
        {"name": "Bancos de Dados (Administração)", "weight": 3},
        {"name": "Service Mesh", "weight": 2},
        {"name": "Estratégias de Escalabilidade", "weight": 3},
        {"name": "Princípios de SRE", "weight": 3}
    ]
}

# Função para criar badges HTML para tecnologias
def create_tech_badge(tech):
    badge_class = next((t["badge_class"] for t_category in technologies.values() 
                        for t in t_category if t["name"] == tech), "badge-node")
    return f'<span class="tech-badge {badge_class}">{tech}</span>'

# Função para gerar HTML de badges para uma lista de tecnologias
def generate_tech_badges(tech_list):
    return ' '.join([create_tech_badge(tech) for tech in tech_list])

# Função para avaliar o nível baseado nas habilidades
def evaluate_skill_level(skills_dict, track="backend"):
    if not skills_dict:
        return "Não foi possível determinar", 0
    
    tracked_skills = skill_evaluation.get(track, [])
    max_score = sum(skill["weight"] for skill in tracked_skills)
    user_score = 0
    
    for skill in tracked_skills:
        skill_name = skill["name"]
        if skill_name in skills_dict:
            user_score += (skills_dict[skill_name] / 100) * skill["weight"]
    
    percentage = (user_score / max_score) * 100
    
    if percentage < 20:
        return "Estagiário", percentage
    elif percentage < 40:
        return "Júnior", percentage
    elif percentage < 60:
        return "Pleno", percentage
    elif percentage < 80:
        return "Sênior", percentage
    else:
        return "Staff/Especialista", percentage
        
# Componentes da Interface
# -------------------------

# Página Inicial
def home_page():
    st.markdown("<h1 class='main-header'>DevLab Pro: Laboratório de Desenvolvimento de Software</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <p>Bem-vindo ao <strong>DevLab Pro</strong>, uma plataforma completa para desenvolvedores de software 
        em todos os níveis. Aprenda, pratique e desenvolva suas habilidades com exercícios, projetos 
        e recursos educacionais abrangentes para Backend, Frontend, Full Stack e DevOps.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Visão geral das principais seções
    st.markdown("<h2 class='sub-header'>Explore Nossas Seções</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-title">🔬 Laboratório Prático</div>
            <p>Mais de 200 exercícios e 120 projetos práticos para desenvolver suas habilidades em várias tecnologias.</p>
            <ul>
                <li>Exercícios com diferentes níveis de dificuldade</li>
                <li>Projetos completos com especificações detalhadas</li>
                <li>Exemplos de código para referência</li>
                <li>Ambiente de teste integrado</li>
            </ul>
            <a href="#" class="styled-button">Acessar Laboratório</a>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">🛣️ Roadmap de Carreira</div>
            <p>Guias detalhados para evoluir do nível iniciante ao especialista em diferentes áreas da tecnologia.</p>
            <ul>
                <li>Roadmaps para Backend, Frontend e DevOps</li>
                <li>Habilidades necessárias para cada nível</li>
                <li>Recursos de estudo recomendados</li>
                <li>Avaliação de nível personalizada</li>
            </ul>
            <a href="#" class="styled-button">Ver Roadmaps</a>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="card">
            <div class="card-title">💼 Desenvolvimento Profissional</div>
            <p>Recursos para ajudar em sua carreira, desde níveis iniciantes até posições de liderança técnica.</p>
            <ul>
                <li>Descrições detalhadas dos níveis de carreira</li>
                <li>Vagas em diferentes áreas e senioridades</li>
                <li>Materiais para entrevistas técnicas</li>
                <li>Tendências do mercado de tecnologia</li>
            </ul>
            <a href="#" class="styled-button">Explorar Carreira</a>
        </div>
        """, unsafe_allow_html=True)
    
    # Tecnologias em destaque
    st.markdown("<h2 class='sub-header'>Tecnologias em Destaque</h2>", unsafe_allow_html=True)
    
    # Backend
    st.markdown("<h3 class='section-header'>Backend</h3>", unsafe_allow_html=True)
    backend_cols = st.columns(3)
    for i, tech in enumerate(technologies["backend"][:6]):
        with backend_cols[i % 3]:
            st.markdown(f"""
            <div class="card">
                <span class="tech-badge {tech['badge_class']}">{tech['name']}</span>
                <p>Versões suportadas: {', '.join(tech['versions'])}</p>
                <p>+ 70 exercícios e 40 projetos disponíveis</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Frontend
    st.markdown("<h3 class='section-header'>Frontend</h3>", unsafe_allow_html=True)
    frontend_cols = st.columns(3)
    for i, tech in enumerate(technologies["frontend"][:6]):
        with frontend_cols[i % 3]:
            st.markdown(f"""
            <div class="card">
                <span class="tech-badge {tech['badge_class']}">{tech['name']}</span>
                <p>Versões suportadas: {', '.join(tech['versions'])}</p>
                <p>+ 70 exercícios e 40 projetos disponíveis</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Estatísticas da plataforma
    st.markdown("<h2 class='sub-header'>Estatísticas da Plataforma</h2>", unsafe_allow_html=True)
    
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    
    with stats_col1:
        st.metric("Exercícios", "840+", "+70 este mês")
    
    with stats_col2:
        st.metric("Projetos Práticos", "480+", "+40 este mês")
    
    with stats_col3:
        st.metric("Recursos de Estudo", "1200+", "+150 este mês")
    
    with stats_col4:
        st.metric("Vagas Disponíveis", "500+", "+125 este mês")
    
    # Depoimentos
    st.markdown("<h2 class='sub-header'>O Que Dizem Nossos Usuários</h2>", unsafe_allow_html=True)
    
    testimonials_col1, testimonials_col2 = st.columns(2)
    
    with testimonials_col1:
        st.markdown("""
        <div class="card">
            <p>"O DevLab Pro revolucionou minha carreira. Os exercícios práticos e roadmaps me ajudaram a sair do nível júnior para sênior em menos de 2 anos. Recomendo para todos os desenvolvedores."</p>
            <p><strong>Ana Silva</strong> - Desenvolvedora Full Stack</p>
        </div>
        """, unsafe_allow_html=True)
        
    with testimonials_col2:
        st.markdown("""
        <div class="card">
            <p>"Como gestor de tecnologia, recomendo o DevLab Pro para toda minha equipe. A plataforma oferece conteúdo atualizado e de alta qualidade, além de exercícios que realmente preparam para desafios reais."</p>
            <p><strong>Carlos Mendes</strong> - CTO, TechSolutions</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>DevLab Pro © 2025 - A plataforma definitiva para desenvolvedores de software</p>
    </div>
    """, unsafe_allow_html=True)

# Página de Laboratório
def lab_page():
    st.markdown("<h1 class='main-header'>Laboratório Prático</h1>", unsafe_allow_html=True)
    
    # Filtros
    st.markdown("<h2 class='sub-header'>Filtros</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        area = st.selectbox("Área", ["Backend", "Frontend", "Full Stack", "DevOps"])
    
    with col2:
        technology = st.selectbox("Tecnologia", 
            ["Todas"] + 
            ([t["name"] for t in technologies["backend"]] if area == "Backend" else
             [t["name"] for t in technologies["frontend"]] if area == "Frontend" else
             [t["name"] for t in technologies["backend"] + technologies["frontend"]] if area == "Full Stack" else
             [t["name"] for t in technologies["devops"]])
        )
    
    with col3:
        difficulty = st.selectbox("Nível", ["Todos", "Iniciante", "Intermediário", "Avançado", "Especialista"])
    
    # Opções Laboratório
    st.markdown("<h2 class='sub-header'>Escolha o tipo de conteúdo</h2>", unsafe_allow_html=True)
    
    lab_option = st.radio("", ["Exercícios", "Projetos", "Exemplos de Código"], horizontal=True)
    
    if lab_option == "Exercícios":
        st.markdown("<h2 class='sub-header'>Exercícios Práticos</h2>", unsafe_allow_html=True)
        
        # Mostrar exercícios (usando Node.js como exemplo)
        for exercise in exercises_nodejs:
            if (difficulty == "Todos" or exercise["difficulty"] == difficulty) and \
               (technology == "Todas" or technology in exercise["technologies"]):
                
                st.markdown(f"""
                <div class="card {exercise['level_class']}">
                    <div class="card-title">{exercise['title']}</div>
                    <p><strong>Dificuldade:</strong> {exercise['difficulty']}</p>
                    <p>{exercise['description']}</p>
                    <p><strong>Tecnologias:</strong> {generate_tech_badges(exercise['technologies'])}</p>
                    <a href="#" class="styled-button">Iniciar Exercício</a>
                    <a href="#" class="styled-button">Ver Solução</a>
                </div>
                """, unsafe_allow_html=True)
    
    elif lab_option == "Projetos":
        st.markdown("<h2 class='sub-header'>Projetos Práticos</h2>", unsafe_allow_html=True)
        
        # Mostrar projetos (usando NestJS como exemplo)
        for project in projects_nestjs:
            if (difficulty == "Todos" or project["difficulty"] == difficulty) and \
               (technology == "Todas" or technology in project["technologies"]):
                
                st.markdown(f"""
                <div class="card {project['level_class']}">
                    <div class="card-title">{project['title']}</div>
                    <p><strong>Dificuldade:</strong> {project['difficulty']} | <strong>Tempo estimado:</strong> {project['estimated_time']}</p>
                    <p>{project['description']}</p>
                    <p><strong>Tecnologias:</strong> {generate_tech_badges(project['technologies'])}</p>
                    <a href="#" class="styled-button">Ver Detalhes</a>
                    <a href="#" class="styled-button">Iniciar Projeto</a>
                </div>
                """, unsafe_allow_html=True)
    
    elif lab_option == "Exemplos de Código":
        st.markdown("<h2 class='sub-header'>Exemplos de Código</h2>", unsafe_allow_html=True)
        
        code_level = st.selectbox("Selecione o nível", list(code_examples.keys()))
        
        example = code_examples[code_level]
        st.markdown(f"""
        <div class="card">
            <div class="card-title">{example['title']}</div>
            <p><strong>Nível:</strong> {code_level}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.code(example['code'], language='javascript')
        
        st.markdown("""
        <div class="card">
            <div class="card-title">Explicação do Código</div>
            <p>Este exemplo demonstra como implementar uma API utilizando Express.js com vários conceitos importantes:</p>
            <ul>
                <li>Configuração básica de um servidor</li>
                <li>Definição de rotas e middlewares</li>
                <li>Manipulação de requisições e respostas</li>
                <li>Boas práticas de estruturação de código</li>
            </ul>
            <p>Você pode usar este código como ponto de partida para seus próprios projetos, adaptando conforme necessário.</p>
        </div>
        """, unsafe_allow_html=True)

# Página de Roadmap
def roadmap_page():
    st.markdown("<h1 class='main-header'>Roadmap de Desenvolvimento</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <p>Os roadmaps abaixo são guias estruturados para o desenvolvimento de suas habilidades técnicas em diferentes áreas. 
        Cada fase inclui tópicos essenciais, recursos recomendados e projetos práticos para consolidar o aprendizado.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Seleção de área
    area = st.selectbox("Selecione a área", ["Backend", "Frontend", "DevOps"])
    
    # Mapeamento de seleção para chave do dicionário
    area_key = area.lower()
    
    # Exibir roadmap da área selecionada
    if area_key in learning_roadmap:
        for phase_index, phase in enumerate(learning_roadmap[area_key]):
            st.markdown(f"<h2 class='sub-header'>{phase['phase']}</h2>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class="timeline-container">
            """, unsafe_allow_html=True)
            
            # Tópicos
            st.markdown("""
            <div class="timeline-item">
                <div class="timeline-content card">
                    <div class="card-title">Tópicos Essenciais</div>
                    <ul>
            """, unsafe_allow_html=True)
            
            for topic in phase["topics"]:
                st.markdown(f"<li>{topic}</li>", unsafe_allow_html=True)
            
            st.markdown("""
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Recursos
            st.markdown("""
            <div class="timeline-item">
                <div class="timeline-content card">
                    <div class="card-title">Recursos Recomendados</div>
                    <ul>
            """, unsafe_allow_html=True)
            
            for resource in phase["resources"]:
                st.markdown(f"<li><strong>{resource['type']}:</strong> <a href='{resource['url']}'>{resource['title']}</a></li>", unsafe_allow_html=True)
            
            st.markdown("""
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Projetos
            st.markdown("""
            <div class="timeline-item">
                <div class="timeline-content card">
                    <div class="card-title">Projetos Práticos</div>
                    <ul>
            """, unsafe_allow_html=True)
            
            for project in phase["projects"]:
                st.markdown(f"<li>{project}</li>", unsafe_allow_html=True)
            
            st.markdown("""
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            </div>
            """, unsafe_allow_html=True)
            
            # Botão para ver exercícios relacionados
            if phase_index < len(learning_roadmap[area_key]) - 1:
                st.markdown("<hr>", unsafe_allow_html=True)

# Página de Níveis de Carreira
def career_levels_page():
    st.markdown("<h1 class='main-header'>Níveis de Carreira em Desenvolvimento de Software</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <p>Entenda os diferentes níveis de carreira em desenvolvimento de software, suas responsabilidades, requisitos técnicos e habilidades necessárias.
        Esta é uma referência para ajudar você a entender onde está e para onde quer ir em sua trajetória profissional.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Exibir cada nível de carreira
    for level in career_levels:
        st.markdown(f"""
        <div class="career-level {level['class']}">
            <h2>{level['name']}</h2>
            <p><strong>Experiência típica:</strong> {level['yearly_experience']}</p>
            <p>{level['description']}</p>
            
            <h3>Requisitos</h3>
            <ul>
        """, unsafe_allow_html=True)
        
        for req in level['requirements']:
            st.markdown(f"<li>{req}</li>", unsafe_allow_html=True)
        
        st.markdown("""
            </ul>
            
            <h3>Habilidades Técnicas</h3>
            <ul>
        """, unsafe_allow_html=True)
        
        for skill in level['skills']['technical']:
            st.markdown(f"<li>{skill}</li>", unsafe_allow_html=True)
        
        st.markdown("""
            </ul>
            
            <h3>Soft Skills</h3>
            <ul>
        """, unsafe_allow_html=True)
        
        for skill in level['skills']['soft']:
            st.markdown(f"<li>{skill}</li>", unsafe_allow_html=True)
        
        st.markdown("""
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Página de Avaliação de Nível
def skill_assessment_page():
    st.markdown("<h1 class='main-header'>Avaliação de Nível Profissional</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <p>Avalie seu nível atual como desenvolvedor indicando sua proficiência nas habilidades listadas abaixo.
        Nossa ferramenta analisará suas respostas e estimará seu nível profissional atual, além de sugerir áreas para desenvolvimento.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Seleção de área
    area = st.selectbox("Selecione sua área principal", ["Backend", "Frontend", "DevOps"])
    area_key = area.lower()
    
    # Inicializar estado se não existir
    if 'user_skills' not in st.session_state:
        st.session_state.user_skills = {}
    
    # Mostrar sliders para cada habilidade
    st.subheader("Avalie suas habilidades de 0 a 100")
    
    skills_input = {}
    
    if area_key in skill_evaluation:
        for skill in skill_evaluation[area_key]:
            skill_name = skill["name"]
            default_value = st.session_state.user_skills.get(skill_name, 50)
            skills_input[skill_name] = st.slider(
                f"{skill_name} (Peso: {skill['weight']})", 
                0, 100, default_value,
                help="0 = Nenhum conhecimento, 100 = Especialista"
            )
    
    # Botão para avaliar
    if st.button("Avaliar Meu Nível"):
        # Armazenar habilidades na sessão
        st.session_state.user_skills = skills_input
        
        # Calcular nível
        level_name, percentage = evaluate_skill_level(skills_input, area_key)
        
        st.markdown(f"""
        <div class="card">
            <h2>Resultado da Avaliação</h2>
            <p>Com base nas suas habilidades, seu nível estimado é:</p>
            <h3 style="color: #4b6cb7; font-size: 2rem; text-align: center;">{level_name}</h3>
            <div class="skill-progress">
                <div class="skill-progress-fill" style="width: {percentage}%;"></div>
            </div>
            <p style="text-align: center;">{percentage:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Encontrar o nível correspondente para mostrar descrição
        level_info = next((level for level in career_levels if level["name"] == level_name), None)
        
        if level_info:
            st.markdown(f"""
            <div class="card {level_info['class']}">
                <h3>Sobre o nível {level_name}</h3>
                <p>{level_info['description']}</p>
                
                <h4>Expectativas para este nível:</h4>
                <ul>
            """, unsafe_allow_html=True)
            
            for req in level_info['requirements']:
                st.markdown(f"<li>{req}</li>", unsafe_allow_html=True)
            
            st.markdown("""
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Recomendar áreas de melhoria
        weak_areas = []
        for skill_name, value in skills_input.items():
            if value < 50:
                weak_areas.append(skill_name)
        
        if weak_areas:
            st.markdown("""
            <div class="card">
                <h3>Áreas para Desenvolvimento</h3>
                <p>Recomendamos que você foque em melhorar nestas áreas:</p>
                <ul>
            """, unsafe_allow_html=True)
            
            for area in weak_areas:
                st.markdown(f"<li>{area}</li>", unsafe_allow_html=True)
            
            st.markdown("""
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Próximos passos
        st.markdown("""
        <div class="card">
            <h3>Próximos Passos</h3>
            <p>Para continuar seu desenvolvimento profissional, sugerimos:</p>
            <ol>
                <li>Consulte o <a href="#">Roadmap de Desenvolvimento</a> específico para sua área</li>
                <li>Pratique com os <a href="#">Exercícios e Projetos</a> recomendados para seu nível</li>
                <li>Explore as <a href="#">Vagas</a> disponíveis para seu nível atual e desejado</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

# Página de Vagas
def job_listings_page():
    st.markdown("<h1 class='main-header'>Vagas em Tecnologia</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <p>Explore oportunidades de trabalho em tecnologia, filtradas por área, nível de senioridade e localização.
        Nossa curadoria foca em vagas de qualidade, com descrições completas e faixas salariais transparentes.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        area = st.selectbox("Área", ["Todas", "Backend", "Frontend", "Full Stack", "DevOps", "Liderança"])
    
    with col2:
        level = st.selectbox("Nível", ["Todos", "Estagiário", "Júnior", "Pleno", "Sênior", "Staff/Especialista"])
    
    with col3:
        location = st.selectbox("Localização", ["Todas", "Remoto", "São Paulo", "Rio de Janeiro", "Belo Horizonte", "Outras"])
    
    # Filtrar vagas
    filtered_jobs = job_listings
    
    if area != "Todas":
        area_map = {
            "Backend": "backend",
            "Frontend": "frontend",
            "Full Stack": "fullstack",
            "DevOps": "devops",
            "Liderança": "leadership"
        }
        filtered_jobs = [job for job in filtered_jobs if job["area"] == area_map.get(area, "")]
    
    if level != "Todos":
        filtered_jobs = [job for job in filtered_jobs if level in job["level"]]
    
    if location != "Todas":
        filtered_jobs = [job for job in filtered_jobs if location in job["location"]]
    
    # Exibir vagas
    st.markdown(f"<h2 class='sub-header'>Vagas Encontradas ({len(filtered_jobs)})</h2>", unsafe_allow_html=True)
    
    for job in filtered_jobs:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">{job['title']}</div>
            <p><strong>{job['company']}</strong> • {job['location']}</p>
            <p><strong>Nível:</strong> {job['level']}</p>
            <p><strong>Stack:</strong> {generate_tech_badges(job['stack'])}</p>
            <p>{job['description']}</p>
            <p><strong>Faixa salarial:</strong> {job['salary_range']}</p>
            <a href="#" class="styled-button">Ver Detalhes</a>
            <a href="#" class="styled-button">Candidatar-se</a>
        </div>
        """, unsafe_allow_html=True)
    
    if not filtered_jobs:
        st.info("Nenhuma vaga encontrada com os filtros selecionados. Tente critérios diferentes.")

# Página sobre a plataforma
def about_page():
    st.markdown("<h1 class='main-header'>Sobre o DevLab Pro</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <p>O <strong>DevLab Pro</strong> é uma plataforma completa para desenvolvimento de software, criada por desenvolvedores para desenvolvedores.
        Nossa missão é democratizar o conhecimento técnico de alta qualidade e oferecer um ambiente estruturado para o aprendizado prático.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Estatísticas da plataforma
    st.markdown("<h2 class='sub-header'>Nossos Números</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Usuários Ativos", "50.000+", "+15% mês")
    
    with col2:
        st.metric("Exercícios Concluídos", "2.5M+", "+120k mês")
    
    with col3:
        st.metric("Tecnologias Cobertas", "35+", "+3 mês")
    
    with col4:
        st.metric("Contratações via Plataforma", "8.000+", "+350 mês")
    
    # Equipe
    st.markdown("<h2 class='sub-header'>Nossa Equipe</h2>", unsafe_allow_html=True)
    
    team_col1, team_col2, team_col3 = st.columns(3)
    
    with team_col1:
        st.markdown("""
        <div class="card">
            <div style="text-align: center;">
                <img src="https://via.placeholder.com/150" style="border-radius: 50%; margin-bottom: 1rem;" />
                <h3>Ana Oliveira</h3>
                <p>CEO & Fundadora</p>
                <p>Ex-CTO de startup unicórnio, +15 anos de experiência em desenvolvimento de software e liderança técnica.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with team_col2:
        st.markdown("""
        <div class="card">
            <div style="text-align: center;">
                <img src="https://via.placeholder.com/150" style="border-radius: 50%; margin-bottom: 1rem;" />
                <h3>Pedro Santos</h3>
                <p>CTO & Co-Fundador</p>
                <p>Especialista em arquitetura de sistemas, +12 anos desenvolvendo plataformas educacionais de larga escala.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with team_col3:
        st.markdown("""
        <div class="card">
            <div style="text-align: center;">
                <img src="https://via.placeholder.com/150" style="border-radius: 50%; margin-bottom: 1rem;" />
                <h3>Camila Ferreira</h3>
                <p>Head de Conteúdo</p>
                <p>Desenvolvedora sênior e educadora, responsável pela curadoria e criação de material didático de alta qualidade.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Missão e valores
    st.markdown("<h2 class='sub-header'>Missão e Valores</h2>", unsafe_allow_html=True)
    
    mission_col1, mission_col2 = st.columns(2)
    
    with mission_col1:
        st.markdown("""
        <div class="card">
            <h3>Nossa Missão</h3>
            <p>Democratizar o acesso ao conhecimento de desenvolvimento de software de alta qualidade e facilitar a evolução profissional de desenvolvedores em todos os níveis.</p>
            
            <h3>Nossa Visão</h3>
            <p>Ser a plataforma de referência global para formação e evolução contínua de desenvolvedores de software, impactando positivamente a carreira de milhões de profissionais.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with mission_col2:
        st.markdown("""
        <div class="card">
            <h3>Nossos Valores</h3>
            <ul>
                <li><strong>Excelência Técnica</strong> - Conteúdo atualizado e de alta qualidade</li>
                <li><strong>Aprendizado Prático</strong> - Foco em exercícios e projetos reais</li>
                <li><strong>Comunidade</strong> - Ambiente colaborativo de crescimento</li>
                <li><strong>Inclusão</strong> - Acessibilidade para desenvolvedores de todos os níveis</li>
                <li><strong>Relevância</strong> - Alinhamento com as demandas reais do mercado</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Contato
    st.markdown("<h2 class='sub-header'>Entre em Contato</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div>
                <h3>Suporte</h3>
                <p>suporte@devlabpro.com</p>
                <p>+55 (11) 99999-8888</p>
            </div>
            <div>
                <h3>Parcerias</h3>
                <p>parcerias@devlabpro.com</p>
                <p>+55 (11) 99999-7777</p>
            </div>
            <div>
                <h3>Imprensa</h3>
                <p>imprensa@devlabpro.com</p>
                <p>+55 (11) 99999-6666</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Função principal para roteamento
def main():
    # Sidebar para navegação
    with st.sidebar:
        st.image("https://via.placeholder.com/200x80?text=DevLab+Pro", width=200)
        
        navigation = st.radio(
            "Navegação",
            ["Início", "Laboratório", "Roadmap", "Níveis de Carreira", "Avaliação de Nível", "Vagas", "Sobre"]
        )
        
        st.markdown("---")
        
        if st.button("Login"):
            st.success("Funcionalidade de login seria implementada aqui.")
        
        if st.button("Cadastre-se"):
            st.info("Funcionalidade de cadastro seria implementada aqui.")
        
        st.markdown("---")
        
        st.markdown("**DevLab Pro** © 2025")
        st.markdown("Versão 2.5.0")
    
    # Roteamento com base na navegação selecionada
    if navigation == "Início":
        home_page()
    elif navigation == "Laboratório":
        lab_page()
    elif navigation == "Roadmap":
        roadmap_page()
    elif navigation == "Níveis de Carreira":
        career_levels_page()
    elif navigation == "Avaliação de Nível":
        skill_assessment_page()
    elif navigation == "Vagas":
        job_listings_page()
    elif navigation == "Sobre":
        about_page()

# Executar o aplicativo
if __name__ == "__main__":
    main()