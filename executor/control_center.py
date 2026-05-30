CONTROL_CENTER_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ΝΟΥΣ AI OS</title>
<style>
body{margin:0;background:#0f0f0f;color:white;font-family:Arial}
.header{padding:14px;background:#151515;font-weight:bold;text-align:center}
.buttons{display:flex;gap:8px;overflow-x:auto;padding:10px;background:#111}
button{background:#00ff88;color:#000;border:0;border-radius:10px;padding:10px;font-weight:bold}
#chat{height:72vh;overflow-y:auto;padding:12px}
.msg{padding:10px;margin:8px 0;border-radius:12px;white-space:pre-wrap}
.user{background:#1d4ed8;margin-left:20%}
.ai{background:#222;margin-right:20%}
.bar{position:fixed;bottom:0;left:0;right:0;display:flex;gap:8px;padding:10px;background:#111}
input{flex:1;padding:12px;border-radius:10px;border:0}
</style>
</head>
<body>
<div class="header">🧠 ΝΟΥΣ AI OS</div>
<div class="buttons">
<button onclick="send('status')">STATUS</button>
<button onclick="send('memory')">MEMORY</button>
<button onclick="send('plugins')">PLUGINS</button>
<button onclick="send('evolve')">EVOLVE</button>
<button onclick="send('internet status')">INTERNET</button>
<button onclick="send('make plugin hello world')">MAKE PLUGIN</button>
<button onclick="send('plugins')">LIST PLUGINS</button>
<button onclick="send('stable')">STABLE</button>

</div>
<div id="chat"></div>

<br>
<input type="file" id="file">
<button onclick="uploadFile()">UPLOAD</button>
<div class="bar">
<input id="cmd" placeholder="Μίλα στον ΝΟΥ...">
<button onclick="send(document.getElementById('cmd').value)">SEND</button>
</div>
<script>
function bubble(text,cls){
 let d=document.createElement("div");
 d.className="msg "+cls;
 d.innerText=text;
 document.getElementById("chat").appendChild(d);
 d.scrollIntoView();
}
async function send(cmd){
 if(!cmd.trim()) return;
 bubble(cmd,"user");
 document.getElementById("cmd").value="";
 let r=await fetch("/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({command:cmd})});
 let data=await r.json();
 
let out = data.output || data.response || data;
if (typeof out === "object") {
  out = JSON.stringify(out, null, 2);
}
bubble(out, "ai");

}

async function uploadFile(){
 let f=document.getElementById("file").files[0];
 if(!f){ bubble("No file selected","ai"); return; }
 let fd=new FormData();
 fd.append("file",f);
 let r=await fetch("/upload",{method:"POST",body:fd});
 let data=await r.json();
 bubble(JSON.stringify(data,null,2),"ai");
}


async function showApps(){
 let r=await fetch("/apps");
 let apps=await r.json();
 if(!apps.length){ bubble("Δεν υπάρχουν εφαρμογές ακόμα.","ai"); return; }

 bubble("Εφαρμογές ΝΟΥΣ:", "ai");

 apps.forEach(a=>{
   let d=document.createElement("div");
   d.className="msg ai";
   d.innerHTML='<button onclick="window.open(\\''+a.url+'\\',\\'_blank\\')">Άνοιγμα '+a.title+'</button>';
   document.getElementById("chat").appendChild(d);
   d.scrollIntoView();
 });
}

</script>
</body>
</html>
"""
