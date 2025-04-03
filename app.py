from flask import Flask, render_template, request, jsonify, Blueprint
import json
import os
import random
import logging
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("codelab.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("codelab")

# Inicialização da aplicação Flask
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False  # Mantém a ordem das chaves nos JSONs
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Recarrega templates automaticamente

# Dados do sistema
#===================================================================================
# Níveis de habilidade para desenvolvedores
SKILL_LEVELS = {
    "Iniciante": {
        "description": "Está começando na área de desenvolvimento, conhece o básico de programação",
        "requirements": ["Lógica de programação", "Conhecimentos básicos de HTML/CSS", "Algoritmos simples"],
        "experience": "0-6 meses"
    },
    "Estagiário": {
        "description": "Está em processo de aprendizado formal, aplica conhecimentos básicos sob supervisão",
        "requirements": ["Conhecimento básico em pelo menos uma linguagem", "Entendimento de estruturas de dados básicas", "Noções de controle de versão"],
        "experience": "0-1 ano"
    },
    "Junior": {
        "description": "Profissional em início de carreira, necessita de acompanhamento frequente",
        "requirements": ["Domínio básico de pelo menos uma linguagem", "Experiência com frameworks básicos", "Conhecimento de banco de dados", "Controle de versão (Git)"],
        "experience": "1-2 anos"
    },
    "Pleno": {
        "description": "Profissional autônomo que resolve problemas sem supervisão constante",
        "requirements": ["Domínio sólido de pelo menos uma linguagem", "Experiência com múltiplos frameworks", "Design patterns", "SQL e NoSQL avançado", "Testes automatizados"],
        "experience": "2-5 anos"
    },
    "Sênior": {
        "description": "Referência técnica no time, capaz de tomar decisões arquiteturais",
        "requirements": ["Domínio profundo de múltiplas linguagens", "Arquitetura de software", "Performance e otimização", "Liderança técnica", "DevOps"],
        "experience": "5-8 anos"
    },
    "Staff": {
        "description": "Influencia múltiplos times e projetos com decisões técnicas de alto impacto",
        "requirements": ["Arquitetura de sistemas distribuídos", "Decisões técnicas estratégicas", "Mentoria de desenvolvedores", "Inovação tecnológica"],
        "experience": "8-12 anos"
    },
    "Especialista": {
        "description": "Autoridade reconhecida em áreas específicas da tecnologia",
        "requirements": ["Conhecimento de estado da arte em áreas específicas", "Contribuições para comunidade", "Pesquisa e inovação", "Visão tecnológica de longo prazo"],
        "experience": "10+ anos"
    }
}

# Tecnologias disponíveis no sistema
TECHNOLOGIES = [
    {"name": "Node.js", "type": "Backend"},
    {"name": "Express", "type": "Backend Framework"},
    {"name": "NestJS", "type": "Backend Framework"},
    {"name": "Fastify", "type": "Backend Framework"},
    {"name": "React", "type": "Frontend"},
    {"name": "Angular", "type": "Frontend"},
    {"name": "Vue.js", "type": "Frontend"},
    {"name": "MongoDB", "type": "Database"},
    {"name": "PostgreSQL", "type": "Database"},
    {"name": "Docker", "type": "DevOps"},
    {"name": "Kubernetes", "type": "DevOps"},
    {"name": "Python", "type": "Backend/Data Science"},
    {"name": "Django", "type": "Backend Framework"},
    {"name": "Flask", "type": "Backend Framework"},
    {"name": "GraphQL", "type": "API"},
    {"name": "TypeScript", "type": "Language"},
    {"name": "JavaScript", "type": "Language"},
    {"name": "Git", "type": "Version Control"},
    {"name": "AWS", "type": "Cloud"},
    {"name": "Azure", "type": "Cloud"}
]

# Áreas da tecnologia e suas características
TECH_AREAS = {
    "Backend": {
        "description": "Desenvolvimento do servidor, APIs e lógica de negócios",
        "core_skills": ["Node.js", "Python", "Java", "C#", "PHP", "Ruby", "Go"],
        "frameworks": ["Express", "NestJS", "Fastify", "Django", "Spring", "Laravel", "Ruby on Rails"],
        "databases": ["MongoDB", "PostgreSQL", "MySQL", "SQLite", "Redis", "Cassandra", "DynamoDB"],
        "tools": ["Docker", "Kubernetes", "Git", "CI/CD", "RabbitMQ", "Kafka"]
    },
    "Frontend": {
        "description": "Desenvolvimento de interfaces de usuário e experiência do cliente",
        "core_skills": ["JavaScript", "TypeScript", "HTML", "CSS", "Responsive Design", "Web Accessibility"],
        "frameworks": ["React", "Angular", "Vue.js", "Svelte", "Next.js", "Nuxt.js"],
        "tools": ["Webpack", "Babel", "ESLint", "Jest", "Cypress", "Storybook"]
    },
    "FullStack": {
        "description": "Desenvolvimento completo, combinando habilidades de frontend e backend",
        "core_skills": ["JavaScript/TypeScript", "Node.js", "HTML/CSS", "SQL/NoSQL"],
        "frameworks": ["MERN (MongoDB, Express, React, Node.js)", "MEAN (MongoDB, Express, Angular, Node.js)", "Next.js + Express", "Django + React"],
        "tools": ["Git", "Docker", "CI/CD", "Testing tools"]
    },
    "DevOps": {
        "description": "Integração de desenvolvimento e operações para entrega contínua",
        "core_skills": ["Linux/Unix", "Networking", "Cloud Infrastructure", "Scripting (Bash, Python)"],
        "tools": ["Docker", "Kubernetes", "Terraform", "Ansible", "Jenkins", "GitHub Actions", "ArgoCD"],
        "platforms": ["AWS", "Azure", "GCP", "DigitalOcean"]
    },
    "QA/Testing": {
        "description": "Garantia de qualidade e teste de software",
        "core_skills": ["Test Planning", "Test Automation", "Performance Testing", "Security Testing"],
        "tools": ["Selenium", "Jest", "Cypress", "JUnit", "PyTest", "Postman"]
    },
    "Data Science": {
        "description": "Análise e interpretação de dados complexos",
        "core_skills": ["Python", "R", "Statistics", "Machine Learning", "Data Visualization"],
        "libraries": ["Pandas", "NumPy", "scikit-learn", "TensorFlow", "PyTorch"],
        "tools": ["Jupyter", "Tableau", "Power BI"]
    },
    "Security": {
        "description": "Proteção de sistemas e dados contra ameaças",
        "core_skills": ["Network Security", "Application Security", "Cryptography", "Ethical Hacking"],
        "tools": ["OWASP tools", "Burp Suite", "Wireshark", "Metasploit"]
    }
}

# Geradores de conteúdo
#===================================================================================
def generate_exercises(technology, level):
    """
    Gera exercícios dinâmicos para uma tecnologia e nível específicos.
    
    Args:
        technology (str): Nome da tecnologia
        level (str): Nível de dificuldade (Básico, Intermediário, Avançado)
        
    Returns:
        list: Lista de exercícios gerados
    """
    exercises = []
    
    # Níveis: Básico, Intermediário, Avançado
    difficulty_levels = {
        "Básico": ["Criar um 'Hello World'", "Trabalhar com variáveis", "Implementar estruturas condicionais", 
                "Usar loops", "Criar funções simples", "Manipular arrays/listas"],
        
        "Intermediário": ["Usar programação orientada a objetos", "Implementar padrões de design", 
                        "Trabalhar com requisições assíncronas", "Manipular dados JSON", 
                        "Criar middlewares", "Implementar autenticação"],
        
        "Avançado": ["Otimizar performance", "Implementar arquitetura de microsserviços", 
                    "Criar sistemas distribuídos", "Trabalhar com streams de dados", 
                    "Implementar segurança avançada", "Deployar em ambientes de produção"]
    }
    
    # Gera temas de exercícios baseados na tecnologia
    tech_specific_themes = {
        "Node.js": ["API REST", "Manipulação de arquivos", "Streams", "Event Loop", "Módulos nativos"],
        "Express": ["Rotas", "Middlewares", "Templates", "Autenticação", "MVC"],
        "NestJS": ["Módulos", "Controladores", "Providers", "Guards", "Interceptors", "Pipes"],
        "Fastify": ["Plugins", "Hooks", "Schemas", "Serialização", "Validação"],
        "React": ["Componentes", "Props", "Estado", "Hooks", "Context API", "Redux"],
        "MongoDB": ["CRUD", "Aggregation", "Indexes", "Schema Design", "Transactions"],
        "PostgreSQL": ["Queries", "Joins", "Transactions", "Stored Procedures", "Triggers"],
        "Docker": ["Containers", "Dockerfile", "Multi-stage builds", "Networks", "Volumes"],
    }
    
    # Pega temas específicos ou usa genéricos
    themes = tech_specific_themes.get(technology, ["API", "CRUD", "Autenticação", "Performance", "Testes"])
    
    # Gera exercícios baseados no nível de dificuldade e nos temas
    base_tasks = difficulty_levels.get(level, difficulty_levels["Básico"])
    
    for i in range(15):  # Gera 15 exercícios por nível (na versão completa seriam mais)
        task = random.choice(base_tasks)
        theme = random.choice(themes)
        exercises.append({
            "id": f"{technology}-{level}-{i+1}",
            "title": f"{task} com {theme} em {technology}",
            "description": f"Exercício para {task.lower()} implementando {theme} utilizando {technology}.",
            "difficulty": level,
            "estimated_time": f"{random.randint(1, 4)} horas"
        })
    
    return exercises

def generate_projects(technology):
    """
    Gera projetos para uma tecnologia específica.
    
    Args:
        technology (str): Nome da tecnologia
        
    Returns:
        list: Lista de projetos gerados
    """
    # Lista de tipos de projetos
    project_types = [
        "API REST", "Autenticação JWT", "Dashboard", "E-commerce", "Blog", 
        "Sistema de gerenciamento", "Chat em tempo real", "Aplicativo de tarefas",
        "Integração com API externa", "Microserviço", "Sistema de notificações",
        "Upload de arquivos", "Sistema de logs", "Monitoramento", "Gateway de pagamento"
    ]
    
    # Características por nível
    level_features = {
        "Básico": ["CRUD simples", "Autenticação básica", "Interface mínima", "Persistência de dados local"],
        "Intermediário": ["Relações entre entidades", "Autenticação JWT", "Interface responsiva", "Validações avançadas"],
        "Avançado": ["Arquitetura escalável", "Microsserviços", "Cache", "Mensageria", "CI/CD", "Monitoramento"]
    }
    
    projects = []
    
    # Gera projetos para cada nível
    for level in ["Básico", "Intermediário", "Avançado"]:
        # Cria aproximadamente 13-14 projetos por nível (40 no total)
        for i in range(13):
            project_type = random.choice(project_types)
            features = random.sample(level_features[level], min(3, len(level_features[level])))
            
            projects.append({
                "id": f"{technology}-{level}-project-{i+1}",
                "title": f"{project_type} com {technology}",
                "description": f"Desenvolva um sistema de {project_type.lower()} utilizando {technology}.",
                "features": features,
                "difficulty": level,
                "estimated_time": f"{random.randint(5, 30)} horas"
            })
    
    return projects

def get_courses_for_technology(technology):
    """
    Retorna cursos disponíveis para uma tecnologia específica.
    
    Args:
        technology (str): Nome da tecnologia
        
    Returns:
        list: Lista de cursos para a tecnologia
    """
    courses = []
    levels = ["Básico", "Intermediário", "Avançado"]
    
    for level in levels:
        courses.append({
            "title": f"{technology} {level}",
            "description": f"Aprenda os fundamentos de {technology} desde o início até aplicações completas.",
            "level": level,
            "duration": f"{random.randint(10, 50)} horas",
            "topics": [f"Introdução a {technology}", f"Fundamentos de {technology}", 
                    f"Aplicações práticas com {technology}", f"Projetos com {technology}"]
        })
    
    return courses

def get_code_examples(technology, level):
    """
    Retorna exemplos de código para uma tecnologia e nível específicos.
    
    Args:
        technology (str): Nome da tecnologia
        level (str): Nível de complexidade
        
    Returns:
        str: Código de exemplo
    """
    examples = {
        "Node.js": {
            "Básico": """
// Hello World em Node.js
console.log('Hello, World!');

// Servidor HTTP básico
const http = require('http');

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World');
});

server.listen(3000, () => {
  console.log('Servidor rodando em http://localhost:3000/');
});
""",
            "Intermediário": """
// API Express com middleware e rotas
const express = require('express');
const app = express();

// Middleware para logging
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);
  next();
});

// Middleware para parsing de JSON
app.use(express.json());

// Rota com parâmetros
app.get('/users/:id', (req, res) => {
  const userId = req.params.id;
  res.json({ id: userId, name: 'Usuário Exemplo' });
});

app.listen(3000, () => {
  console.log('API rodando na porta 3000');
});
""",
            "Avançado": """
// Aplicação Node.js com conexão ao banco e padrão Repository
const express = require('express');
const { MongoClient, ObjectId } = require('mongodb');

class UserRepository {
  constructor(db) {
    this.collection = db.collection('users');
  }

  async findAll() {
    return await this.collection.find().toArray();
  }

  async findById(id) {
    return await this.collection.findOne({ _id: new ObjectId(id) });
  }

  async create(userData) {
    const result = await this.collection.insertOne(userData);
    return result.insertedId;
  }
}

async function startServer() {
  const client = new MongoClient('mongodb://localhost:27017');
  await client.connect();
  
  const db = client.db('app_database');
  const userRepository = new UserRepository(db);
  
  const app = express();
  app.use(express.json());
  
  app.get('/users', async (req, res) => {
    try {
      const users = await userRepository.findAll();
      res.json(users);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });
  
  app.listen(3000, () => {
    console.log('Server running on port 3000');
  });
  
  process.on('SIGINT', async () => {
    await client.close();
    process.exit(0);
  });
}

startServer().catch(console.error);
"""
        },
        "Express": {
            "Básico": """
// Aplicação Express básica
const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
""",
            "Intermediário": """
// API REST com Express
const express = require('express');
const app = express();
const port = 3000;

// Middleware
app.use(express.json());

// Simulando um banco de dados
let users = [
  { id: 1, name: 'Alice', email: 'alice@example.com' },
  { id: 2, name: 'Bob', email: 'bob@example.com' }
];

// Rotas
app.get('/users', (req, res) => {
  res.json(users);
});

app.get('/users/:id', (req, res) => {
  const user = users.find(u => u.id === parseInt(req.params.id));
  if (!user) return res.status(404).json({ message: 'User not found' });
  res.json(user);
});

app.post('/users', (req, res) => {
  const user = {
    id: users.length + 1,
    name: req.body.name,
    email: req.body.email
  };
  users.push(user);
  res.status(201).json(user);
});

app.put('/users/:id', (req, res) => {
  const user = users.find(u => u.id === parseInt(req.params.id));
  if (!user) return res.status(404).json({ message: 'User not found' });
  
  user.name = req.body.name;
  user.email = req.body.email;
  
  res.json(user);
});

app.delete('/users/:id', (req, res) => {
  const userIndex = users.findIndex(u => u.id === parseInt(req.params.id));
  if (userIndex === -1) return res.status(404).json({ message: 'User not found' });
  
  users.splice(userIndex, 1);
  res.status(204).end();
});

app.listen(port, () => {
  console.log(`API running at http://localhost:${port}`);
});
""",
            "Avançado": """
// API Express com autenticação JWT e organização MVC
const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const { body, validationResult } = require('express-validator');

// Controllers
class AuthController {
  static async login(req, res) {
    try {
      const { email, password } = req.body;
      
      // Verificação de usuário simulada
      const user = await UserModel.findByEmail(email);
      if (!user) {
        return res.status(401).json({ message: 'Invalid credentials' });
      }
      
      const passwordValid = await bcrypt.compare(password, user.password);
      if (!passwordValid) {
        return res.status(401).json({ message: 'Invalid credentials' });
      }
      
      const token = jwt.sign(
        { id: user.id, email: user.email },
        process.env.JWT_SECRET,
        { expiresIn: '1h' }
      );
      
      res.json({ token });
    } catch (error) {
      res.status(500).json({ message: error.message });
    }
  }
}

class UserController {
  static async getAll(req, res) {
    try {
      const users = await UserModel.findAll();
      res.json(users);
    } catch (error) {
      res.status(500).json({ message: error.message });
    }
  }
  
  static async getById(req, res) {
    try {
      const user = await UserModel.findById(req.params.id);
      if (!user) {
        return res.status(404).json({ message: 'User not found' });
      }
      res.json(user);
    } catch (error) {
      res.status(500).json({ message: error.message });
    }
  }
}

// Middlewares
const authMiddleware = (req, res, next) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) {
      return res.status(401).json({ message: 'Authentication required' });
    }
    
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ message: 'Invalid token' });
  }
};

const validationMiddleware = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }
  next();
};

// Routes
const app = express();
app.use(express.json());

// Auth routes
app.post(
  '/login',
  [
    body('email').isEmail(),
    body('password').isLength({ min: 6 }),
    validationMiddleware
  ],
  AuthController.login
);

// User routes
app.get('/users', authMiddleware, UserController.getAll);
app.get('/users/:id', authMiddleware, UserController.getById);

// Error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ message: 'Something went wrong!' });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
"""
        },
        "NestJS": {
            "Básico": """
// main.ts - Ponto de entrada do aplicativo NestJS
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(3000);
}
bootstrap();

// app.module.ts - Módulo principal
import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';

@Module({
  imports: [],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}

// app.controller.ts - Controlador básico
import { Controller, Get } from '@nestjs/common';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }
}

// app.service.ts - Serviço básico
import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
  getHello(): string {
    return 'Hello World!';
  }
}
""",
            "Intermediário": """
// users.controller.ts - Controlador CRUD para usuários
import { 
  Controller, 
  Get, 
  Post, 
  Put, 
  Delete, 
  Param, 
  Body, 
  UseGuards 
} from '@nestjs/common';
import { UsersService } from './users.service';
import { CreateUserDto } from './dto/create-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get()
  findAll() {
    return this.usersService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.usersService.findOne(id);
  }

  @Post()
  @UseGuards(JwtAuthGuard)
  create(@Body() createUserDto: CreateUserDto) {
    return this.usersService.create(createUserDto);
  }

  @Put(':id')
  @UseGuards(JwtAuthGuard)
  update(@Param('id') id: string, @Body() updateUserDto: UpdateUserDto) {
    return this.usersService.update(id, updateUserDto);
  }

  @Delete(':id')
  @UseGuards(JwtAuthGuard)
  remove(@Param('id') id: string) {
    return this.usersService.remove(id);
  }
}

// create-user.dto.ts - DTO para criação de usuário
import { IsEmail, IsNotEmpty, MinLength } from 'class-validator';

export class CreateUserDto {
  @IsNotEmpty()
  name: string;

  @IsEmail()
  email: string;

  @MinLength(6)
  password: string;
}

// users.service.ts - Serviço para usuários
import { Injectable, NotFoundException } from '@nestjs/common';
import { CreateUserDto } from './dto/create-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';

@Injectable()
export class UsersService {
  private users = [];

  findAll() {
    return this.users;
  }

  findOne(id: string) {
    const user = this.users.find(user => user.id === id);
    if (!user) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }
    return user;
  }

  create(createUserDto: CreateUserDto) {
    const newUser = {
      id: Date.now().toString(),
      ...createUserDto,
    };
    this.users.push(newUser);
    return newUser;
  }

  update(id: string, updateUserDto: UpdateUserDto) {
    const userIndex = this.users.findIndex(user => user.id === id);
    if (userIndex === -1) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }
    
    this.users[userIndex] = {
      ...this.users[userIndex],
      ...updateUserDto,
    };
    
    return this.users[userIndex];
  }

  remove(id: string) {
    const userIndex = this.users.findIndex(user => user.id === id);
    if (userIndex === -1) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }
    
    this.users.splice(userIndex, 1);
    return { deleted: true };
  }
}
""",
            "Avançado": """
// Exemplo avançado de NestJS com TypeORM, autenticação e microsserviços

// app.module.ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { UsersModule } from './users/users.module';
import { AuthModule } from './auth/auth.module';
import { ProductsModule } from './products/products.module';
import { OrdersModule } from './orders/orders.module';
import { ClientsModule, Transport } from '@nestjs/microservices';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: `.env.${process.env.NODE_ENV}`,
    }),
    TypeOrmModule.forRootAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: async (configService: ConfigService) => ({
        type: 'postgres',
        host: configService.get('DB_HOST'),
        port: configService.get('DB_PORT'),
        username: configService.get('DB_USERNAME'),
        password: configService.get('DB_PASSWORD'),
        database: configService.get('DB_DATABASE'),
        entities: [__dirname + '/**/*.entity{.ts,.js}'],
        synchronize: configService.get('NODE_ENV') !== 'production',
      }),
    }),
    ClientsModule.registerAsync([
      {
        name: 'NOTIFICATION_SERVICE',
        imports: [ConfigModule],
        inject: [ConfigService],
        useFactory: (configService: ConfigService) => ({
          transport: Transport.RMQ,
          options: {
            urls: [configService.get('RABBITMQ_URL')],
            queue: 'notifications_queue',
            queueOptions: {
              durable: true,
            },
          },
        }),
      },
    ]),
    UsersModule,
    AuthModule,
    ProductsModule,
    OrdersModule,
  ],
})
export class AppModule {}

// users/user.entity.ts
import {
  Entity,
  Column,
  PrimaryGeneratedColumn,
  CreateDateColumn,
  UpdateDateColumn,
  OneToMany,
  BeforeInsert,
} from 'typeorm';
import { Order } from '../orders/order.entity';
import * as bcrypt from 'bcrypt';

@Entity()
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  name: string;

  @Column({ unique: true })
  email: string;

  @Column()
  password: string;

  @Column({ default: 'user' })
  role: string;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;

  @OneToMany(() => Order, order => order.user)
  orders: Order[];

  @BeforeInsert()
  async hashPassword() {
    this.password = await bcrypt.hash(this.password, 10);
  }
}

// auth/auth.service.ts
import { Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { UsersService } from '../users/users.service';
import * as bcrypt from 'bcrypt';

@Injectable()
export class AuthService {
  constructor(
    private usersService: UsersService,
    private jwtService: JwtService,
  ) {}

  async validateUser(email: string, password: string): Promise<any> {
    const user = await this.usersService.findByEmail(email);
    if (!user) {
      throw new UnauthorizedException('Invalid credentials');
    }
    
    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      throw new UnauthorizedException('Invalid credentials');
    }
    
    const { password: _, ...result } = user;
    return result;
  }

  async login(user: any) {
    const payload = { email: user.email, sub: user.id, role: user.role };
    return {
      access_token: this.jwtService.sign(payload),
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role,
      },
    };
  }
}

// orders/orders.controller.ts
import { 
  Controller, 
  Get, 
  Post, 
  Body, 
  Param, 
  UseGuards,
  Inject 
} from '@nestjs/common';
import { OrdersService } from './orders.service';
import { CreateOrderDto } from './dto/create-order.dto';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { RolesGuard } from '../auth/roles.guard';
import { Roles } from '../auth/roles.decorator';
import { ClientProxy } from '@nestjs/microservices';

@Controller('orders')
@UseGuards(JwtAuthGuard, RolesGuard)
export class OrdersController {
  constructor(
    private readonly ordersService: OrdersService,
    @Inject('NOTIFICATION_SERVICE') private notificationClient: ClientProxy,
  ) {}

  @Post()
  async create(@Body() createOrderDto: CreateOrderDto) {
    const order = await this.ordersService.create(createOrderDto);
    
    // Enviar notificação para o microserviço
    this.notificationClient.emit('order_created', {
      orderId: order.id,
      userId: order.userId,
      totalAmount: order.totalAmount,
    });
    
    return order;
  }

  @Get()
  @Roles('admin')
  findAll() {
    return this.ordersService.findAll();
  }

  @Get('user/:userId')
  findByUser(@Param('userId') userId: string) {
    return this.ordersService.findByUser(userId);
  }
}
"""
        },
        "Fastify": {
            "Básico": """
// Servidor Fastify básico
const fastify = require('fastify')({ logger: true });

// Declarar uma rota
fastify.get('/', async (request, reply) => {
  return { hello: 'world' };
});

// Executar o servidor
const start = async () => {
  try {
    await fastify.listen(3000);
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

start();
""",
            "Intermediário": """
// API Fastify com plugins e esquemas
const fastify = require('fastify')({ logger: true });

// Registrar plugin para suporte a CORS
fastify.register(require('@fastify/cors'));

// Registrar plugin para suporte a JWT
fastify.register(require('@fastify/jwt'), {
  secret: 'supersecret'
});

// Definir esquema para validação
const userSchema = {
  type: 'object',
  required: ['username', 'email', 'password'],
  properties: {
    username: { type: 'string' },
    email: { type: 'string', format: 'email' },
    password: { type: 'string', minLength: 6 }
  }
};

// Middleware de autenticação
fastify.decorate('authenticate', async (request, reply) => {
  try {
    await request.jwtVerify();
  } catch (err) {
    reply.send(err);
  }
});

// Rotas
fastify.post('/register', {
  schema: {
    body: userSchema,
    response: {
      201: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          username: { type: 'string' },
          email: { type: 'string' }
        }
      }
    }
  }
}, async (request, reply) => {
  const { username, email, password } = request.body;
  
  // Simulando criação de usuário
  const userId = Date.now().toString();
  
  reply.code(201).send({
    id: userId,
    username,
    email
  });
});

fastify.post('/login', async (request, reply) => {
  const { email, password } = request.body;
  
  // Simulando verificação de usuário
  if (email === 'user@example.com' && password === 'password') {
    const token = fastify.jwt.sign({ email });
    return { token };
  }
  
  reply.code(401).send({ error: 'Invalid credentials' });
});

fastify.get('/protected', {
  preHandler: [fastify.authenticate]
}, async (request, reply) => {
  return { user: request.user };
});

// Iniciar servidor
const start = async () => {
  try {
    await fastify.listen(3000);
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

start();
""",
            "Avançado": """
// Aplicação Fastify avançada com TypeScript
import fastify, { FastifyInstance, FastifyRequest, FastifyReply } from 'fastify';
import { Server, IncomingMessage, ServerResponse } from 'http';
import fastifyJwt from '@fastify/jwt';
import fastifyCors from '@fastify/cors';
import fastifySwagger from '@fastify/swagger';
import fastifyRateLimit from '@fastify/rate-limit';
import { PrismaClient } from '@prisma/client';

// Tipos
interface IUser {
  id: string;
  email: string;
  name: string;
  role: string;
}

interface IJwtPayload {
  id: string;
  email: string;
  role: string;
}

// Plugin de autenticação
async function authPlugin(fastify: FastifyInstance) {
  fastify.decorate(
    'authenticate',
    async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        await request.jwtVerify<IJwtPayload>();
      } catch (err) {
        reply.send(err);
      }
    }
  );
  
  fastify.decorate(
    'authorizeAdmin',
    async (request: FastifyRequest, reply: FastifyReply) => {
      if (request.user.role !== 'admin') {
        return reply.code(403).send({
          error: 'Forbidden',
          message: 'Admin role required',
        });
      }
    }
  );
}

// Aplicação principal
async function build(): Promise<FastifyInstance> {
  const app: FastifyInstance = fastify({
    logger: {
      level: process.env.LOG_LEVEL || 'info',
    },
  });
  
  // Base de dados
  const prisma = new PrismaClient();
  
  // Plugins globais
  app.register(fastifyCors, {
    origin: process.env.CORS_ORIGIN || true,
  });
  
  app.register(fastifyJwt, {
    secret: process.env.JWT_SECRET || 'supersecret',
    sign: {
      expiresIn: '1h',
    },
  });
  
  app.register(fastifySwagger, {
    routePrefix: '/documentation',
    swagger: {
      info: {
        title: 'Fastify API',
        description: 'API documentation',
        version: '1.0.0',
      },
      externalDocs: {
        url: 'https://swagger.io',
        description: 'Find more info here',
      },
      host: 'localhost:3000',
      schemes: ['http'],
      consumes: ['application/json'],
      produces: ['application/json'],
    },
    exposeRoute: true,
  });
  
  app.register(fastifyRateLimit, {
    max: 100,
    timeWindow: '1 minute',
  });
  
  // Registrar plugin de autenticação
  app.register(authPlugin);
  
  // Rotas
  app.post('/register', {
    schema: {
      body: {
        type: 'object',
        required: ['email', 'password', 'name'],
        properties: {
          email: { type: 'string', format: 'email' },
          password: { type: 'string', minLength: 6 },
          name: { type: 'string' },
        },
      },
    },
  }, async (request, reply) => {
    const { email, password, name } = request.body as any;
    
    try {
      // Verificar se usuário já existe
      const existingUser = await prisma.user.findUnique({
        where: { email },
      });
      
      if (existingUser) {
        return reply.code(400).send({
          error: 'Bad Request',
          message: 'Email already registered',
        });
      }
      
      // Criar usuário
      const user = await prisma.user.create({
        data: {
          email,
          password: await app.bcrypt.hash(password),
          name,
          role: 'user',
        },
      });
      
      // Remover senha do resultado
      const { password: _, ...userData } = user;
      
      reply.code(201).send(userData);
    } catch (error) {
      request.log.error(error);
      reply.code(500).send({
        error: 'Internal Server Error',
        message: 'Something went wrong',
      });
    }
  });
  
  app.post('/login', async (request, reply) => {
    const { email, password } = request.body as any;
    
    try {
      const user = await prisma.user.findUnique({
        where: { email },
      });
      
      if (!user) {
        return reply.code(401).send({
          error: 'Unauthorized',
          message: 'Invalid credentials',
        });
      }
      
      const validPassword = await app.bcrypt.compare(password, user.password);
      
      if (!validPassword) {
        return reply.code(401).send({
          error: 'Unauthorized',
          message: 'Invalid credentials',
        });
      }
      
      const token = app.jwt.sign({
        id: user.id,
        email: user.email,
        role: user.role,
      });
      
      const { password: _, ...userData } = user;
      
      reply.send({
        user: userData,
        token,
      });
    } catch (error) {
      request.log.error(error);
      reply.code(500).send({
        error: 'Internal Server Error',
        message: 'Something went wrong',
      });
    }
  });
  
  // Rota protegida
  app.get(
    '/users',
    {
      preHandler: [
        app.authenticate,
        app.authorizeAdmin,
      ],
    },
    async (request, reply) => {
      try {
        const users = await prisma.user.findMany({
          select: {
            id: true,
            email: true,
            name: true,
            role: true,
            createdAt: true,
          },
        });
        
        reply.send(users);
      } catch (error) {
        request.log.error(error);
        reply.code(500).send({
          error: 'Internal Server Error',
          message: 'Something went wrong',
        });
      }
    }
  );
  
  // Tratamento de erros 404
  app.setNotFoundHandler((request, reply) => {
    reply.code(404).send({
      error: 'Not Found',
      message: `Route ${request.method}:${request.url} not found`,
    });
  });
  
  // Tratamento de erros globais
  app.setErrorHandler((error, request, reply) => {
    request.log.error(error);
    reply.code(500).send({
      error: 'Internal Server Error',
      message: 'Something went wrong',
    });
  });
  
  return app;
}

// Iniciar servidor
async function start() {
  try {
    const app = await build();
    
    await app.listen({
      port: parseInt(process.env.PORT || '3000'),
      host: '0.0.0.0',
    });
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
}

start();
"""
        },
    }
    
    return examples.get(technology, {}).get(level, "// Código de exemplo não disponível para esta tecnologia e nível.")

# Criação de Blueprints para organizar as rotas
#===================================================================================

# Blueprint para páginas principais
main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index():
    """Renderiza a página inicial do CodeLab."""
    logger.info("Acessando página inicial")
    return render_template('index.html', levels=SKILL_LEVELS)

@main_routes.route('/about')
def about():
    """Renderiza a página 'Sobre' com informações do projeto."""
    logger.info("Acessando página sobre")
    return render_template('about.html', levels=SKILL_LEVELS)

# Blueprint para o laboratório e recursos de aprendizado
learning_routes = Blueprint('learning', __name__, url_prefix='/learning')

@learning_routes.route('/laboratory')
def laboratory():
    """Renderiza a página do laboratório com recursos por tecnologia."""
    logger.info("Acessando laboratório")
    return render_template('laboratory.html', technologies=TECHNOLOGIES)

@learning_routes.route('/roadmap')
def roadmap():
    """Renderiza a página de roadmaps de desenvolvimento."""
    logger.info("Acessando roadmaps")
    return render_template('roadmap.html', tech_areas=TECH_AREAS, levels=SKILL_LEVELS)

@learning_routes.route('/codes')
def codes():
    """Renderiza a página de exemplos de código."""
    logger.info("Acessando exemplos de código")
    return render_template('codes.html', technologies=TECHNOLOGIES, levels=SKILL_LEVELS)

@learning_routes.route('/practice')
def practice():
    """Renderiza a página de exercícios e projetos práticos."""
    logger.info("Acessando página de prática")
    return render_template('practice.html', technologies=TECHNOLOGIES, levels=SKILL_LEVELS)

@learning_routes.route('/scripts')
def scripts():
    """Renderiza a página de scripts úteis."""
    logger.info("Acessando página de scripts")
    return render_template('scripts.html', levels=SKILL_LEVELS)

# Blueprint para carreira e nível profissional
career_routes = Blueprint('career', __name__, url_prefix='/career')

@career_routes.route('/jobs')
def jobs():
    """Renderiza a página de vagas de trabalho."""
    logger.info("Acessando página de vagas")
    return render_template('jobs.html', tech_areas=TECH_AREAS, levels=SKILL_LEVELS)

@career_routes.route('/skill-level')
def skill_level():
    """Renderiza a página de níveis de habilidade."""
    logger.info("Acessando página de níveis de habilidade")
    return render_template('skill-level.html', levels=SKILL_LEVELS)

@career_routes.route('/level-finder')
def level_finder():
    """Renderiza a ferramenta para descobrir o nível de carreira."""
    logger.info("Acessando ferramenta de descoberta de nível")
    return render_template('level-finder.html', technologies=TECHNOLOGIES, tech_areas=TECH_AREAS, levels=SKILL_LEVELS)

# Blueprint para API
api_routes = Blueprint('api', __name__, url_prefix='/api')

@api_routes.route('/exercises/<technology>/<level>')
def api_exercises(technology, level):
    """
    API para obter exercícios por tecnologia e nível.
    
    Args:
        technology (str): Nome da tecnologia
        level (str): Nível de dificuldade
        
    Returns:
        JSON: Lista de exercícios
    """
    logger.info(f"API: Buscando exercícios para {technology} nível {level}")
    return jsonify(generate_exercises(technology, level))

@api_routes.route('/projects/<technology>')
def api_projects(technology):
    """
    API para obter projetos por tecnologia.
    
    Args:
        technology (str): Nome da tecnologia
        
    Returns:
        JSON: Lista de projetos
    """
    logger.info(f"API: Buscando projetos para {technology}")
    return jsonify(generate_projects(technology))

@api_routes.route('/courses/<technology>')
def api_courses(technology):
    """
    API para obter cursos por tecnologia.
    
    Args:
        technology (str): Nome da tecnologia
        
    Returns:
        JSON: Lista de cursos
    """
    logger.info(f"API: Buscando cursos para {technology}")
    return jsonify(get_courses_for_technology(technology))

@api_routes.route('/code-examples/<technology>/<level>')
def api_code_examples(technology, level):
    """
    API para obter exemplos de código por tecnologia e nível.
    
    Args:
        technology (str): Nome da tecnologia
        level (str): Nível de complexidade
        
    Returns:
        JSON: Exemplo de código
    """
    logger.info(f"API: Buscando exemplo de código para {technology} nível {level}")
    return jsonify({"code": get_code_examples(technology, level)})

@api_routes.route('/find-level', methods=['POST'])
def api_find_level():
    """
    API para determinar o nível profissional baseado em habilidades.
    
    Returns:
        JSON: Nível profissional e detalhes
    """
    skills = request.json.get('skills', [])
    tech_areas = request.json.get('techAreas', [])
    
    logger.info(f"API: Avaliando nível para {len(skills)} habilidades e {len(tech_areas)} áreas")
    
    # Avaliação básica de nível baseada em quantidade e tipos de habilidades
    total_skills = len(skills) + len(tech_areas)
    
    # Implementação básica, em produção seria algo mais sofisticado
    if total_skills < 3:
        level = "Iniciante"
    elif total_skills < 5:
        level = "Estagiário"
    elif total_skills < 8:
        level = "Junior" 
    elif total_skills < 12:
        level = "Pleno"
    elif total_skills < 15:
        level = "Sênior"
    elif total_skills < 18:
        level = "Staff"
    else:
        level = "Especialista"
        
    return jsonify({
        "level": level,
        "description": SKILL_LEVELS[level]["description"],
        "requirements": SKILL_LEVELS[level]["requirements"],
        "experience": SKILL_LEVELS[level]["experience"]
    })

@api_routes.route('/tech-areas')
def api_tech_areas():
    """API para obter todas as áreas de tecnologia."""
    return jsonify(TECH_AREAS)

@api_routes.route('/technologies')
def api_technologies():
    """API para obter todas as tecnologias disponíveis."""
    return jsonify(TECHNOLOGIES)

# Redirecionar rotas antigas para novas (compatibilidade)
#===================================================================================
@app.route('/laboratory')
def redirect_laboratory():
    """Redireciona a rota antiga para a nova."""
    return render_template('laboratory.html', technologies=TECHNOLOGIES)

@app.route('/roadmap')
def redirect_roadmap():
    """Redireciona a rota antiga para a nova."""
    return render_template('roadmap.html', tech_areas=TECH_AREAS, levels=SKILL_LEVELS)

@app.route('/codes')
def redirect_codes():
    """Redireciona a rota antiga para a nova."""
    return render_template('codes.html', technologies=TECHNOLOGIES, levels=SKILL_LEVELS)

@app.route('/practice')
def redirect_practice():
    """Redireciona a rota antiga para a nova."""
    return render_template('practice.html', technologies=TECHNOLOGIES, levels=SKILL_LEVELS)

@app.route('/scripts')
def redirect_scripts():
    """Redireciona a rota antiga para a nova."""
    return render_template('scripts.html', levels=SKILL_LEVELS)

@app.route('/jobs')
def redirect_jobs():
    """Redireciona a rota antiga para a nova."""
    return render_template('jobs.html', tech_areas=TECH_AREAS, levels=SKILL_LEVELS)

@app.route('/skill-level')
def redirect_skill_level():
    """Redireciona a rota antiga para a nova."""
    return render_template('skill-level.html', levels=SKILL_LEVELS)

@app.route('/level-finder')
def redirect_level_finder():
    """Redireciona a rota antiga para a nova."""
    return render_template('level-finder.html', technologies=TECHNOLOGIES, tech_areas=TECH_AREAS, levels=SKILL_LEVELS)

# Registro dos blueprints na aplicação
#===================================================================================
app.register_blueprint(main_routes)
app.register_blueprint(learning_routes)
app.register_blueprint(career_routes)
app.register_blueprint(api_routes)

# Tratamento de erros
#===================================================================================
@app.errorhandler(404)
def page_not_found(e):
    """Handler para erro 404 (página não encontrada)."""
    logger.warning(f"Página não encontrada: {request.path}")
    return render_template('error.html', error_code=404, error_message="Página não encontrada"), 404

@app.errorhandler(500)
def server_error(e):
    """Handler para erro 500 (erro interno do servidor)."""
    logger.error(f"Erro interno do servidor: {str(e)}")
    return render_template('error.html', error_code=500, error_message="Erro interno do servidor"), 500

# Inicialização da aplicação
#===================================================================================
if __name__ == '__main__':
    # Verifica se diretórios importantes existem
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/img', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Informação de inicialização
    logger.info(f"CodeLab iniciado em http://127.0.0.1:5000 - Versão: 1.0.0 - Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Inicia o servidor Flask
    app.run(debug=True)