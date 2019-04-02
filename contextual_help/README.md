# CMS contextual help review

A series of scripts to automatically export the fields used in CMS pages, for future review.

## Requirements

- [Node](https://nodejs.org)
- `npm install`
- Working install of [directory-cms](https://github.com/uktrade/directory-cms)

## Usage

Here is the workflow:

### Extract data from the CMS

1. Discover all of the pages / page types used on the site, by navigating the page structure using Wagtail’s explorer menu (manual). More ideal but not attempted: by querying the admin API
2. With the [Redux DevTools](https://github.com/zalmoxisus/redux-devtools-extension) Chrome extension, export the Redux state with all of the site’s pages visited. Save as `staging-redux-state.json` here.
3. Use `node normalise-pages-state.js` to convert the Redux state into a format that’s easier to read.
4. (From the resulting `cms-pages.json`, manually (regex-fu) extract a list of all of the page types used on the site.)
5. This is then hard-coded into `help_review.py`
6. Place `help_review.py` within `core` folder of the CMS repo.
7. From the CMS repo, `make debug_manage cmd=shell` to start a Django-aware Python shell.
8. `from core.help_review import save_all_fields_json; save_all_fields_json()`
9. [`cms-fields.json`](data/cms-fields.json) now has a list of all of the fields.

### Export spreadsheets

1. Use `node generate-sheets.js` to generate spreadsheets (CSV) for each sub-section of the CMS
2. Upload those spreadsheets to Google Sheets.
3. Use the "Transpose" feature to convert them from rows to columns, to simplify the review (horizontal scrolling is hard)
4. Manually re-order fields that are out of place as needed.

### Export screenshots

Screenshots are taken with [BackstopJS](https://github.com/garris/BackstopJS), a tool initially meant for visual regression tests, that can easily take batch screenshots of parts of pages.

1. `npm install -g backstopjs`
2. `backstop init`
3. Populate the Backstop scenarios with the result of `node generate-sheets.js`
4. Add manually-generated scenarios from `data/pagetype-panels.md`
5. `backstop test`
6. Manually insert the screenshots in the spreadsheets
