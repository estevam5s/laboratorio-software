document.addEventListener('DOMContentLoaded', function() {
  // Menu toggle para dispositivos móveis
  const menuToggle = document.querySelector('.menu-toggle');
  const mainNav = document.querySelector('.main-nav');
  
  if (menuToggle && mainNav) {
      menuToggle.addEventListener('click', function() {
          mainNav.classList.toggle('active');
          
          // Alterna o ícone do menu
          const icon = menuToggle.querySelector('i');
          if (icon.classList.contains('fa-bars')) {
              icon.classList.remove('fa-bars');
              icon.classList.add('fa-times');
          } else {
              icon.classList.remove('fa-times');
              icon.classList.add('fa-bars');
          }
      });
  }
  
  // Ativa a guia atual nas navegações com tabs
  const tabItems = document.querySelectorAll('.tab-item');
  if (tabItems.length > 0) {
      tabItems.forEach(tab => {
          tab.addEventListener('click', function() {
              // Remove a classe active de todas as guias
              tabItems.forEach(item => item.classList.remove('active'));
              
              // Adiciona a classe active à guia clicada
              this.classList.add('active');
              
              // Ativa o conteúdo da guia correspondente
              const target = this.dataset.target;
              const tabContents = document.querySelectorAll('.tab-content');
              
              tabContents.forEach(content => {
                  content.classList.remove('active');
                  if (content.id === target) {
                      content.classList.add('active');
                  }
              });
          });
      });
      
      // Ativa a primeira guia por padrão
      tabItems[0].click();
  }
  
  // Código específico para a página de descoberta de nível
  const levelFinderForm = document.getElementById('level-finder-form');
  if (levelFinderForm) {
      levelFinderForm.addEventListener('submit', async function(e) {
          e.preventDefault();
          
          // Coleta todas as habilidades selecionadas
          const selectedTechs = Array.from(document.querySelectorAll('input[name="technologies"]:checked')).map(input => input.value);
          const selectedAreas = Array.from(document.querySelectorAll('input[name="tech_areas"]:checked')).map(input => input.value);
          
          // Envia os dados para a API
          try {
              const response = await fetch('/api/find-level', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json'
                  },
                  body: JSON.stringify({
                      skills: selectedTechs,
                      techAreas: selectedAreas
                  })
              });
              
              const data = await response.json();
              
              // Exibe o resultado
              const resultContainer = document.getElementById('level-result');
              resultContainer.innerHTML = `
                  <div class="alert alert-success">
                      <h3>Seu nível: ${data.level}</h3>
                      <p>${data.description}</p>
                      <h4 class="mt-3">Requisitos para este nível:</h4>
                      <ul class="mt-2">
                          ${data.requirements.map(req => `<li>${req}</li>`).join('')}
                      </ul>
                      <p class="mt-3"><strong>Experiência típica:</strong> ${data.experience}</p>
                  </div>
              `;
              
              // Exibe as recomendações
              showRecommendations(data.level);
              
              // Rola a página para o resultado
              resultContainer.scrollIntoView({ behavior: 'smooth' });
          } catch (error) {
              console.error('Erro ao determinar o nível:', error);
          }
      });
  }
  
  // Função para mostrar recomendações baseadas no nível
  function showRecommendations(level) {
      const recommendationsContainer = document.getElementById('recommendations');
      if (!recommendationsContainer) return;
      
      let levelIndex = 0;
      const levels = ['Iniciante', 'Estagiário', 'Junior', 'Pleno', 'Sênior', 'Staff', 'Especialista'];
      
      levelIndex = levels.indexOf(level);
      
      // Recomendações para cada nível
      const recommendations = {
          'Iniciante': [
              'Fortaleça seus conhecimentos em lógica de programação',
              'Aprenda uma linguagem de programação em profundidade (JavaScript, Python, Java)',
              'Estude estruturas de dados básicas e algoritmos',
              'Faça projetos simples para praticar'
          ],
          'Estagiário': [
              'Aprofunde-se em pelo menos uma stack de desenvolvimento',
              'Aprenda sobre controle de versão (Git)',
              'Pratique com projetos mais complexos',
              'Estude boas práticas de codificação'
          ],
          'Junior': [
              'Aprenda padrões de design de software',
              'Aprofunde-se em bancos de dados e ORM',
              'Estude frameworks populares da sua stack',
              'Aprenda sobre testes automatizados'
          ],
          'Pleno': [
              'Aprenda arquitetura de software',
              'Estude práticas de CI/CD',
              'Aprenda sobre microsserviços e arquiteturas distribuídas',
              'Desenvolva habilidades de mentoria'
          ],
          'Sênior': [
              'Aprenda sobre escalabilidade e performance',
              'Estude práticas de DevOps avançadas',
              'Desenvolva habilidades de liderança técnica',
              'Aprofunde-se em segurança de aplicações'
          ],
          'Staff': [
              'Aprenda sobre arquitetura de sistemas complexos',
              'Desenvolva habilidades de comunicação estratégica',
              'Estude sobre tomada de decisões técnicas de alto impacto',
              'Aprofunde-se em métricas de engenharia e qualidade'
          ],
          'Especialista': [
              'Contribua para projetos open source',
              'Compartilhe conhecimento (palestras, artigos)',
              'Influencie decisões arquiteturais de longo prazo',
              'Mantenha-se atualizado com tendências emergentes'
          ]
      };
      
      // Exibe as recomendações para o nível atual
      recommendationsContainer.innerHTML = `
          <h3 class="mb-3">Recomendações para seu desenvolvimento</h3>
          <div class="card">
              <div class="card-body">
                  <h4>Próximos passos para ${level}</h4>
                  <ul class="mt-3">
                      ${recommendations[level].map(rec => `<li>${rec}</li>`).join('')}
                  </ul>
                  ${levelIndex < levels.length - 1 ? `
                      <div class="mt-4">
                          <h5>Para avançar para ${levels[levelIndex + 1]}, concentre-se em:</h5>
                          <ul class="mt-2">
                              ${recommendations[levels[levelIndex + 1]].slice(0, 2).map(rec => `<li>${rec}</li>`).join('')}
                          </ul>
                      </div>
                  ` : ''}
              </div>
          </div>
      `;
      
      recommendationsContainer.style.display = 'block';
  }
  
  // Manipulação das abas na página de prática e códigos
  const techSelectors = document.querySelectorAll('.tech-selector');
  if (techSelectors.length > 0) {
      techSelectors.forEach(selector => {
          selector.addEventListener('change', function() {
              const technology = this.value;
              const levelSelector = document.querySelector('.level-selector');
              
              if (levelSelector) {
                  loadExercisesOrCodes(technology, levelSelector.value);
              } else {
                  loadProjects(technology);
              }
          });
      });
      
      const levelSelectors = document.querySelectorAll('.level-selector');
      if (levelSelectors.length > 0) {
          levelSelectors.forEach(selector => {
              selector.addEventListener('change', function() {
                  const level = this.value;
                  const technology = document.querySelector('.tech-selector').value;
                  
                  loadExercisesOrCodes(technology, level);
              });
          });
      }
  }
  
  // Carrega exercícios ou exemplos de código da API
  async function loadExercisesOrCodes(technology, level) {
      const exercisesContainer = document.getElementById('exercises-container');
      const codesContainer = document.getElementById('code-examples-container');
      const container = exercisesContainer || codesContainer;
      
      if (!container) return;
      
      container.innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin fa-2x"></i><p>Carregando...</p></div>';
      
      try {
          let data;
          
          if (exercisesContainer) {
              const response = await fetch(`/api/exercises/${technology}/${level}`);
              data = await response.json();
              
              renderExercises(data, container);
          } else {
              const response = await fetch(`/api/code-examples/${technology}/${level}`);
              data = await response.json();
              
              renderCodeExample(data.code, container);
          }
      } catch (error) {
          console.error('Erro ao carregar dados:', error);
          container.innerHTML = `<div class="alert alert-danger">Erro ao carregar os dados. Por favor, tente novamente.</div>`;
      }
  }
  
  // Renderiza exercícios na interface
  function renderExercises(exercises, container) {
      if (exercises.length === 0) {
          container.innerHTML = `<div class="alert alert-info">Nenhum exercício encontrado para esta tecnologia e nível.</div>`;
          return;
      }
      
      let html = '<div class="grid grid-3">';
      
      exercises.forEach(exercise => {
          html += `
              <div class="card exercise-card">
                  <div class="card-body">
                      <span class="badge badge-${getDifficultyClass(exercise.difficulty)} mb-2">${exercise.difficulty}</span>
                      <h3 class="card-title">${exercise.title}</h3>
                      <p>${exercise.description}</p>
                      <div class="exercise-meta">
                          <span><i class="far fa-clock"></i> ${exercise.estimated_time}</span>
                          <a href="#" class="btn btn-sm btn-primary">Iniciar</a>
                      </div>
                  </div>
              </div>
          `;
      });
      
      html += '</div>';
      container.innerHTML = html;
  }
  
  // Renderiza exemplos de código
  function renderCodeExample(code, container) {
      const html = `
          <div class="card">
              <div class="card-body">
                  <pre class="code-block"><code>${escapeHtml(code)}</code></pre>
                  <div class="text-right">
                      <button class="btn btn-sm btn-primary copy-code">Copiar Código</button>
                  </div>
              </div>
          </div>
      `;
      
      container.innerHTML = html;
      
      // Adiciona funcionalidade de copiar código
      const copyButton = container.querySelector('.copy-code');
      if (copyButton) {
          copyButton.addEventListener('click', function() {
              const codeText = code;
              navigator.clipboard.writeText(codeText)
                  .then(() => {
                      this.textContent = 'Copiado!';
                      setTimeout(() => {
                          this.textContent = 'Copiar Código';
                      }, 2000);
                  })
                  .catch(err => {
                      console.error('Erro ao copiar:', err);
                  });
          });
      }
  }
  
  // Carrega projetos da API
  async function loadProjects(technology) {
      const projectsContainer = document.getElementById('projects-container');
      if (!projectsContainer) return;
      
      projectsContainer.innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin fa-2x"></i><p>Carregando...</p></div>';
      
      try {
          const response = await fetch(`/api/projects/${technology}`);
          const projects = await response.json();
          
          if (projects.length === 0) {
              projectsContainer.innerHTML = `<div class="alert alert-info">Nenhum projeto encontrado para esta tecnologia.</div>`;
              return;
          }
          
          // Agrupa projetos por nível
          const groupedProjects = {};
          projects.forEach(project => {
              if (!groupedProjects[project.difficulty]) {
                  groupedProjects[project.difficulty] = [];
              }
              groupedProjects[project.difficulty].push(project);
          });
          
          let html = '';
          
          // Renderiza projetos por nível
          Object.keys(groupedProjects).forEach(level => {
              html += `<h2 class="mb-3 mt-4">Projetos ${level}</h2>`;
              html += '<div class="grid grid-3">';
              
              groupedProjects[level].forEach(project => {
                  html += `
                      <div class="card project-card">
                          <div class="card-body">
                              <span class="badge badge-${getDifficultyClass(project.difficulty)} mb-2">${project.difficulty}</span>
                              <h3 class="card-title">${project.title}</h3>
                              <p>${project.description}</p>
                              <div class="mt-3">
                                  <h4 class="mb-2">Características:</h4>
                                  <ul>
                                      ${project.features.map(feature => `<li>${feature}</li>`).join('')}
                                  </ul>
                              </div>
                              <div class="project-meta">
                                  <span><i class="far fa-clock"></i> ${project.estimated_time}</span>
                                  <a href="#" class="btn btn-sm btn-primary">Iniciar</a>
                              </div>
                          </div>
                      </div>
                  `;
              });
              
              html += '</div>';
          });
          
          projectsContainer.innerHTML = html;
      } catch (error) {
          console.error('Erro ao carregar projetos:', error);
          projectsContainer.innerHTML = `<div class="alert alert-danger">Erro ao carregar os projetos. Por favor, tente novamente.</div>`;
      }
  }
  
  // Utilitário para obter classe de cores baseada na dificuldade
  function getDifficultyClass(difficulty) {
      switch (difficulty) {
          case 'Básico':
              return 'success';
          case 'Intermediário':
              return 'warning';
          case 'Avançado':
              return 'danger';
          default:
              return 'primary';
      }
  }
  
  // Utilitário para escapar HTML
  function escapeHtml(unsafe) {
      return unsafe
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;")
          .replace(/"/g, "&quot;")
          .replace(/'/g, "&#039;");
  }
  
  // Inicia a carga de conteúdo para páginas específicas
  initPageSpecificContent();
});

