import { createSlice } from '@reduxjs/toolkit';

const enrollmentSlice = createSlice({
    name: 'enrollment',
    initialState: { enrolledCourses: [] },
    reducers: {
        // Step 87: enroll action — add course if not already enrolled
        enroll(state, action) {
            const exists = state.enrolledCourses.find(c => c.id === action.payload.id);
            if (!exists) {
                state.enrolledCourses.push(action.payload);
            }
        },
        // Step 87: unenroll action — remove course by id
        unenroll(state, action) {
            state.enrolledCourses = state.enrolledCourses.filter(c => c.id !== action.payload);
        },
    },
});

export const { enroll, unenroll } = enrollmentSlice.actions;
export default enrollmentSlice.reducer;
