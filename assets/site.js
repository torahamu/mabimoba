/* サイト共通ナビ。jobs/ 下のページでは data-root="../" を使用。 */
(function(){
 const host=document.querySelector('#siteNav');if(!host)return;
 const root=host.dataset.root||'';
 const links=[['index.html','ホーム','home'],['jobs/index.html','職業別攻略','jobs'],['content/index.html','コンテンツ','content'],['runes/index.html','ルーン図鑑','rune'],['tools/damagecalc.html','ダメージ計算','damagecalc'],['tools/weeklyplanner.html','週数計算','tools']];
 const current=host.dataset.current;
 const header=document.createElement('header');header.className='portal-topbar';
 const inner=document.createElement('div');inner.className='portal-top-inner';
 const brand=document.createElement('a');brand.className='portal-brand';brand.href=root+'index.html';
 brand.innerHTML='<span class="portal-logo" aria-hidden="true">✧</span><span class="portal-brand-copy"><small>MABINOGI MOBILE · RESEARCH</small><strong>エリン調査ノート</strong></span>';
 const nav=document.createElement('nav');nav.className='portal-nav';nav.setAttribute('aria-label','サイト内メニュー');
 for(const [url,label,key] of links){const a=document.createElement('a');a.href=root+url;a.textContent=label;if(key===current)a.setAttribute('aria-current','page');nav.appendChild(a)}
 inner.append(brand,nav);header.appendChild(inner);host.replaceWith(header);
})();
