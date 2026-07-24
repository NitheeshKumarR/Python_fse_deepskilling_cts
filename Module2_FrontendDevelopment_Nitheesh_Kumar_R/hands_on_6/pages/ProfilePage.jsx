import { useSelector, useDispatch } from 'react-redux';
import { unenroll } from '../store/enrollmentSlice';

// Step 83 & 84: read enrolledCourses from Redux, dispatch unenroll
function ProfilePage() {
    const enrolledCourses = useSelector(state => state.enrollment.enrolledCourses);
    const dispatch = useDispatch();

    return (
        <div style={{ padding: '24px' }}>
            <h2>My Profile</h2>
            <h3 style={{ marginTop: '16px' }}>Enrolled Courses ({enrolledCourses.length})</h3>
            {enrolledCourses.length === 0 && <p>No courses enrolled yet.</p>}
            <ul style={{ marginTop: '12px', listStyle: 'none', padding: 0 }}>
                {enrolledCourses.map(course => (
                    <li key={course.id} style={{ border: '1px solid #ddd', borderRadius: '4px', padding: '12px', marginBottom: '8px' }}>
                        <strong>{course.code}</strong> — {course.name}
                        <button
                            onClick={() => dispatch(unenroll(course.id))}
                            style={{ marginLeft: '12px', padding: '4px 10px', cursor: 'pointer', color: 'red' }}
                        >
                            Remove
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default ProfilePage;
