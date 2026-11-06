/* v7: local, deterministic research calculations. All % models are nonofficial. */
(() => {
  const $ = (id) => document.getElementById(id);
  const format = (n, d=1) => Number(n).toLocaleString('ja-JP',{maximumFractionDigits:d,minimumFractionDigits:d});
  const raw = (id, fallback=0) => { const x=Number($(id)?.value); return Number.isFinite(x)? Math.max(0,x):fallback; };
  const data = {
    critical:1057,extra:369,skill:887,strong:764,rapid:531,area:591,combo:501,break:664,ultimate:862
  };
  const single = (v, den) => 1 + v / den;
  const metrics = {
    skill:{label:'スキル威力部分',calc:v=>single(v,8500),suffix:'倍',formula:'1 + スキル威力 / 8500'},
    strong:{label:'強打時の能力値部分',calc:v=>single(v,8500),suffix:'倍',formula:'1 + 強打強化 / 8500'},
    rapid:{label:'連打時の能力値部分',calc:v=>single(v,8500),suffix:'倍',formula:'1 + 連打強化 / 8500'},
    area:{label:'マルチヒット時の能力値部分',calc:v=>single(v,8500),suffix:'倍',formula:'1 + 広域強化 / 8500'},
    combo:{label:'コンボ最大段階の能力値部分',calc:v=>single(v,17500),suffix:'倍',formula:'1 + コンボ強化 / 17500（最大段階）'},
    break:{label:'無防備時の能力値部分',calc:v=>single(v,5250),suffix:'倍',formula:'1 + ブレイク / 5250'},
    extra:{label:'追加攻撃の期待倍率',calc:v=>single(v,13000),suffix:'倍',formula:'1 + 追加攻撃 / 13000'},
  };
  function renderStat(){
    const kind=$('statCalcType').value;
    let x=raw('statCalcCurrent'),y=x+raw('statCalcPlus');
    const output=$('statCalcResult');
    if(kind === 'critical'){
      const p=v=>0.5*v/(v+2000), m=v=>1.4+v/5000, e=v=>1+p(v)*(m(v)-1);
      output.innerHTML=`<div class="result-main"><b>${format(p(x)*100,2)}% → ${format(p(y)*100,2)}%</b><small>能力値だけから求めた基礎クリ率（バフ・戦闘力差なし）</small></div><div class="result-columns"><span>発動時倍率 ${format(m(x),3)} → ${format(m(y),3)}倍</span><span>期待倍率 ${format(e(x),3)} → ${format(e(y),3)}倍</span><span>期待ダメージ差 +${format((e(y)/e(x)-1)*100,2)}%</span></div><p class="muted-note">近似式：基礎率=0.5×C/(C+2000)、倍率=1.4+C/5000。期待倍率は他条件を固定した数学モデルです。</p>`;
      return;
    }
    if(kind==='ultimate'){
      const gd=v=>single(v,7250),dd=v=>single(v,8750);
      output.innerHTML=`<div class="result-main"><b>${format(dd(x),3)} → ${format(dd(y),3)}倍</b><small>究極技ダメージの能力値部分</small></div><div class="result-columns"><span>ゲージ獲得倍率 ${format(gd(x),3)} → ${format(gd(y),3)}倍</span><span>ダメージ側差 +${format((dd(y)/dd(x)-1)*100,2)}%</span></div><p class="muted-note">韓国非公式：究極技/8750（ダメージ）と究極技/7250（ゲージ）。</p>`;
      return;
    }
    const m=metrics[kind],a=m.calc(x),b=m.calc(y);
    output.innerHTML=`<div class="result-main"><b>${format(a,3)} → ${format(b,3)}${m.suffix}</b><small>${m.label}</small></div><div class="result-columns"><span>相対的な増加 ${format((b/a-1)*100,2)}%</span><span>能力値 +${format(y-x,0)}</span></div><p class="muted-note">非公式式：${m.formula}。判定が成立した時の部分倍率であり、戦闘全体のDPSではありません。</p>`;
  }
  $('statCalcType')?.addEventListener('change', () => { $('statCalcCurrent').value=data[$('statCalcType').value]; renderStat(); });
  ['statCalcCurrent','statCalcPlus'].forEach(x=>$(x)?.addEventListener('input',renderStat));
  function renderDefense(){
    const incoming=raw('defIncoming',10000), def=raw('defValue',5752), down=raw('defDownValue',791);
    const a=incoming/(1+(def/6500)*(1+down/6500));
    const b=Math.max(0,incoming/(1+def/10000)-down);
    $('defResult').innerHTML=`<div><b>推定式A（6500モデル）</b><div><strong>${format(a,0)}</strong></div><p>約${format(100*(1-a/incoming),1)}%軽減。防御とダウンを乗算的に処理</p></div><div><b>推定式B（固定減算説）</b><div><strong>${format(b,0)}</strong></div><p>約${format(100*(1-b/incoming),1)}%軽減。防御で割った後にダウンを減算</p></div>`;
  }
  ['defIncoming','defValue','defDownValue'].forEach(x=>$(x)?.addEventListener('input',renderDefense));
  const titleBoxes=Array.from(document.querySelectorAll('input[data-title]'));
  const KEYS=['STR','DEX','INT','WILL','LUCK'];
  const colors={STR:'str',DEX:'dex',INT:'int',WILL:'will',LUCK:'luck'};
  function renderTitles(){
    const bonus=Object.fromEntries(KEYS.map(x=>[x,0]));let count=0;
    const chosen=[];
    for(const input of titleBoxes){if(!input.checked)continue;count++;chosen.push(input.dataset.title);for(const key of input.dataset.attrs.split(','))bonus[key]+=25;}
    $('titleDone').innerHTML=`${count} <small>/ 18職</small>`;
    $('titleTotal').innerHTML=`+${count*50} <small>能力値ポイント</small>`;
    $('titleBonus').innerHTML=KEYS.map(x=>`<div class="stat-tone-${colors[x]}"><span>${x}</span><strong>+${bonus[x]}</strong></div>`).join('');
    try{localStorage.setItem('mabimoba-v7-class65',JSON.stringify(chosen));}catch(_){/* private browsing etc */}
  }
  try{
    const saved=JSON.parse(localStorage.getItem('mabimoba-v7-class65')||'[]');
    if(Array.isArray(saved)) for(const b of titleBoxes)b.checked=saved.includes(b.dataset.title);
  }catch(_){/* ignore invalid storage */}
  for(const input of titleBoxes)input.addEventListener('change',renderTitles);
  $('titlesAll')?.addEventListener('click',()=>{titleBoxes.forEach(x=>x.checked=true);renderTitles();});
  $('titlesClear')?.addEventListener('click',()=>{titleBoxes.forEach(x=>x.checked=false);renderTitles();});
  renderStat();renderDefense();renderTitles();
})();
