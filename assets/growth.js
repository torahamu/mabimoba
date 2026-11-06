/* KR Season 0 class EXP data is embedded into growth/index.html at build-time. */
(() => {
  'use strict';
  const el = id => document.getElementById(id);
  const levels = JSON.parse(el('classExpDataset').textContent);
  const byLevel = new Map(levels.map(r => [r.level, r]));
  const fmt = n => n.toLocaleString('ja-JP');
  el('traceStart').value = '1';
  el('traceGoal').value = '65';
  function calculate() {
    const a = Number(el('traceStart').value), b = Number(el('traceGoal').value);
    const target = el('traceResult');
    if (a >= b) {
      target.innerHTML = '<div class="result-main"><b>目標Lvを現在より高くしてください</b></div>';
      return;
    }
    const start = byLevel.get(a), goal = byLevel.get(b);
    if (!start || !goal) return;
    const xp = goal.expCumulative - start.expCumulative;
    const traces = goal.tracesCumulative - start.tracesCumulative;
    const note = b === 65
      ? 'この痕跡数は韓国Season 0の一つの実測表に基づきます。別の報告ではLv1→65に約156,888個必要とされ、差があります。'
      : '韓国Season 0のLv別経験値表と痕跡消費表から計算。必要な痕跡は端数・現在のEXP残高によって変動します。';
    target.innerHTML = `<div class="result-main"><b>${fmt(xp)} EXP</b><small>Lv${a} → Lv${b} に必要なクラス経験値</small></div><div class="result-columns"><span>精霊の痕跡 <strong>${fmt(traces)} 個</strong></span><span>累積EXP ${fmt(start.expCumulative)} → ${fmt(goal.expCumulative)}</span></div><p class="muted-note">${note} 現在Lvで既に獲得した経験値は含みません。</p>`;
  }
  ['traceStart', 'traceGoal'].forEach(id => el(id).addEventListener('change', calculate));
  calculate();
})();
