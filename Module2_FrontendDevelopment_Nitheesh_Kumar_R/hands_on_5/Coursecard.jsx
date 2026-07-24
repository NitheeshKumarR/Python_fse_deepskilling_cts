// Task 1 Step 65: CourseCard — accepts name, code, credits, grade, onEnroll as props
function CourseCard({ name, code, credits, grade, onEnroll }) {
    return (
        <div style={{ border: '1px solid #ddd', borderRadius: '4px', padding: '16px', background: '#fafafa' }}>
            <h3>{code}</h3>
            <p>{name}</p>
            <p>{credits} Credits | Grade: {grade}</p>
            {/* Task 2 Step 69: Enroll button — calls handler passed from App */}
            <button onClick={onEnroll} style={{ marginTop: '8px', padding: '6px 12px', cursor: 'pointer' }}>
                Enroll
            </button>
        </div>
    );
}

export default CourseCard;