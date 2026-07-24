import { courses } from './data.js';

// Polyfill initialization
if (window.cssVars) {
    cssVars();
}

const grid = document.querySelector('.course-grid');
const totalEl = document.getElementById('total-credits');
const selectedEl = document.getElementById('selected-course');
const resultsCountEl = document.getElementById('results-count');

function renderCourses(list) {
    grid.innerHTML = '';

    const fragment = document.createDocumentFragment();

    list.forEach(course => {
        const card = document.createElement('article');
        card.className = 'course-card';
        card.dataset.id = course.id;
        // Step 129: Make course cards keyboard-accessible
        card.tabIndex = 0; 
        
        // Add ARIA attributes for better screen reader experience
        card.setAttribute('role', 'button');
        card.setAttribute('aria-label', `${course.name}, ${course.credits} credits`);

        card.innerHTML = `
            <h3>${course.code}</h3>
            <p>${course.name}</p>
            <p>${course.credits} Credits</p>
        `;
        fragment.appendChild(card);
    });

    grid.appendChild(fragment);

    const total = list.reduce((sum, c) => sum + c.credits, 0);
    totalEl.textContent = `Total Credits: ${total}`;

    // Step 130: Update the polite ARIA live region
    resultsCountEl.textContent = `${list.length} courses found`;
}

renderCourses(courses);

document.getElementById('search-courses').addEventListener('input', function () {
    const query = this.value.toLowerCase();
    const filtered = courses.filter(c => c.name.toLowerCase().includes(query));
    renderCourses(filtered);
});

document.getElementById('sort-btn').addEventListener('click', () => {
    const sorted = [...courses].sort((a, b) => b.credits - a.credits);
    renderCourses(sorted);
});

// Event Delegation for both click and keydown (Enter) on course cards
grid.addEventListener('click', handleCardInteraction);
grid.addEventListener('keydown', (event) => {
    // Step 129: Pressing Enter on a focused card triggers the same action as a click
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent default scroll on Enter if any
        handleCardInteraction(event);
    }
});

function handleCardInteraction(event) {
    const card = event.target.closest('.course-card');
    if (!card) return;

    const id = Number(card.dataset.id);
    const course = courses.find(c => c.id === id);

    selectedEl.textContent = `Selected: ${course.name} | Grade: ${course.grade || 'N/A'}`;
}

// Step 131: Toggle aria-expanded on expandable element
const menuBtn = document.getElementById('menu-btn');
if (menuBtn) {
    menuBtn.addEventListener('click', () => {
        const isExpanded = menuBtn.getAttribute('aria-expanded') === 'true';
        menuBtn.setAttribute('aria-expanded', !isExpanded);
    });
}