(() => {
  const filters = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('.projects-card')];
  const empty = document.querySelector('.projects-empty');
  if (!filters.length || !cards.length) return;
  filters.forEach((button) => button.addEventListener('click', () => {
    const kind = button.dataset.filter;
    let shown = 0;
    filters.forEach((item) => item.classList.toggle('is-active', item === button));
    cards.forEach((card) => {
      const visible = kind === 'all' || card.dataset.kind === kind;
      card.hidden = !visible;
      if (visible) shown += 1;
    });
    if (empty) empty.hidden = shown !== 0;
  }));
})();
