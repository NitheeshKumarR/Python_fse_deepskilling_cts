import { useState, useEffect } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import CourseCard from './components/CourseCard';
import StudentProfile from './components/StudentProfile';

function App() {

    // Task 3 Step 71–73: fetch from API, loading + error state
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Task 2 Step 68: search input state
    const [searchTerm, setSearchTerm] = useState('');

    // Task 2 Step 69: enrolled courses state (lifted up)
    const [enrolledCourses, setEnrolledCourses] = useState([]);

    // Task 3 Step 71: useEffect to fetch on mount ([] = runs once after mount)
    useEffect(() => {
        fetch('https://jsonplaceholder.typicode.com/posts')
            .then(res => res.json())
            .then(posts => {
                // map first 5 posts to course-like objects
                const mapped = posts.slice(0, 5).map((post, i) => ({
                    id: post.id,
                    code: `CS10${i + 1}`,
                    name: post.title.slice(0, 30),
                    credits: (i % 2 === 0) ? 4 : 3,
                    grade: ['A', 'B', 'A', 'B', 'C'][i],
                }));
                setCourses(mapped);
                setLoading(false);
            })
            .catch(err => {
                setError(err.message);
                setLoading(false);
            });
    }, []);

    // Task 3 Step 75: log whenever courses state changes
    // dependency array [courses] means this runs only when courses updates,
    // not on every render — without it, this would run after every render
    useEffect(() => {
        console.log('Courses updated:', courses.length);
    }, [courses]);

    // Task 2 Step 69: enroll handler — lifts state up from CourseCard
    function handleEnroll(course) {
        const alreadyEnrolled = enrolledCourses.find(c => c.id === course.id);
        if (!alreadyEnrolled) {
            setEnrolledCourses([...enrolledCourses, course]);
        }
    }

    // Task 2 Step 68: filter courses by search term
    const filteredCourses = courses.filter(c =>
        c.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <>
            {/* Task 1 Step 64: siteName passed as prop, enrolledCount from state */}
            <Header siteName="EduCore Student Portal" enrolledCount={enrolledCourses.length} />

            <main style={{ maxWidth: '960px', margin: '24px auto', padding: '0 16px' }}>

                <h2 style={{ marginBottom: '12px' }}>Courses</h2>

                {/* Task 2 Step 68: search input */}
                <input
                    type="text"
                    placeholder="Search courses..."
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                    style={{ padding: '8px', marginBottom: '16px', width: '100%' }}
                />

                {/* Task 3 Step 72: loading state */}
                {loading && <p>Loading...</p>}

                {/* Task 3 Step 73: error state */}
                {error && <p style={{ color: 'red' }}>Error: {error}</p>}

                {/* Task 2 Step 67: map over filtered courses */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
                    {filteredCourses.map(course => (
                        <CourseCard
                            key={course.id}
                            {...course}
                            onEnroll={() => handleEnroll(course)}
                        />
                    ))}
                </div>

                <StudentProfile />

            </main>

            <Footer />
        </>
    );
}

export default App;
