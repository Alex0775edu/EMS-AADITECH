from pathlib import Path
from datetime import date

from django.core.files.storage import default_storage

from .models import Attendance
from students.models import Student


def mark_attendance_from_face(uploaded_file):
    """
    Placeholder integration point for OpenCV + face_recognition.
    Replace simulated matching with actual face encoding comparison.
    """
    save_path = default_storage.save(f'face_scans/{uploaded_file.name}', uploaded_file)
    _ = Path(default_storage.path(save_path))

    # TODO: Implement real face recognition pipeline.
    student = Student.objects.select_related('user').order_by('id').first()
    if not student:
        return {'success': False, 'message': 'No students available for face matching.'}

    record, created = Attendance.objects.get_or_create(student=student, date=date.today(), defaults={'status': 'PRESENT'})
    if not created:
        record.status = 'PRESENT'
        record.save(update_fields=['status'])

    return {'success': True, 'message': f'Attendance marked for {student.user.username}.'}
