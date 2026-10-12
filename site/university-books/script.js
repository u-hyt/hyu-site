const routeData = {
  foundation: {
    number: 'ROUTE 01', caption: 'START WITH THE BASICS', title: 'わからない単元を、<br>一つずつ解けるに変える。',
    description: 'まず教科書レベルの理解を整え、例題を自力で解き直せる状態へ。難しい問題集を何冊も進めるより、基礎の穴を見つけて埋めることから始めます。',
    steps: [['数学の考え方を確認', '講義型の解説で、公式の意味と基本例題をつかむ'], ['教科書例題を自力で再現', '解説を閉じて、解法の手順を説明できるか確認'], ['学校・志望校の範囲を照合', '未習範囲や不要科目を先に確認して計画に反映']],
    ladder: ['基礎の理解', '典型問題', '志望校の過去問']
  },
  national: {
    number: 'ROUTE 02', caption: 'BUILD A BALANCED PLAN', title: '共通テストと個別試験、<br>必要な力を分けて考える。',
    description: '国公立を考えるなら、共通テストと個別試験で使う科目・配点を早めに並べて確認。広い範囲を学びつつ、二次試験で使う科目は記述問題にも進みます。',
    steps: [['受験科目・配点を一覧に', '大学入試センターと志望大学の最新要項を照合'], ['共通の基礎を一冊で固める', '数学は基礎〜標準の例題を解き直せる状態へ'], ['個別試験の形式を追加', '記述・論述など、志望学部の過去問で不足を確認']],
    ladder: ['科目と配点', '基礎〜標準', '二次・個別対策']
  },
  selective: {
    number: 'ROUTE 03', caption: 'GO DEEPER, STEP BY STEP', title: '標準問題を固めてから、<br>難問に挑戦する。',
    description: '難関大志望でも、最初から最難度の教材に進む必要はありません。基礎例題の解法を自力で再現し、標準問題の失点を減らしてから大学別演習へ。',
    steps: [['標準問題の完成度を確認', '例題の方針を説明し、解答を白紙から再現'], ['必要科目を重点強化', '学部の出題範囲・形式に合わせて演習を選択'], ['大学別の過去問で調整', '出題傾向と時間配分を公式の過去問で確認']],
    ladder: ['標準問題の定着', '重点科目の演習', '大学別の過去問']
  },
  private: {
    number: 'ROUTE 04', caption: 'FOCUS ON YOUR EXAM FORMAT', title: '受験方式に合わせて、<br>使う科目を絞り込む。',
    description: '私立大は大学・学部・方式によって受験科目や配点が異なります。候補校の要項を並べ、共通して使う科目と個別に必要な科目を分けて教材を選びます。',
    steps: [['志望方式ごとの科目を確認', '一般選抜・共通テスト利用などを区別'], ['共通科目の教材を優先', '複数校で使う科目から基礎と標準を固める'], ['学部の出題形式を仕上げる', '記述・選択・時間制限を過去問で確認']],
    ladder: ['方式・科目を確認', '共通科目を固める', '学部別の過去問']
  }
};

const tabs = [...document.querySelectorAll('.route-tab')];
const stepsList = document.querySelector('#route-steps');
function setRoute(key) {
  const data = routeData[key];
  if (!data) return;
  tabs.forEach(tab => {
    const active = tab.dataset.route === key;
    tab.classList.toggle('is-active', active);
    tab.setAttribute('aria-selected', String(active));
  });
  document.querySelector('#route-number').textContent = data.number;
  document.querySelector('#route-caption').textContent = data.caption;
  document.querySelector('#route-title').innerHTML = data.title;
  document.querySelector('#route-description').textContent = data.description;
  stepsList.innerHTML = data.steps.map((step, index) => `<li><span>${index + 1}</span><div><b>${step[0]}</b><small>${step[1]}</small></div></li>`).join('');
  ['#ladder-one', '#ladder-two', '#ladder-three'].forEach((selector, index) => {
    document.querySelector(selector).textContent = data.ladder[index];
  });
}
tabs.forEach(tab => tab.addEventListener('click', () => setRoute(tab.dataset.route)));

document.querySelectorAll('.filter-pill').forEach(button => button.addEventListener('click', () => {
  const filter = button.dataset.filter;
  document.querySelectorAll('.filter-pill').forEach(item => {
    const active = item === button;
    item.classList.toggle('is-active', active);
    item.setAttribute('aria-pressed', String(active));
  });
  document.querySelectorAll('.book-card').forEach(card => {
    card.hidden = filter !== 'all' && card.dataset.subject !== filter;
  });
}));

const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('.main-nav');
menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'メニューを閉じる' : 'メニューを開く');
  nav.classList.toggle('is-open', open);
});
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  nav.classList.remove('is-open');
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', 'メニューを開く');
}));
