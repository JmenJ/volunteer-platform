// Обработка меню пользователя
document.querySelector('.user-btn').addEventListener('click', function() {
    const dropdown = document.querySelector('.dropdown-content');
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
});

window.addEventListener('click', function(e) {
    if (!e.target.matches('.user-btn') && !e.target.matches('.user-btn *')) {
        const dropdowns = document.querySelectorAll('.dropdown-content');
        dropdowns.forEach(dropdown => {
            if (dropdown.style.display === 'block') {
                dropdown.style.display = 'none';
            }
        });
    }
});

// Фильтрация компаний по тегам
const filterCheckboxes = document.querySelectorAll('.filter-tags input[type="checkbox"]');
const companies = document.querySelectorAll('.company');

filterCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', filterCompanies);
});

function filterCompanies() {
    const selectedTags = Array.from(filterCheckboxes)
        .filter(checkbox => checkbox.checked)
        .map(checkbox => checkbox.value);

    companies.forEach(company => {
        const companyTags = company.dataset.tags.split(',');
        
        if (selectedTags.length === 0) {
            company.style.display = 'block';
        } else {
            const hasMatchingTag = selectedTags.some(tag => companyTags.includes(tag));
            company.style.display = hasMatchingTag ? 'block' : 'none';
        }
    });
}