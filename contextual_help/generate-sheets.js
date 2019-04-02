const fs = require("fs");
const path = require("path");
const { convertArrayToCSV } = require("convert-array-to-csv");

const pages = require("./cms-pages.json");
const fields = require("./data/cms-fields.json");

const CMS_INSTANCE_URL = process.env.CMS_INSTANCE_URL;

/**
 * Generates spreadsheets with fields used in the CMS, as well as screenshot scenarios.
 * Input: cms-pages.json, cms.fields.json
 * Output: CSV sheets for each sub-section of the site, as well as screenshots scenarios.
 */

const rootPage = pages[0];
const sections = rootPage.children.map((id) => pages.find((p) => p.id === id));

const fieldHeaders = ["", "Name", "Help text"];

const header = [
  "",
  "Page type",
  "Example",
  "",
  "Fields",
  // There are many more fields than those headers suggest.
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
  ...fieldHeaders.slice(),
];

const exportedPageTypes = [];

const screenshotScenarios = [];

const findAndList = (rows, id) => {
  const page = pages.find((p) => p.id === id);

  if (!!page.type && !exportedPageTypes.includes(page.type)) {
    const editURL = `${CMS_INSTANCE_URL}/admin/pages/${id}/edit/`;
    const typePath = page.type.split(".");
    const humanPageType = typePath[typePath.length - 1];

    const pageTypeColumns = [
      "Current",
      humanPageType,
      page.admin_display_title,
      editURL,
      "",
      "",
    ];

    const pageFields = fields[page.type];

    if (pageFields) {
      const fieldColumns = pageFields
        .map((pageType) => [pageType.verbose_name, pageType.help_text, ""])
        .reduce((allColumns, cols) => allColumns.concat(cols), []);

      const row = [...pageTypeColumns, ...fieldColumns];

      rows.push(row);
      rows.push(["Suggested"]);
      rows.push(["Screenshots"]);

      screenshotScenarios.push({
        name: humanPageType,
        url: editURL,
      });
    }

    exportedPageTypes.push(page.type);
  }

  page.children.forEach(findAndList.bind(null, rows));
};

sections.forEach((page) => {
  let rows = [];
  findAndList(rows, page.id);

  const typePath = page.type.split(".");
  const humanPageType = typePath[typePath.length - 1];

  screenshotScenarios.push({
    label: humanPageType,
    url: `${CMS_INSTANCE_URL}/admin/pages/${page.id}/edit/`,
  });

  const csv = convertArrayToCSV(rows, {
    header,
  });

  fs.writeFileSync(`./data/${page.admin_display_title}.csv`, csv, "utf8");
});

fs.writeFileSync(
  "./screenshots.json",
  JSON.stringify(screenshotScenarios, null, 2),
  "utf8",
);
