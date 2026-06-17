// ---------------- SERVICE URLs ----------------
const API_GATEWAY = "http://127.0.0.1:8005/api";
const COURSE_SERVICE = "http://127.0.0.1:8001/api";
const TIMETABLE_SERVICE = "http://127.0.0.1:8004/api";
const SCHEDULE_SERVICE = "http://127.0.0.1:8002/api"; // ✅

let token = "";
let role = "";
let userId = "";
let currentWeekId = "week1";

// ---------------- DOM ELEMENTS ----------------
const authSection = document.getElementById("authSection");
const adminDashboard = document.getElementById("adminDashboard");
const studentDashboard = document.getElementById("studentDashboard");
const adminOutput = document.getElementById("adminOutput");
const studentOutput = document.getElementById("studentOutput");
const coursesModulesOutput = document.getElementById("coursesModulesOutput");

const studentDropdown = document.getElementById("studentDropdown");
const courseDropdown = document.getElementById("courseDropdown");
const slotCourseDropdown = document.getElementById("slotCourseDropdown");
const slotTrainerDropdown = document.getElementById("slotTrainerDropdown");

// Auth inputs
const nameInput = document.getElementById("name");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const roleSelect = document.getElementById("role");

// ---------------- AUTH ----------------
async function register() {
    const res = await fetch(`${API_GATEWAY}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name: nameInput.value,
            email: emailInput.value,
            password: passwordInput.value,
            role: roleSelect.value
        })
    });
    const data = await res.json();
    alert(data.message);
}

async function login() {
    const res = await fetch(`${API_GATEWAY}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            email: emailInput.value,
            password: passwordInput.value
        })
    });

    const data = await res.json();
    if (!res.ok) return alert(data.message);

    token = data.token;
    const payload = JSON.parse(atob(token.split(".")[1]));
    role = payload.role;
    userId = payload.user_id;

    authSection.classList.add("hidden");

    if (role === "Admin") {
        adminDashboard.classList.remove("hidden");
        populateEnrollDropdowns();
        populateAllocationDropdowns();
    }

    if (role === "Student") {
        studentDashboard.classList.remove("hidden");
        viewTimetable();
    }
}

// ---------------- VIEW TRAINERS ----------------
async function viewTrainers() {
    const res = await fetch(`${API_GATEWAY}/users/trainers`, {
        headers: { Authorization: token } // ✅ must include token
    });
    const trainers = await res.json();

    let html = `<table border="1">
        <tr><th>ID</th><th>Name</th><th>Email</th></tr>`;
    trainers.forEach(t => {
        html += `<tr><td>${t.id}</td><td>${t.name}</td><td>${t.email}</td></tr>`;
    });
    html += `</table>`;
    adminOutput.innerHTML = html;
}

// ---------------- VIEW COURSES ----------------
async function viewCourses() {
    coursesModulesOutput.innerHTML = "";
    const res = await fetch(`${COURSE_SERVICE}/courses`, {
        headers: { Authorization: token } // ✅ include token
    });
    const courses = await res.json();

    let html = `<table border="1">
        <tr><th>ID</th><th>Name</th><th>Duration</th></tr>`;
    courses.forEach(c => {
        html += `<tr><td>${c.id}</td><td>${c.name}</td><td>${c.duration}</td></tr>`;
    });
    html += `</table><br>`;

    // Modules for each course
    for (let c of courses) {
        const mRes = await fetch(`${COURSE_SERVICE}/courses/${c.id}/modules`, {
            headers: { Authorization: token } // ✅ include token
        });
        const modules = await mRes.json();
        html += `<b>${c.name} Modules:</b> ${modules.map(m => m.name).join(", ")}<br><br>`;
    }

    coursesModulesOutput.innerHTML = html;
}

// ---------------- CREATE SCHEDULE ----------------
async function createSchedule() {
    const res = await fetch(`${SCHEDULE_SERVICE}/schedule`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ week_id: currentWeekId })
    });
    const data = await res.json();
    alert(data.message);
}

