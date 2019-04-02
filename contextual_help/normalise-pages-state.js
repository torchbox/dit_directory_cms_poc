const fs = require("fs");
const path = require("path");
const state = require("./staging-redux-state.json");

/**
 * Input: Wagtail explorer menu’s Redux state, with all pages fetched.
 * Output: Normalised page state, with irrelevant metadata removed.
 * How to run: `node normalise-pages-state.js`
 */

const rawPages = Object.values(JSON.parse(state.preloadedState).nodes);

// Add more metadata to the root page.
Object.assign(rawPages[0], {
  id: 1,
  title: "Root",
  type: "Root",
  admin_display_title: "Root",
});

const pages = rawPages.map((page) => {
  delete page.isFetching;
  delete page.isError;
  delete page.meta.status;
  delete page.meta.children;
  if (page.children.items) {
    page.children = page.children.items;
  } else {
    page.children = [];
  }
  Object.assign(page, page.meta);
  delete page.meta;

  return page;
});

fs.writeFileSync("./cms-pages.json", JSON.stringify(pages, null, 2), "utf8");
