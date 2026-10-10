import { chromium } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';

const browser=await chromium.launch({headless:true});
const context=await browser.newContext();
const page=await context.newPage();
await fs.mkdir('artifacts',{recursive:true});
await page.emulateMedia({reducedMotion:'reduce'});
// Visual checks use prepared responses, preserving the application's live AI default.
await page.route(/\/api\/matches\/[^/]+\/catch-up/,route=>{
 const url=new URL(route.request().url());url.searchParams.set('ai','false');
 return route.continue({url:url.toString()});
});
try {
 await page.goto('http://127.0.0.1:5180/?match=ind-aus');
 await page.locator('.player-card').first().waitFor();
 for(const language of ['en','hi']) {
  await page.getByRole('button',{name:language==='hi'?'हिंदी':'EN',exact:true}).click();
  await page.locator('.player-card').first().waitFor();
  for(const width of [320,375,600,768,900,1024,1440]) {
   await page.setViewportSize({width,height:900});
   const bounds=await page.locator('.hero-visual').evaluate(el=>{
    const parent=el.getBoundingClientRect();
    return [...el.querySelectorAll('.pitch-orbit,.pitch-surface,.floating-story,.visual-coordinate')].map(child=>{
     const b=child.getBoundingClientRect();return {name:child.className,left:b.left-parent.left,top:b.top-parent.top,right:parent.right-b.right,bottom:parent.bottom-b.bottom};
    });
   });
   for(const b of bounds) assert.ok(Math.min(b.left,b.top,b.right,b.bottom)>=-1,`${language} ${width}px: clipped ${JSON.stringify(b)}`);
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${language} ${width}px page overflow`);
   await page.locator('.player-grid').scrollIntoViewIfNeeded();
   await page.waitForFunction(()=>[...document.querySelectorAll('.player-portrait')].every(img=>img.complete&&img.naturalWidth>0));
   assert.equal(await page.locator('.player-portrait').count(),3);
   if([375,1440].includes(width)) {
    await page.locator('.player-grid').screenshot({path:`artifacts/portraits-${language}-${width}.png`});
    await page.evaluate(()=>scrollTo(0,0));
    await page.locator('.story-hero').screenshot({path:`artifacts/hero-${language}-${width}.png`});
    const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
    assert.deepEqual(result.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)})),[]);
   }
  }
 }
 console.log('PASS: 3 portraits load; complete hero artwork fits at 7 widths in English and Hindi; no overflow; 4 accessibility scans.');
} finally {await browser.close();}
