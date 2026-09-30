(() => {
  const input = document.querySelector('#term-search');
  if (!input) return;
  const cards = [...document.querySelectorAll('.term-card')];
  const counter = document.querySelector('#term-count');
  const zh = document.documentElement.lang.startsWith('zh');
  const update = () => {
    const query = input.value.trim().toLocaleLowerCase();
    let count = 0;
    cards.forEach(card => {
      const match = card.textContent.toLocaleLowerCase().includes(query);
      card.hidden = !match;
      if (match) count += 1;
    });
    counter.textContent = zh ? `显示 ${count} / ${cards.length} 个术语` : `${count} / ${cards.length} terms shown`;
  };
  input.addEventListener('input', update);
  update();
})();
