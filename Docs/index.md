---
hide:
  - navigation
  - toc
---

<!-- HERO SECTION: aparece primeiro -->
<div class="eletta-hero-section" style="position:relative; min-height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:flex-start; padding-top:7vh;">
  <!-- Fundo animado customizado -->
  <div id="eletta-bg" style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:-2;pointer-events:none;">
    <canvas id="eletta-particles" style="width:100vw;height:100vh;display:block;"></canvas>
  </div>

  <!-- Banner animado -->
  <div align="center" style="margin-bottom: 1.5em; display:flex; justify-content:center; align-items:center; height: 260px;">
    <img src="assets/images/logo.png" alt="Eletta Logo" width="270" style="animation: pulse 2s infinite; filter: drop-shadow(0 0 32px #009688cc); display:block; margin:auto;">
  </div>

  <h1 align="center" class="eletta-title" style="font-size: 5em; letter-spacing: 5px; background: linear-gradient(90deg,#009688,#673ab7,#ff9800); -webkit-background-clip: text; color: #fff; animation: gradient-move 8s ease-in-out infinite alternate; text-shadow: 0 5px 12px #000a; margin-bottom: 0.4em; margin-top: 1em;">
    Eletta
  </h1>
  <p align="center" class="eletta-subtitle" style="font-size: 1.5em; color: #fff; margin-bottom: 1.5em; margin-top: 2em; text-shadow: 0 2px 8px #000a;">
    <b>Aplicativo Android de votações presenciais</b><br>
    Transformando decisões em experiências digitais seguras, rápidas e transparentes.
  </p>

  <p align="center">
    <img src="https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white" alt="Android">
    <a href="https://github.com/unb-mds/2025-1-Squad06">
      <img src="https://img.shields.io/badge/GitHub-Eletta-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
    </a>
    <a href="https://miro.com/app/board/uXjVIJOVs_Y=/?moveToWidget=3458764627105264746&cot=14">
      <img src="https://img.shields.io/badge/Miro-Story%20Map-yellow?style=for-the-badge&logo=miro&logoColor=black" alt="Miro">
    </a>
  </p>

  <!-- Botão de chamada para ação -->


  <!-- Seta para rolar -->
  <div id="eletta-scroll-down" class="eletta-scroll-down" title="Ver mais" style="position:absolute;left:50%;bottom:32px;transform:translateX(-50%);z-index:2;cursor:pointer;animation:eletta-bounce 1.6s infinite;font-size:2.5em;color:#fff;opacity:0.8;text-shadow:0 2px 8px #000a;">
    &#8595;
  </div>
</div>

