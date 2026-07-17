const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const SIZES = [
  { name: 'instagram', width: 1080, height: 1080 },
  { name: 'linkedin', width: 1200, height: 627 },
  { name: 'reels', width: 1080, height: 1920 },
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

      // For non-square formats, create a modified temp file
      const filePath = path.join(socialDir, file);
      
      if (size.name === 'instagram') {
        // Use the file directly via goto (photos resolve relative to HTML)
        await page.goto(`file://${filePath}`);
      } else {
        // Modify dimensions for other formats
        let html = fs.readFileSync(filePath, 'utf-8');
        html = html.replace(/width:\s*1080px/g, `width: ${size.width}px`);
        html = html.replace(/height:\s*1080px/g, `height: ${size.height}px`);
        
        if (size.name === 'linkedin') {
          html = html.replace(/padding:\s*56px/g, 'padding: 32px 44px');
          html = html.replace(/font-size:\s*28px/g, 'font-size: 20px');
          html = html.replace(/font-size:\s*26px/g, 'font-size: 19px');
          html = html.replace(/font-size:\s*64px/g, 'font-size: 40px');
          html = html.replace(/margin-bottom:\s*20px/g, 'margin-bottom: 10px');
          html = html.replace(/margin-bottom:\s*28px/g, 'margin-bottom: 12px');
          html = html.replace(/margin-bottom:\s*18px/g, 'margin-bottom: 8px');
          html = html.replace(/padding:\s*20px 24px/g, 'padding: 10px 16px');
          html = html.replace(/font-size:\s*17px/g, 'font-size: 14px');
          html = html.replace(/font-size:\s*16px/g, 'font-size: 13px');
        }

        if (size.name === 'reels') {
          html = html.replace(/padding:\s*56px/g, 'padding: 72px 56px');
          html = html.replace(/font-size:\s*28px/g, 'font-size: 34px');
          html = html.replace(/font-size:\s*26px/g, 'font-size: 32px');
          html = html.replace(/font-size:\s*64px/g, 'font-size: 90px');
          html = html.replace(/margin-bottom:\s*20px/g, 'margin-bottom: 32px');
          html = html.replace(/margin-bottom:\s*28px/g, 'margin-bottom: 40px');
          html = html.replace(/margin-bottom:\s*18px/g, 'margin-bottom: 28px');
          html = html.replace(/padding:\s*20px 24px/g, 'padding: 28px 30px');
          html = html.replace(/font-size:\s*17px/g, 'font-size: 21px');
          html = html.replace(/font-size:\s*16px/g, 'font-size: 20px');
        }

        // Write temp file so relative paths work
        const tmpFile = path.join(socialDir, `_tmp_${size.name}_${file}`);
        fs.writeFileSync(tmpFile, html);
        await page.goto(`file://${tmpFile}`);
        // Cleanup after screenshot
        await page.waitForTimeout(500);
        const pngName = file.replace('.html', '.png');
        await page.screenshot({ path: path.join(outDir, pngName), type: 'png' });
        await page.close();
        fs.unlinkSync(tmpFile);
        console.log(`  ✅ ${size.name}/${pngName}`);
        continue;
      }

      await page.waitForTimeout(500);
      const pngName = file.replace('.html', '.png');
      await page.screenshot({ path: path.join(outDir, pngName), type: 'png' });
      await page.close();
      console.log(`  ✅ ${size.name}/${pngName}`);
    }
    console.log(`📁 ${size.name}/ — ${files.length} cards (${size.width}×${size.height})\n`);
  }
  
  await browser.close();
  console.log(`🎉 Done! ${files.length * SIZES.length} images generated.`);
})();
