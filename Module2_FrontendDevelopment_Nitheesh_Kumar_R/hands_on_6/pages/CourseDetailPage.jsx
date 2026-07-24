import { useParams } from 'react-router-dom';

// Step 79: useParams reads :courseId from the URL
function CourseDetailPage() {
    const { courseId } = useParams();

    return (
        <div style={{ padding: '24px' }}>
            <h2>Course Detail</h2>
            <p>Showing details for course ID: <strong>{courseId}</strong></p>
            <p>In a real app, fetch course data using this ID from the API.</p>
        </div>
    );
}

export default CourseDetailPage;
