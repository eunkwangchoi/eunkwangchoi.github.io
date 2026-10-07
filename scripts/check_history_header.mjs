// Compare History/CV chrome with the same-version original site build.
import fs from 'node:fs/promises';
import http from 'node:http';
import path from 'node:path';
import {chromium} from 'playwright';
const option=(name,fallback)=>process.argv.find(x=>x.startsWith(`--${name}=`))?.slice(name.length+3)||fallback;
const roots={baseline:path.resolve(option('baseline','.build/baseline-fair')),current:path.resolve(option('current','.build/review-site'))};
const server=http.createServer(async(req,res)=>{
 try{
  const url=new URL(req.url,'http://localhost');
  const [,,version,...parts]=url.pathname.split('/');
  // URLs are /site/<version>/<relative route>.
  const prefixed=url.pathname.startsWith('/site/');
  const root=prefixed?roots[version]:roots.current;if(!root)throw Error();
  let file=path.resolve(root,decodeURIComponent(prefixed?parts.join('/'):url.pathname.slice(1)));
  if(!file.startsWith(root+path.sep))throw Error();
  if((await fs.stat(file)).isDirectory())file=path.join(file,'index.html');
  res.setHeader('Content-Type',file.endsWith('.html')?'text/html; charset=utf-8':file.endsWith('.jpg')?'image/jpeg':file.endsWith('.png')?'image/png':file.endsWith('.svg')?'image/svg+xml':'application/octet-stream');
  res.end(await fs.readFile(file));
 }catch{res.writeHead(404);res.end();}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const base='http://127.0.0.1:'+server.address().port;
const browser=await chromium.launch();const results=[];
const metrics=page=>page.locator('body>nav').evaluate(nav=>{
 const rect=el=>{const r=el.getBoundingClientRect();return [r.x,r.y,r.width,r.height].map(v=>Math.round(v*10)/10)};
 return {nav:rect(nav),bodyColor:getComputedStyle(document.body).color,bodyBackground:getComputedStyle(document.body).backgroundColor,
  items:[...nav.querySelectorAll('a,button')].map(el=>({text:el.textContent.trim(),rect:rect(el),color:getComputedStyle(el).color,font:getComputedStyle(el).fontFamily,display:getComputedStyle(el).display}))};
});
try{
 for(const width of [390,1280])for(const colorScheme of ['light','dark']){
  const context=await browser.newContext({viewport:{width,height:900},colorScheme});
  await context.route('**/*',route=>new URL(route.request().url()).origin===base?route.continue():route.abort());
  const original=await context.newPage();await original.goto(base+'/site/baseline/about/');
  const expected=await metrics(original);
  for(const route of ['about/','about/cv/','about/cv/en/']){
   const page=await context.newPage();await page.goto(base+'/site/current/'+route);
   if(JSON.stringify(await metrics(page))!==JSON.stringify(expected))throw Error('Header mismatch: '+route+' '+width+' '+colorScheme+'\n'+JSON.stringify(await metrics(page))+'\n'+JSON.stringify(expected));
   if(width===390){
    await page.locator('body>nav .navbar-toggler').click();
    await page.locator('body>nav .navbar-collapse.show').waitFor();
    if(await page.locator('body>nav .navbar-nav').evaluate(el=>getComputedStyle(el).flexDirection)!=='column')throw Error('Mobile navigation must stack vertically');
   }
   await fs.mkdir('dist-local/qa',{recursive:true});
   if(route==='about/')await page.screenshot({path:`dist-local/qa/history-header-${width}-${colorScheme}.png`});
   results.push({route,width,colorScheme,headerMatchesOriginal:true,mobileToggle:width===390});
   await page.close();
  }
  await context.close();
 }
 await fs.writeFile('dist-local/qa/history-header.json',JSON.stringify(results,null,2));
 console.log('History/CV header positions, colors and mobile menu match the original site in all 12 cases.');
}finally{await browser.close();server.close();}
