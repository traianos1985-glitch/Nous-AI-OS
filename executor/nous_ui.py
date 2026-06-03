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

<style id="nous-sidebar-groups-css">
.navGroup{
  border:1px solid rgba(255,255,255,.08);
  border-radius:14px;
  margin:8px 10px;
  overflow:hidden;
  background:rgba(255,255,255,.025);
}
.navGroup summary{
  cursor:pointer;
  padding:10px 12px;
  font-weight:700;
  opacity:.95;
  list-style:none;
  user-select:none;
}
.navGroup summary::-webkit-details-marker{display:none}
.navGroup summary:after{
  content:"▾";
  float:right;
  opacity:.65;
}
.navGroup:not([open]) summary:after{content:"▸"}
.navGroup .navGroupBody{
  display:flex;
  flex-direction:column;
  gap:6px;
  padding:0 8px 10px 8px;
}
.navGroup .navGroupBody button,
.navGroup .navGroupBody a{
  width:100%;
  text-align:left;
}
.sidebarHint{
  font-size:12px;
  opacity:.65;
  padding:6px 18px 2px 18px;
}
</style>


<style id="nous-hide-tech-details-css">
.nousTechDetails{
  margin-top:10px;
  opacity:.75;
  font-size:12px;
}
.nousTechDetails summary{
  cursor:pointer;
  opacity:.8;
}
.nousTechDetails pre{
  display:none;
}
.nousTechDetails[open] pre{
  display:block;
  max-height:260px;
  overflow:auto;
  white-space:pre-wrap;
  padding:10px;
  border-radius:10px;
  background:rgba(0,0,0,.25);
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
      
<div class="navGroup" open id="nous-chat-main-nav">
  <summary>💬 Chat</summary>
  <div class="navGroupBody">
    <button onclick="showSection('chat')">💬 Άνοιγμα Chat</button>
  </div>
</div>

<div class="sidebarHint">NOUS modules grouped</div>
<details class="navGroup" open><summary>🏠 Κέντρο</summary><div class="navGroupBody"><button onclick="showSection('home')" class="active">🏠 Home</button>
<button onclick="showSection('command')">🧭 Command</button></div></details>
<details class="navGroup"><summary>🎯 Goals & Missions</summary><div class="navGroupBody"><button onclick="showSection('goals')">🏁 Goals</button>
<button onclick="showSection('missions')">🎯 Missions</button>
<button onclick="showSection('planner')">🧩 Planner</button></div></details>
<details class="navGroup"><summary>🧠 Memory & Knowledge</summary><div class="navGroupBody"><button onclick="showSection('brain')">🧠 Brain</button></div></details>
<details class="navGroup"><summary>🛠 Maintenance</summary><div class="navGroupBody"><button onclick="showSection('diagnosis')">🩺 Diagnosis</button>
<button onclick="showSection('repair')">🛠 Repair</button>
<button onclick="showSection('patchapply')">🩹 PatchApply</button></div></details>
<details class="navGroup"><summary>🤖 Automation</summary><div class="navGroupBody"><button onclick="showSection('scheduler')">⏱ Scheduler</button>
<button onclick="showSection('autoexec')">🤖 AutoExec</button>
<button onclick="showSection('autoscheduler')">🔁 AutoSched</button>
<button onclick="showSection('loopv2')">♻ Loop v2</button>
<button onclick="showSection('loopv3')">👑 LoopV3</button></div></details>
<details class="navGroup"><summary>☁ Cloud & Deploy</summary><div class="navGroupBody"><button onclick="showSection('deploy')">🚀 Deploy</button>
<button onclick="showSection('backup')">☁️ Backup</button></div></details>
<details class="navGroup"><summary>⚙ Settings</summary><div class="navGroupBody"><button onclick="showSection('settings')">⚙ Settings</button></div></details>
<details class="navGroup"><summary>📦 Other</summary><div class="navGroupBody"><button onclick="showSection('chat')">💬 Chat</button>
<button onclick="showSection('approvals')">✅ Approvals</button>
<button onclick="showSection('companion')">📱 Companion</button>
<button onclick="showSection('system')">📊 System</button>
<button onclick="showSection('intelligence')">🧭 Intelligence</button>
<button onclick="showSection('learning')">🎓 Learning</button>
<button onclick="showSection('audit')">🧪 Audit</button>
<button onclick="showSection('analyst')">🧠 Analyst</button>
<button onclick="showSection('pending')">📥 Pending</button>
<button onclick="showSection('selfheal')">🧬 SelfHeal</button>
<button onclick="showSection('mega')">🧱 Mega</button>
<button onclick="showSection('upgrades')">📦 Upgrades</button>
<button onclick="showSection('graphs')">🕸 Graphs</button></div></details>
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
  <button onclick="showSection('documents')">📚 Documents</button>
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
          
<div class="card" id="chatUploadCard">
  <h3>📎 Upload & Learn</h3>
  <p>Ανέβασε PDF, DOCX, TXT ή εικόνα. Ο ΝΟΥΣ θα προσπαθήσει να το μάθει και μετά θα μπορείς να τον ρωτάς.</p>
  <input type="file" id="chatUploadFile" multiple>
  <input id="chatUploadNote" placeholder="Σημείωση π.χ. εγχειρίδιο αποκρύψεων" style="width:100%;padding:10px;margin-top:8px;">
  <button class="miniBtn" onclick="uploadChatFiles()">Upload & Learn</button>
</div>


<div class="card" id="conversationPanel">
  <h3>💬 Συνομιλίες</h3>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px;">
    <button class="miniBtn" onclick="newNousConversation()">Νέα συνομιλία</button>
    <button class="miniBtn" onclick="loadNousConversations()">Ανανέωση</button>
  </div>
  <select id="nousConversationSelect" onchange="selectNousConversation()" style="width:100%;padding:10px;">
    <option value="">Νέα συνομιλία</option>
  </select>
  <div id="activeConversationLabel" style="font-size:12px;opacity:.75;margin-top:6px;">Ενεργή: νέα συνομιλία</div>
</div>

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


      
      <section id="brain" class="section">
        <div class="hero">
          <h1>🧠 Brain State</h1>
          <p>Κεντρική εικόνα του ΝΟΥΣ: readiness, goals, missions, approvals και υγεία συστήματος.</p>
        </div>

        <div class="grid">
          <div class="card">
            <h3>Brain Status</h3>
            <div id="brainStatus">Loading...</div>
          </div>

          <div class="card">
            <h3>Readiness</h3>
            <div id="brainReadiness">Loading...</div>
          </div>
        </div>

        <div class="card">
          <h3>Brain Snapshot</h3>
          <pre id="brainSnapshot">Loading...</pre>
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

      
      
      
      <section id="intelligence" class="section">
        <div class="hero">
          <h1>🧭 Executive Intelligence</h1>
          <p>Τι πιστεύει ο ΝΟΥΣ ότι πρέπει να γίνει μετά, με βάση goals, missions, approvals, decisions και lessons.</p>
        </div>

        <div class="grid">
          <div class="card">
            <h3>Next Best Action</h3>
            <div id="nextBestAction">Loading...</div>
          </div>

          <div class="card">
            <h3>System Summary</h3>
            <div id="intelligenceSummary">Loading...</div>
          </div>
        </div>

        <div class="card">
          <h3>Recommendations</h3>
          <div id="intelligenceRecommendations">Loading...</div>
        </div>

        <div class="card">
          <h3>Executive Report</h3>
          <button class="miniBtn" onclick="loadIntelligence()">Refresh Intelligence</button>
          <pre id="executiveReport">Loading...</pre>
        </div>
      </section>


      <section id="learning" class="section">
        <div class="hero">
          <h1>🎓 Learning Memory</h1>
          <p>Τι έχει μάθει ο ΝΟΥΣ από missions, decisions και εκτελέσεις.</p>
        </div>

        <div class="grid">
          <div class="card">
            <h3>Learning Status</h3>
            <div id="learningStatus">Loading...</div>
          </div>

          <div class="card">
            <h3>Search Lessons</h3>
            <textarea id="lessonSearch" placeholder="π.χ. backup, companion, mission"></textarea>
            <button class="miniBtn" onclick="searchLessons()">Search</button>
            <button class="miniBtn" onclick="loadLearning()">Refresh</button>
          </div>
        </div>

        <div class="card">
          <h3>Recent Lessons</h3>
          <div id="lessonList">Loading...</div>
        </div>

        <div class="card">
          <h3>Lesson Search Results</h3>
          <pre id="lessonSearchResults">–</pre>
        </div>
      </section>


      <section id="backup" class="section">
        <div class="hero">
          <h1>☁️ Brain Backup / Restore</h1>
          <p>Portable brain snapshots, verification και restore preview.</p>
        </div>

        <div class="grid">
          <div class="card">
            <h3>Backup Actions</h3>
            <button class="miniBtn" onclick="createBrainBackup()">Create Brain Backup</button>
            <button class="miniBtn" onclick="loadBackupPanel()">Refresh Backups</button>
          </div>

          <div class="card">
            <h3>Restore Status</h3>
            <div id="restoreStatus">Loading...</div>
          </div>
        </div>

        <div class="card">
          <h3>Available Backups</h3>
          <div id="backupList">Loading...</div>
        </div>

        <div class="card">
          <h3>Backup Inspection</h3>
          <pre id="backupInspect">–</pre>
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
  
      <section id="scheduler" class="section">
        <div class="hero">
          <h1>⏱ Executive Scheduler</h1>
          <p>Safe executive review loop.</p>
        </div>

        <div class="card">
          <button class="miniBtn" onclick="schedulerRunOnce()">Run Once</button>
          <button class="miniBtn" onclick="schedulerStart()">Start</button>
          <button class="miniBtn" onclick="schedulerStop()">Stop</button>
          <button class="miniBtn" onclick="loadScheduler()">Refresh</button>
        </div>

        <div class="card">
          <h3>Status</h3>
          <pre id="schedulerStatus">Loading...</pre>
        </div>
      </section>


      <section id="planner" class="section">
        <div class="hero">
          <h1>🧩 Mission Planner</h1>
          <p>Ο ΝΟΥΣ προτείνει αποστολές για goals, και εσύ τις εγκρίνεις ή τις απορρίπτεις.</p>
        </div>

        <div class="grid">
          <div class="card">
            <h3>Planner Actions</h3>
            <button class="miniBtn" onclick="proposeMission()">➕ Propose New Mission</button>
            <button class="miniBtn" onclick="loadPlanner()">🔄 Refresh</button>
          </div>

          <div class="card">
            <h3>Planner Status</h3>
            <div id="plannerStatus">Loading...</div>
          </div>
        </div>

        <div class="card">
          <h3>Mission Proposals</h3>
          <div id="plannerProposals">Loading...</div>
        </div>
      </section>


      <section id="audit" class="section">
        <div class="hero">
          <h1>🧪 Dashboard Action Audit</h1>
          <p>Έλεγχος ότι τα βασικά κουμπιά/endpoints του NOUS απαντούν σωστά.</p>
        </div>
        <div class="card">
          <button class="miniBtn" onclick="runDashboardAudit()">Run Button Audit</button>
        </div>
        <div class="card">
          <h3>Audit Results</h3>
          <pre id="auditResults">–</pre>
        </div>
      </section>


      <section id="diagnosis" class="section">
        <div class="hero">
          <h1>🩺 Self Diagnosis</h1>
          <p>Ο ΝΟΥΣ ελέγχει backend, frontend endpoints, dashboard actions και προτείνει ασφαλείς διορθώσεις.</p>
        </div>
        <div class="card">
          <button class="miniBtn" onclick="runSelfDiagnosis()">Run Self Diagnosis</button>
          <button class="miniBtn" onclick="loadSelfDiagnosis()">Refresh Report</button>
        </div>
        <div class="card">
          <h3>Diagnosis Report</h3>
          <pre id="diagnosisReport">–</pre>
        </div>
      </section>


      <section id="repair" class="section">
        <div class="hero">
          <h1>🛠 Autonomous Repair</h1>
          <p>Ο ΝΟΥΣ δημιουργεί ασφαλείς repair proposals από τη διάγνωση και τα εφαρμόζει μόνο με έγκριση.</p>
        </div>

        <div class="grid">
          <div class="card">
            <h3>Repair Actions</h3>
            <button class="miniBtn" onclick="proposeRepair()">Generate Repair Proposal</button>
            <button class="miniBtn" onclick="loadRepair()">Refresh</button>
          </div>
          <div class="card">
            <h3>Repair Status</h3>
            <div id="repairStatus">Loading...</div>
          </div>
        </div>

        <div class="card">
          <h3>Repair Proposals</h3>
          <div id="repairProposals">Loading...</div>
        </div>
      </section>


      <section id="autoexec" class="section">
        <div class="hero">
          <h1>🤖 Auto Mission Executor</h1>
          <p>Εκτελεί μόνο ασφαλείς, allowlisted αποστολές χωρίς deploy, tap, restore ή destructive actions.</p>
        </div>

        <div class="grid">
          <div class="card">
            <h3>AutoExec Actions</h3>
            <button class="miniBtn" onclick="loadAutoExec()">Refresh</button>
            <button class="miniBtn" onclick="runAutoExec()">Run Safe Cycle</button>
            <button class="miniBtn" onclick="enableAutoExec()">Enable</button>
            <button class="miniBtn" onclick="disableAutoExec()">Disable</button>
          </div>
          <div class="card">
            <h3>Status</h3>
            <div id="autoExecStatus">Loading...</div>
          </div>
        </div>

        <div class="card">
          <h3>Safe Candidates</h3>
          <pre id="autoExecCandidates">Loading...</pre>
        </div>

        <div class="card">
          <h3>Blocked / Needs Approval</h3>
          <pre id="autoExecBlocked">Loading...</pre>
        </div>
      </section>


      <section id="autoscheduler" class="section">
        <div class="hero">
          <h1>🔁 Auto Mission Scheduler</h1>
          <p>Τρέχει αυτόματα safe auto mission cycles σε χρονικό διάστημα.</p>
        </div>
        <div class="card">
          <button class="miniBtn" onclick="loadAutoScheduler()">Refresh</button>
          <button class="miniBtn" onclick="runAutoSchedulerOnce()">Run Once</button>
          <button class="miniBtn" onclick="startAutoScheduler()">Start</button>
          <button class="miniBtn" onclick="stopAutoScheduler()">Stop</button>
        </div>
        <div class="card">
          <h3>Status</h3>
          <pre id="autoSchedulerStatus">Loading...</pre>
        </div>
      </section>

      <section id="analyst" class="section">
        <div class="hero">
          <h1>🧠 Code Analyst</h1>
          <p>Αναλύει failures, βρίσκει πιθανή αιτία και προτείνει candidate files χωρίς να αλλάζει κώδικα.</p>
        </div>
        <div class="card">
          <button class="miniBtn" onclick="analyzeLatestDiagnosis()">Analyze Latest Diagnosis</button>
          <button class="miniBtn" onclick="loadCodeAnalyst()">Refresh</button>
        </div>
        <div class="card">
          <h3>Reports</h3>
          <pre id="codeAnalystReports">Loading...</pre>
        </div>
      </section>


      <section id="pending" class="section">
        <div class="hero">
          <h1>📥 Pending Review Inbox</h1>
          <p>Όλα όσα περιμένουν την έγκρισή σου από Planner, Repair, Approvals και Executive Intelligence.</p>
        </div>
        <div class="card">
          <button class="miniBtn" onclick="loadPendingReview()">Refresh Pending</button>
        </div>
        <div class="card">
          <h3>Pending Summary</h3>
          <div id="pendingSummary">Loading...</div>
        </div>
        <div class="card">
          <h3>Pending Items</h3>
          <div id="pendingItems">Loading...</div>
        </div>
      </section>

      <section id="loopv2" class="section">
        <div class="hero">
          <h1>♻ Executive Loop v2</h1>
          <p>Τρέχει diagnosis, code analysis, repair proposal, mission planner, safe execution και goal progress.</p>
        </div>
        <div class="card">
          <button class="miniBtn" onclick="runExecutiveLoopV2()">Run Executive Loop v2</button>
          <button class="miniBtn" onclick="loadExecutiveLoopV2()">Refresh</button>
        </div>
        <div class="card">
          <h3>Loop v2 Status</h3>
          <pre id="loopV2Status">Loading...</pre>
        </div>
      </section>


      <section id="command" class="section">
        <div class="hero">
          <h1>🧭 Executive Command Center</h1>
          <p>Κεντρική οθόνη ελέγχου: pending, goals, missions, diagnosis, repair, auto executor και backups.</p>
        </div>

        <div class="card">
          <button class="miniBtn" onclick="loadCommandCenter()">Refresh Command Center</button>
          <button class="miniBtn" onclick="runCommandCycle()">🚀 Run Executive Cycle</button>
        </div>

        <div class="grid">
          <div class="card">
            <h3>Command Summary</h3>
            <div id="commandSummary">Loading...</div>
          </div>
          <div class="card">
            <h3>Next Best Action</h3>
            <div id="commandNextAction">Loading...</div>
          </div>
        </div>

        <div class="grid">
          <div class="card">
            <h3>Pending Inbox</h3>
            <div id="commandPending">Loading...</div>
          </div>
          <div class="card">
            <h3>Automation State</h3>
            <div id="commandAutomation">Loading...</div>
          </div>
        </div>

        <div class="card">
          <h3>Full Command Data</h3>
          <pre id="commandFull">Loading...</pre>
        </div>
      </section>


      <section id="selfheal" class="section">
        <div class="hero">
          <h1>🧬 Self-Healing Lab</h1>
          <p>Deep code analysis, patch proposals και safe apply μόνο με έγκριση.</p>
        </div>

        <div class="card">
          <button class="miniBtn" onclick="runSelfHealing()">Run Self-Healing Analysis</button>
          <button class="miniBtn" onclick="loadSelfHealing()">Refresh</button>
        </div>

        <div class="grid">
          <div class="card">
            <h3>Status</h3>
            <div id="selfHealingStatus">Loading...</div>
          </div>
          <div class="card">
            <h3>Patch Proposals</h3>
            <div id="patchProposals">Loading...</div>
          </div>
        </div>

        <div class="card">
          <h3>Full Self-Healing Data</h3>
          <pre id="selfHealingFull">Loading...</pre>
        </div>
      </section>


      <section id="mega" class="section">
        <div class="hero">
          <h1>🧱 Mega Systems</h1>
          <p>Cleanup Engine, Goal Manager V2 και Executive Memory V3.</p>
        </div>
        <div class="grid">
          <div class="card">
            <h3>Cleanup Engine</h3>
            <button class="miniBtn" onclick="cleanupPreview()">Preview Cleanup</button>
            <button class="miniBtn" onclick="cleanupApply()">Apply Cleanup</button>
            <pre id="cleanupBox">–</pre>
          </div>
          <div class="card">
            <h3>Goal Manager V2</h3>
            <button class="miniBtn" onclick="generateGoalProjects()">Generate Projects</button>
            <button class="miniBtn" onclick="loadMegaSystems()">Refresh</button>
            <pre id="goalManagerBox">–</pre>
          </div>
        </div>
        <div class="card">
          <h3>Executive Memory V3</h3>
          <button class="miniBtn" onclick="learnExecutiveMemory()">Learn From Current State</button>
          <pre id="execMemoryBox">–</pre>
        </div>
      </section>

      <section id="upgrades" class="section">
        <div class="hero">
          <h1>📦 Upgrade Planner</h1>
          <p>Ο ΝΟΥΣ προτείνει μεγάλα upgrade packs και τα βάζει σε pending review.</p>
        </div>
        <div class="card">
          <button class="miniBtn" onclick="proposeUpgradePlan()">Propose Upgrade Plan</button>
          <button class="miniBtn" onclick="loadUpgradePlans()">Refresh</button>
        </div>
        <div class="card">
          <h3>Upgrade Plans</h3>
          <div id="upgradePlansBox">Loading...</div>
        </div>
      </section>


      <section id="patchapply" class="section">
        <div class="hero"><h1>🩹 Patch Apply & Rollback</h1><p>Εφαρμογή approved patch με backup, validation και rollback.</p></div>
        <div class="card">
          <button class="miniBtn" onclick="loadPatchApply()">Refresh</button>
        </div>
        <div class="grid">
          <div class="card"><h3>Patch Apply</h3><pre id="patchApplyBox">Loading...</pre></div>
          <div class="card"><h3>Rollback</h3><pre id="rollbackBox">Loading...</pre></div>
        </div>
      </section>

      <section id="graphs" class="section">
        <div class="hero"><h1>🕸 Repository & Knowledge Graph</h1><p>Χάρτης αρχείων, routes, functions, goals, missions και lessons.</p></div>
        <div class="card">
          <button class="miniBtn" onclick="buildRepoGraph()">Build Repository Graph</button>
          <button class="miniBtn" onclick="buildKnowledgeGraph()">Build Knowledge Graph</button>
          <button class="miniBtn" onclick="loadGraphs()">Refresh</button>
        </div>
        <div class="grid">
          <div class="card"><h3>Repository Graph</h3><pre id="repoGraphBox">Loading...</pre></div>
          <div class="card"><h3>Knowledge Graph</h3><pre id="knowledgeGraphBox">Loading...</pre></div>
        </div>
      </section>

      <section id="loopv3" class="section">
        <div class="hero"><h1>👑 Executive Loop V3</h1><p>Observe → Diagnose → Analyze → Plan → Execute → Learn.</p></div>
        <div class="card">
          <button class="miniBtn" onclick="runLoopV3()">Run Executive Loop V3</button>
          <button class="miniBtn" onclick="loadLoopV3()">Refresh</button>
        </div>
        <div class="card"><pre id="loopV3Box">Loading...</pre></div>
      </section>

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
function addMsg(text,cls=""){const c=document.getElementById("chatlog");const d=document.createElement("div");d.className="msg "+cls;if(window.NOUS_RENDER_CLEAN_MESSAGE){window.NOUS_RENDER_CLEAN_MESSAGE(d,text)}else{d.textContent=(typeof text==="object"?JSON.stringify(text):String(text))}c.appendChild(d);c.scrollTop=c.scrollHeight}

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
  if(id==="brain") return loadBrain();
  if(id==="goals") return loadGoals();
  if(id==="missions") return loadMissions();
  if(id==="companion") return loadCompanion();
  if(id==="deploy") return loadDeploy();
  if(id==="system") return loadSystem();
  if(id==="approvals") return loadApprovals();
}


