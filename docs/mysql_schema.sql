-- EMS SaaS Upgrade Schema (MySQL 8+)
-- Apply using Django migrations in production. This file is a reference schema.

ALTER TABLE core_institution
    ADD COLUMN admin_email varchar(254) NULL,
    ADD COLUMN created_at datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6);

CREATE TABLE IF NOT EXISTS dashboard_course (
    id bigint AUTO_INCREMENT PRIMARY KEY,
    institute_id bigint NOT NULL,
    teacher_id bigint NULL,
    name varchar(150) NOT NULL,
    code varchar(40) NOT NULL UNIQUE,
    description longtext NOT NULL,
    credits smallint unsigned NOT NULL DEFAULT 3,
    created_at datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    CONSTRAINT fk_course_institute FOREIGN KEY (institute_id) REFERENCES core_institution(id),
    CONSTRAINT fk_course_teacher FOREIGN KEY (teacher_id) REFERENCES teachers_teacher(id)
);

CREATE TABLE IF NOT EXISTS dashboard_assignment (
    id bigint AUTO_INCREMENT PRIMARY KEY,
    institute_id bigint NOT NULL,
    course_id bigint NOT NULL,
    created_by_id bigint NULL,
    title varchar(200) NOT NULL,
    description longtext NOT NULL,
    due_date date NOT NULL,
    attachment varchar(100) NULL,
    created_at datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    CONSTRAINT fk_assignment_institute FOREIGN KEY (institute_id) REFERENCES core_institution(id),
    CONSTRAINT fk_assignment_course FOREIGN KEY (course_id) REFERENCES dashboard_course(id),
    CONSTRAINT fk_assignment_user FOREIGN KEY (created_by_id) REFERENCES accounts_user(id)
);

CREATE TABLE IF NOT EXISTS dashboard_announcement (
    id bigint AUTO_INCREMENT PRIMARY KEY,
    institute_id bigint NOT NULL,
    created_by_id bigint NULL,
    title varchar(160) NOT NULL,
    message longtext NOT NULL,
    is_active tinyint(1) NOT NULL DEFAULT 1,
    created_at datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    CONSTRAINT fk_announcement_institute FOREIGN KEY (institute_id) REFERENCES core_institution(id),
    CONSTRAINT fk_announcement_user FOREIGN KEY (created_by_id) REFERENCES accounts_user(id)
);

CREATE TABLE IF NOT EXISTS dashboard_feepayment (
    id bigint AUTO_INCREMENT PRIMARY KEY,
    student_id bigint NOT NULL,
    amount decimal(10,2) NOT NULL,
    status varchar(20) NOT NULL,
    payment_date date NULL,
    reference varchar(80) NOT NULL,
    created_at datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    CONSTRAINT fk_feepayment_student FOREIGN KEY (student_id) REFERENCES students_student(id)
);

CREATE TABLE IF NOT EXISTS dashboard_studentperformance (
    id bigint AUTO_INCREMENT PRIMARY KEY,
    student_id bigint NOT NULL,
    course_id bigint NOT NULL,
    score double NOT NULL,
    remarks varchar(200) NOT NULL,
    graded_at date NOT NULL,
    UNIQUE KEY uq_student_course (student_id, course_id),
    CONSTRAINT fk_perf_student FOREIGN KEY (student_id) REFERENCES students_student(id),
    CONSTRAINT fk_perf_course FOREIGN KEY (course_id) REFERENCES dashboard_course(id)
);

CREATE TABLE IF NOT EXISTS dashboard_activitylog (
    id bigint AUTO_INCREMENT PRIMARY KEY,
    user_id bigint NULL,
    action varchar(255) NOT NULL,
    path varchar(255) NOT NULL,
    method varchar(10) NOT NULL,
    ip_address char(39) NULL,
    created_at datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    CONSTRAINT fk_log_user FOREIGN KEY (user_id) REFERENCES accounts_user(id)
);
