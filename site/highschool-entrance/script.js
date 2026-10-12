const routeData = {
  foundation: {
    number: 'ROUTE 01', caption: 'START WITH THE BASICS', title: '教科書の基本を、<br>自力で解ける力にする。',
    description: '苦手な教科は、入試向けの難問に進む前に、単元の説明と基本問題を結び直します。解説を読んだあと、答えを見ずに解き直せるかを目安にしましょう。',
    steps: [['苦手単元を一つ選ぶ', '学校のワークやテストで、間違いが続く単元を確認'], ['説明と例題のセットで学ぶ', '解説を閉じて、解き方を自分で再現できるか確認'], ['同じ本の問題を解き直す', '正答できた単元から、入試形式の問題へ進む']],
    ladder: ['基礎の理解', '基本問題', '入試形式の演習']
  },
  public: {
    number: 'ROUTE 02', caption: 'CHECK YOUR PREFECTURE', title: '地域の選抜方法に合わせて、<br>五教科を組み立てる。',
    description: '公立高校を目指す場合も、教科数・配点・調査書や面接の扱いは都道府県や年度で異なります。自治体の最新要項を確認してから、五教科の基礎と地域の過去問を組み合わせましょう。',
    steps: [['教育委員会の要項を確認', '検査教科・配点・調査書・面接等を照合'], ['五教科の基礎を整理', '解説と基本問題で、苦手な単元から埋める'], ['地域の過去問で形式を確認', '問題の傾向や時間配分を練習に反映']],
    ladder: ['募集要項', '五教科の基礎', '地域の過去問']
  },
  selective: {
    number: 'ROUTE 03', caption: 'STEP UP AFTER STANDARD', title: '標準問題を固めてから、<br>発展問題へ進む。',
    description: '上位校や独自問題校を志望する場合も、まず標準問題を自力で解き切れるか確認。学校や自治体が公開する過去問と照らし、必要な教科・単元だけ発展演習を追加します。',
    steps: [['志望校の過去問を確認', '独自問題の有無、教科、出題形式を確認'], ['標準問題の失点を減らす', '基礎教材を解き直し、解法を説明できるか確認'], ['必要な分野に絞って発展演習', '過去問で出題を確かめてから追加教材を選ぶ']],
    ladder: ['出題形式を確認', '標準の完成', '必要な発展演習']
  },
  private: {
    number: 'ROUTE 04', caption: 'FOCUS ON EACH SCHOOL', title: '学校ごとの入試形式から、<br>使う教科を決める。',
    description: '私立・国立高校は学校ごとに募集要項や問題形式が異なります。受験日程、必要教科、面接・作文の有無を確認し、共通の基礎と学校別の対策を分けて計画します。',
    steps: [['学校の募集要項を読む', '受験科目・出願条件・検査内容を確認'], ['共通する教科の基礎を固める', '複数校で必要な科目を先に準備'], ['学校別の過去問で調整', '問題形式と時間配分を確認し、弱点を補う']],
    ladder: ['募集要項', '共通科目の基礎', '学校別の過去問']
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
    const subjects = (card.dataset.subject || '').split(/\s+/);
    card.hidden = filter !== 'all' && !subjects.includes(filter);
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
