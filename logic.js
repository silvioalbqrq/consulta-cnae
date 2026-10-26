/* Lógica pura compartilhada entre index.html e test_logic.mjs (node --test). */
(function(){
const TAB={I:[[180000,4,0],[360000,7.3,5940],[720000,9.5,13860],[1800000,10.7,22500],[3600000,14.3,87300],[4800000,19,378000]],II:[[180000,4.5,0],[360000,7.8,5940],[720000,10,13860],[1800000,11.2,22500],[3600000,14.7,85500],[4800000,30,720000]],III:[[180000,6,0],[360000,11.2,9360],[720000,13.5,17640],[1800000,16,35640],[3600000,21,125640],[4800000,33,648000]],IV:[[180000,4.5,0],[360000,9,8100],[720000,10.2,12420],[1800000,14,39780],[3600000,22,183780],[4800000,33,828000]],V:[[180000,15.5,0],[360000,18,4500],[720000,19.5,12780],[1800000,20.5,25560],[3600000,23,62100],[4800000,30.5,540000]]};
const norm=s=>(s||"").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"");
const soDig=s=>(s||"").replace(/\D/g,"");
const fmtC=d=>d.length===7?d.slice(0,2)+"."+d.slice(2,4)+"-"+d.slice(4,5)+"-"+d.slice(5):d;

/* Aceita 00.00-0-00, 0000-0/00, 0000000 e separadores – — /. Não deixa espaço
   entre os grupos, para não transformar CNPJ/telefone em CNAE. */
function extractCnaes(text,exists){
  const found=[];
  const push=(raw,pos)=>{found.push({raw,pos});};
  const has=exists||(()=>true);
  let m;
  const reF=/\b(\d{2})[.\-–—/]?(\d{2})[.\-–—/]?(\d)[.\-–—/]?(\d{2})\b/g;
  while((m=reF.exec(text))){push(m[1]+m[2]+m[3]+m[4],m.index);}
  const re7=/(?<!\d)(\d{7})(?!\d)/g;
  while((m=re7.exec(text))){if(has(m[1]))push(m[1],m.index);}
  const seen=new Set(),out=[];
  for(const f of found){if(!seen.has(f.raw)){seen.add(f.raw);out.push(f);}}
  return out.sort((a,b)=>a.pos-b.pos);
}

function splitSections(text){
  const iP=text.search(/ATIVIDADE\s*ECON[OÔ]MICA\s*PRINCIPAL/i);
  const iS=text.search(/SECUND[AÁ]RIAS?/i);
  return {iP,iS};
}

function companyInfo(text){
  const out={cnpj:"",razao:""};
  const mc=text.match(/\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}/);
  if(mc)out.cnpj=mc[0];
  const mr=text.match(/NOME\s*EMPRESARIAL\s*\n?\s*([^\n]{3,80})/i);
  if(mr)out.razao=mr[1].replace(/[*_#]/g,"").trim();
  return out;
}

/* Faixa e alíquota efetiva. Devolve null quando o RBT12 passa do teto do Simples. */
function rateFor(anexo,rbt){
  const t=TAB[anexo];
  if(!t)return null;
  if(rbt>4800000)return null;
  const f=t.find(x=>rbt<=x[0])||t[t.length-1];
  const ef=rbt>0?((rbt*f[1]/100-f[2])/rbt*100):0;
  return {f,ef};
}

/* rows = [{cnae, x}] onde x é a linha da base (ou undefined). */
function verdictFor(rows){
  const known=rows.filter(r=>r.x);
  const ved=known.filter(r=>r.x.status==="VEDADO");
  const amb=known.filter(r=>r.x.status==="AMBIGUO");
  const des=known.filter(r=>r.x.status==="DESATIVADA");
  const unk=rows.filter(r=>!r.x);
  const meiOk=known.filter(r=>r.x.mei==="SIM");
  const anxSet=new Set();
  known.forEach(r=>{if(r.x.anexos&&r.x.anexos!=="?")r.x.anexos.split(",").forEach(a=>{if(TAB[a])anxSet.add(a);});});
  const anx=[...anxSet].sort();
  let cls,ico,txt;
  if(ved.length){
    if(ved.every(r=>r.x.revisar)){
      cls="warn";ico="⚠️";
      txt="<b>VEDAÇÃO A CONFIRMAR</b> — atividade(s) classificada(s) como vedada(s) por regra e marcada(s) <b>VALIDAR</b> na base: <b>"+ved.map(r=>fmtC(r.cnae)).join(", ")+"</b>. Confirme o enquadramento antes de concluir.";
    }else{
      cls="no";ico="⛔";
      txt="<b>EMPRESA IMPEDIDA de optar pelo Simples Nacional</b> (art. 17, LC 123/2006) — atividade vedada: <b>"+ved.map(r=>fmtC(r.cnae)).join(", ")+"</b>.";
      if(ved.some(r=>r.x.revisar))txt+=" <small>Há atividade(s) marcada(s) VALIDAR — confirme.</small>";
    }
  }else if(unk.length){
    cls="warn";ico="⚠️";
    txt="<b>INCONCLUSIVO</b> — "+unk.length+" código(s) não localizado(s) na base 2.3: <b>"+unk.map(r=>fmtC(r.cnae)).join(", ")+"</b>. O veredito não pode ser concluído.";
  }else if(des.length){
    cls="warn";ico="⚠️";
    txt="<b>CÓDIGO 2.2 DESATIVADO</b> — use o correspondente 2.3 antes de concluir: <b>"+des.map(r=>fmtC(r.cnae)).join(", ")+"</b>.";
  }else if(amb.length){
    cls="warn";ico="⚠️";
    const rev=amb.filter(r=>r.x.revisar);
    const semAnexo=amb.filter(r=>!r.x.anexos||r.x.anexos==="?");
    const ambAnx=[...new Set(amb.flatMap(r=>(r.x.anexos||"").split(",").filter(a=>TAB[a])))].sort();
    const frAmb=amb.some(r=>r.x.fatorR==="SIM");
    let why;
    if(semAnexo.length)why="há <b>"+semAnexo.length+"</b> atividade(s) sem anexo definido — <b>análise manual</b>";
    else why="há <b>"+amb.length+"</b> atividade(s) em <b>"+(ambAnx.length?"Anexo "+ambAnx.join(" / "):"anexo variável")+"</b> "+(frAmb?"sujeita(s) ao <b>Fator R</b> (folha ÷ receita ≥ 28% → Anexo III, senão V)":"com <b>mais de um anexo possível</b>");
    txt="<b>PODE OPTAR COM RESSALVA</b> — nenhuma atividade vedada, mas "+why+".";
    if(rev.length)txt+=" <small>Inclui "+rev.length+" classificação(ões) marcada(s) VALIDAR.</small>";
  }else{
    const rev=known.filter(r=>r.x.revisar);
    if(rev.length){
      cls="warn";ico="⚠️";
      txt="<b>PODE OPTAR</b> pelo Simples Nacional — todas as atividades permitem, mas <b>"+rev.length+"</b> classificação(ões) estão marcadas <b>VALIDAR</b> na base. Confirme antes de concluir.";
    }else{
      cls="ok";ico="✅";
      txt="<b>PODE OPTAR pelo Simples Nacional</b> — todas as atividades permitem.";
    }
  }
  let meiTxt="";
  if(unk.length)meiTxt="🧾 <b>MEI não confirmado</b> — há código(s) fora da base 2.3.";
  else if(known.length===1&&meiOk.length===1)meiTxt="🧾 <b>PODE SER MEI</b> — a atividade consta no Anexo XI (DAS fixo).";
  else if(known.length&&meiOk.length===known.length)meiTxt="🧾 As <b>"+known.length+"</b> atividades constam no Anexo XI, mas o <b>MEI exige uma única ocupação</b> — não é possível confirmar com mais de uma atividade.";
  else if(meiOk.length)meiTxt="🧾 <b>Permite MEI apenas em:</b> "+meiOk.map(r=>fmtC(r.cnae)).join(", ")+" — com as demais atividades combinadas, a empresa <b>não</b> pode ser MEI.";
  else if(known.length)meiTxt="🧾 Nenhuma atividade permite MEI.";
  return {cls,ico,txt,meiTxt,anx,ved,amb,unk,known,meiOk};
}

const CNAELogic={TAB,norm,soDig,fmtC,extractCnaes,splitSections,companyInfo,rateFor,verdictFor};
globalThis.CNAELogic=CNAELogic;
if(typeof module!=="undefined"&&module.exports)module.exports=CNAELogic;
})();
