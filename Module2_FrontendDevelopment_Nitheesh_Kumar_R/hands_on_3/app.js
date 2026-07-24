import { courses } from './data.js';

courses.forEach(course => {
    const { name, credits } = course;
    console.log(name, credits);
});

const formatted = courses.map(({ code, name, credits }) =>
    `${code} — ${name} (${credits} credits)`
);
console.log('Formatted:', formatted);

const highCredit = courses.filter(course => course.credits >= 4);
console.log('Courses with 4+ credits:', highCredit.length);

const totalCredits = courses.reduce((sum, course) => sum + course.credits, 0);
console.log('Total credits:', totalCredits);


const grid = document.querySelector('.course-grid');
const totalEl = document.getElementById('total-credits');
const selectedEl = document.getElementById('selected-course');

function renderCourses(list) {
    grid.innerHTML = '';

    const fragment = document.createDocumentFragment();

    list.forEach(course => {
        const card = document.createElement('article');
        card.className = 'course-card';
        card.dataset.id = course.id;
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

grid.addEventListener('click', (event) => {
    const card = event.target.closest('.course-card');
    if (!card) return;

    const id = Number(card.dataset.id);
    const course = courses.find(c => c.id === id);

    selectedEl.textContent = `Selected: ${course.name} | Grade: ${course.grade}`;
});