// Função para inicializar conteúdo específico de cada página
function initPageSpecificContent() {
  // Página inicial
  const featuredTechs = document.getElementById('featured-techs');
  if (featuredTechs) {
      fetchAndRenderTechnologies();
  }
  
  // Página de laboratório
  const labContent = document.getElementById('lab-content');
  if (labContent) {
      const techSelector = document.querySelector('.tech-selector');
      if (techSelector && techSelector.value) {
          fetchAndRenderCourses(techSelector.value);
      }
  }
  
  // Página de prática
  const practiceContent = document.getElementById('exercises-container');
  if (practiceContent) {
      const techSelector = document.querySelector('.tech-selector');
      const levelSelector = document.querySelector('.level-selector');
      if (techSelector && techSelector.value && levelSelector && levelSelector.value) {
          loadExercisesOrCodes(techSelector.value, levelSelector.value);
      }
  }
  
  // Página de projetos
  const projectsContainer = document.getElementById('projects-container');
  if (projectsContainer) {
      const techSelector = document.querySelector('.tech-selector');
      if (techSelector && techSelector.value) {
          loadProjects(techSelector.value);
      }
  }
  
  // Página de exemplos de código
  const codeExamplesContainer = document.getElementById('code-examples-container');
  if (codeExamplesContainer) {
      const techSelector = document.querySelector('.tech-selector');
      const levelSelector = document.querySelector('.level-selector');
      if (techSelector && techSelector.value && levelSelector && levelSelector.value) {
          loadExercisesOrCodes(techSelector.value, levelSelector.value);
      }
  }
}

