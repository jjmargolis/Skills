// node render.cjs diagram.bpmn  ->  diagram.svg + diagram.png
// Needs bpmn-js installed in the working directory, and Playwright with Chromium.
const { chromium } = require('playwright');
const fs = require('fs');
const src = process.argv[2], out = src.replace(/\.bpmn$/, '');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 2 });
  await page.setContent('<div id="c" style="width:2000px;height:1500px"></div>');
  await page.addScriptTag({ path: require.resolve('bpmn-js/dist/bpmn-viewer.production.min.js', { paths: [process.cwd(), __dirname] }) });
  const { svg, warnings } = await page.evaluate(async xml => {
    const viewer = new BpmnJS({ container: '#c' });
    const { warnings } = await viewer.importXML(xml);
    return { svg: (await viewer.saveSVG()).svg, warnings: warnings.map(w => w.message) };
  }, fs.readFileSync(src, 'utf8'));
  if (warnings.length) { console.error(warnings.join('\n')); process.exitCode = 1; }
  fs.writeFileSync(out + '.svg', svg);
  await page.setContent(`<body style="margin:16px;background:#fff">${svg}</body>`);
  await (await page.$('svg')).screenshot({ path: out + '.png' });
  await browser.close();
})();
