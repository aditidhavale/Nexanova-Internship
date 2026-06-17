// ================= LOGIN =================
document.getElementById("loginForm")?.addEventListener("submit", e=>{
    e.preventDefault();

    fetch("/login",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            email: email.value.trim(),
            password: password.value.trim()
        })
    })
    .then(r=>r.json())
    .then(d=>{
        if(d.role === "ADMIN"){
            window.location.href = "/dashboard";
        }
        else if(d.role === "EVALUATOR"){
            window.location.href = "/evaluation_page";
        }
        else{
            alert("Invalid login");
        }
    });
});


// ================= CONFIG =================
function createBatch(){
    fetch("/create_batch",{method:"POST",headers:{"Content-Type":"application/json"},
    body:JSON.stringify({name:bname.value,start:start.value,end:end.value})})
    .then(r=>r.json()).then(d=>alert(d.msg));
}

function createTech(){
    fetch("/create_tech",{method:"POST",headers:{"Content-Type":"application/json"},
    body:JSON.stringify({name:techname.value})})
    .then(r=>r.json()).then(d=>alert(d.msg));
}

function setRounds(){
    fetch("/set_rounds",{method:"POST",headers:{"Content-Type":"application/json"},
    body:JSON.stringify({batch:rbatch.value,technology:rtech.value,rounds:rounds.value})})
    .then(r=>r.json()).then(d=>alert(d.msg));
}


// ================= USER =================
function addUser(){
    fetch("/add_user",{method:"POST",headers:{"Content-Type":"application/json"},
    body:JSON.stringify({
        name:uname.value,
        email:uemail.value,
        password:upass.value,
        role:urole.value.toUpperCase()   // ✅ fix role
    })})
    .then(r=>r.json()).then(d=>alert(d.msg));
}


// ================= PARTICIPANT =================
function addParticipant(){
    fetch("/add_participant",{method:"POST",headers:{"Content-Type":"application/json"},
    body:JSON.stringify({name:pname.value,batch:pbatch.value,technology:ptech.value})})
    .then(r=>r.json()).then(d=>alert(d.msg));
}


// ================= ASSIGN =================
function assignEval(){
    fetch("/assign",{method:"POST",headers:{"Content-Type":"application/json"},
    body:JSON.stringify({
        participant:aparticipant.value,
        evaluator:aevaluator.value,
        technology:atech.value,
        round:around.value
    })})
    .then(r=>r.json()).then(d=>alert(d.msg));
}


// ================= EVALUATION =================
function submitEval(){
    fetch("/submit_eval",{method:"POST",headers:{"Content-Type":"application/json"},
    body:JSON.stringify({
        participant:participant.value,
        evaluator:evaluator.value,
        technology:tech.value,
        round:round.value,
        score:score.value,
        feedback:feedback.value
    })})
    .then(r=>r.json()).then(d=>alert(d.msg));
}


// ================= VIEW PARTICIPANTS =================
function viewParticipants(){
    fetch("/view_participants")
    .then(r=>r.json())
    .then(data=>{
        let list = document.getElementById("participantList");
        list.innerHTML = "";

        data.forEach(p=>{
            list.innerHTML += `<li>${p.name} | ${p.batch} | ${p.technology}</li>`;
        });
    });
}


// ================= ASSIGNMENTS VIEW =================
function getAssignments(){
    fetch("/get_assignments/"+evalname.value)
    .then(r=>r.json())
    .then(data=>{
        let list=document.getElementById("assignList");
        list.innerHTML="";
        data.forEach(i=>{
            list.innerHTML+=`<li>${i.participant} - Round ${i.round}</li>`;
        });
    });
}


// ================= REPORT =================
function getReport(){
    fetch("/report",{method:"POST",headers:{"Content-Type":"application/json"},
    body:JSON.stringify({technology:rtechfilter.value})})
    .then(r=>r.json())
    .then(data=>{
        let list=document.getElementById("reportList");
        list.innerHTML="";
        data.forEach(i=>{
            list.innerHTML+=`<li>${i.participant} - ${i.score}</li>`;
        });
    });
}


// ================= AVG =================
function getAvg(){
    fetch("/average",{method:"POST",headers:{"Content-Type":"application/json"},
    body:JSON.stringify({technology:avgtech.value})})
    .then(r=>r.json())
    .then(data=>{
        let list=document.getElementById("avgList");
        list.innerHTML="";
        data.forEach(i=>{
            list.innerHTML+=`<li>Round ${i.round} - Avg ${i.avg_score}</li>`;
        });
    });
}


// ================= EXPORT =================
function exportData(){
    fetch("/export")
    .then(r=>r.json())
    .then(d=>alert(d.msg));
}


// ================= ADMIN ACTIONS =================

// VIEW BATCH
function viewBatch(){
    fetch("/view_batch")
    .then(r=>r.json())
    .then(data=>{
        alert(JSON.stringify(data));
    });
}

// UPDATE BATCH
function updateBatch(){
    let id = prompt("Enter Batch ID:");
    let name = prompt("Enter New Name:");
    let start = prompt("Enter Start Date:");
    let end = prompt("Enter End Date:");

    fetch("/update_batch",{
        method:"PUT",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({id:id,name:name,start:start,end:end})
    })
    .then(r=>r.json())
    .then(d=>alert(d.msg));
}

// DELETE BATCH
function deleteBatch(){
    let id = prompt("Enter Batch ID:");
    if(confirm("Are you sure?")){
        fetch("/delete_batch/"+id,{ method:"DELETE" })
        .then(r=>r.json())
        .then(d=>alert(d.msg));
    }
}


// VIEW TECHNOLOGY
function viewTech(){
    fetch("/view_tech")
    .then(r=>r.json())
    .then(data=>{
        alert(JSON.stringify(data));
    });
}

// UPDATE TECHNOLOGY
function updateTech(){
    let id = prompt("Enter Tech ID:");
    let name = prompt("Enter New Name:");

    fetch("/update_tech",{
        method:"PUT",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({id:id,name:name})
    })
    .then(r=>r.json())
    .then(d=>alert(d.msg));
}

// DELETE TECHNOLOGY
function deleteTech(){
    let id = prompt("Enter Tech ID:");
    if(confirm("Are you sure?")){
        fetch("/delete_tech/"+id,{ method:"DELETE" })
        .then(r=>r.json())
        .then(d=>alert(d.msg));
    }
}