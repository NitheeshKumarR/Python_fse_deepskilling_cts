import { Link } from 'react-router-dom';

// Step 79: each card links to /courses/:courseId
function CourseCard({ id, name, code, credits, grade, onEnroll }) {
    return (
        <div style={{ border: '1px solid #ddd', borderRadius: '4px', padding: '16px', background: '#fafafa' }}>
            <h3>{code}</h3>
            <p>{name}</p>
            <p>{credits} Credits | Grade: {grade}</p>
            <Link to={`/courses/${id}`} style={{ display: 'inline-block', marginTop: '8px', marginRight: '8px' }}>
                Details
            </Link>
            <button onClick={onEnroll} style={{ marginTop: '8px', padding: '6px 12px', cursor: 'pointer' }}>
                Enroll
            </button>
        </div>
    );
}

export default CourseCard;
