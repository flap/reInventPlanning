const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  const socialDir = path.join(__dirname);
  const files = fs.readdirSync(socialDir).filter(f => f.endsWith('.html') && f.startsWith('card-'));
  
  for (const file of files) {
    const page = await browser.newPage();
    await page.setViewportSize({ width: 1080, height: 1080 });
    const filePath = path.join(socialDir, file);
    await page.goto(`file://${filePath}`);
    await page.waitForTimeout(500);
    const pngName = file.replace('.html', '.png');
    await page.screenshot({ path: path.join(socialDir, pngName), type: 'png' });
    await page.close();
    console.log(`✅ ${pngName}`);
  }
  
  await browser.close();
  console.log(`\n🎉 Done! ${files.length} cards generated.`);
})();
