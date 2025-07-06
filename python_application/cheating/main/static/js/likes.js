// static/js/favorites.js

// Получаем CSRF-токен из куки
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    document.cookie.split(';').forEach(cookie => {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
      }
    });
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Ждём загрузки DOM, затем навешиваем обработчики
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.favorite-heart').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      
      fetch(this.dataset.url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
          'Accept': 'application/json'
        }
      })
      .then(response => {
        if (!response.ok) {
          // если 403 или 401 — предполагаем, что неавторизован
          throw new Error('Unauthorized');
        }
        return response.json();
      })
      .then(data => {
        const icon = this.querySelector('i');
        if (!icon) return;
        if (data.status === 'add') {
          icon.classList.remove('empty-heart');
          icon.classList.add('red-heart');
        } else if (data.status === 'remove') {
          icon.classList.remove('red-heart');
          icon.classList.add('empty-heart');
        }
      })
      .catch(error => {
        console.error(error);
        alert("Сначала необходимо авторизоваться");
      });
    });
  });
});
