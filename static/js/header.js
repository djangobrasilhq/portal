// Funcionalidade de toggle do menu do header
(function () {
  const header = document.getElementById("siteHeader");
  const btn = document.getElementById("menuBtn");
  if (!header || !btn) return;

  btn.addEventListener("click", function () {
    const open = header.classList.toggle("is-open");
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  });
})();

// Funcionalidade de toggle de tema
(function () {
  const themeToggle = document.getElementById("themeToggle");
  const html = document.documentElement;
  
  // Função para obter o tema preferido
  function getTheme() {
    const saved = localStorage.getItem("theme");
    if (saved) return saved;
    
    // Verifica preferência do sistema
    if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
      return "dark";
    }
    return "light";
  }

  // Função para aplicar o tema
  function setTheme(theme) {
    html.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
    
    // Atualiza o aria-label
    if (themeToggle) {
      themeToggle.setAttribute("aria-label", `Alternar tema (tema atual: ${theme})`);
    }
  }

  // Inicializa o tema
  const currentTheme = getTheme();
  setTheme(currentTheme);

  // Adiciona listener ao botão
  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      const current = html.getAttribute("data-theme");
      const newTheme = current === "dark" ? "light" : "dark";
      setTheme(newTheme);
    });
  }

  // Observa mudanças na preferência do sistema
  if (window.matchMedia) {
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function (e) {
      // Só aplica se o usuário não tiver uma preferência salva
      if (!localStorage.getItem("theme")) {
        setTheme(e.matches ? "dark" : "light");
      }
    });
  }
})();

