(() => {
  const tabs = [...document.querySelectorAll("[data-ebook-tab]")];
  const panels = [...document.querySelectorAll("[data-ebook-panel]")];
  if (!tabs.length || !panels.length) return;

  const activate = (name, moveFocus = false) => {
    tabs.forEach(tab => {
      const selected = tab.dataset.ebookTab === name;
      tab.setAttribute("aria-selected", String(selected));
      tab.tabIndex = selected ? 0 : -1;
      if (selected && moveFocus) tab.focus();
    });
    panels.forEach(panel => {
      panel.hidden = panel.dataset.ebookPanel !== name;
    });
  };

  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => {
      const name = tab.dataset.ebookTab;
      activate(name);
      history.replaceState(null, "", `#${name}`);
    });
    tab.addEventListener("keydown", event => {
      if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
      event.preventDefault();
      let next = index;
      if (event.key === "ArrowLeft") next = (index - 1 + tabs.length) % tabs.length;
      if (event.key === "ArrowRight") next = (index + 1) % tabs.length;
      if (event.key === "Home") next = 0;
      if (event.key === "End") next = tabs.length - 1;
      activate(tabs[next].dataset.ebookTab, true);
      history.replaceState(null, "", `#${tabs[next].dataset.ebookTab}`);
    });
  });

  const requested = location.hash.slice(1);
  activate(tabs.some(tab => tab.dataset.ebookTab === requested) ? requested : "darmowe");
})();