function getToken(){
  return localStorage.getItem("NOUS_TOKEN") || "";
}

function authHeaders(extra){
  const t = getToken();
  const h = Object.assign({"Content-Type":"application/json"}, extra || {});
  if(t){
    h["X-NOUS-Token"] = t;
    h["Authorization"] = "Bearer " + t;
  }
  return h;
}

async function getJson(url){
  const r = await fetch(url, {headers: authHeaders({})});
  const data = await r.json().catch(()=>({error:"invalid_json"}));
  if(!r.ok){
    const err = {ok:false, status:r.status, error:data.error || "request_failed", url, data};
    renderObject(err);
    feed("GET failed " + r.status + " " + url);
    return err;
  }
  return data;
}

async function postJson(url, body){
  const r = await fetch(url, {
    method:"POST",
    headers: authHeaders({}),
    body: JSON.stringify(body || {})
  });
  const data = await r.json().catch(()=>({error:"invalid_json"}));
  if(!r.ok || data.error){
    const err = {ok:false, status:r.status, error:data.error || "request_failed", url, data};
    renderObject(err);
    feed("POST failed " + r.status + " " + url + " — " + err.error);
    return err;
  }
  return data;
}


async function loadHome(){
  const st=await getJson("/remote/status"); const ms=await getJson("/remote/missions/status"); const cp=await getJson("/remote/companion/status"); const rt=await getJson("/remote/reality/status");
  document.getElementById("homeStatus").innerHTML=kv("status","online")+kv("keys",Object.keys(st).length);
  document.getElementById("homeCaps").innerHTML=kv("internet",rt.internet?.real?"✅":"❌")+kv("android intents",rt.android?.real_intents?"✅":"❌")+kv("gestures",rt.android?.real_gestures?"✅":"❌");
  document.getElementById("homeCompanion").innerHTML=kv("available",cp.available?"✅":"❌")+kv("commands",(cp.commands||[]).join(", "));
  document.getElementById("homeMissions").innerHTML=kv("total",ms.total)+kv("active",ms.active)+kv("done",ms.done)+kv("blocked",ms.blocked);
  renderObject({status:st,missions:ms,companion:cp,reality:rt});
}






