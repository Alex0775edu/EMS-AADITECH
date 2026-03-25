# SaaS Architecture Blueprint (EMS)

## Goals
Create a scalable EdTech platform with modular services, secure multi-tenant data, and premium UX.

## System Architecture
1. **Frontend**
   - Django templates + componentized UI
   - Progressive enhancement (JS widgets)
   - Responsive design and reusable UI blocks
2. **Backend**
   - Django apps per domain (users, courses, assessments, communication, billing)
   - Service layer for complex workflows
   - Background jobs for long-running tasks (Celery in production)
3. **Realtime**
   - WebSockets for chat, attendance, and notifications (Channels + Redis in production)
4. **Storage**
   - Object storage for video/PDF assets with signed URLs
5. **Analytics**
   - Event logs + aggregated metrics for dashboards and audits

## Domain Apps (current codebase)
- `accounts`: identity, login, roles
- `dashboard`: core admin dashboards + course/assignment foundation
- `attendance`: attendance sessions, QR scans
- `exams`: question bank, online exams, attempts, auto-grading
- `notifications`: in-app + push notifications
- `communications`: chat + support tickets
- `materials`: course files, previews, download tracking
- `billing`: plans, subscriptions, coupons, invoices
- `ai_services`: AI chat, recommendations, insights
- `analytics`: event tracking and metrics

## Data Model Highlights
1. **Learning**
   - Course → Module → Lesson
   - CourseEnrollment + LessonProgress for progress tracking
   - CourseReview for ratings
2. **Assessments**
   - QuestionBank → Question
   - OnlineExam → ExamAttempt → ExamAnswer
   - Assignment → AssignmentSubmission
3. **Communication**
   - Thread → Message
   - SupportTicket → TicketMessage
4. **Monetization**
   - Plan → Subscription → Invoice → PaymentRecord
   - Coupon for discounts
5. **Materials**
   - CourseMaterial + MaterialAccessLog

## Security & Compliance
- CSRF protection, XSS protections, secure cookies
- Rate limiting middleware
- Activity logs + event logs
- Production HTTPS + HSTS enabled when `DEBUG=False`
- Recommended additions for production:
  - JWT authentication (DRF + SimpleJWT)
  - Social login (django-allauth)
  - 2FA (django-otp / django-two-factor-auth)
  - CSP headers with report-only rollout

## Performance & SEO
- Asset caching with `STATIC_VERSION`
- Lazy loading on media
- Optimized component CSS
- Recommended additions:
  - CDN for static/media
  - Image compression pipeline
  - Database indexing on high-traffic tables

## Next Steps
1. Implement JWT auth + social login + 2FA
2. Add real-time messaging and notifications
3. Introduce background processing for video and reports
4. Complete billing workflow integration
