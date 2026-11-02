(function(){
 'use strict';
 const data=JSON.parse(document.getElementById('runeDataset').textContent);
 const els={q:document.getElementById('runeSearch'),status:document.getElementById('filterStatus'),slot:document.getElementById('filterSlot'),grade:document.getElementById('filterGrade'),cls:document.getElementById('filterClass'),grid:document.getElementById('runeGrid'),count:document.getElementById('runeCount'),more:document.getElementById('runeMore'),empty:document.getElementById('runeEmpty'),reset:document.getElementById('resetFilters')};
 const classes=[...new Set(data.flatMap(d=>d.classes).filter(c=>c!=='全クラス'))].sort((a,b)=>a.localeCompare(b,'ja'));
 for(const c of classes){const op=document.createElement('option');op.value=c;op.textContent=c;els.cls.appendChild(op)}
 const normal=s=>String(s??'').normalize('NFKC').toLocaleLowerCase('ja').replace(/\s+/g,' ').trim();
 const symbols={'武器':'⚔','防具':'⬡','アクセサリー':'✧','エンブレム':'◈'};
 const gradeClasses={'神話':'mythic','伝説':'legendary','エピック':'epic','エリート':'elite','レア':'rare','未確認':'unknown'};
 const statusClasses={'日本版実装':'status-jp','日本未実装':'status-future','日本未確認':'status-unknown','韓国のみ':'status-kr'};
 const incomingQuery=new URLSearchParams(window.location.search).get('q');
 if(incomingQuery)els.q.value=incomingQuery;
 const PAGE=48;let list=[],shown=0;
 function el(tag,cl,text){const x=document.createElement(tag);if(cl)x.className=cl;if(text!==undefined)x.textContent=text;return x}
 function card(r){
  const article=el('article','rune-item');article.dataset.grade=r.grade;
  const top=el('div','rune-top'), titleWrap=el('div','rune-title-wrap');
  const glyph=el('span','rune-glyph',symbols[r.slot]||'◇');glyph.setAttribute('aria-hidden','true');
  const name=el('h2','rune-title',r.name);titleWrap.append(glyph,name);
  const grade=el('span','rune-grade '+(gradeClasses[r.grade]||''),r.grade);top.append(titleWrap,grade);
  const tags=el('div','rune-badges');
  tags.append(el('span','rune-badge',r.slot),el('span','rune-badge '+(statusClasses[r.status]||''),r.status));
  for(const c of r.classes){tags.append(el('span','rune-badge',c))}
  const effect=el('p','rune-effect',r.effect);article.append(top,tags,effect);
  return article;
 }
 function appendMore(){
  const page=list.slice(shown,shown+PAGE),fragment=document.createDocumentFragment();
  for(const r of page)fragment.appendChild(card(r));els.grid.appendChild(fragment);shown+=page.length;
  els.more.hidden=shown>=list.length;
  els.more.textContent=`さらに表示（残り ${(list.length-shown).toLocaleString('ja-JP')} 件）`;
  els.count.textContent=`${list.length.toLocaleString('ja-JP')} 件一致 ／ ${shown.toLocaleString('ja-JP')} 件表示`;
 }
 function filter(){
  const q=normal(els.q.value),parts=q.split(' ').filter(Boolean);
  list=data.filter(r=>
   (!els.status.value||r.status===els.status.value)&&
   (!els.slot.value||r.slot===els.slot.value)&&
   (!els.grade.value||r.grade===els.grade.value)&&
   (!els.cls.value||r.classes.includes(els.cls.value)||r.classes.includes('全クラス'))&&
   parts.every(p=>normal(r.name+' '+r.effect).includes(p))
  );
  shown=0;els.grid.replaceChildren();els.empty.hidden=list.length!==0;els.more.hidden=true;
  appendMore();
 }
 [els.q,els.status,els.slot,els.grade,els.cls].forEach(e=>e.addEventListener(e===els.q?'input':'change',filter));
 els.reset.addEventListener('click',()=>{els.q.value='';for(const x of [els.status,els.slot,els.grade,els.cls])x.value='';filter();els.q.focus()});
 els.more.addEventListener('click',appendMore);
 filter();
})();