async function approveRecommendation(index){
  const ok = confirm("Να εγκρίνω και να εκτελέσω αυτή την πρόταση;");
  if(!ok) return;

  const data = await postJson("/remote/executive-intelligence/execute-recommendation", {index});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  feed("Approved recommendation " + index);
  await loadIntelligence();
  if(typeof loadApprovals === "function") await loadApprovals();
  if(typeof loadMissions === "function") await loadMissions();
}

async function rejectRecommendation(index){
  const reason = prompt("Λόγος απόρριψης:", "Δεν το εγκρίνω τώρα") || "User rejected recommendation";
  const data = await postJson("/remote/executive-intelligence/reject-recommendation", {index, reason});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  feed("Rejected recommendation " + index);
  await loadIntelligence();
}


async function loadIntelligence(){
  const status = await getJson("/remote/executive-intelligence/status");
  const report = await getJson("/remote/executive-intelligence/report");

  renderObject(status);

  const n = status.next_best_action || {};
  const sum = status.summary || {};

  document.getElementById("nextBestAction").innerHTML =
    kv("title", n.title || "-") +
    kv("type", n.type || "-") +
    kv("priority", n.priority ?? "-") +
    kv("action", n.action || "-") +
    `<div class="small" style="margin-top:8px">${n.reason || ""}</div>`;

  document.getElementById("intelligenceSummary").innerHTML =
    kv("goals", (sum.goals_active ?? "-") + " active / " + (sum.goals_total ?? "-")) +
    kv("missions", (sum.missions_active ?? "-") + " active, " + (sum.missions_blocked ?? "-") + " blocked") +
    kv("approvals", sum.approvals_pending ?? "-") +
    kv("decisions", sum.decisions_total ?? "-") +
    kv("lessons", (sum.lessons_total ?? "-") + " total") +
    kv("cloud ready", sum.cloud_ready) +
    kv("device ready", sum.device_ready);

  const recs = status.recommendations || [];
  document.getElementById("intelligenceRecommendations").innerHTML =
    recs.map((r,i)=>`
      <div class="card">
        <h3>${r.priority}. ${r.title}</h3>
        ${kv("type", r.type)}
        ${kv("action", r.action)}
        <div class="small">${r.reason}</div>
        <button class="miniBtn" onclick="approveRecommendation(${i})">✅ Approve & Execute</button>
        <button class="miniBtn" onclick="rejectRecommendation(${i})">❌ Reject</button>
      </div>
    `).join("");

  document.getElementById("executiveReport").textContent = report.report || JSON.stringify(report, null, 2);
}


