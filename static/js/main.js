/**
 * Kaushal Setu — Main Application Script
 * Bridging the Skills-to-Employment Gap
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Password Visibility Toggle
    const togglePasswordBtns = document.querySelectorAll('.toggle-password-btn');
    togglePasswordBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            const targetInputId = this.getAttribute('data-target');
            const targetInput = document.getElementById(targetInputId);
            if (targetInput) {
                const isPassword = targetInput.getAttribute('type') === 'password';
                targetInput.setAttribute('type', isPassword ? 'text' : 'password');
                const icon = this.querySelector('i');
                if (icon) {
                    icon.classList.toggle('bi-eye', !isPassword);
                    icon.classList.toggle('bi-eye-slash', isPassword);
                }
            }
        });
    });

    // 2. Mobile Sidebar Toggle
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebarNav');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function () {
            sidebar.classList.toggle('show');
        });
    }

    // 3. Assessment Radio Choice Selection Highlighting & Progress
    const assessmentForm = document.getElementById('assessmentForm');
    if (assessmentForm) {
        const radioInputs = assessmentForm.querySelectorAll('input[type="radio"]');
        const progressBar = document.getElementById('assessmentProgressBar');
        const progressCount = document.getElementById('assessmentProgressCount');
        const totalCount = parseInt(assessmentForm.getAttribute('data-total') || '12', 10);

        function updateAssessmentProgress() {
            const answeredNames = new Set();
            radioInputs.forEach(r => {
                if (r.checked) {
                    answeredNames.add(r.name);
                }
            });
            const answered = answeredNames.size;
            const pct = Math.round((answered / totalCount) * 100);

            if (progressBar) {
                progressBar.style.width = pct + '%';
                progressBar.setAttribute('aria-valuenow', pct);
            }
            if (progressCount) {
                progressCount.textContent = `${answered} / ${totalCount} Answered`;
            }

            const submitBtn = document.getElementById('submitAssessmentBtn');
            if (submitBtn) {
                if (answered === totalCount) {
                    submitBtn.classList.remove('disabled');
                    submitBtn.removeAttribute('disabled');
                }
            }
        }

        radioInputs.forEach(radio => {
            radio.addEventListener('change', function () {
                // Remove 'selected' styling on siblings
                const parentGroup = this.closest('.question-card');
                if (parentGroup) {
                    parentGroup.querySelectorAll('.option-label').forEach(lbl => lbl.classList.remove('selected'));
                }
                const label = this.closest('.option-label');
                if (label && this.checked) {
                    label.classList.add('selected');
                }
                updateAssessmentProgress();
            });
        });

        // Initialize progress on page load
        updateAssessmentProgress();
    }

    // 4. Interactive Roadmap Task Checkbox Toggle via AJAX
    const taskToggles = document.querySelectorAll('.task-checkbox-toggle');
    taskToggles.forEach(chk => {
        chk.addEventListener('change', function () {
            const taskId = this.getAttribute('data-task-id');
            const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
            const card = document.getElementById(`task-card-${taskId}`);

            fetch(`/roadmap/toggle/${taskId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ is_completed: this.checked })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    if (card) {
                        card.classList.toggle('task-done', data.is_completed);
                    }
                    // Update roadmap progress bars on page if present
                    const mainPctLabel = document.getElementById('roadmapPercentageText');
                    const mainProgressBar = document.getElementById('roadmapMainProgress');
                    if (mainPctLabel) {
                        mainPctLabel.textContent = `${data.completion_percentage}%`;
                    }
                    if (mainProgressBar) {
                        mainProgressBar.style.width = `${data.completion_percentage}%`;
                    }
                }
            })
            .catch(err => {
                console.error("Error updating task status:", err);
            });
        });
    });

    // 5. Auto dismiss flash alerts after 6 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 6000);
    });
});

// Helper for Demo Credentials
function fillDemoCredentials() {
    const emailInput = document.getElementById('loginEmail');
    const pwdInput = document.getElementById('loginPassword');
    if (emailInput && pwdInput) {
        emailInput.value = 'student@example.com';
        pwdInput.value = 'Password123';
        emailInput.dispatchEvent(new Event('input', { bubbles: true }));
        pwdInput.dispatchEvent(new Event('input', { bubbles: true }));
    }
}