// ---------------- VIEW SCHEDULE ----------------
async function viewSchedule() {
    const res = await fetch(`${SCHEDULE_SERVICE}/schedule/${currentWeekId}`, {
        headers: { Authorization: token } // ✅ include token
    });
    const slots = await res.json();

    if (!Array.isArray(slots) || slots.length === 0) {
        adminOutput.innerHTML = "Create schedule first";
        return;
    }

    let html = `<table border="1">
        <tr><th>Day</th><th>Time</th><th>Course</th><th>Trainer</th></tr>`;

    slots.forEach(s => {
        html += `<tr>
            <td>${s.day}</td>
            <td>${s.time}</td>
            <td>${s.course_name || "-"}</td>
            <td>${s.trainer_name || "-"}</td>
        </tr>`;
    });

    html += `</table>`;
    adminOutput.innerHTML = html;
}

// ---------------- ENROLL STUDENT ----------------
async function populateEnrollDropdowns() {
    const sRes = await fetch(`${API_GATEWAY}/users/students`, {
        headers: { Authorization: token } // ✅ include token
    });
    const students = await sRes.json();

    studentDropdown.innerHTML = `<option value="">Select Student</option>`;
    students.forEach(s =>
        studentDropdown.innerHTML += `<option value="${s.id}">${s.name}</option>`
    );

    const cRes = await fetch(`${COURSE_SERVICE}/courses`, {
        headers: { Authorization: token } // ✅ include token
    });
    const courses = await cRes.json();

    courseDropdown.innerHTML = `<option value="">Select Course</option>`;
    courses.forEach(c =>
        courseDropdown.innerHTML += `<option value="${c.id}">${c.name}</option>`
    );
}

async function enrollStudent() {
    if (!studentDropdown.value || !courseDropdown.value) {
        alert("Please select student and course");
        return;
    }

    const res = await fetch(`${API_GATEWAY}/enrollments`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: token // ✅ include token
        },
        body: JSON.stringify({
            student_id: Number(studentDropdown.value),
            course_id: Number(courseDropdown.value)
        })
    });

    const data = await res.json();
    alert(data.message || "Student enrolled successfully");
}

// ---------------- SLOT ALLOCATION ----------------
async function populateAllocationDropdowns() {
    const courses = await (await fetch(`${COURSE_SERVICE}/courses`, {
        headers: { Authorization: token } // ✅ include token
    })).json();
    slotCourseDropdown.innerHTML = `<option value="">Select Course</option>`;
    courses.forEach(c =>
        slotCourseDropdown.innerHTML += `<option value="${c.id}">${c.name}</option>`
    );

    const trainers = await (await fetch(`${API_GATEWAY}/users/trainers`, {
        headers: { Authorization: token } // ✅ include token
    })).json();

    slotTrainerDropdown.innerHTML = `<option value="">Select Trainer</option>`;
    trainers.forEach(t =>
        slotTrainerDropdown.innerHTML += `<option value="${t.id}">${t.name}</option>`
    );
}

async function allocateSlot() {
    const day = document.getElementById("slotDayDropdown").value;
    const time = document.getElementById("slotTimeDropdown").value;
    const courseId = slotCourseDropdown.value;
    const trainerId = slotTrainerDropdown.value;

    if (!day || !time || !courseId || !trainerId) {
        alert("Please select all fields");
        return;
    }

    const res = await fetch(`${SCHEDULE_SERVICE}/schedule/${currentWeekId}`, {
        headers: { Authorization: token } // ✅ include token
    });
    const slots = await res.json();

    const slot = slots.find(s => s.day === day && s.time === time);
    if (!slot) {
        alert("Slot not found");
        return;
    }

    await fetch(`${SCHEDULE_SERVICE}/schedule/slot/${slot.slot_id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json", Authorization: token },
        body: JSON.stringify({
            week_id: currentWeekId,
            course_id: Number(courseId),
            course_name: slotCourseDropdown.selectedOptions[0].text,
            trainer_id: Number(trainerId),
            trainer_name: slotTrainerDropdown.selectedOptions[0].text
        })
    });

    alert("Slot allocated successfully");
    viewSchedule();
}

// ---------------- STUDENT TIMETABLE ----------------
async function viewTimetable() {
    const res = await fetch(`${TIMETABLE_SERVICE}/timetable/student/${userId}`, {
        headers: { Authorization: token } // ✅ include token
    });
    const timetable = await res.json();

    let html = `<table border="1">
        <tr><th>Day</th><th>Courses</th></tr>`;

    Object.keys(timetable).forEach(day => {
        html += `<tr>
            <td>${day}</td>
            <td>${timetable[day].join(", ")}</td>
        </tr>`;
    });

    html += `</table>`;
    studentOutput.innerHTML = html;
}

// ---------------- LOGOUT ----------------
function logout() {
    location.reload();
}
