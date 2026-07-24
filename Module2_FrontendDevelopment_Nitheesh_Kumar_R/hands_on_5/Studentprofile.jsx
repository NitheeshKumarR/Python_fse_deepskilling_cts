import { useState } from 'react';

// Task 3 Step 74: StudentProfile — own local state, form with onChange handlers
function StudentProfile() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [semester, setSemester] = useState('');

    return (
        <div style={{ border: '1px solid #ddd', borderRadius: '4px', padding: '20px', marginTop: '24px' }}>
            <h2>Student Profile</h2>
            <div style={{ marginTop: '12px' }}>
                <input
                    type="text"
                    placeholder="Name"
                    value={name}
                    onChange={e => setName(e.target.value)}
                    style={{ display: 'block', marginBottom: '8px', padding: '8px', width: '100%' }}
                />
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                    style={{ display: 'block', marginBottom: '8px', padding: '8px', width: '100%' }}
                />
                <input
                    type="text"
                    placeholder="Semester"
                    value={semester}
                    onChange={e => setSemester(e.target.value)}
                    style={{ display: 'block', padding: '8px', width: '100%' }}
                />
            </div>
            {name && <p style={{ marginTop: '12px' }}>Hello, {name}! Semester: {semester}</p>}
        </div>
    );
}

export default StudentProfile;