async function loadLearning(){
  const status = await getJson("/remote/lessons/status");
  const lessons = await getJson("/remote/lessons/list");

  renderObject({status, lessons});

  document.getElementById("learningStatus").innerHTML =
    kv("total", status.total ?? "-") +
    kv("success", status.success ?? "-") +
    kv("failure", status.failure ?? "-");

  if(!lessons || lessons.length===0){
    document.getElementById("lessonList").innerHTML = "No lessons yet.";
    return;
  }

  document.getElementById("lessonList").innerHTML = lessons.slice(-20).reverse().map(l=>`
    <div class="card">
      <h3>${l.lesson}</h3>
      ${kv("outcome", l.outcome)}
      ${kv("confidence", l.confidence)}
      ${kv("mission", l.mission_id || "-")}
      <div style="margin-top:8px">${(l.tags||[]).map(x=>`<span class="pill">${x}</span>`).join("")}</div>
    </div>
  `).join("");
}

async function searchLessons(){
  const q = document.getElementById("lessonSearch").value || "";
  const data = await postJson("/remote/lessons/search", {query:q});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  document.getElementById("lessonSearchResults").textContent = JSON.stringify(data, null, 2);
  feed("Searched lessons");
}


async function loadBackupPanel(){
  const backups = await getJson("/remote/brain-backup/list");
  const restore = await getJson("/remote/brain-restore/status");

  renderObject({backups, restore});

  document.getElementById("restoreStatus").innerHTML =
    kv("restore_dir", restore.restore_dir || "-") +
    kv("safety_backups", (restore.safety_backups || []).length) +
    kv("blocked", (restore.blocked || []).join(", "));

  if(!backups.backups || backups.backups.length===0){
    document.getElementById("backupList").innerHTML="No backups yet.";
    return;
  }

  document.getElementById("backupList").innerHTML = backups.backups.map(b=>`
    <div class="card">
      <h3>${b.name}</h3>
      ${kv("size", b.size + " bytes")}
      ${kv("sha256", b.sha256.slice(0,16)+"...")}
      <div class="small">${b.path}</div>
      <button class="miniBtn" onclick="inspectBackup('${b.path}')">Inspect Backup</button>
      <button class="miniBtn" onclick="previewRestore('${b.path}')">Restore Preview</button>
    </div>
  `).join("");
}

async function createBrainBackup(){
  const data = await postJson("/remote/brain-backup/create", {});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  feed("Created brain backup");
  await loadBackupPanel();
}

async function inspectBackup(path){
  const data = await postJson("/remote/brain-restore/inspect", {path});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  document.getElementById("backupInspect").textContent = JSON.stringify(data, null, 2);
  feed("Inspected backup");
}

async function previewRestore(path){
  const data = await postJson("/remote/brain-restore/apply", {path, apply:false});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  document.getElementById("backupInspect").textContent = JSON.stringify(data, null, 2);
  feed("Restore preview completed");
}


async function loadBrain(){
  const status = await getJson("/remote/brain/status");
  const state = await getJson("/remote/brain/state");

  renderObject(status);

  document.getElementById("brainStatus").innerHTML =
    kv("goals", status.goals?.total ?? "-") +
    kv("missions", status.missions?.total ?? "-") +
    kv("blocked", status.missions?.blocked ?? "-") +
    kv("approvals", status.approvals?.count ?? "-");

  const r = status.readiness || {};

  document.getElementById("brainReadiness").innerHTML =
    kv("cloud_ready", r.cloud_ready_foundation) +
    kv("device_ready", r.device_control_foundation) +
    kv("pending_approvals", r.pending_approvals ?? 0) +
    kv("ready_modules", (r.ready || []).length) +
    kv("missing_modules", (r.missing || []).length);

  document.getElementById("brainSnapshot").textContent =
    JSON.stringify(state.readiness, null, 2);
}


