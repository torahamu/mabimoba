(() => {
  const items={
    'raid-armour':{name:'グラスギブネン防具選択箱',cost:70,currency:'遠征の証',income:10},
    'raid-emblem':{name:'グラスギブネンエンブレム箱',cost:50,currency:'遠征の証',income:10},
    'abyss-emblem':{name:'アビスエンブレム選択壺',cost:900,unlock:1200,currency:'赤い深淵の化石',income:240},
    'tab-armour':{name:'タバルタス防具選択箱',cost:120,currency:'タバルタス専用証',income:16},
    'tab-emblem':{name:'タバルタス未所持エンブレム箱',cost:120,currency:'タバルタス専用証',income:16},
    'tab-enchant':{name:'タバルタス武器エンチャント箱',cost:150,currency:'タバルタス専用証',income:16}
  };
  const $=id=>document.getElementById(id);
  const number=id=>Math.min(100000,Math.max(0,Number($(id).value)||0));
  function compute(){
    const item=items[$('planItem').value], count=Math.max(1,number('planCount'));
    const weekly=number('planWeekly'),owned=number('planOwned'),first=number('planFirst');
    const spent=Math.min(item.unlock||0,number('planSpent'));
    const unlockLeft=Math.max(0,(item.unlock||0)-spent);
    const required=unlockLeft+item.cost*count;
    const deficit=Math.max(0,required-owned-first);
    const weeks=deficit===0?0:(weekly>0?Math.ceil(deficit/weekly):null);
    const box=$('plannerResult');
    box.replaceChildren();
    const h=document.createElement('strong');h.textContent=weeks===null?'週収入が0のため到達不可':weeks===0?'現在の分で交換可能':`あと ${weeks} 週`;box.append(h);
    const p=document.createElement('p');p.textContent=`${item.name} ×${count}／必要総量 ${required.toLocaleString()} ${item.currency}（条件用残り ${unlockLeft.toLocaleString()} + 箱代 ${(item.cost*count).toLocaleString()}）／所持 ${owned} + 初回 ${first}／週 ${weekly}`;box.append(p);
    const n=document.createElement('p');n.textContent=item.unlock?'注意：1,200個は先に他の商品へ消費して解放し、その後に900個で購入。消費条件を箱代と二重カウントしていません。':'注意：商品はクラス帰属／ランダム／選択を確認してください。';box.append(n);
  }
  $('planItem').addEventListener('change',()=>{$('planWeekly').value=items[$('planItem').value].income;$('planOwned').value=0;$('planFirst').value=0;$('planSpent').value=0;$('spentHolder').hidden=!items[$('planItem').value].unlock;compute()});
  document.querySelectorAll('input').forEach(el=>el.addEventListener('input',compute));
  document.querySelectorAll('[data-preset]').forEach(b=>b.addEventListener('click',()=>{$('planWeekly').value=b.dataset.preset;compute()}));
  $('spentHolder').hidden=true;compute();
})();