<style>
@keyframes eletta-bounce {
  0%, 100% { transform: translateX(-50%) translateY(0);}
  50% { transform: translateX(-50%) translateY(18px);}
}
.eletta-main-content {
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.6s;
}
.eletta-main-content.eletta-show {
  opacity: 1;
  pointer-events: auto;
  transition: opacity 0.6s;
}
@keyframes pulse {
  0% { transform: scale(1);}
  50% { transform: scale(1.08);}
  100% { transform: scale(1);}
}
@keyframes gradient-move {
  0% { background-position: 0%;}
  100% { background-position: 100%;}
}
@keyframes ctaPulse {
  0% { box-shadow: 0 4px 24px #00968855;}
  100% { box-shadow: 0 8px 32px #ff980055;}
}

/* Esconde o menu de abas superior apenas na página inicial */
body[data-md-path="index"] .md-tabs {
  display: none;
}

@keyframes animStar {
  from { transform: translateY(0px); }
  to { transform: translateY(-2000px); }
}
#stars1, #stars2, #stars3 {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  display: block;
  background: transparent;
}
#stars1 {
  background-image: 
    radial-gradient(1px 1px at 20px 30px, #eee, transparent),
    radial-gradient(1px 1px at 40px 70px, #fff, transparent),
    radial-gradient(1px 1px at 50px 160px, #ddd, transparent),
    radial-gradient(1px 1px at 90px 40px, #fff, transparent),
    radial-gradient(1px 1px at 130px 80px, #fff, transparent),
    radial-gradient(1px 1px at 160px 120px, #ddd, transparent);
  background-repeat: repeat;
  background-size: 200px 200px;
  animation: animStar 50s linear infinite;
}
#stars2 {
  background-image: 
    radial-gradient(1.5px 1.5px at 10px 60px, #fff, transparent),
    radial-gradient(1.5px 1.5px at 80px 20px, #fff, transparent),
    radial-gradient(1.5px 1.5px at 120px 140px, #eee, transparent);
  background-repeat: repeat;
  background-size: 250px 250px;
  animation: animStar 100s linear infinite;
}
#stars3 {
  background-image: 
    radial-gradient(2px 2px at 50px 50px, #fff, transparent),
    radial-gradient(2px 2px at 200px 150px, #eee, transparent),
    radial-gradient(2.5px 2.5px at 300px 80px, #fff, transparent);
  background-repeat: repeat;
  background-size: 350px 350px;
  animation: animStar 150s linear infinite;
}
.feature-card {
  background: linear-gradient(135deg,#e0f7fa 60%,#ede7f6 100%);
  border-radius: 14px;
  box-shadow: 0 2px 12px #0001;
  padding: 1.2em;
  margin: 0.5em 0.5em 1.5em 0.5em;
  min-width: 220px;
  flex: 1;
  transition: transform 0.2s;
}
.feature-card:hover {
  transform: translateY(-6px) scale(1.03);
  box-shadow: 0 6px 24px #0002;
}

/* --- Estilos da Simulação Interativa --- */
.eletta-sim-container {
  background: #fff;
  border-radius: 25px;
  box-shadow: 0 15px 40px rgba(0,0,0,0.5);
  max-width: 280px;
  margin: 2em auto;
  overflow: hidden;
  border: 3px solid #e2e8f0;
  position: relative;
  aspect-ratio: 9/19.5;
}
.eletta-sim-container::before {
  content: '';
  position: absolute;
  top: 6px;
  left: 50%;
  transform: translateX(-50%);
  width: 50px;
  height: 3px;
  background: #d1d5db;
  border-radius: 2px;
  z-index: 2;
}
.eletta-sim-header {
  background: #6366f1;
  padding: 2.5em 1em 1.5em 1em;
  position: relative;
  text-align: center;
}
.eletta-logo {
  color: #fff;
  font-size: 1.8em;
  font-weight: 700;
  text-align: center;
  letter-spacing: 1px;
}
.eletta-sim-screen {
  background: #f8fafc;
  height: calc(100% - 100px);
  position: relative;
  overflow: hidden;
}
.sim-screen {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  padding: 1.2em;
  overflow-y: auto;
}
.sim-screen.active {
  opacity: 1;
  visibility: visible;
}
.sim-screen-title {
  color: #1e293b;
  text-align: center;
  margin-bottom: 1.5em;
  font-size: 1.2em;
  font-weight: 700;
}
.sim-voting-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1em;
}
.sim-voting-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 1.5em;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  position: relative;
}
.sim-voting-card:hover {
  border-color: #6366f1;
  box-shadow: 0 4px 20px rgba(99,102,241,0.15);
  transform: translateY(-2px);
}
.voting-card-title {
  color: #1e293b;
  font-weight: 600;
  margin-bottom: 0.8em;
  font-size: 0.95em;
  line-height: 1.3;
}
.voting-card-status {
  color: #10b981;
  font-size: 0.8em;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.4em;
}
.sim-back-btn {
  background: none;
  border: none;
  color: #6366f1;
  cursor: pointer;
  font-size: 0.9em;
  margin-bottom: 1.2em;
  display: flex;
  align-items: center;
  gap: 0.4em;
  font-weight: 500;
}
.vote-question {
  background: #fff;
  border-radius: 16px;
  padding: 1.5em;
  margin-bottom: 1.8em;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.vote-question h4 {
  color: #1e293b;
  margin: 0 0 0.8em 0;
  font-size: 1.1em;
  font-weight: 600;
  line-height: 1.3;
}
.vote-question p {
  color: #64748b;
  margin: 0;
  font-size: 0.85em;
  line-height: 1.4;
}
.sim-options {
  display: flex;
  flex-direction: column;
  gap: 1em;
}
.sim-option {
  background: #fff;
  color: #1e293b;
  border: 2px solid #e2e8f0;
  padding: 1.2em;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 600;
  font-size: 0.9em;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6em;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.sim-option:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.sim-option.yes { 
  border-color: #10b981; 
  color: #10b981;
}
.sim-option.yes:hover { 
  background: #ecfdf5; 
  border-color: #059669;
}
.sim-option.no { 
  border-color: #ef4444; 
  color: #ef4444;
}
.sim-option.no:hover { 
  background: #fef2f2; 
  border-color: #dc2626;
}
.sim-option:not(.yes):not(.no) {
  border-color: #6b7280;
  color: #6b7280;
}
.sim-option:not(.yes):not(.no):hover {
  background: #f9fafb;
  border-color: #4b5563;
}
.sim-results-container {
  background: #fff;
  border-radius: 16px;
  padding: 1.5em;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.sim-results-chart {
  display: flex;
  flex-direction: column;
  gap: 1.2em;
  margin-bottom: 1.5em;
}
.result-item {
  display: flex;
  flex-direction: column;
  gap: 0.6em;
}
.result-label {
  display: flex;
  justify-content: space-between;
  font-size: 0.9em;
  color: #1e293b;
  font-weight: 600;
}
.result-bar-bg {
  background: #f1f5f9;
  border-radius: 6px;
  height: 10px;
  overflow: hidden;
}
.result-bar {
  height: 100%;
  width: 0;
  border-radius: 6px;
  transition: width 1.2s ease-out;
}
.result-bar.yes { background: #10b981; }
.result-bar.no { background: #ef4444; }
.result-bar.abstain { background: #6b7280; }
.sim-thanks {
  text-align: center;
  color: #10b981;
  font-weight: 600;
  background: #ecfdf5;
  padding: 1em;
  border-radius: 12px;
  font-size: 0.85em;
  border: 1px solid #d1fae5;
}

body {
  background: linear-gradient(135deg, #24544e 0%, #39746F 40%, #60a89e 100%);
  min-height: 100vh;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}
#eletta-bg {
  background: transparent !important;
}
.eletta-title,
.eletta-subtitle {
  color: #fff !important;
  text-shadow: 0 4px 24px #000a, 0 1px 2px #0008;
}
</style>
<script>
document.addEventListener("DOMContentLoaded", function() {
  function showMainContent() {
    document.querySelector('.eletta-main-content').classList.add('eletta-show');
  }
  window.addEventListener('scroll', function() {
    if (window.scrollY > window.innerHeight * 0.2) showMainContent();
  });
  var scrollBtn = document.getElementById('eletta-scroll-down');
  if (scrollBtn) {
    scrollBtn.addEventListener('click', function() {
      window.scrollTo({top: window.innerHeight, behavior: 'smooth'});
      setTimeout(showMainContent, 400);
    });
  }
});
(function() {
  // Partículas animadas simples
  const canvas = document.getElementById('eletta-particles');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let w = window.innerWidth, h = window.innerHeight;
  canvas.width = w; canvas.height = h;
  let particles = Array.from({length: 40}, () => ({
    x: Math.random()*w,
    y: Math.random()*h,
    r: 2+Math.random()*3,
    dx: (Math.random()-0.5)*0.5,
    dy: 0.3+Math.random()*0.7,
    alpha: 0.2+Math.random()*0.5
  }));
  function draw() {
    ctx.clearRect(0,0,w,h);
    for (const p of particles) {
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, 2*Math.PI);
      ctx.fillStyle = `rgba(255,255,255,${p.alpha})`;
      ctx.shadowColor = "#fff";
      ctx.shadowBlur = 8;
      ctx.fill();
      ctx.shadowBlur = 0;
      p.y += p.dy;
      p.x += p.dx;
      if (p.y > h+10) { p.y = -10; p.x = Math.random()*w; }
      if (p.x < -10 || p.x > w+10) { p.x = Math.random()*w; }
    }
    requestAnimationFrame(draw);
  }
  draw();
  window.addEventListener('resize', () => {
    w = window.innerWidth; h = window.innerHeight;
    canvas.width = w; canvas.height = h;
  });
})();
</script>

<!-- CONTEÚDO PRINCIPAL ESCONDIDO ATÉ ROLAR -->
<div class="eletta-main-content">
<!-- ...existing code a partir do próximo conteúdo... -->



<div style="display: flex; justify-content: center; align-items: stretch; gap: 2.5em; flex-wrap: wrap; margin: 2em 0 2.5em 0;">
  <!-- Caixa de texto -->
  <div style="flex:2; min-width:320px; max-width: 900px; background: rgba(255,255,255,0.07); border-radius: 14px; box-shadow: 0 2px 12px #0001; padding: 1.5em; display: flex; align-items: center;">
    <p style="font-size:1.15em; color:#f5f5f5; text-shadow: 0 1px 4px #0006; margin:0;">
     O Eletta é um <b>aplicativo Android</b> para criar votações locais de forma simples, segura e transparente.
      Ele permite que grupos tomem decisões coletivas, com anonimato e resultados em tempo real.
      <b>Sem necessidade de internet</b>, bastando que todos estejam conectados à mesma rede local.
    </p>
  </div>
  <!-- Layout de telefone com vídeo -->
  <div style="flex:1; min-width:260px; display:flex; justify-content:center; align-items:center;">
    <div style="background:#fff; border-radius:32px; box-shadow:0 8px 32px #0003; border:4px solid #e0e0e0; width:260px; height:520px; display:flex; align-items:center; justify-content:center; position:relative; overflow:hidden;">
      <video autoplay loop muted playsinline style="width:100%; height:100%; object-fit:cover; border-radius:28px;">
        <source src="assets/videos/VideoHost.mp4" type="video/mp4">
        Seu navegador não suporta vídeo HTML5.
      </video>
      <!-- Simula botão home do celular -->
      <div style="position:absolute;bottom:14px;left:50%;transform:translateX(-50%);width:38px;height:5px;background:#e0e0e0;border-radius:3px;"></div>
    </div>
  </div>
  <div style="flex:1; min-width:260px; display:flex; justify-content:center; align-items:center;">
    <div style="background:#fff; border-radius:32px; box-shadow:0 8px 32px #0003; border:4px solid #e0e0e0; width:260px; height:520px; display:flex; align-items:center; justify-content:center; position:relative; overflow:hidden;">
      <video autoplay loop muted playsinline style="width:100%; height:100%; object-fit:cover; border-radius:28px;">
        <source src="assets/videos/VideoVotante.mp4" type="video/mp4">
        Seu navegador não suporta vídeo HTML5.
      </video>
      <!-- Simula botão home do celular -->
      <div style="position:absolute;bottom:14px;left:50%;transform:translateX(-50%);width:38px;height:5px;background:#e0e0e0;border-radius:3px;"></div>
    </div>
  </div>
</div>
<br>
<!-- Aqui podemos colocar o APK -->
<div align="center" style="margin: 2em 0;">
    <a href="https://github.com/unb-mds/2025-1-Squad06" style="display:inline-block;padding:1em 2.2em;font-size:1.2em;font-weight:bold;color:#fff;background:#39745F;border-radius:40px;box-shadow:0 4px 24px #0003;transition:transform 0.2s;animation:ctaPulse 2.5s infinite alternate;text-decoration:none;">
      ⭐️ Experimente o Eletta agora!
    </a>
</div>
<br>
<h2>🌟 Por que usar o Eletta?</h2>

<div style="display: flex; gap: 1.5em; flex-wrap: wrap; justify-content: center;">
  <div class="feature-card" style="border-left: 6px solid #009688; background: linear-gradient(135deg,#b2dfdb 60%,#80cbc4 100%); color: #1a2a2a;">
      <h3 style="color:#004d40;" align= "center">🔒 Segurança</h3>
      <p style="color:#1a2a2a;" align= "center">
        Anonimato garantido, resultados transparentes e integridade dos votos para máxima confiança no processo.
      </p>
  </div>
  <div class="feature-card" style="border-left: 6px solid #673ab7; background: linear-gradient(135deg,#d1c4e9 60%,#9575cd 100%); color: #2e2257;">
    <h3 style="color:#4527a0;" align= "center">⚡ Rapidez</h3>
    <p style="color:#2e2257;" align= "center">Resultados instantâneos e interface responsiva para qualquer dispositivo Android.</p>
  </div>
  <div class="feature-card" style="border-left: 6px solid #ff9800; background: linear-gradient(135deg,#ffe0b2 60%,#ffb74d 100%); color: #6d4c1b;">
    <h3 style="color:#ef6c00;" align= "center">🧩 Flexibilidade</h3>
    <p style="color:#6d4c1b;" align= "center">Ideal para empresas, escolas, comunidades e qualquer grupo que precise decidir.</p>
  </div>

</div>


<br>
<h2>👥 Nossa Equipe</h2>
<br>
<!-- Carrossel de colaboradores (transição slide suave real, mais largo) -->
<div id="eletta-collab-carousel" style="display: flex; flex-direction: column; align-items: center; gap: 1.5em;">
  <div style="display: flex; align-items: center; gap: 2em;">
    <button id="collab-prev" style="background: none; border: none; font-size: 2.5em; color: #fff; cursor: pointer; padding: 0 0.5em; border-radius: 50%; transition: background 0.2s;" onmouseover="this.style.background='#e0e0e0';this.style.color='#39745F'" onmouseout="this.style.background='none';this.style.color='#fff'">&#8592;</button>
    <div id="collab-cards-viewport" style="overflow:hidden; width:1100px; min-height:270px; display:flex; align-items:stretch; justify-content:center;">
      <div id="collab-cards" style="display: flex; gap: 2.5em; transition: transform 0.7s cubic-bezier(.77,0,.18,1); will-change: transform;">
        <!-- Cards dos colaboradores via JS -->
      </div>
    </div>
    <button id="collab-next" style="background: none; border: none; font-size: 2.5em; color: #fff; cursor: pointer; padding: 0 0.5em; border-radius: 50%; transition: background 0.2s;" onmouseover="this.style.background='#e0e0e0';this.style.color='#39745F'" onmouseout="this.style.background='none';this.style.color='#fff'">&#8594;</button>
  </div>
  <div id="collab-indicators" style="display: flex; gap: 0.4em; margin-top: 0.5em;"></div>
</div>

<style>
#collab-cards .collab-card {
  min-width: 320px;
  max-width: 340px;
  min-height: 280px;
  margin: 0;
  /* Fundo claro e agradável, texto escuro para contraste */
  background: linear-gradient(135deg, #e0f7fa 10%, #009688 100%);
  border-radius: 22px;
  box-shadow: 0 6px 32px #0002;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2.2em 1.2em 1.5em 1.2em;
  border: 3px solid #e0e0e0;
  transition: box-shadow 0.2s, transform 0.2s;
  color: #1a2a2a;
}
#collab-cards .collab-card:hover {
  box-shadow: 0 12px 36px #39745F33;
  transform: scale(1.04);
}
#collab-cards .collab-card b {
  color: #24544e;
}
#collab-cards .collab-card span {
  color: #444;
}
#collab-cards .collab-card a {
  color: #39745F;
  text-decoration: none;
  font-weight: 500;
}
#collab-cards .collab-card a:hover {
  text-decoration: underline;
}
</style>

<script>
const collabs = [
  {
    img: "https://avatars.githubusercontent.com/u/191532479?v=4",
    name: "Giovanni Mateus",
    role: "🧑‍💼 Product Owner",
    github: "GiovanniMateus"
  },
  {
    img: "https://avatars.githubusercontent.com/u/108472844?v=4",
    name: "Lívia Yasmin",
    role: "🧑‍🏫 Scrum Master",
    github: "LiviaYasmin"
  },
  {
    img: "https://avatars.githubusercontent.com/u/198164711?v=4",
    name: "Enzo Borges",
    role: "💻 Dev",
    github: "enzo-fb"
  },
  {
    img: "https://avatars.githubusercontent.com/u/84422077?v=4",
    name: "Davi de Araújo",
    role: "💻 Dev",
    github: "daviaraujobr"
  },

  {
    img: "https://avatars.githubusercontent.com/u/145588777?v=4",
    name: "Renan Ribeiro",
    role: "💻 Dev",
    github: "rsribeiro1"
  },
  {
    img: "https://avatars.githubusercontent.com/u/181674474?v=4",
    name: "André Livio",
    role: "💻 Dev",
    github: "AndreLivio"
  }
];
let collabIdx = 0;
let collabInterval = null;
let isHovered = false;
let isTransitioning = false;

// Para slide: duplicar os cards para efeito infinito
function getVisibleCards(idx) {
  const total = collabs.length;
  let cards = [];
  for (let i = 0; i < total; i++) {
    cards.push(collabs[i]);
  }
  // Para looping suave, duplicar o array
  return cards.concat(cards);
}

function renderCollabs(idx, animate = true) {
  const total = collabs.length;
  const cardsDiv = document.getElementById('collab-cards');
  const visibleCards = getVisibleCards(idx);
  let html = '';
  for (let i = 0; i < visibleCards.length; i++) {
    const c = visibleCards[i];
    html += `
      <div class="collab-card">
        <img src="${c.img}" width="120" style="border-radius:50%;box-shadow:0 2px 12px #0002;">
        <b style="margin-top:1.1em; font-size:1.22em; color:#39745F">${c.name}</b>
        <span style="font-size:1.18em; margin:0.5em 0 0.7em 0; color:#555;">${c.role}</span>
        <a href="https://github.com/${c.github}" target="_blank" style="font-size:1.13em; color:#333; text-decoration:none;">@${c.github}</a>
      </div>
    `;
  }
  cardsDiv.innerHTML = html;

  // Calcula o deslocamento para mostrar o trio correto
  const cardWidth = 340 + 40; // largura + gap (aprox)
  let offset = idx * cardWidth;
  cardsDiv.style.transform = `translateX(-${offset}px)`;

  // Indicadores
  let indicators = '';
  for (let i = 0; i < total; i++) {
    indicators += `<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:${i===idx?'#39745F':'#bdbdbd'};margin:0 2px;transition:background 0.2s;"></span>`;
  }
  document.getElementById('collab-indicators').innerHTML = indicators;
}

function nextCollab() {
  if (isTransitioning) return;
  isTransitioning = true;
  const total = collabs.length;
  collabIdx = (collabIdx + 1) % total;
  renderCollabs(collabIdx, true);
  setTimeout(() => { isTransitioning = false; }, 700);
}

function prevCollab() {
  if (isTransitioning) return;
  const total = collabs.length;
  collabIdx = (collabIdx - 1 + total) % total;
  isTransitioning = true;
  renderCollabs(collabIdx, true);
  setTimeout(() => { isTransitioning = false; }, 700);
}

document.getElementById('collab-prev').onclick = prevCollab;
document.getElementById('collab-next').onclick = nextCollab;

// Auto-move
function startAutoMove() {
  if (collabInterval) clearInterval(collabInterval);
  collabInterval = setInterval(() => {
    if (!isHovered && !isTransitioning) nextCollab();
  }, 3500);
}
function stopAutoMove() {
  if (collabInterval) clearInterval(collabInterval);
}

const carousel = document.getElementById('eletta-collab-carousel');
carousel.addEventListener('mouseenter', () => { isHovered = true; });
carousel.addEventListener('mouseleave', () => { isHovered = false; });

renderCollabs(collabIdx, false);
startAutoMove();
</script>

<!-- ...existing code... -->

<p align="center" style="margin-top:4em;">
  Junte-se a nós e transforme a forma de decidir!<br>
  <sub>© 2025 Eletta &mdash; Licença <a href="https://github.com/unb-mds/2025-1-Eletta/blob/main/LICENSE">MIT</a></sub>
</p>