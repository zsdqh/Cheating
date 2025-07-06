// Функция для настройки обработки кликов на карточках упражнений
function setupExerciseCards() {
    // Обработка кликов на мышцы
    document.querySelectorAll('.single-muscle').forEach(muscle => {
        muscle.addEventListener('click', function(e) {
            e.stopPropagation();
            window.location.href = this.dataset.url;
        });
    });

 // Обработка кликов по карточке
    document.querySelectorAll('.home-card').forEach(card => {
        card.addEventListener('click', function(e) {
            // Исключаем клики на мышцы И сердечко
            if (!e.target.closest('.single-muscle') && !e.target.closest('.favorite-heart')) {
                const link = this.querySelector('.card-main-link');
                if (link) window.location.href = link.href;
            }
        });
    });
}

// Инициализация при загрузке документа
document.addEventListener('DOMContentLoaded', function() {
    setupExerciseCards();
});