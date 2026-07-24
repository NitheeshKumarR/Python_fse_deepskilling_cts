import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';

// Step 78: nav links use <Link> instead of <a>
// Step 83: enrolled count read from Redux via useSelector — no props needed
function Header({ siteName }) {
    const enrolledCourses = useSelector(state => state.enrollment.enrolledCourses);

    return (
        <header style={{ background: '#1e3a5f', color: '#fff', padding: '16px 24px' }}>
            <h1>{siteName}</h1>
            <nav style={{ marginTop: '8px' }}>
                <Link to="/" style={{ color: '#fff', marginRight: '16px' }}>Home</Link>
                <Link to="/courses" style={{ color: '#fff', marginRight: '16px' }}>Courses</Link>
                <Link to="/profile" style={{ color: '#fff' }}>Profile</Link>
            </nav>
            <p style={{ marginTop: '8px' }}>Enrolled: {enrolledCourses.length}</p>
        </header>
    );
}

export default Header;
