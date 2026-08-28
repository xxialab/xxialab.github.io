(() => {
  const menu = document.querySelector(".site-menu");
  if (!menu) return;

  const mobile = window.matchMedia("(max-width: 760px)");
  const syncMenu = () => {
    menu.open = !mobile.matches;
  };

  syncMenu();
  mobile.addEventListener?.("change", syncMenu);

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && mobile.matches && menu.open) {
      menu.open = false;
      menu.querySelector("summary")?.focus();
    }
  });

  document.addEventListener("click", (event) => {
    if (mobile.matches && menu.open && !menu.contains(event.target)) {
      menu.open = false;
    }
  });
})();
