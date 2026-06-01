def nous_dashboard_html():
    return r'''<!doctype html>
<html lang="el">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NOUS AI OS</title>
<style>
:root{
  --bg:#080d1c;
  --panel:#10172a;
  --panel2:#17203a;
  --card:#131c33;
  --text:#edf3ff;
  --muted:#8fa2c8;
  --line:#283552;
  --accent:#7c5cff;
  --accent2:#22d3ee;
  --ok:#22c55e;
  --bad:#ef4444;
  --warn:#f59e0b;
}
*{box-sizing:border-box}
body{
  margin:0;
  background:radial-gradient(circle at top left,#172554,#080d1c 45%);
  color:var(--text);
  font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}
button,input,textarea{font-family:inherit}
.app{display:grid;grid-template-columns:280px 1fr 380px;height:100vh;overflow:hidden}
.sidebar,.right{background:rgba(16,23,42,.94);border-color:var(--line);overflow:auto}
.sidebar{border-right:1px solid var(--line);padding:18px}
.right{border-left:1px solid var(--line);padding:14px}
.logo{font-size:23px;font-weight:900;margin-bottom:4px}
.sub{color:var(--muted);font-size:13px;margin-bottom:18px}
.nav button,.quick button,.miniBtn{
  width:100%;
  border:1px solid var(--line);
  background:var(--panel2);
  color:var(--text);
  padding:12px;
  margin:5px 0;
  border-radius:15px;
  text-align:left;
}
.nav button.active{border-color:var(--accent);background:rgba(124,92,255,.22)}
.nav button:hover,.quick button:hover,.miniBtn:hover{border-color:var(--accent)}
.main{display:flex;flex-direction:column;min-width:0}
.topbar{
  display:flex;align-items:center;justify-content:space-between;gap:10px;
  padding:14px 18px;border-bottom:1px solid var(--line);background:rgba(8,13,28,.8)
}
.badge{border:1px solid var(--line);border-radius:999px;padding:6px 10px;color:var(--muted);font-size:13px}
.ok{color:var(--ok)}.bad{color:var(--bad)}.warn{color:var(--warn)}
.workspace{flex:1;overflow:auto;padding:18px}
.hero{
  border:1px solid var(--line);border-radius:24px;padding:18px;
  background:linear-gradient(135deg,rgba(124,92,255,.20),rgba(34,211,238,.09));
  margin-bottom:14px;
}
.hero h1{margin:0 0 6px 0;font-size:24px}
.hero p{margin:0;color:var(--muted)}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.card{
  background:rgba(19,28,51,.92);border:1px solid var(--line);border-radius:20px;
  padding:14px;margin-bottom:12px;
}
.card h3{margin:0 0 10px 0;font-size:16px}
.kv{display:flex;justify-content:space-between;gap:8px;border-bottom:1px solid rgba(255,255,255,.06);padding:7px 0;font-size:13px}
.kv span:first-child{color:var(--muted)}
.chat{display:flex;flex-direction:column;height:100%}
.chatlog{flex:1;overflow:auto;padding:18px}
.msg{max-width:900px;margin:0 auto 12px auto;padding:14px;border:1px solid var(--line);border-radius:18px;background:rgba(19,28,51,.86);white-space:pre-wrap}
.msg.user{background:rgba(124,92,255,.16)}
.composer{padding:14px;border-top:1px solid var(--line);background:rgba(8,13,28,.88)}
.composer-inner{max-width:940px;margin:auto;display:flex;gap:10px}
textarea{
  flex:1;resize:none;min-height:54px;max-height:160px;border-radius:16px;
  border:1px solid var(--line);padding:14px;background:var(--panel);color:var(--text);outline:none
}
.send{border:none;border-radius:16px;padding:0 18px;background:var(--accent);color:white;font-weight:800}
pre{white-space:pre-wrap;word-break:break-word;max-height:300px;overflow:auto;background:#070b16;border:1px solid var(--line);border-radius:12px;padding:10px;font-size:12px}
.section{display:none}
.section.active{display:block}
.activity{font-size:13px;color:var(--muted);line-height:1.45}
.menuBtn{display:none;position:fixed;top:12px;left:12px;z-index:50;width:44px;height:44px;border-radius:14px;border:1px solid var(--line);background:var(--accent);color:white;font-size:22px;font-weight:900}
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:40}
.small{font-size:12px;color:var(--muted)}
.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:5px 8px;margin:3px;color:var(--muted);font-size:12px}
@media(max-width:1050px){
  .menuBtn{display:block}
  .app{grid-template-columns:1fr;height:auto;min-height:100vh;overflow:auto}
  .sidebar{position:fixed;left:-300px;top:0;bottom:0;width:292px;z-index:60;transition:left .22s ease;border-right:1px solid var(--line)}
  .sidebar.open{left:0}
  .overlay.show{display:block}
  .right{border:0;border-top:1px solid var(--line)}
  .main{min-height:100vh}
  .topbar{padding-left:64px}
  .grid{grid-template-columns:1fr}
}
</style>
</head>
<body>
<button class="menuBtn" onclick="openMenu()">☰</button>
<div class="overlay" id="overlay" onclick="closeMenu()"></div>

<div class="app">
  <aside class="sidebar" id="sidebar">
    <div class="logo">🧠 NOUS AI OS</div>
    <div class="sub">Personal agent workspace</div>

    <div class="nav" id="nav">
      <button onclick="showSection('home')" class="active">🏠 Home</button>
      <button onclick="showSection('chat')">💬 Chat</button>
      <button onclick="showSection('goals')">🏁 Goals</button>
      <button onclick="showSection('missions')">🎯 Missions</button>
      <button onclick="showSection('approvals')">✅ Approvals</button>
      <button onclick="showSection('companion')">📱 Companion</button>
      <button onclick="showSection('deploy')">🚀 Deploy</button>
      <button onclick="showSection('system')">📊 System</button>
      <button onclick="showSection('settings')">⚙ Settings</button>
    </div>

    <div class="card">
      <h3>Quick Actions</h3>
      <div class="quick">
        <button onclick="ops('full_validation')">🧠 Full Validation</button>
        <button onclick="ops('git_status')">📦 Git Status</button>
        <button onclick="ops('code_health')">🧪 Code Health</button>
        <button onclick="ops('reality_status')">✅ Reality Check</button>
        <button onclick="postAction('/remote/companion/home')">🏠 Android Home</button>
        <button onclick="postAction('/remote/companion/back')">↩ Android Back</button>
      </div>
    </div>
  </aside>

  <main class="main">
    <div class="topbar">
      <div><strong id="title">NOUS Home</strong> <span class="badge" id="healthBadge">loading...</span></div>
      <span class="badge">Owner Mode</span>
    </div>

    <div class="workspace">
      <section id="home" class="section active">
        <div class="hero">
          <h1>Καλώς ήρθες στον ΝΟΥΣ</h1>
          <p>ChatGPT-style agent + Replit-style workspace + Android Companion + Vercel deploy.</p>
        </div>
        <div class="grid">
          <div class="card"><h3>System Snapshot</h3><div id="homeStatus">Loading...</div></div>
          <div class="card"><h3>Capabilities</h3><div id="homeCaps">Loading...</div></div>
          <div class="card"><h3>Companion</h3><div id="homeCompanion">Loading...</div></div>
          <div class="card"><h3>Missions</h3><div id="homeMissions">Loading...</div></div>
        </div>
      </section>

      <section id="chat" class="section">
        <div class="chat" style="height:calc(100vh - 96px)">
          <div class="chatlog" id="chatlog">
            <div class="msg">Γράψε εντολή. Παραδείγματα: /status, /home, /back, /plan βελτίωσε το UI, /run έλεγξε το companion. Αν γράψεις απλό στόχο, ο Executive Layer θα φτιάξει mission και θα τρέξει ασφαλή βήματα.</div>
          </div>
          <div class="composer">
            <div class="composer-inner">
              <textarea id="prompt" placeholder="Γράψε στον ΝΟΥΣ..."></textarea>
              <button class="send" onclick="sendPrompt()">Send</button>
            </div>
          </div>
        </div>
      </section>


      <section id="goals" class="section">
        <div class="hero"><h1>🏁 Goals</h1><p>Μακροπρόθεσμοι στόχοι, progress, linked missions και next actions.</p></div>
        <div class="grid">
          <div class="card">
            <h3>Goal Actions</h3>
            <button class="miniBtn" onclick="seedGoals()">Seed Core Goals</button>
            <button class="miniBtn" onclick="loadGoals()">Refresh Goals</button>
          </div>
          <div class="card"><h3>Goal Status</h3><div id="goalStatus">Loading...</div></div>
        </div>
        <div class="card"><h3>Goal List</h3><div id="goalList">Loading...</div></div>
      </section>

      <section id="missions" class="section">
        <div class="hero"><h1>🎯 Missions</h1><p>Αποστολές, αυτόνομα σχέδια, progress και εκτέλεση ασφαλών tasks.</p></div>
        <div class="grid">
          <div class="card">
            <h3>Create Mission</h3>
            <button class="miniBtn" onclick="createMission('system_check')">System Check Mission</button>
            <button class="miniBtn" onclick="createMission('android_check')">Android Companion Mission</button>
            <button class="miniBtn" onclick="createMission('deploy_check')">Deploy Mission</button>
            <textarea id="missionPrompt" placeholder="π.χ. βελτίωσε το UI του ΝΟΥΣ"></textarea>
            <button class="miniBtn" onclick="createWorkspaceMission()">Create From Prompt</button>
          </div>
          <div class="card"><h3>Mission Status</h3><div id="missionStatus">Loading...</div></div>
        </div>
        <div class="card"><h3>Mission List</h3><pre id="missionList">Loading...</pre></div>
      </section>

      <section id="approvals" class="section">
        <div class="hero"><h1>✅ Approvals</h1><p>Εδώ θα εμφανίζονται tasks που χρειάζονται έγκριση πριν εκτελεστούν.</p></div>
        <div class="card"><h3>Pending Approvals</h3><pre id="approvalsBox">Loading...</pre></div>
      </section>

      <section id="companion" class="section">
        <div class="hero"><h1>📱 Android Companion</h1><p>Χέρια και μάτια του ΝΟΥΣ στο Android μέσω Accessibility.</p></div>
        <div class="grid">
          <div class="card">
            <h3>Controls</h3>
            <button class="miniBtn" onclick="postAction('/remote/companion/home')">HOME</button>
            <button class="miniBtn" onclick="postAction('/remote/companion/back')">BACK</button>
            <button class="miniBtn" onclick="postAction('/remote/companion/ui-tree')">Request UI Tree</button>
          </div>
          <div class="card"><h3>Status</h3><div id="companionStatus">Loading...</div></div>
        </div>
      </section>

      <section id="deploy" class="section">
        <div class="hero"><h1>🚀 Deployments</h1><p>Vercel deployment backend και ιστορικό.</p></div>
        <div class="grid">
          <div class="card">
            <h3>Deploy Actions</h3>
            <button class="miniBtn" onclick="ops('vercel_status')">Vercel Status</button>
            <button class="miniBtn" onclick="ops('deploy_vercel_test_app')">Deploy Test App</button>
          </div>
          <div class="card"><h3>Vercel</h3><div id="deployStatus">Loading...</div></div>
        </div>
      </section>

      <section id="system" class="section">
        <div class="hero"><h1>📊 System</h1><p>Reality gate, ops, health και raw status.</p></div>
        <div class="grid">
          <div class="card"><h3>Reality</h3><div id="realityStatus">Loading...</div></div>
          <div class="card"><h3>Ops</h3><div id="opsStatus">Loading...</div></div>
        </div>
      </section>

      <section id="settings" class="section">
        <div class="hero"><h1>⚙ Settings</h1><p>Owner token και local UI ρυθμίσεις.</p></div>
        <div class="card">
          <h3>Token</h3>
          <button class="miniBtn" onclick="setToken()">Set / Change Token</button>
          <button class="miniBtn" onclick="localStorage.removeItem('NOUS_TOKEN');alert('Token cleared')">Clear Token</button>
        </div>
      </section>
    </div>
  </main>

  <aside class="right">
    <div class="card"><h3>Live Output</h3><pre id="raw">–</pre></div>
    <div class="card"><h3>Activity Feed</h3><div class="activity" id="activity">Ready.</div></div>
  </aside>
</div>

<script>
const tokenKey="NOUS_TOKEN";
let currentSection="home";

function token(){
  let t=localStorage.getItem(tokenKey);
  if(!t){ t=prompt("Βάλε NOUS token για protected actions:"); if(t)localStorage.setItem(tokenKey,t); }
  return t||"";
}
function setToken(){ const t=prompt("NOUS token:", localStorage.getItem(tokenKey)||""); if(t)localStorage.setItem(tokenKey,t); }
function openMenu(){document.getElementById("sidebar").classList.add("open");document.getElementById("overlay").classList.add("show")}
function closeMenu(){document.getElementById("sidebar").classList.remove("open");document.getElementById("overlay").classList.remove("show")}
function renderObject(obj){document.getElementById("raw").textContent=JSON.stringify(obj,null,2)}
function feed(text){document.getElementById("activity").innerHTML=new Date().toLocaleTimeString()+" — "+text+"<br>"+document.getElementById("activity").innerHTML}
function kv(k,v){return `<div class="kv"><span>${k}</span><b>${v}</b></div>`}
async function getJson(path){const r=await fetch(path);return await r.json()}
async function postJson(path,body={}){const r=await fetch(path,{method:"POST",headers:{"Content-Type":"application/json","X-NOUS-TOKEN":token()},body:JSON.stringify(body)});return await r.json()}
function addMsg(text,cls=""){const c=document.getElementById("chatlog");const d=document.createElement("div");d.className="msg "+cls;d.textContent=text;c.appendChild(d);c.scrollTop=c.scrollHeight}

function showSection(id){
  closeMenu(); currentSection=id;
  document.querySelectorAll(".section").forEach(x=>x.classList.remove("active"));
  document.getElementById(id).classList.add("active");
  document.querySelectorAll(".nav button").forEach(x=>x.classList.remove("active"));
  [...document.querySelectorAll(".nav button")].find(b=>b.textContent.toLowerCase().includes(labelFor(id)))?.classList.add("active");
  document.getElementById("title").textContent="NOUS "+id.charAt(0).toUpperCase()+id.slice(1);
  refreshSection(id);
}
function labelFor(id){return ({home:"home",chat:"chat",missions:"missions",approvals:"approvals",companion:"companion",deploy:"deploy",system:"system",settings:"settings"}[id]||id)}

async function refreshSection(id){
  if(id==="home") return loadHome();
  if(id==="goals") return loadGoals();
  if(id==="missions") return loadMissions();
  if(id==="companion") return loadCompanion();
  if(id==="deploy") return loadDeploy();
  if(id==="system") return loadSystem();
  if(id==="approvals") return loadApprovals();
}

async function loadHome(){
  const st=await getJson("/remote/status"); const ms=await getJson("/remote/missions/status"); const cp=await getJson("/remote/companion/status"); const rt=await getJson("/remote/reality/status");
  document.getElementById("homeStatus").innerHTML=kv("status","online")+kv("keys",Object.keys(st).length);
  document.getElementById("homeCaps").innerHTML=kv("internet",rt.internet?.real?"✅":"❌")+kv("android intents",rt.android?.real_intents?"✅":"❌")+kv("gestures",rt.android?.real_gestures?"✅":"❌");
  document.getElementById("homeCompanion").innerHTML=kv("available",cp.available?"✅":"❌")+kv("commands",(cp.commands||[]).join(", "));
  document.getElementById("homeMissions").innerHTML=kv("total",ms.total)+kv("active",ms.active)+kv("done",ms.done)+kv("blocked",ms.blocked);
  renderObject({status:st,missions:ms,companion:cp,reality:rt});
}

async function loadGoals(){
  const data=await getJson("/remote/goals-v2/status");
  renderObject(data);

  document.getElementById("goalStatus").innerHTML=
    kv("total",data.total ?? "-")+
    kv("active",data.active ?? "-")+
    kv("done",data.done ?? "-");

  if(!data.goals || data.goals.length===0){
    document.getElementById("goalList").innerHTML="No goals yet.";
    return;
  }

  document.getElementById("goalList").innerHTML=data.goals.map(g=>`
    <div class="card">
      <h3>${g.title}</h3>
      ${kv("priority",g.priority)}
      ${kv("status",g.status)}
      ${kv("progress",(g.progress ?? 0)+"%")}
      ${kv("missions",(g.missions||[]).length)}
      <div class="small">${g.description||""}</div>
      <div style="margin-top:8px">${(g.next_actions||[]).map(x=>`<span class="pill">${x}</span>`).join("")}</div>
      <button class="miniBtn" onclick="refreshGoal('${g.id}')">Refresh Progress</button>
    </div>
  `).join("");
}

async function seedGoals(){
  const data=await postJson("/remote/goals-v2/seed",{});
  renderObject(data);
  feed("Seeded core goals");
  await loadGoals();
}

async function refreshGoal(id){
  const data=await postJson("/remote/goals-v2/refresh",{id});
  renderObject(data);
  feed("Refreshed goal "+id);
  await loadGoals();
}

async function loadMissions(){
  const ms=await getJson("/remote/missions/status"); const list=await getJson("/remote/missions");
  document.getElementById("missionStatus").innerHTML=kv("total",ms.total)+kv("active",ms.active)+kv("done",ms.done)+kv("blocked",ms.blocked);
  document.getElementById("missionList").textContent=JSON.stringify(list.slice(-8),null,2);
  renderObject(ms);
}
async function loadCompanion(){const d=await getJson("/remote/companion/status");document.getElementById("companionStatus").innerHTML=kv("package",d.package)+kv("available",d.available?"✅":"❌")+kv("commands",(d.commands||[]).join(", "));renderObject(d)}
async function loadDeploy(){const d=await getJson("/remote/vercel/status");document.getElementById("deployStatus").innerHTML=kv("installed",d.installed?"✅":"❌")+kv("logged in",d.logged_in?"✅":"❌")+kv("deployments",(d.deployments||[]).length);renderObject(d)}
async function loadSystem(){const r=await getJson("/remote/reality/status");const o=await getJson("/remote/ops/status");document.getElementById("realityStatus").innerHTML=kv("internet",r.internet?.real?"✅":"❌")+kv("browser read",r.browser_read?.real?"✅":"❌")+kv("gestures",r.android?.real_gestures?"✅":"❌");document.getElementById("opsStatus").innerHTML=kv("safe actions",(o.safe_actions||[]).length)+kv("blocked",(o.blocked||[]).length);renderObject({reality:r,ops:o})}
async function loadApprovals(){
  const data=await getJson("/remote/missions/approvals");
  renderObject(data);

  if(!data.approvals || data.approvals.length===0){
    document.getElementById("approvalsBox").innerHTML="No pending approvals.";
    return;
  }

  document.getElementById("approvalsBox").innerHTML=data.approvals.map(a=>`
    <div class="card">
      <h3>${a.task_title}</h3>
      ${kv("mission",a.mission_title)}
      ${kv("action",a.action)}
      ${kv("status",a.status)}
      <button class="miniBtn" onclick="approveTask('${a.mission_id}','${a.task_id}')">✅ Approve Task</button>
      <button class="miniBtn" onclick="runMission('${a.mission_id}')">▶ Run Mission</button>
    </div>
  `).join("");
}


async function approveTask(missionId, taskId){
  const data=await postJson("/remote/missions/approve-task",{mission_id:missionId,task_id:taskId});
  renderObject(data);
  feed("Approved task "+taskId);
  await loadApprovals();
  await loadMissions();
}

async function runMission(id){
  const data=await postJson("/remote/missions/run-cycle",{id:id,max_steps:3});
  renderObject(data);
  feed("Ran mission "+id);
  await loadApprovals();
  await loadMissions();
}

async function postAction(path){closeMenu();const data=await postJson(path,{});renderObject(data);feed("Action "+path);addMsg("Action: "+path+"\n"+JSON.stringify(data,null,2))}
async function ops(action){closeMenu();const payload={};if(action==="checkpoint")payload.message=prompt("Commit message:","NOUS safe checkpoint")||"NOUS safe checkpoint";const data=await postJson("/remote/ops/run",{action,payload});renderObject(data);feed("Ops "+action);addMsg("Ops: "+action+"\n"+JSON.stringify(data,null,2))}
async function createMission(kind){const data=await postJson("/remote/missions/create-standard",{kind});renderObject(data);feed("Mission created "+kind);await loadMissions()}
async function createWorkspaceMission(){const prompt=document.getElementById("missionPrompt").value||"";const data=await postJson("/remote/workspace/create-mission",{prompt});renderObject(data);feed("Workspace mission created");await loadMissions()}

async function sendPrompt(){
  const p=document.getElementById("prompt"); const text=p.value.trim(); if(!text)return; p.value=""; addMsg(text,"user");
  if(text==="/status"){const d=await getJson("/remote/status");renderObject(d);addMsg(JSON.stringify(d,null,2));return}
  if(text==="/home"){const d=await postJson("/remote/companion/home",{});renderObject(d);addMsg(JSON.stringify(d,null,2));return}
  if(text==="/back"){const d=await postJson("/remote/companion/back",{});renderObject(d);addMsg(JSON.stringify(d,null,2));return}
  if(text.startsWith("/mission ")){const d=await postJson("/remote/workspace/create-mission",{prompt:text.slice(9)});renderObject(d);addMsg(JSON.stringify(d,null,2));return}
  if(text.startsWith("/plan ")){const d=await postJson("/remote/executive/plan",{prompt:text.slice(6)});renderObject(d);addMsg(JSON.stringify(d,null,2));return}
  if(text.startsWith("/run ")){const d=await postJson("/remote/executive/run",{prompt:text.slice(5),max_steps:3,execute:true});renderObject(d);addMsg(JSON.stringify(d,null,2));return}

  const d=await postJson("/remote/executive/run",{prompt:text,max_steps:2,execute:true});
  renderObject(d);
  addMsg(JSON.stringify(d,null,2));
}

async function boot(){
  try{await getJson("/health");document.getElementById("healthBadge").textContent="healthy";document.getElementById("healthBadge").className="badge ok"}catch(e){document.getElementById("healthBadge").textContent="offline";document.getElementById("healthBadge").className="badge bad"}
  await loadHome();
}
boot();
</script>
</body>
</html>'''
