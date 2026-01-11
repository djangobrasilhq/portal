class Toast {
  constructor() {
    this.container = null;
    this.init();
  }

  init() {
    if (!document.getElementById('toast-container')) {
      this.container = document.createElement('div');
      this.container.id = 'toast-container';
      this.container.className = 'toast-container';
      document.body.appendChild(this.container);
    } else {
      this.container = document.getElementById('toast-container');
    }
  }

  show(message, type = 'info', duration = 5000) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');

    const icon = this.getIcon(type);
    const typeLabel = this.getTypeLabel(type);

    toast.innerHTML = `
      <div class="toast__content">
        <div class="toast__icon">${icon}</div>
        <div class="toast__message">
          <div class="toast__title">${typeLabel}</div>
          <div class="toast__text">${message}</div>
        </div>
        <button class="toast__close" aria-label="Fechar">&times;</button>
      </div>
      <div class="toast__progress"></div>
    `;

    this.container.appendChild(toast);

    setTimeout(() => {
      toast.classList.add('toast--show');
    }, 10);

    const autoRemove = setTimeout(() => {
      this.remove(toast);
    }, duration);

    const closeBtn = toast.querySelector('.toast__close');
    closeBtn.addEventListener('click', () => {
      clearTimeout(autoRemove);
      this.remove(toast);
    });

    const progressBar = toast.querySelector('.toast__progress');
    progressBar.style.animation = `toast-progress ${duration}ms linear forwards`;

    return toast;
  }

  remove(toast) {
    toast.classList.add('toast--hide');
    setTimeout(() => {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, 300);
  }

  getIcon(type) {
    const icons = {
      success: '✓',
      error: '✕',
      warning: '⚠',
      info: 'ℹ',
    };
    return icons[type] || icons.info;
  }

  getTypeLabel(type) {
    const labels = {
      success: 'Sucesso',
      error: 'Erro',
      warning: 'Aviso',
      info: 'Info',
    };
    return labels[type] || labels.info;
  }

  success(message, duration) {
    return this.show(message, 'success', duration);
  }

  error(message, duration) {
    return this.show(message, 'error', duration);
  }

  warning(message, duration) {
    return this.show(message, 'warning', duration);
  }

  info(message, duration) {
    return this.show(message, 'info', duration);
  }
}

const toast = new Toast();

window.toast = toast;

document.addEventListener('DOMContentLoaded', () => {
  const messages = document.querySelectorAll('.django-message');
  messages.forEach((msg) => {
    const messageText = msg.textContent.trim();
    const messageType = msg.classList.contains('success') ? 'success' :
                       msg.classList.contains('error') ? 'error' :
                       msg.classList.contains('warning') ? 'warning' : 'info';
    
    if (messageText) {
      toast.show(messageText, messageType);
      msg.style.display = 'none';
    }
  });
});
