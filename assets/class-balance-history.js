(function () {
  'use strict';
  const $ = id => document.getElementById(id);
  const cls = $('balanceClass'), phase = $('balancePhase'), typ = $('balanceType'), q = $('balanceSearch'), count = $('balanceCount');
  if (!cls || !phase || !typ || !q) return;
  const panels = [...document.querySelectorAll('.balance-class')];
  function update() {
    let jobs = 0, rows = 0;
    const keyword = q.value.trim().toLocaleLowerCase();
    for (const panel of panels) {
      let matched = 0;
      for (const event of panel.querySelectorAll('.balance-event')) {
        const pass = (phase.value === 'all' || event.dataset.phase === phase.value) &&
          (typ.value === 'all' || event.dataset.type === typ.value) &&
          (!keyword || (panel.querySelector('h2').textContent + ' ' + event.textContent).toLocaleLowerCase().includes(keyword));
        event.hidden = !pass;
        if (pass) matched++;
      }
      panel.hidden = matched === 0 || (cls.value !== 'all' && panel.dataset.class !== cls.value);
      if (!panel.hidden) { jobs++; rows += matched; }
    }
    count.textContent = `表示：${jobs}職 / ${rows}件の変更`; 
    document.querySelectorAll('[data-jump]').forEach(a => {a.setAttribute('aria-current', a.dataset.jump === cls.value ? 'true' : 'false');});
  }
  [cls, phase, typ].forEach(x => x.addEventListener('change', update));
  q.addEventListener('input', update);
  $('balanceReset').addEventListener('click', () => { cls.value = phase.value = typ.value = 'all'; q.value = ''; history.replaceState(null, '', location.pathname); update(); });
  document.querySelectorAll('[data-jump]').forEach(a => a.addEventListener('click', () => {
    cls.value = a.dataset.jump; update();
  }));
  function selectFromHash() {
    if (!location.hash.startsWith('#class-')) return;
    const slug = decodeURIComponent(location.hash.slice(7));
    if (panels.some(p => p.dataset.class === slug)) { cls.value = slug; update(); }
  }
  window.addEventListener('hashchange', selectFromHash);
  selectFromHash(); update();
})();
