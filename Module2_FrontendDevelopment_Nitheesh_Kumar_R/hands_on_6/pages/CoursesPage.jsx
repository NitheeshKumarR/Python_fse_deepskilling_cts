import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { enroll } from '../store/enrollmentSlice';
import CourseCard from '../components/CourseCard';

function CoursesPage() {
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');

    const dispatch = useDispatch();
    const navigate = useNavigate();

    useEffect(() => {
        fetch('https://jsonplaceholder.typicode.com/posts')
            .then(res => res.json())
            .then(posts => {
                const mapped = posts.slice(0, 5).map((post, i) => ({
                    id: post.id,
                    code: `CS10${i + 1}`,
                    name: post.title.slice(0, 30),
                    credits: i % 2 === 0 ? 4 : 3,
                    grade: ['A', 'B', 'A', 'B', 'C'][i],
                }));
                setCourses(mapped);
                setLoading(false);
            });
    }, []);

    // Step 88: dispatch enroll action, then Step 80: navigate to /profile
    function handleEnroll(course) {
        dispatch(enroll(course));
        navigate('/profile');
    }

    const filtered = courses.filter(c =>
        c.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div style={{ padding: '24px' }}>
            <h2>Courses</h2>
            <input
                type="text"
                placeholder="Search courses..."
                value={searchTerm}
                onChange={e => setSearchTerm(e.target.value)}
                style={{ padding: '8px', marginBottom: '16px', width: '100%' }}
            />
            {loading && <p>Loading...</p>}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
                {filtered.map(course => (
                    <CourseCard
                        key={course.id}
                        {...course}
                        onEnroll={() => handleEnroll(course)}
                    />
                ))}
            </div>
        </div>
    );
}

export default CoursesPage;
