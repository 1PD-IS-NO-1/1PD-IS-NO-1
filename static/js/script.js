document.addEventListener('DOMContentLoaded', function() {
    const markAttendanceBtn = document.getElementById('mark-attendance');
    const recognitionResults = document.getElementById('recognition-results');

    markAttendanceBtn.addEventListener('click', function() {
        const course = '{{ course }}';
        const date = '{{ date }}';

        fetch('/mark_attendance', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `course=${course}&date=${date}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                recognitionResults.textContent = `Recognized students: ${data.recognized.join(', ')}`;
            } else {
                recognitionResults.textContent = 'Failed to mark attendance';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            recognitionResults.textContent = 'An error occurred';
        });
    });
});
