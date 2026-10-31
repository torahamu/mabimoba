/* 共通ナビ。今後ページを追加する時は links に一行増やすだけです。 */
(function(){
 const links=[['index.html','ホーム','home'],['rune.html','ルーン図鑑','rune'],['damagecalc.html','ダメージ計算','damagecalc']];
 const host=document.querySelector('#siteNav');if(!host)return;
 const current=host.dataset.current;
 const header=document.createElement('header');header.className='portal-topbar';
 const inner=document.createElement('div');inner.className='portal-top-inner';
 const brand=document.createElement('a');brand.className='portal-brand';brand.href='index.html';
 brand.innerHTML='<span class="portal-logo" aria-hidden="true">✧</span><span class="portal-brand-copy"><small>MABINOGI MOBILE · RESEARCH</small><strong>エリン調査ノート</strong></span>';
 const nav=document.createElement('nav');nav.className='portal-nav';nav.setAttribute('aria-label','サイト内メニュー');
 for(const [url,label,key] of links){const a=document.createElement('a');a.href=url;a.textContent=label;if(key===current)a.setAttribute('aria-current','page');nav.appendChild(a)}
 inner.append(brand,nav);header.appendChild(inner);host.replaceWith(header);
})();
