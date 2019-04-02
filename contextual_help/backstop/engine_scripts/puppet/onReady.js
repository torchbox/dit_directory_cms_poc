const styles = `
header,
footer,
.tab-nav,
#nav-toggle {
    display: none;
}`;

module.exports = async (page, scenario, vp) => {
  console.log("SCENARIO > " + scenario.label);

  // add more ready handlers here...
  await page.addStyleTag({
    content: styles,
  });
};
