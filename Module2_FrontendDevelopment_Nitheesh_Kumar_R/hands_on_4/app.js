import { courses } from './data.js';

const BASE = 'https://jsonplaceholder.typicode.com';


// ============================================================
// TASK 1 — Promises and async/await
// ============================================================

// Step 45: Promise chain
function fetchUserPromise(id) {
    return fetch(`${BASE}/users/${id}`)
        .then(res => res.json())
        .then(user => console.log('Promise chain - user name:', user.name));
}
fetchUserPromise(1);

// Step 46: same function rewritten with async/await + try/catch
async function fetchUser(id) {
    try {
        const res = await fetch(`${BASE}/users/${id}`);
        const user = await res.json();
        console.log('async/await - user name:', user.name);
    } catch (err) {
        console.error('fetchUser error:', err.message);
    }
}
fetchUser(1);

// Step 47: simulated 1-second delay then returns local courses
function fetchAllCourses() {
    return new Promise(resolve => setTimeout(() => resolve(courses), 1000));
}

// Step 48: show loading, render cards after promise resolves
const courseGrid = document.getElementById('course-grid');
const loadingEl = document.getElementById('courses-loading');
const totalEl = document.getElementById('total-credits');

fetchAllCourses().then(list => {
    loadingEl.style.display = 'none';
    list.forEach(course => {
        const card = document.createElement('article');
        card.className = 'course-card';
        card.innerHTML = `<h3>${course.code}</h3><p>${course.name}</p><p>${course.credits} Credits</p>`;
        courseGrid.appendChild(card);
    });
    const total = list.reduce((sum, c) => sum + c.credits, 0);
    totalEl.textContent = `Total Credits: ${total}`;
});

// Step 49: Promise.all — fetch two users simultaneously
Promise.all([
    fetch(`${BASE}/users/1`).then(r => r.json()),
    fetch(`${BASE}/users/2`).then(r => r.json())
]).then(([user1, user2]) => {
    console.log('Promise.all - users:', user1.name, '&', user2.name);
});


// ============================================================
// TASK 2 — Fetch API with Error Handling
// ============================================================

// Step 50: reusable fetch wrapper
async function apiFetch(url) {
    const res = await fetch(url);
    if (!res.ok) {
        throw new Error(`HTTP error ${res.status}: ${url}`);
    }
    return res.json();
}

const notifLoading = document.getElementById('notif-loading');
const notifError = document.getElementById('notif-error');
const notifList = document.getElementById('notif-list');

// Step 51 + 52: load posts, show loading spinner, render cards
async function loadNotifications(url) {
    notifLoading.style.display = 'block';   // show loading
    notifError.innerHTML = '';
    notifList.innerHTML = '';

    try {
        const posts = await apiFetch(url);
        notifLoading.style.display = 'none';
        posts.slice(0, 5).forEach(post => {
            const card = document.createElement('div');
            card.className = 'notif-card';
            card.innerHTML = `<strong>${post.title}</strong><p>${post.body.slice(0, 60)}...</p>`;
            notifList.appendChild(card);
        });
    } catch (err) {
        // Step 53: user-friendly error message in UI
        notifLoading.style.display = 'none';
        notifError.innerHTML = `
            <p class="error-msg">Failed to load: ${err.message}</p>
            <button id="retry-btn" type="button">Retry</button>
        `;
        // Step 54: retry button re-calls the function
        document.getElementById('retry-btn').addEventListener('click', () => {
            loadNotifications(`${BASE}/posts`);
        });
    }
}

// Load successfully first
loadNotifications(`${BASE}/posts`);

// Uncomment to test Step 53 error + retry:
// loadNotifications(`${BASE}/nonexistent`);


// ============================================================
// TASK 3 — Axios
// ============================================================

// Step 58: request interceptor — logs before every request
axios.interceptors.request.use(config => {
    console.log('API call started:', config.url);
    return config;
});

// Step 56: apiFetch rewritten with axios (auto JSON parse, throws on non-2xx)
async function axiosFetch(url) {
    const res = await axios.get(url);
    return res.data;
}

// Step 57: fetch posts for userId=1 using params object
async function loadAxiosPosts() {
    try {
        const res = await axios.get(`${BASE}/posts`, { params: { userId: 1 } });
        const posts = res.data;
        const container = document.getElementById('axios-posts');
        posts.slice(0, 3).forEach(post => {
            const card = document.createElement('div');
            card.className = 'notif-card';
            card.innerHTML = `<strong>${post.title}</strong>`;
            container.appendChild(card);
        });
    } catch (err) {
        console.error('Axios error:', err.message);
    }
}
loadAxiosPosts();

/*
 * Step 59 — fetch vs axios differences:
 *
 * 1. JSON parsing: fetch requires res.json() manually; axios parses automatically (res.data).
 * 2. Error handling: fetch only rejects on network failure, NOT on 404/500 — you must check
 *    response.ok manually. Axios throws automatically on any non-2xx status.
 * 3. Features: Axios has built-in request/response interceptors, timeout support, and
 *    request cancellation. fetch has none of these out of the box.
 */