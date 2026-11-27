"use strict";

const imageDialog = document.querySelector("#image-dialog");
const fullImage = document.querySelector("#full-image");
const imageTitle = document.querySelector("#image-title");
const imageOriginal = document.querySelector("#image-original");
const closeImage = document.querySelector("#close-image");
let imageTrigger;

if (typeof imageDialog.showModal === "function") {
  document.querySelectorAll("a[data-caption]").forEach(link => {
    link.addEventListener("click", event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;

      event.preventDefault();
      imageTrigger = link;
      fullImage.src = link.href;
      imageOriginal.href = link.href;
      fullImage.alt = link.querySelector("img").alt;
      imageTitle.textContent = link.dataset.caption;
      imageDialog.showModal();
      closeImage.focus();
    });
  });

  closeImage.addEventListener("click", () => imageDialog.close());
  imageDialog.addEventListener("click", event => {
    const bounds = imageDialog.getBoundingClientRect();
    const outside = event.clientX < bounds.left || event.clientX > bounds.right ||
      event.clientY < bounds.top || event.clientY > bounds.bottom;
    if (event.target === imageDialog && outside) imageDialog.close();
  });
  imageDialog.addEventListener("close", () => {
    if (imageDialog.open) return;
    fullImage.removeAttribute("src");
    imageOriginal.removeAttribute("href");
    imageTrigger.focus({ preventScroll: true });
  });
}

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

function setLibraryFilter(value) {
  activeFilter = value;
  filterButtons.forEach(button => {
    button.setAttribute("aria-pressed", String(button.dataset.filter === value));
  });
  filterLibrary();
}

filterButtons.forEach(button => {
  button.addEventListener("click", () => setLibraryFilter(button.dataset.filter));
});
search.addEventListener("input", filterLibrary);
document.querySelector("#clear-search").addEventListener("click", () => {
  search.value = "";
  setLibraryFilter("Все");
  search.focus({ preventScroll: true });
});
document.querySelector(".library-controls").hidden = false;

function openLinkedDetails() {
  const target = document.getElementById(location.hash.slice(1));
  if (!target) return;

  const outer = target.closest(".more-cases");
  const details = target.matches(".case > details, .approach") ? target : null;
  const openOuter = outer && !outer.open;
  const openDetails = details && !details.open;
  if (openOuter) outer.open = true;
  if (openDetails) details.open = true;
  if (openOuter || openDetails) requestAnimationFrame(() => target.scrollIntoView());
}

openLinkedDetails();
window.addEventListener("hashchange", openLinkedDetails);
