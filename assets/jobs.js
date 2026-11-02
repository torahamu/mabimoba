(function(){
 const search=document.getElementById('jobSearch');if(!search)return;
 const buttons=Array.from(document.querySelectorAll('.job-filter'));
 const cards=Array.from(document.querySelectorAll('.job-directory-card'));
 const found=document.getElementById('jobFound');let active='all';
 const normalize=s=>String(s||'').normalize('NFKC').toLocaleLowerCase('ja').replace(/\s+/g,'');
 function update(){const q=normalize(search.value);let count=0;
  for(const card of cards){const okay=(active==='all'||card.dataset.family===active)&&normalize(card.dataset.name+' '+card.dataset.family).includes(q);card.hidden=!okay;if(okay)count++}
  found.textContent=`${count}職を表示`;
 }
 search.addEventListener('input',update);
 for(const b of buttons)b.addEventListener('click',()=>{active=b.dataset.family;for(const other of buttons){const yes=other===b;other.classList.toggle('active',yes);other.setAttribute('aria-pressed',String(yes))}update()});
 update();
})();
