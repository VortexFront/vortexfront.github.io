"use strict";

const imageDialog = document.querySelector("#image-dialog");
const fullImage = document.querySelector("#full-image");
const imageTitle = document.querySelector("#image-title");
const closeImage = document.querySelector("#close-image");
let imageTrigger;

function showImage(path, button) {
  if (!imageDialog || !fullImage) return;
  imageTrigger = button;
  fullImage.src = path;
  fullImage.alt = button.dataset.caption || "Снимок локального приложения на синтетических данных";
  imageTitle.textContent = button.dataset.caption || "Снимок локального приложения";
  imageDialog.showModal();
  closeImage.focus();
}

document.querySelectorAll("[data-gallery]").forEach(button => {
  button.addEventListener("click", () => showImage(button.querySelector("img").getAttribute("src"), button));
});
document.querySelectorAll("[data-image]").forEach(button => {
  button.addEventListener("click", () => showImage(button.dataset.image, button));
});
closeImage?.addEventListener("click", () => imageDialog.close());
imageDialog?.addEventListener("keydown", event => {
  if (event.key === "Tab") {
    event.preventDefault();
    closeImage.focus();
  }
});
imageDialog?.addEventListener("click", event => {
  const bounds = imageDialog.getBoundingClientRect();
  if (event.target === imageDialog && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) imageDialog.close();
});
imageDialog?.addEventListener("close", () => {
  fullImage.removeAttribute("src");
  imageTrigger?.focus({ preventScroll: true });
});

document.querySelectorAll(".case-link").forEach(link => {
  link.addEventListener("click", () => {
    const detail = document.querySelector(link.getAttribute("href"));
    if (detail) detail.open = true;
  });
});

const filterButtons = [...document.querySelectorAll("[data-filter]")];
const rows = [...document.querySelectorAll(".library-row")];
const search = document.querySelector("#project-search");
const status = document.querySelector(".filter-status[role='status']");
const emptyState = document.querySelector(".empty-state");
const normalize = value => value.trim().toLocaleLowerCase("ru").replaceAll("ё", "е");
const searchable = new Map(rows.map(row => [row, normalize(row.textContent)]));
let activeFilter = "Все";

function filterLibrary() {
  const query = normalize(search.value);
  let count = 0;
  rows.forEach(row => {
    const categoryMatches = activeFilter === "Все" || row.dataset.category === activeFilter;
    row.hidden = !(categoryMatches && searchable.get(row).includes(query));
    if (!row.hidden) count++;
  });
  status.textContent = `${count} из ${rows.length} проектов · ${activeFilter === "Все" ? "все направления" : activeFilter}${query ? " · по вашему запросу" : ""}`;
  emptyState.hidden = count !== 0;
}

filterButtons.forEach(button => {
  button.addEventListener("click", () => {
    activeFilter = button.dataset.filter;
    filterButtons.forEach(item => item.setAttribute("aria-pressed", String(item === button)));
    filterLibrary();
  });
});
search?.addEventListener("input", filterLibrary);
document.querySelector("#clear-search")?.addEventListener("click", () => {
  search.value = "";
  activeFilter = "Все";
  filterButtons.forEach(item => item.setAttribute("aria-pressed", String(item.dataset.filter === "Все")));
  filterLibrary();
  search.focus({ preventScroll: true });
});
const controls = document.querySelector(".library-controls");
if (controls) controls.hidden = false;
