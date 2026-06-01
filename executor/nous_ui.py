def nous_dashboard_html():
    return r'''<!doctype html>
<html lang="el">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NOUS AI OS</title>
<style>
:root{
  --bg:#0b1020;
  --panel:#11182d;
  --panel2:#151f3a;
  --text:#eaf0ff;
  --muted:#8ea0c8;
  --line:#263453;
  --accent:#7c5cff;
  --ok:#22c55e;
  --bad:#ef4444;
  --warn:#f59e0b;
}
*{box-sizing:border-box}
body{
  margin:0;
  background:linear-gradient(135deg,#070b16,#101936);
  color:var(--text);
  font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}
.app{
  display:grid;
  grid-template-columns:260px 1fr 360px;
  height:100vh;
}
.sidebar,.right{
  background:rgba(17,24,45,.92);
  border-color:var(--line);
  overflow:auto;
}
.sidebar{border-right:1px solid var(--line);padding:18px}
.right{border-left:1px solid var(--line);padding:14px}
.logo{
  font-size:22px;
  font-weight:800;
  letter-spacing:.5px;
  margin-bottom:6px;
}
.sub{color:var(--muted);font-size:13px;margin-bottom:22px}
.nav button,.quick button,.toolbar button{
  width:100%;
  border:1px solid var(--line);
  background:var(--panel2);
  color:var(--text);
  padding:12px;
  margin:6px 0;
  border-radius:14px;
  text-align:left;
}
.nav button:hover,.quick button:hover,.toolbar button:hover{
  border-color:var(--accent);
}
.main{
  display:flex;
  flex-direction:column;
  min-width:0;
}
.topbar{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:14px 18px;
  border-bottom:1px solid var(--line);
  background:rgba(11,16,32,.72);
}
.badge{
  border:1px solid var(--line);
  border-radius:999px;
  padding:6px 10px;
  color:var(--muted);
  font-size:13px;
}
.chat{
  flex:1;
  overflow:auto;
  padding:20px;
}
.msg{
  max-width:880px;
  margin:0 auto 14px auto;
  padding:15px;
  border:1px solid var(--line);
  border-radius:18px;
  background:rgba(17,24,45,.82);
  white-space:pre-wrap;
}
.msg.user{background:rgba(124,92,255,.13)}
.composer{
  padding:14px;
  border-top:1px solid var(--line);
  background:rgba(11,16,32,.9);
}
.composer-inner{
  max-width:900px;
  margin:auto;
  display:flex;
  gap:10px;
}
textarea{
  flex:1;
  resize:none;
  min-height:54px;
  max-height:160px;
  border-radius:16px;
  border:1px solid var(--line);
  padding:14px;
  background:var(--panel);
  color:var(--text);
  outline:none;
}
.send{
  border:none;
  border-radius:16px;
  padding:0 18px;
  background:var(--accent);
  color:white;
  font-weight:700;
}
.card{
  background:rgba(21,31,58,.9);
  border:1px solid var(--line);
  border-radius:18px;
  padding:14px;
  margin-bottom:12px;
}
.card h3{
  margin:0 0 10px 0;
  font-size:15px;
}
.kv{
  display:flex;
  justify-content:space-between;
  gap:8px;
  border-bottom:1px solid rgba(255,255,255,.06);
  padding:7px 0;
  font-size:13px;
}
.kv span:first-child{color:var(--muted)}
pre{
  white-space:pre-wrap;
  word-break:break-word;
  max-height:260px;
  overflow:auto;
  background:#070b16;
  border:1px solid var(--line);
  border-radius:12px;
  padding:10px;
  font-size:12px;
}
.ok{color:var(--ok)}
.bad{color:var(--bad)}
.warn{color:var(--warn)}
.menuBtn{
  display:none;
  position:fixed;
  top:12px;
  left:12px;
  z-index:50;
  width:44px;
  height:44px;
  border-radius:14px;
  border:1px solid var(--line);
  background:var(--accent);
  color:white;
  font-size:22px;
  font-weight:800;
}
.overlay{
  display:none;
  position:fixed;
  inset:0;
  background:rgba(0,0,0,.55);
  z-index:40;
}
@media(max-width:980px){
  .menuBtn{display:block}
  .app{grid-template-columns:1fr;height:auto;min-height:100vh}
  .sidebar{
    position:fixed;
    left:-285px;
    top:0;
    bottom:0;
    width:280px;
    z-index:60;
    transition:left .22s ease;
    border-right:1px solid var(--line);
  }
  .sidebar.open{left:0}
  .overlay.show{display:block}
  .right{border:0;border-top:1px solid var(--line)}
  .main{min-height:100vh}
  .topbar{padding-left:64px}
}
</style>
</head>
<body>
<button class="menuBtn" onclick="openMenu()">☰</button>
<div class="overlay" id="overlay" onclick="closeMenu()"></div>

<div class="app">
  <aside class="sidebar" id="sidebar">
    <div class="logo">🧠 NOUS AI OS</div>
    <div class="sub">Cloud-ready agent workspace</div>

    <div class="nav">
      <button onclick="loadPanel('status')">📊 System Status</button>
      <button onclick="loadPanel('reality')">✅ Reality Gate</button>
      <button onclick="loadPanel('companion')">📱 Companion</button>
      <button onclick="loadPanel('knowledge')">📚 Knowledge</button>
      <button onclick="loadPanel('deploy')">🚀 Deploy</button>
      <button onclick="loadPanel('queue')">🧾 Queue</button>
    </div>


    <div class="card">
      <h3>Ops Console</h3>
      <div class="quick">
        <button onclick="ops('git_status')">📦 Git Status</button>
        <button onclick="ops('code_health')">🧪 Code Health</button>
        <button onclick="ops('reality_status')">✅ Reality Check</button>
        <button onclick="ops('full_validation')">🧠 Full Validation</button>
        <button onclick="ops('checkpoint')">💾 Safe Checkpoint</button>
        <button onclick="ops('deploy_vercel_test_app')">🚀 Deploy Test App</button>
      </div>
    </div>

    <div class="card">
      <h3>Quick Actions</h3>
      <div class="quick">
        <button onclick="postAction('/remote/companion/home')">🏠 Android Home</button>
        <button onclick="postAction('/remote/companion/back')">↩ Android Back</button>
        <button onclick="postAction('/remote/companion/ui-tree')">👁 Request UI Tree</button>
      </div>
    </div>
  </aside>

  <main class="main">
    <div class="topbar">
      <div>
        <strong>NOUS Console</strong>
        <span class="badge" id="healthBadge">loading...</span>
      </div>
      <span class="badge">Owner Mode</span>
    </div>

    <section class="chat" id="chat">
      <div class="msg">
Καλώς ήρθες στον νέο ΝΟΥΣ.

Μπορώ να δείχνω status, capabilities, companion state, deployments και actions.
Αυτό είναι UI v2: ChatGPT-style συνομιλία + Replit-style control workspace.
      </div>
    </section>

    <div class="composer">
      <div class="composer-inner">
        <textarea id="prompt" placeholder="Γράψε εντολή στον ΝΟΥΣ..."></textarea>
        <button class="send" onclick="sendPrompt()">Send</button>
      </div>
    </div>
  </main>

  <aside class="right">
    <div class="card">
      <h3>Live Panel</h3>
      <div id="panel">Loading...</div>
    </div>

    <div class="card">
      <h3>Raw Output</h3>
      <pre id="raw">–</pre>
    </div>
  </aside>
</div>

<script>
const tokenKey = "NOUS_TOKEN";

function token(){
  let t = localStorage.getItem(tokenKey);
  if(!t){
    t = prompt("Βάλε NOUS token για protected actions:");
    if(t) localStorage.setItem(tokenKey,t);
  }
  return t || "";
}

function addMsg(text, cls=""){
  const c=document.getElementById("chat");
  const d=document.createElement("div");
  d.className="msg "+cls;
  d.textContent=text;
  c.appendChild(d);
  c.scrollTop=c.scrollHeight;
}

async function getJson(path){
  const r=await fetch(path);
  return await r.json();
}

async function postJson(path, body={}){
  const r=await fetch(path,{
    method:"POST",
    headers:{
      "Content-Type":"application/json",
      "X-NOUS-TOKEN":token()
    },
    body:JSON.stringify(body)
  });
  return await r.json();
}

function renderObject(obj){
  document.getElementById("raw").textContent=JSON.stringify(obj,null,2);
}

function kv(k,v){
  return `<div class="kv"><span>${k}</span><b>${v}</b></div>`;
}

async function loadPanel(name){
  closeMenu();
  let data,path;
  if(name==="status") path="/remote/status";
  if(name==="reality") path="/remote/reality/status";
  if(name==="companion") path="/remote/companion/status";
  if(name==="knowledge") path="/remote/knowledge";
  if(name==="deploy") path="/remote/vercel/status";
  if(name==="queue") path="/remote/queue";

  data=await getJson(path);
  renderObject(data);

  let html="";
  if(name==="status"){
    html+=kv("status","online");
    html+=kv("keys",Object.keys(data).length);
  } else if(name==="reality"){
    html+=kv("internet",data.internet?.real ? "✅ real":"❌");
    html+=kv("browser read",data.browser_read?.real ? "✅ real":"❌");
    html+=kv("android intents",data.android?.real_intents ? "✅ real":"❌");
    html+=kv("gestures",data.android?.real_gestures ? "✅ real":"❌ blocked");
  } else if(name==="companion"){
    html+=kv("package",data.package || "-");
    html+=kv("available",data.available ? "✅":"❌");
    html+=kv("commands",(data.commands||[]).join(", "));
  } else if(name==="knowledge"){
    html+=kv("topics",data.topics ?? "-");
    html+=kv("open",data.open ?? "-");
    html+=kv("learned",data.learned ?? "-");
  } else if(name==="deploy"){
    html+=kv("installed",data.installed ? "✅":"❌");
    html+=kv("logged in",data.logged_in ? "✅":"❌");
    html+=kv("deployments",(data.deployments||[]).length);
  } else {
    html+=`<pre>${JSON.stringify(data,null,2)}</pre>`;
  }
  document.getElementById("panel").innerHTML=html;
}


async function ops(action){
  closeMenu();
  const payload = {};
  if(action==="checkpoint"){
    payload.message = prompt("Commit message:", "NOUS safe checkpoint") || "NOUS safe checkpoint";
  }
  const data = await postJson("/remote/ops/run", {action, payload});
  renderObject(data);
  addMsg("Ops action: "+action+"\n"+JSON.stringify(data,null,2));
}

async function postAction(path){
  closeMenu();
  const data=await postJson(path,{});
  renderObject(data);
  addMsg("Action: "+path+"\\n"+JSON.stringify(data,null,2));
}

async function sendPrompt(){
  const p=document.getElementById("prompt");
  const text=p.value.trim();
  if(!text)return;
  p.value="";
  addMsg(text,"user");

  if(text.startsWith("/status")){
    const d=await getJson("/remote/status");
    renderObject(d);
    addMsg(JSON.stringify(d,null,2));
    return;
  }

  if(text.startsWith("/home")){
    const d=await postJson("/remote/companion/home",{});
    renderObject(d);
    addMsg(JSON.stringify(d,null,2));
    return;
  }

  if(text.startsWith("/back")){
    const d=await postJson("/remote/companion/back",{});
    renderObject(d);
    addMsg(JSON.stringify(d,null,2));
    return;
  }

  addMsg("UI v2 command router ενεργό. Γράψε /status, /home, /back ή χρησιμοποίησε τα panels.");
}

function openMenu(){
  document.getElementById("sidebar").classList.add("open");
  document.getElementById("overlay").classList.add("show");
}
function closeMenu(){
  document.getElementById("sidebar").classList.remove("open");
  document.getElementById("overlay").classList.remove("show");
}

async function boot(){
  try{
    const h=await getJson("/health");
    document.getElementById("healthBadge").textContent="healthy";
    document.getElementById("healthBadge").className="badge ok";
  }catch(e){
    document.getElementById("healthBadge").textContent="offline";
    document.getElementById("healthBadge").className="badge bad";
  }
  loadPanel("status");
}
boot();
</script>
</body>
</html>'''