async function loadGoals(){
  const data=await getJson("/remote/goals-v2/status");
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}

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
      <button class="miniBtn" onclick="createMissionForGoal('${g.id}', '${g.title.replace(/'/g, "\\'")}')">Create Mission For Goal</button>
    </div>
  `).join("");
}

async function seedGoals(){
  const data=await postJson("/remote/goals-v2/seed",{});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  feed("Seeded core goals");
  await loadGoals();
}

async function refreshGoal(id){
  const data=await postJson("/remote/goals-v2/refresh",{id});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  feed("Refreshed goal "+id);
  await loadGoals();
}


async function createMissionForGoal(goalId, goalTitle){
  const title = prompt("Mission title:", "Advance goal: " + goalTitle);
  if(!title) return;

  const description = prompt("Mission description:", "Mission linked to goal: " + goalTitle) || "";

  const data = await postJson("/remote/goals-v2/create-mission", {
    goal_id: goalId,
    title,
    description,
    tasks: [
      {title:"Check code health", action:"code_health"},
      {title:"Check git status", action:"git_status"},
      {title:"Run reality check", action:"reality_status"},
      {title:"Full validation", action:"full_validation"}
    ]
  });

  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  feed("Created mission for goal");
  await loadGoals();
  await loadMissions();
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
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}

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
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  feed("Approved task "+taskId);
  await loadApprovals();
  await loadMissions();
}

async function runMission(id){
  const data=await postJson("/remote/missions/run-cycle",{id:id,max_steps:3});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  feed("Ran mission "+id);
  await loadApprovals();
  await loadMissions();
}

async function postAction(path){closeMenu();const data=await postJson(path,{});renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}feed("Action "+path);addMsg("Action: "+path+"\n"+JSON.stringify(data,null,2))}
async function ops(action){closeMenu();const payload={};if(action==="checkpoint")payload.message=prompt("Commit message:","NOUS safe checkpoint")||"NOUS safe checkpoint";const data=await postJson("/remote/ops/run",{action,payload});renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}feed("Ops "+action);addMsg("Ops: "+action+"\n"+JSON.stringify(data,null,2))}
async function createMission(kind){const data=await postJson("/remote/missions/create-standard",{kind});renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}feed("Mission created "+kind);await loadMissions()}
async function createWorkspaceMission(){const prompt=document.getElementById("missionPrompt").value||"";const data=await postJson("/remote/workspace/create-mission",{prompt});renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}feed("Workspace mission created");await loadMissions()}

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













async function loadPatchApply(){
  const a = await getJson("/remote/patch-apply/status");
  const r = await getJson("/remote/rollback/status");
  renderObject({patch_apply:a, rollback:r});
  document.getElementById("patchApplyBox").textContent = JSON.stringify(a, null, 2);
  document.getElementById("rollbackBox").textContent = JSON.stringify(r, null, 2);
}

async function loadGraphs(){
  const repo = await getJson("/remote/repository-graph/status");
  const kg = await getJson("/remote/knowledge-graph/status");
  renderObject({repository:repo, knowledge:kg});
  document.getElementById("repoGraphBox").textContent = JSON.stringify(repo, null, 2);
  document.getElementById("knowledgeGraphBox").textContent = JSON.stringify(kg, null, 2);
}

async function buildRepoGraph(){
  const data = await postJson("/remote/repository-graph/build", {});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  await loadGraphs();
}

async function buildKnowledgeGraph(){
  const data = await postJson("/remote/knowledge-graph/build", {});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  await loadGraphs();
}

async function loadLoopV3(){
  const data = await getJson("/remote/executive-loop-v3/status");
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  document.getElementById("loopV3Box").textContent = JSON.stringify(data, null, 2);
}

async function runLoopV3(){
  const ok = confirm("Να τρέξει Executive Loop V3; Θα κάνει μόνο safe execution και θα αφήσει approvals για εσένα.");
  if(!ok) return;
  const data = await postJson("/remote/executive-loop-v3/run", {trigger:"dashboard"});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  document.getElementById("loopV3Box").textContent = JSON.stringify(data, null, 2);
}


async function loadMegaSystems(){
  const cleanup = await getJson("/remote/cleanup/status");
  const goals = await getJson("/remote/goal-manager-v2/status");
  const mem = await getJson("/remote/executive-memory-v3/status");

  renderObject({cleanup, goals, mem});
  document.getElementById("cleanupBox").textContent = JSON.stringify(cleanup, null, 2);
  document.getElementById("goalManagerBox").textContent = JSON.stringify(goals, null, 2);
  document.getElementById("execMemoryBox").textContent = JSON.stringify(mem, null, 2);
}

async function cleanupPreview(){
  const data = await postJson("/remote/cleanup/preview", {});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  document.getElementById("cleanupBox").textContent = JSON.stringify(data, null, 2);
}

async function cleanupApply(){
  const ok = confirm("Να εφαρμοστεί cleanup; Θα απορρίψει duplicate pending proposals και θα κρατήσει λίγα backups.");
  if(!ok) return;
  const data = await postJson("/remote/cleanup/apply", {});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  document.getElementById("cleanupBox").textContent = JSON.stringify(data, null, 2);
  if(typeof loadPendingReview === "function") await loadPendingReview();
}

async function generateGoalProjects(){
  const data = await postJson("/remote/goal-manager-v2/generate", {});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  document.getElementById("goalManagerBox").textContent = JSON.stringify(data, null, 2);
}

async function learnExecutiveMemory(){
  const data = await postJson("/remote/executive-memory-v3/learn", {});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  document.getElementById("execMemoryBox").textContent = JSON.stringify(data, null, 2);
}

async function loadUpgradePlans(){
  const data = await getJson("/remote/upgrade-planner/plans");
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  if(!data || data.length===0){
    document.getElementById("upgradePlansBox").innerHTML = "No upgrade plans.";
    return;
  }
  document.getElementById("upgradePlansBox").innerHTML = data.slice().reverse().map(p=>`
    <div class="card">
      <h3>${p.title}</h3>
      ${kv("status", p.status)}
      <pre>${JSON.stringify(p.upgrades || [], null, 2)}</pre>
      ${
        p.status === "pending"
        ? `<button class="miniBtn" onclick="approveUpgradePlan('${p.id}')">✅ Approve Plan</button>
           <button class="miniBtn" onclick="rejectUpgradePlan('${p.id}')">❌ Reject</button>`
        : ""
      }
    </div>
  `).join("");
}

async function proposeUpgradePlan(){
  const data = await postJson("/remote/upgrade-planner/propose", {});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  await loadUpgradePlans();
  if(typeof loadPendingReview === "function") await loadPendingReview();
}

async function approveUpgradePlan(id){
  const data = await postJson("/remote/upgrade-planner/approve", {plan_id:String(id)});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  await loadUpgradePlans();
}

async function rejectUpgradePlan(id){
  const reason = prompt("Λόγος απόρριψης:", "Δεν το εγκρίνω τώρα") || "User rejected upgrade plan";
  const data = await postJson("/remote/upgrade-planner/reject", {plan_id:String(id), reason});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  await loadUpgradePlans();
}


async function loadSelfHealing(){
  const status = await getJson("/remote/self-healing/status");
  const proposals = await getJson("/remote/patch-generator/proposals");

  renderObject({status, proposals});

  const pg = status.patch_generator || {};
  document.getElementById("selfHealingStatus").innerHTML =
    kv("patch total", pg.total ?? 0) +
    kv("pending", pg.pending ?? 0) +
    kv("approved", pg.approved ?? 0) +
    kv("rejected", pg.rejected ?? 0);

  if(!proposals || proposals.length === 0){
    document.getElementById("patchProposals").innerHTML = "No patch proposals.";
  } else {
    document.getElementById("patchProposals").innerHTML = proposals.slice().reverse().map(p=>`
      <div class="card">
        <h3>${p.title}</h3>
        ${kv("status", p.status)}
        ${kv("risk", p.risk)}
        ${kv("can apply", p.can_apply)}
        <div class="small">${p.reason || ""}</div>
        <pre>${JSON.stringify(p.patches || [], null, 2)}</pre>
        ${
          p.status === "pending"
          ? `<button class="miniBtn" onclick="approvePatch('${p.id}')">✅ Approve Patch</button>
             <button class="miniBtn" onclick="rejectPatch('${p.id}')">❌ Reject Patch</button>`
          : ""
        }
      </div>
    `).join("");
  }

  document.getElementById("selfHealingFull").textContent = JSON.stringify({status, proposals}, null, 2);
}

async function runSelfHealing(){
  const data = await postJson("/remote/self-healing/run-analysis", {});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  feed("Self-healing analysis completed");
  await loadSelfHealing();
  if(typeof loadPendingReview === "function") await loadPendingReview();
}

async function approvePatch(id){
  const ok = confirm("Να εφαρμοστεί αυτό το patch; Θα γίνει compile check μετά.");
  if(!ok) return;
  const data = await postJson("/remote/patch-generator/approve", {proposal_id:String(id)});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  if(data.ok){ feed("Patch approved/applied"); }
  else { feed("Patch approval failed: " + (data.error || "unknown")); }
  await loadSelfHealing();
}

async function rejectPatch(id){
  const reason = prompt("Λόγος απόρριψης:", "Δεν το εγκρίνω τώρα") || "User rejected patch proposal";
  const data = await postJson("/remote/patch-generator/reject", {proposal_id:String(id), reason});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  feed("Patch proposal rejected");
  await loadSelfHealing();
}


async function loadCommandCenter(){
  const data = await getJson("/remote/command-center/status");
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}

  const s = data.summary || {};
  document.getElementById("commandSummary").innerHTML =
    kv("pending", s.pending_total ?? 0) +
    kv("active goals", s.goals_active ?? 0) +
    kv("active missions", s.missions_active ?? 0) +
    kv("blocked missions", s.missions_blocked ?? 0) +
    kv("repair pending", s.repair_pending ?? 0) +
    kv("diagnosis ok", s.diagnosis_ok) +
    kv("backups", s.backup_count ?? 0);

  const next = data.intelligence?.next_best_action || {};
  document.getElementById("commandNextAction").innerHTML =
    `<h3>${next.title || "No action"}</h3>` +
    kv("type", next.type || "-") +
    kv("action", next.action || "-") +
    `<div class="small">${next.reason || ""}</div>`;

  const pending = data.pending || {};
  document.getElementById("commandPending").innerHTML =
    kv("total", pending.total ?? 0) +
    kv("repair", pending.counts?.repair_proposals ?? 0) +
    kv("missions", pending.counts?.mission_proposals ?? 0) +
    kv("approvals", pending.counts?.mission_task_approvals ?? 0) +
    kv("executive", pending.counts?.executive_recommendations ?? 0) +
    `<button class="miniBtn" onclick="showSection('pending')">Open Pending Inbox</button>`;

  document.getElementById("commandAutomation").innerHTML =
    kv("auto executor", s.auto_executor_enabled) +
    kv("auto scheduler", s.auto_scheduler_enabled) +
    `<button class="miniBtn" onclick="showSection('autoexec')">Open AutoExec</button>
     <button class="miniBtn" onclick="showSection('autoscheduler')">Open AutoSched</button>`;

  document.getElementById("commandFull").textContent = JSON.stringify(data, null, 2);
}

async function runCommandCycle(){
  const ok = confirm("Να τρέξει ο πλήρης Executive Cycle; Θα κάνει safe execution και θα αφήσει εγκρίσεις στο Pending Inbox.");
  if(!ok) return;
  const data = await postJson("/remote/command-center/run-cycle", {trigger:"command_center"});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  document.getElementById("commandFull").textContent = JSON.stringify(data, null, 2);
  feed("Executive command cycle completed");
  await loadCommandCenter();
}


async function loadPendingReview(){
  const data = await getJson("/remote/pending-review/status");
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}

  document.getElementById("pendingSummary").innerHTML =
    kv("total", data.total ?? 0) +
    kv("repair", data.counts?.repair_proposals ?? 0) +
    kv("missions", data.counts?.mission_proposals ?? 0) +
    kv("approvals", data.counts?.mission_task_approvals ?? 0) +
    kv("executive", data.counts?.executive_recommendations ?? 0);

  const items = data.items || [];
  if(items.length === 0){
    document.getElementById("pendingItems").innerHTML = "No pending items.";
    return;
  }

  document.getElementById("pendingItems").innerHTML = items.map(x=>`
    <div class="card">
      <h3>${x.title || "-"}</h3>
      ${kv("type", x.type)}
      ${kv("source", x.source)}
      ${kv("risk", x.risk || "-")}
      <pre>${JSON.stringify(x.data || x, null, 2)}</pre>
      <button class="miniBtn" onclick="showSection('${x.action_tab}')">Open ${x.action_tab}</button>
    </div>
  `).join("");
}

async function loadExecutiveLoopV2(){
  const data = await getJson("/remote/executive-loop-v2/status");
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  document.getElementById("loopV2Status").textContent = JSON.stringify(data, null, 2);
}

async function runExecutiveLoopV2(){
  const ok = confirm("Να τρέξει Executive Loop v2; Θα κάνει μόνο safe execution και θα αφήσει approvals για εσένα.");
  if(!ok) return;
  const data = await postJson("/remote/executive-loop-v2/run", {trigger:"dashboard"});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  document.getElementById("loopV2Status").textContent = JSON.stringify(data, null, 2);
  feed("Executive Loop v2 completed");
  await loadPendingReview();
}


async function loadAutoScheduler(){
  const data = await getJson("/remote/auto-mission-scheduler/status");
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  document.getElementById("autoSchedulerStatus").textContent = JSON.stringify(data, null, 2);
}

async function runAutoSchedulerOnce(){
  const data = await postJson("/remote/auto-mission-scheduler/run-once", {});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  await loadAutoScheduler();
}

async function startAutoScheduler(){
  const secs = prompt("Interval seconds", "900");
  const data = await postJson("/remote/auto-mission-scheduler/start", {interval_seconds: parseInt(secs || "900")});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  await loadAutoScheduler();
}

async function stopAutoScheduler(){
  const data = await postJson("/remote/auto-mission-scheduler/stop", {});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  await loadAutoScheduler();
}

async function loadCodeAnalyst(){
  const data = await getJson("/remote/code-analyst/reports");
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  document.getElementById("codeAnalystReports").textContent = JSON.stringify(data, null, 2);
}

async function analyzeLatestDiagnosis(){
  const data = await postJson("/remote/code-analyst/analyze-latest-diagnosis", {});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  await loadCodeAnalyst();
}


async function loadAutoExec(){
  const data = await getJson("/remote/auto-mission-executor/status");
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}

  document.getElementById("autoExecStatus").innerHTML =
    kv("enabled", data.enabled) +
    kv("candidates", (data.candidates || []).length) +
    kv("blocked", (data.blocked || []).length);

  document.getElementById("autoExecCandidates").textContent = JSON.stringify(data.candidates || [], null, 2);
  document.getElementById("autoExecBlocked").textContent = JSON.stringify(data.blocked || [], null, 2);
}

async function runAutoExec(){
  const ok = confirm("Να τρέξει safe auto mission cycle; Θα εκτελεστούν μόνο allowlisted safe tasks.");
  if(!ok) return;
  const data = await postJson("/remote/auto-mission-executor/run", {
    max_missions: 1,
    max_steps_per_mission: 3,
    trigger: "dashboard"
  });
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  if(data.ok){ feed("Auto mission executor completed"); }
  else { feed("Auto mission executor failed: " + (data.error || "unknown")); }
  await loadAutoExec();
  if(typeof loadMissions === "function") await loadMissions();
  if(typeof loadGoals === "function") await loadGoals();
}

async function enableAutoExec(){
  const data = await postJson("/remote/auto-mission-executor/enable", {});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  await loadAutoExec();
}

async function disableAutoExec(){
  const data = await postJson("/remote/auto-mission-executor/disable", {});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  await loadAutoExec();
}


async function loadRepair(){
  const status = await getJson("/remote/autonomous-repair/status");
  const proposals = await getJson("/remote/autonomous-repair/proposals");

  renderObject({status, proposals});

  document.getElementById("repairStatus").innerHTML =
    kv("total", status.total ?? "-") +
    kv("pending", status.pending ?? "-") +
    kv("approved", status.approved ?? "-") +
    kv("rejected", status.rejected ?? "-");

  if(!proposals || proposals.length===0){
    document.getElementById("repairProposals").innerHTML = "No repair proposals yet.";
    return;
  }

  document.getElementById("repairProposals").innerHTML = proposals.slice().reverse().map(p=>`
    <div class="card">
      <h3>${p.title}</h3>
      ${kv("status", p.status)}
      ${kv("fix", p.fix_id)}
      ${kv("risk", p.risk)}
      <div class="small">${p.description || ""}</div>
      <h4>Diff / Patch</h4>
      <pre>${p.diff || ""}</pre>
      ${
        p.status === "pending" && p.fix_id !== "no_action_needed"
        ? `<button class="miniBtn" onclick="approveRepair('${p.id}')">✅ Approve Repair</button>
           <button class="miniBtn" onclick="rejectRepair('${p.id}')">❌ Reject</button>`
        : ""
      }
    </div>
  `).join("");
}

async function proposeRepair(){
  const data = await postJson("/remote/autonomous-repair/propose", {});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  feed("Repair proposal generated");
  await loadRepair();
}

async function approveRepair(id){
  const ok = confirm("Να εφαρμόσω αυτή την ασφαλή διόρθωση;");
  if(!ok) return;
  const data = await postJson("/remote/autonomous-repair/approve", {proposal_id:String(id)});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  if(data.ok){ feed("Repair approved/applied"); }
  else { feed("Repair failed: " + (data.error || "unknown")); }
  await loadRepair();
}

async function rejectRepair(id){
  const reason = prompt("Λόγος απόρριψης:", "Δεν το εγκρίνω τώρα") || "User rejected repair proposal";
  const data = await postJson("/remote/autonomous-repair/reject", {proposal_id:String(id), reason});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  feed("Repair proposal rejected");
  await loadRepair();
}


async function loadSelfDiagnosis(){
  const data = await getJson("/remote/self-diagnosis/status");
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  document.getElementById("diagnosisReport").textContent = JSON.stringify(data, null, 2);
}

async function runSelfDiagnosis(){
  const data = await postJson("/remote/self-diagnosis/run", {});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  document.getElementById("diagnosisReport").textContent = JSON.stringify(data, null, 2);
  feed("Self diagnosis completed");
}


async function runDashboardAudit(){
  const data = await getJson("/remote/dashboard-action-audit");
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  document.getElementById("auditResults").textContent = JSON.stringify(data, null, 2);
  feed("Dashboard action audit completed");
}


async function loadPlanner(){
  const status = await getJson("/remote/mission-planner/status");
  const proposals = await getJson("/remote/mission-planner/proposals");

  renderObject({status, proposals});

  document.getElementById("plannerStatus").innerHTML =
    kv("total", status.total ?? "-") +
    kv("pending", status.pending ?? "-") +
    kv("approved", status.approved ?? "-") +
    kv("rejected", status.rejected ?? "-");

  if(!proposals || proposals.length===0){
    document.getElementById("plannerProposals").innerHTML = "No proposals yet.";
    return;
  }

  document.getElementById("plannerProposals").innerHTML = proposals.slice().reverse().map(p=>`
    <div class="card">
      <h3>${p.title}</h3>
      ${kv("status", p.status)}
      ${kv("goal", p.goal_title || "-")}
      ${kv("kind", p.kind || "-")}
      ${kv("risk", p.risk || "-")}
      ${kv("impact", p.expected_impact || "-")}
      <div class="small">${p.reason || ""}</div>
      <h4>Tasks</h4>
      <pre>${JSON.stringify(p.tasks || [], null, 2)}</pre>
      ${
        p.status === "pending"
        ? `<button class="miniBtn" onclick="approveProposal(String('${p.id}'))">✅ Approve Mission</button>
           <button class="miniBtn" onclick="rejectProposal(String('${p.id}'))">❌ Reject</button>`
        : ""
      }
    </div>
  `).join("");
}

async function proposeMission(){
  const data = await postJson("/remote/mission-planner/propose", {});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  feed("Mission proposal created");
  await loadPlanner();
}

async function approveProposal(id){
  const ok = confirm("Να εγκρίνω αυτή την πρόταση και να δημιουργηθεί mission;");
  if(!ok) return;
  const data = await postJson("/remote/mission-planner/approve", {proposal_id:String(id)});
  document.getElementById("liveOutput").textContent = JSON.stringify(data, null, 2);
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  if(data.ok){ feed("Mission proposal approved"); }
  else { feed("Mission proposal approval failed: " + (data.error || "unknown")); }
  await loadPlanner();
}

async function rejectProposal(id){
  const reason = prompt("Λόγος απόρριψης:", "Δεν το εγκρίνω τώρα") || "User rejected mission proposal";
  const data = await postJson("/remote/mission-planner/reject", {proposal_id:String(id), reason});
  document.getElementById("liveOutput").textContent = JSON.stringify(data, null, 2);
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  if(data.ok){ feed("Mission proposal rejected"); }
  else { feed("Mission proposal rejection failed: " + (data.error || "unknown")); }
  await loadPlanner();
}


async function loadScheduler(){
  const data = await getJson("/remote/executive-scheduler-loop/status");
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  document.getElementById("schedulerStatus").textContent = JSON.stringify(data,null,2);
}

async function schedulerRunOnce(){
  const data = await postJson("/remote/executive-scheduler-loop/run-once",{});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  await loadScheduler();
}

async function schedulerStart(){
  const secs = prompt("Interval seconds","1800");
  const data = await postJson("/remote/executive-scheduler-loop/start",{interval_seconds:parseInt(secs||"1800")});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  await loadScheduler();
}

async function schedulerStop(){
  const data = await postJson("/remote/executive-scheduler-loop/stop",{});
  renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
  await loadScheduler();
}

async function boot(){
  try{await getJson("/health");document.getElementById("healthBadge").textContent="healthy";document.getElementById("healthBadge").className="badge ok"}catch(e){document.getElementById("healthBadge").textContent="offline";document.getElementById("healthBadge").className="badge bad"}
  await loadHome();
}
boot();
</script>

<script id="nous-auto-linkify">
(function(){
  function escapeHtml(s){
    return String(s)
      .replaceAll("&","&amp;")
      .replaceAll("<","&lt;")
      .replaceAll(">","&gt;");
  }

  function linkifyText(s){
    let html = escapeHtml(s);

    html = html.replace(
      /\b((https?:\/\/|www\.)[^\s<>"']+)/gi,
      function(url){
        let href = url.startsWith("http") ? url : "https://" + url;
        return '<a href="' + href + '" target="_blank" rel="noopener noreferrer">' + url + '</a>';
      }
    );

    html = html.replace(
      /\b([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})\b/gi,
      function(email){
        return '<a href="mailto:' + email + '">' + email + '</a>';
      }
    );

    return html;
  }

  function linkifyElement(el){
    if(!el || el.dataset.linkified === "1") return;
    if(el.children.length > 0) return;
    const text = el.textContent || "";
    if(!/(https?:\/\/|www\.|[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})/i.test(text)) return;
    el.innerHTML = linkifyText(text);
    el.dataset.linkified = "1";
  }

  function scan(){
    const selectors = [
      "#chat", "#messages", "#feed", "#raw",
      ".chat", ".message", ".bubble", ".answer",
      ".assistant", ".result", ".output", "pre"
    ];
    document.querySelectorAll(selectors.join(",")).forEach(function(el){
      if(el.children.length === 0){
        linkifyElement(el);
      }else{
        el.querySelectorAll("p,div,span,pre").forEach(linkifyElement);
      }
    });
  }

  const css = document.createElement("style");
  css.id = "nous-auto-linkify-css";
  css.textContent = `
    a[href^="http"], a[href^="mailto"]{
      text-decoration: underline;
      font-weight: 700;
      word-break: break-word;
    }
  `;
  if(!document.getElementById("nous-auto-linkify-css")){
    document.head.appendChild(css);
  }

  scan();
  new MutationObserver(scan).observe(document.body, {childList:true, subtree:true});
})();
</script>


<section id="documents" class="section">
  <div class="hero">
    <h1>📚 Document Intake</h1>
    <p>Ανέβασε ή κόλλησε κείμενο ώστε ο ΝΟΥΣ να το περάσει σε γνώση/μνήμη.</p>
  </div>
  <div class="card">
    <h3>Paste document text</h3>
    <input id="docTitle" placeholder="Τίτλος εγγράφου π.χ. manual αποκρύψεων" style="width:100%;padding:10px;margin-bottom:8px;">
    <textarea id="docText" placeholder="Κόλλησε εδώ κείμενο από εγχειρίδιο, σημειώσεις, οδηγίες..." style="width:100%;min-height:180px;padding:10px;"></textarea>
    <button class="miniBtn" onclick="saveLocalDocument()">Save local document memory</button>
    <button class="miniBtn" onclick="listLocalDocuments()">List local documents</button>
  </div>
  <div class="card">
    <h3>Local file preview</h3>
    <input type="file" id="docFile" multiple onchange="previewLocalFiles(event)">
    <p>Σημείωση: Το UI preview διαβάζει κείμενα τοπικά. Για μόνιμη εισαγωγή από Termux χρησιμοποίησε: <b>python run_document_intake.py path/to/file.pdf</b></p>
    <pre id="docPreview"></pre>
  </div>
</section>


<script id="nous-document-intake-ui">
function _docStore(){
  try { return JSON.parse(localStorage.getItem("NOUS_DOCUMENT_MEMORY") || "[]"); }
  catch(e){ return []; }
}
function _saveDocStore(items){
  localStorage.setItem("NOUS_DOCUMENT_MEMORY", JSON.stringify(items));
}
function saveLocalDocument(){
  const title = document.getElementById("docTitle")?.value || "Untitled document";
  const text = document.getElementById("docText")?.value || "";
  if(!text.trim()){ alert("Δεν υπάρχει κείμενο για αποθήκευση."); return; }
  const items = _docStore();
  items.push({
    id: Date.now(),
    created_at: new Date().toISOString(),
    title,
    text,
    summary: text.slice(0, 1200),
    words: text.trim().split(/\s+/).length
  });
  _saveDocStore(items);
  alert("Αποθηκεύτηκε τοπικά στο UI document memory.");
}
function listLocalDocuments(){
  const items = _docStore();
  renderObject({
    local_document_memory: items.map(x => ({
      id:x.id,
      title:x.title,
      created_at:x.created_at,
      words:x.words,
      summary:x.summary
    }))
  });
}
function previewLocalFiles(event){
  const out = document.getElementById("docPreview");
  const files = Array.from(event.target.files || []);
  out.textContent = "";
  files.forEach(file => {
    const reader = new FileReader();
    reader.onload = function(){
      out.textContent += "\n\n===== " + file.name + " =====\n" + String(reader.result).slice(0, 5000);
    };
    if(file.type.startsWith("text/") || /\.(txt|md|json|csv|py|html|css|js)$/i.test(file.name)){
      reader.readAsText(file);
    }else{
      out.textContent += "\n\n===== " + file.name + " =====\nStored preview only. Use Termux intake command for permanent library.";
    }
  });
}
</script>

















<script id="nous-clean-live-output-layer">
(function(){
  if(window.NOUS_CLEAN_LIVE_OUTPUT_LAYER) return;
  window.NOUS_CLEAN_LIVE_OUTPUT_LAYER = true;

  function parseMaybeJson(text){
    try { return JSON.parse(String(text || "").trim()); } catch(e){ return null; }
  }

  function cleanOutputFromObject(obj){
    if(!obj || typeof obj !== "object") return null;

    if(obj.mode === "document_recall" || obj.source === "document_chat_bridge"){
      return obj.human_answer || obj.answer || obj.response || obj.text || "Απάντηση από μαθημένο έγγραφο.";
    }

    if(obj.human_answer) return obj.human_answer;
    if(obj.summary && typeof obj.summary === "string") return obj.summary;
    if(obj.answer && typeof obj.answer === "string") return obj.answer;
    if(obj.response && typeof obj.response === "string") return obj.response;
    if(obj.text && typeof obj.text === "string") return obj.text;

    if(obj.executed && obj.mission){
      const title = obj.mission.title || "Αποστολή";
      const status = obj.mission.status || "άγνωστη";
      const tasks = Array.isArray(obj.mission.tasks) ? obj.mission.tasks.length : 0;
      return "Ο ΝΟΥΣ δημιούργησε αποστολή: " + title + ".\nΚατάσταση: " + status + ".\nΒήματα: " + tasks + ".";
    }

    if(obj.ok === true) return "Η ενέργεια ολοκληρώθηκε επιτυχώς.";
    if(obj.ok === false || obj.error) return "Προέκυψε σφάλμα: " + (obj.error || "άγνωστο σφάλμα") + ".";

    return null;
  }

  function cleanLiveOutputElement(el){
    if(!el || el.dataset.nousCleaned === "1") return;

    const text = el.textContent || "";
    const obj = parseMaybeJson(text);
    if(!obj) return;

    const clean = cleanOutputFromObject(obj);
    if(!clean) return;

    el.dataset.nousRawJson = text;
    el.dataset.nousCleaned = "1";
    el.textContent = clean;
  }

  function scan(){
    const candidates = [
      "#raw", "#output", "#liveOutput", "#live-output",
      ".raw", ".output", ".liveOutput", ".live-output",
      "pre"
    ];
    document.querySelectorAll(candidates.join(",")).forEach(cleanLiveOutputElement);
  }

  scan();
  new MutationObserver(scan).observe(document.body, {
    childList:true,
    subtree:true,
    characterData:true
  });
})();
</script>





<script id="nous-clean-human-answer-layer">
(function(){
  window.NOUS_CLEAN_HUMAN_ANSWER_LAYER = true;

  function normalizeText(input){
    if(input === null || input === undefined) return "";
    if(typeof input === "string") return input;
    if(typeof input === "object"){
      if(input.human_answer) return String(input.human_answer);
      if(input.answer) return String(input.answer);
      if(input.response) return String(input.response);
      if(input.text) return String(input.text);
      try { return JSON.stringify(input); } catch(e){ return String(input); }
    }
    return String(input);
  }

  function looksJson(text){
    text = String(text || "").trim();
    return text.startsWith("{") || text.startsWith("[");
  }

  function parseMaybeJson(text){
    try { return JSON.parse(String(text || "").trim()); } catch(e){ return null; }
  }

  function bestHuman(obj){
    if(!obj || typeof obj !== "object") return null;
    return obj.human_answer || obj.answer || obj.response || obj.text || obj.summary || null;
  }

  function renderCleanMessage(el, input){
    let text = normalizeText(input);

    if(!looksJson(text)){
      el.textContent = text;
      return;
    }

    const obj = parseMaybeJson(text);
    if(!obj){
      el.textContent = text;
      return;
    }

    const human = bestHuman(obj);
    if(!human){
      el.textContent = text;
      return;
    }

    el.innerHTML = "";

    const main = document.createElement("div");
    main.className = "nousHumanAnswer";
    main.textContent = String(human);
    el.appendChild(main);

    const sources = obj.sources || [];
    if(Array.isArray(sources) && sources.length){
      const srcBox = document.createElement("div");
      srcBox.className = "nousSourcesBox";
      srcBox.innerHTML = "<b>Πηγές:</b>";
      sources.slice(0,5).forEach(function(s, i){
        const line = document.createElement("div");
        line.textContent = "[" + (i+1) + "] " + (s.document || "document");
        srcBox.appendChild(line);
      });
      el.appendChild(srcBox);
    }
  }

  window.NOUS_RENDER_CLEAN_MESSAGE = renderCleanMessage;
  window.NOUS_HUMANIZE_TEXT = function(input){
    const text = normalizeText(input);
    if(!looksJson(text)) return text;
    const obj = parseMaybeJson(text);
    const human = bestHuman(obj);
    return human || text;
  };
})();
</script>


<script id="nous-chat-upload-ui">
async function uploadChatFiles(){
  const input = document.getElementById("chatUploadFile");
  const note = document.getElementById("chatUploadNote")?.value || "uploaded_from_chat";
  const files = Array.from(input?.files || []);

  if(!files.length){
    alert("Διάλεξε πρώτα αρχείο.");
    return;
  }

  for(const file of files){
    const fd = new FormData();
    fd.append("file", file);
    fd.append("note", note);

    addMsg("Ανεβάζω και μαθαίνω το αρχείο: " + file.name, "user");

    try{
      const r = await fetch("/remote/document/upload", {
        method: "POST",
        body: fd
      });

      const data = await r.json();
      addMsg(data, "bot");

      if(typeof renderObject === "function"){
        renderObject(data); if(window.nousCaptureConversation){nousCaptureConversation(data);}
      }
    }catch(e){
      addMsg("Σφάλμα upload: " + e, "bot");
    }
  }
}
</script>


<script id="nous-conversation-selector-js">
let NOUS_ACTIVE_CONVERSATION_ID = "";

function newNousConversation(){
  NOUS_ACTIVE_CONVERSATION_ID = "";
  const sel = document.getElementById("nousConversationSelect");
  if(sel) sel.value = "";
  const label = document.getElementById("activeConversationLabel");
  if(label) label.textContent = "Ενεργή: νέα συνομιλία";
  addMsg("Ξεκινάμε νέα συνομιλία.", "bot");
}

async function loadNousConversations(){
  try{
    const r = await fetch("/remote/conversations");
    const data = await r.json();
    const sel = document.getElementById("nousConversationSelect");
    if(!sel) return;

    const old = sel.value || NOUS_ACTIVE_CONVERSATION_ID || "";
    sel.innerHTML = '<option value="">Νέα συνομιλία</option>';

    (data.conversations || []).forEach(c => {
      const o = document.createElement("option");
      o.value = c.id;
      o.textContent = (c.title || "Συνομιλία") + " (" + (c.messages || 0) + ")";
      sel.appendChild(o);
    });

    if(old) sel.value = old;
  }catch(e){
    console.log("conversation list failed", e);
  }
}

async function selectNousConversation(){
  const sel = document.getElementById("nousConversationSelect");
  const id = sel ? sel.value : "";
  NOUS_ACTIVE_CONVERSATION_ID = id || "";

  const label = document.getElementById("activeConversationLabel");

  if(!id){
    if(label) label.textContent = "Ενεργή: νέα συνομιλία";
    addMsg("Άνοιξες νέα συνομιλία.", "bot");
    return;
  }

  try{
    const r = await fetch("/remote/conversations/" + encodeURIComponent(id));
    const data = await r.json();

    if(label) label.textContent = "Ενεργή: " + (data.title || id);

    const msgs = data.messages || [];
    const last = msgs.slice(-8).map(m => {
      const role = m.role === "user" ? "Εσύ" : "ΝΟΥΣ";
      return role + ": " + (m.content || "");
    }).join("\\n\\n");

    addMsg("Συνέχεια παλιάς συνομιλίας:\\n\\n" + last, "bot");
  }catch(e){
    addMsg("Δεν μπόρεσα να ανοίξω τη συνομιλία: " + e, "bot");
  }
}

window.addEventListener("load", () => {
  setTimeout(loadNousConversations, 800);
});
</script>


<script id="NOUS_CAPTURE_CONVERSATION_ID">
function nousCaptureConversation(data){
  try{
    if(data && data.conversation_id){
      NOUS_ACTIVE_CONVERSATION_ID = data.conversation_id;
      const label = document.getElementById("activeConversationLabel");
      if(label) label.textContent = "Ενεργή: " + (data.conversation?.title || data.conversation_id);
      loadNousConversations();
    }
  }catch(e){}
}
</script>

</body>
</html>'''
