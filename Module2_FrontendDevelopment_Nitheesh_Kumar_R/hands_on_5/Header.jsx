// Task 1 Step 62 & 64: Header component — receives siteName and enrolledCount as props
function Header({ siteName, enrolledCount }) {
    return (
        <header style={{ background: '#1e3a5f', color: '#fff', padding: '16px 24px' }}>
            <h1>{siteName}</h1>
            <nav>
                <a href="#" style={{ color: '#fff', marginRight: '16px' }}>Home</a>
                <a href="#" style={{ color: '#fff', marginRight: '16px' }}>Courses</a>
                <a href="#" style={{ color: '#fff' }}>Profile</a>
            </nav>
            {/* Task 2 Step 70: enrolled count passed as prop */}
            <p>Enrolled: {enrolledCount}</p>
        </header>
    );
}

export default Header;