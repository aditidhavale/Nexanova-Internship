// ================= GLOBAL VARIABLES =================
let currentQuestion = 0;
let totalQuestions = 0;
let timerInterval = null;

// ================= INIT QUIZ =================
function initQuiz(total, duration) {
    totalQuestions = total;
    currentQuestion = 0;

    showQuestion(0);
    startTimer(duration);
    updateNavColors();
}

// ================= SHOW QUESTION =================
function showQuestion(index) {
    document.querySelectorAll(".question").forEach(q => q.style.display = "none");

    let currentQ = document.getElementById("q" + index);
    if (currentQ) {
        currentQ.style.display = "block";
        currentQuestion = index;
    }

    updateNavColors();
}

// ================= NEXT / PREV =================
function nextQuestion() {
    if (currentQuestion < totalQuestions - 1) {
        showQuestion(currentQuestion + 1);
    }
}

function prevQuestion() {
    if (currentQuestion > 0) {
        showQuestion(currentQuestion - 1);
    }
}

// ================= DIRECT NAV =================
function goToQuestion(index) {
    showQuestion(index);
}

// ================= UPDATE NAV COLORS =================
function updateNavColors() {
    for (let i = 0; i < totalQuestions; i++) {
        let btn = document.getElementById("nav" + i);

        if (!btn) continue;

        if (i === currentQuestion) {
            btn.className = "nav-btn orange";
        } else {
            let answered = document.querySelector(
                '#q' + i + ' input[type=radio]:checked'
            );

            if (answered) {
                btn.className = "nav-btn green";
            } else {
                btn.className = "nav-btn red";
            }
        }
    }
}

// ================= AUTO SAVE =================
function attachAutoSave() {
    document.querySelectorAll(".answer-form").forEach(form => {
        form.addEventListener("change", function () {
            let formData = new FormData(this);

            fetch("/quiz/save_answer", {
                method: "POST",
                body: formData
            }).then(() => {
                updateNavColors();
            });
        });
    });
}

// ================= TIMER =================
function startTimer(duration) {
    let timeLeft = duration;

    let timerDisplay = document.getElementById("time");

    timerInterval = setInterval(() => {
        timeLeft--;

        if (timerDisplay) {
            timerDisplay.innerText = timeLeft;
        }

        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            alert("Time's up! Auto submitting quiz...");
            autoSubmit();
        }
    }, 1000);
}

// ================= AUTO SUBMIT =================
function autoSubmit() {
    let submitBtn = document.querySelector(".submit-btn");
    if (submitBtn) {
        submitBtn.click();
    }
}

// ================= SAFE SUBMIT =================
function confirmSubmit() {
    return confirm("Are you sure you want to submit the quiz?");
}

// ================= PAGE LOAD =================
window.onload = function () {

    let questionElements = document.querySelectorAll(".question");

    // Only run if quiz page
    if (questionElements.length > 0) {

        totalQuestions = questionElements.length;

        // Get duration from HTML
        let durationElement = document.getElementById("time");
        let duration = durationElement ? parseInt(durationElement.innerText) : 0;

        initQuiz(totalQuestions, duration);
        attachAutoSave();
    }
};