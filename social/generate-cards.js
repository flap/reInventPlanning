const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const SIZES = [
  { name: 'instagram', width: 1080, height: 1080 },
  { name: 'linkedin', width: 1200, height: 627 },
];

(async () => {
  const browser = await chromium.launch();
  const socialDir = path.join(__dirname);
  const files = fs.readdirSync(socialDir).filter(f => f.endsWith('.html') && f.startsWith('card-'));
  
  for (const size of SIZES) {
    const outDir = path.join(socialDir, size.name);
    if (!fs.existsSync(outDir)) fs.mkdirSync(outDir);

    for (const file of files) {
      const page = await browser.newPage();
      await page.setViewportSize({ width: size.width, height: size.height });

      // Read HTML content and adjust body dimensions for this size
      let html = fs.readFileSync(path.join(socialDir, file), 'utf-8');
      html = html.replace(/width:\s*1080px/g, `width: ${size.width}px`);
      html = html.replace(/height:\s*1080px/g, `height: ${size.height}px`);
      
      // For LinkedIn (shorter), reduce padding and font sizes
      if (size.name === 'linkedin') {
        html = html.replace(/padding:\s*56px/g, 'padding: 36px 48px');
        html = html.replace(/font-size:\s*28px/g, 'font-size: 22px');
        html = html.replace(/font-size:\s*64px/g, 'font-size: 48px');
        html = html.replace(/margin-bottom:\s*20px/g, 'margin-bottom: 12px');
        html = html.replace(/margin-bottom:\s*28px/g, 'margin-bottom: 16px');
        html = html.replace(/padding:\s*20px 24px/g, 'padding: 12px 18px');
        html = html.replace(/margin-bottom:\s*20px;/g, 'margin-bottom: 10px;');
      }

      await page.setContent(html, { waitUntil: 'load' });
      await page.waitForTimeout(300);
      
      const pngName = file.replace('.html', '.png');
      await page.screenshot({ path: path.join(outDir, pngName), type: 'png' });
      await page.close();
      console.log(`  ✅ ${size.name}/${pngName}`);
    }
    console.log(`📁 ${size.name}/ — ${files.length} cards (${size.width}×${size.height})`);
  }
  
  await browser.close();
  console.log(`\n🎉 Done! ${files.length * SIZES.length} images generated.`);
})();