// Busca e renderiza as tecnologias na página inicial
async function fetchAndRenderTechnologies() {
  const featuredTechs = document.getElementById('featured-techs');
  if (!featuredTechs) return;
  
  try {
      const response = await fetch('/api/technologies');
      const technologies = await response.json();
      
      // Seleciona 6 tecnologias aleatórias para destaque
      const randomTechs = technologies.sort(() => 0.5 - Math.random()).slice(0, 6);
      
      let html = '<div class="grid grid-3">';
      
      randomTechs.forEach(tech => {
          html += `
              <div class="card">
                  <div class="card-body text-center">
                      <div class="feature-icon">
                          <i class="fas fa-code"></i>
                      </div>
                      <h3>${tech.name}</h3>
                      <p>${tech.type}</p>
                      <a href="/laboratory?tech=${tech.name}" class="btn btn-primary mt-3">Explorar</a>
                  </div>
              </div>
          `;
      });
      
      html += '</div>';
      featuredTechs.innerHTML = html;
  } catch (error) {
      console.error('Erro ao carregar tecnologias:', error);
      featuredTechs.innerHTML = '<div class="alert alert-danger">Erro ao carregar tecnologias.</div>';
  }
}

// Busca e renderiza os cursos para uma tecnologia
async function fetchAndRenderCourses(technology) {
  const labContent = document.getElementById('lab-content');
  if (!labContent) return;
  
  try {
      const response = await fetch(`/api/courses/${technology}`);
      const courses = await response.json();
      
      if (courses.length === 0) {
          labContent.innerHTML = '<div class="alert alert-info">Nenhum curso disponível para esta tecnologia.</div>';
          return;
      }
      
      let html = '<div class="grid grid-3">';
      
      courses.forEach(course => {
          html += `
              <div class="card">
                  <div class="card-header">
                      <span class="badge badge-${course.level === 'Básico' ? 'success' : course.level === 'Intermediário' ? 'warning' : 'danger'}">${course.level}</span>
                      <h3 class="card-title mt-2">${course.title}</h3>
                  </div>
                  <div class="card-body">
                      <p>${course.description}</p>
                      <ul class="mt-3">
                          ${course.topics.map(topic => `<li>${topic}</li>`).join('')}
                      </ul>
                  </div>
                  <div class="card-footer">
                      <div class="flex justify-between align-center">
                          <span><i class="far fa-clock"></i> ${course.duration}</span>
                          <a href="#" class="btn btn-primary">Ver curso</a>
                      </div>
                  </div>
              </div>
          `;
      });
      
      html += '</div>';
      labContent.innerHTML = html;
  } catch (error) {
      console.error('Erro ao carregar cursos:', error);
      labContent.innerHTML = '<div class="alert alert-danger">Erro ao carregar cursos.</div>';
  }
}