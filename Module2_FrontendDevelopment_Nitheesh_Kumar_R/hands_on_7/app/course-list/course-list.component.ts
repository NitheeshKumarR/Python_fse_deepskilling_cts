import { Component, OnInit } from '@angular/core';
import { CourseService } from '../course.service';

@Component({
  selector: 'app-course-list',
  templateUrl: './course-list.component.html',
  styleUrls: ['./course-list.component.css']
})
export class CourseListComponent implements OnInit {
  courses: any[] = [];
  searchTerm: string = '';
  loading: boolean = false;

  constructor(private courseService: CourseService) {}

  ngOnInit(): void {
    this.loading = true;
    this.courseService.getCourses().subscribe({
      next: (data) => {
        this.courses = data.map(post => ({
          name: post.title,
          code: `CS-${post.id}00`,
          credits: 3,
          grade: 'A'
        }));
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      }
    });
  }

  get filteredCourses() {
    if (!this.searchTerm) return this.courses;
    return this.courses.filter(c => 
      c.name.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  trackByCode(index: number, course: any): string {
    return course.code;
  }
}
