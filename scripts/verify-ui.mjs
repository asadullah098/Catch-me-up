import { chromium } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const browser=await chromium.launch({headless:true});
await fs.mkdir('artifacts',{recursive:true});
const context=await browser.newContext({viewport:{width:1440,height:1050}});
const page=await context.newPage();page.setDefaultTimeout(15000);
const errors=[];page.on('pageerror',e=>errors.push(e.message));
const requestedAI=[];
// Verify the UI requests AI while using deterministic responses for repeatable tests.
await page.route(/\/api\/matches\/[^/]+\/catch-up/,route=>{
 const url=new URL(route.request().url());
 requestedAI.push(url.searchParams.get('ai'));
 url.searchParams.set('ai','false');
 return route.continue({url:url.toString()});
});
const ready=async()=>{await page.getByRole('heading',{name:'A rookie changed the chase.'}).waitFor();await page.waitForFunction(()=>[...document.querySelectorAll('.player-card')].every(el=>Number(getComputedStyle(el).opacity)===1));};
const scan=async(name)=>{const results=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();await fs.writeFile(`artifacts/accessibility-${name}.json`,JSON.stringify(results.violations,null,2));assert.deepEqual(results.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)})),[]);};
try{
 await page.goto('http://127.0.0.1:5180');await ready();
 assert.equal(await page.locator('.player-card').count(),3);assert.equal(await page.locator('.story-bullets>li').count(),3);
 await page.screenshot({path:'artifacts/desktop.png',fullPage:true,animations:'disabled'});await scan('desktop-en');console.log('English desktop passed.');
 await page.getByRole('button',{name:'The spin squeeze',exact:false}).click();
 await page.getByRole('heading',{name:'Same score. A very different story.'}).waitFor();
 await page.getByText('+32',{exact:true}).waitFor();assert.ok(await page.locator('.score').first().innerText().then(t=>t.includes('132/3')));
 await page.getByRole('button',{name:'The comeback',exact:false}).click();await ready();await page.getByText('+49',{exact:true}).waitFor();
 await page.getByLabel('Match ID',{exact:true}).fill('unknown');await page.getByRole('button',{name:'Load match',exact:true}).click();
 await page.getByRole('alert').waitFor();await page.getByRole('button',{name:'Retry snapshot'}).click();await ready();
 await page.getByRole('button',{name:'3 overs',exact:true}).click();await page.getByText('+38',{exact:true}).waitFor();assert.equal(await page.locator('.over-tile').count(),3);
 await page.getByRole('button',{name:'5 overs',exact:true}).click();await ready();
 await page.getByRole('button',{name:'See the deliveries',exact:true}).first().click();assert.equal(await page.locator('#commentary-feed li').count(),2);await page.getByRole('button',{name:'Close',exact:true}).click();
 await page.getByRole('button',{name:'Explore ball-by-ball'}).click();assert.equal(await page.locator('#commentary-feed li').count(),31);await page.getByRole('button',{name:'Close',exact:true}).click();
 const card=page.locator('.player-card').first();await card.getByRole('button',{name:'Meet the player'}).click();await card.getByText('Recent form, explained',{exact:true}).waitFor();
 await card.getByRole('button',{name:/^Save .* to shortlist$/}).click();await page.getByRole('button',{name:/^Shortlist/}).click();assert.equal(await page.locator('.player-card').count(),1);
 await page.reload();await ready();assert.equal(await page.getByRole('button',{name:/^Remove .* from shortlist$/}).count(),1);
 await page.getByRole('combobox',{name:'Filter players by role'}).selectOption('Bowler');assert.equal(await page.locator('.player-card').count(),1);await page.getByRole('combobox',{name:'Filter players by role'}).selectOption('All players');
 await page.getByRole('button',{name:'Catch me up',exact:true}).click();await ready();
 await page.locator('.demo-tools summary').click();await page.getByLabel('Feed scenario').selectOption('empty');await page.getByRole('heading',{name:'The story hasn’t started yet.'}).waitFor();await page.getByRole('button',{name:'Return to snapshot'}).click();await ready();
 await page.getByLabel('Feed scenario').selectOption('error');await page.getByRole('heading',{name:'We lost the feed for a moment.'}).waitFor();await page.getByRole('button',{name:'Retry snapshot'}).click();await ready();
 await page.route('**/api/matches/**/catch-up*',async route=>{await new Promise(r=>setTimeout(r,600));await route.fallback();});await page.getByRole('button',{name:'Refresh snapshot'}).click();await page.getByText('Reading the match story…').waitFor();await ready();await page.unroute('**/api/matches/**/catch-up*');
 await page.route('**/api/matches/**/catch-up*',route=>route.abort());await page.getByRole('button',{name:'Refresh snapshot'}).click();await page.getByRole('alert').waitFor();await page.unroute('**/api/matches/**/catch-up*');await page.getByRole('button',{name:'Retry snapshot'}).click();await ready();await page.locator('.demo-tools summary').click();
 console.log('Story, evidence, profiles, and recovery passed.');
 for(const [name,width,height]of [['mobile',375,812],['tablet',768,1024],['landscape',812,375]]){await page.setViewportSize({width,height});await page.screenshot({path:`artifacts/${name}.png`,fullPage:true});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${name} overflow`);}
 await page.setViewportSize({width:1440,height:1050});await page.getByRole('button',{name:'हिंदी',exact:true}).click();await page.getByRole('heading',{name:'नए खिलाड़ी ने बदली मैच की कहानी।'}).waitFor();await page.waitForFunction(()=>[...document.querySelectorAll('.player-card')].every(el=>Number(getComputedStyle(el).opacity)===1));
 assert.equal(await page.locator('html').getAttribute('lang'),'hi');assert.equal(await page.locator('.story-bullets>li').count(),3);
 await page.screenshot({path:'artifacts/desktop-hi.png',fullPage:true});await scan('desktop-hi');
 await page.getByRole('button',{name:'गेंदों की कमेंट्री देखें'}).first().click();assert.ok(await page.locator('#commentary-feed').innerText().then(t=>t.includes('विकेट')));await page.getByRole('button',{name:'बंद करें',exact:true}).click();
 await page.reload();await page.getByRole('heading',{name:'नए खिलाड़ी ने बदली मैच की कहानी।'}).waitFor();assert.equal(await page.locator('html').getAttribute('lang'),'hi');
 await page.setViewportSize({width:375,height:812});await page.emulateMedia({reducedMotion:'reduce'});await page.reload();await page.getByRole('heading',{name:'नए खिलाड़ी ने बदली मैच की कहानी।'}).waitFor();
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Hindi mobile overflow');assert.equal(await page.locator('.player-card').first().evaluate(el=>getComputedStyle(el).opacity),'1');await scan('mobile-hi');await page.screenshot({path:'artifacts/mobile-hi.png',fullPage:true});
 await page.keyboard.press('Tab');assert.equal(await page.evaluate(()=>document.activeElement?.textContent),'मैच की जानकारी पर जाएँ');
 await page.getByRole('button',{name:'EN',exact:true}).click();await ready();await scan('mobile-en');await page.evaluate(()=>window.scrollTo(0,0));await page.screenshot({path:'artifacts/mobile-top.png'});
 await page.setViewportSize({width:1440,height:1050});await page.screenshot({path:'artifacts/desktop-top.png'});
 assert.ok(requestedAI.length>0&&requestedAI.every(v=>v==='true'),'UI must request AI by default on every context change');
 assert.deepEqual(errors,[]);console.log('PASS: default AI requests (provider-isolated), two same-score stories, match ID, exact active players, three evidence-linked bullets, shortlist, form, filters, states, English/Hindi, language persistence, keyboard, reduced motion, responsive layout, four accessibility scans, and console.');
}finally{await browser.close();}
