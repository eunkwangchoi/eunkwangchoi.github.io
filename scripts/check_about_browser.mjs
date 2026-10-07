import fs from 'node:fs/promises';
import http from 'node:http';
import path from 'node:path';
import {chromium} from 'playwright';
const root=process.cwd();
const publicRoot=path.resolve(process.argv[2]||'public');
const server=http.createServer(async(req,res)=>{
 try{let file=path.resolve(publicRoot,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));if(!file.startsWith(publicRoot+path.sep))throw Error();if((await fs.stat(file)).isDirectory())file=path.join(file,'index.html');res.setHeader('Content-Type',file.endsWith('.html')?'text/html; charset=utf-8':file.endsWith('.svg')?'image/svg+xml':file.endsWith('.jpg')?'image/jpeg':'application/octet-stream');res.end(await fs.readFile(file));}catch{res.writeHead(404);res.end();}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const base='http://127.0.0.1:'+server.address().port;
const browser=await chromium.launch();const report=[];
try{
 await fs.mkdir('dist-local/qa',{recursive:true});
 for(const colorScheme of ['light','dark']){
  const context=await browser.newContext({viewport:{width:390,height:844},javaScriptEnabled:false,colorScheme});
  const page=await context.newPage();await page.goto(base+'/about/');
  const links=await page.locator('.about-featured>a').all();
  if(links.length!==1||await links[0].innerText().then(text=>!text.startsWith('CV')))throw Error('Hub must feature only CV');
  if(await page.locator('.about-social-badge').count()!==3)throw Error('Expected three SNS badges');
  for(const badge of await page.locator('.about-social-badge').all()){
   const box=await badge.boundingBox();if(box.width<44||box.height<44||!await badge.getAttribute('aria-label'))throw Error('Invalid SNS target');
  }
  if(await page.locator('.about-identity img').evaluate(el=>getComputedStyle(el).borderRadius)!=='50%')throw Error('Avatar must be circular');
  for(const [i,link] of links.entries()){const box=await link.boundingBox();if(box.height<44)throw Error('Touch target is smaller than 44px');if(i<2&&box.y+box.height>844)throw Error('Top two links fall below the first screen');}
  if(await page.locator('body').evaluate(el=>el.scrollWidth>390))throw Error('Horizontal overflow on mobile');
  await page.screenshot({path:'dist-local/qa/hub-'+colorScheme+'.png',fullPage:true});
  report.push({page:'hub',colorScheme,width:390,javaScript:false,touchTargets:true,firstScreen:true,overflow:false});
  await context.close();
 }
 const page=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:3});
 for(const route of ['/about/cv/','/about/cv/en/']){
  await page.goto(base+route);await page.screenshot({path:'dist-local/qa/cv-'+(route.includes('/en/')?'en':'ko')+'.png',fullPage:true});
  if(route.includes('/en/')){
   const untranslated=await page.locator('.about-cv header p,.about-cv section').evaluateAll(nodes=>nodes.map(node=>node.innerText).filter(text=>/[가-힣]/.test(text)));
   if(untranslated.length)throw Error('Untranslated Korean remains in English CV content');
  }
  if(await page.locator('body').evaluate(el=>el.scrollWidth>390))throw Error('Horizontal overflow on CV');
  const before=await page.locator('details').first().getAttribute('open');await page.locator('summary').first().click();
  if(!await page.locator('details').first().evaluate(el=>el.open))throw Error('Series disclosure did not open');
  report.push({page:route,seriesDisclosure:true,overflow:false});
 }
 // Shared OG bitmap is generated from the project's own monogram SVG.
 const svg=await fs.readFile('assets/about/og.svg','utf8');await page.setViewportSize({width:1200,height:630});
 await page.setContent('<style>body{margin:0}</style>'+svg);await page.screenshot({path:'assets/about/og.png'});
 // Signature PNGs use the local avatar before deployment; source HTML keeps its public URL.
 await page.route('https://eunkwangchoi.com/about/avatar/128.jpg',route=>route.fulfill({contentType:'image/jpeg',path:path.join(publicRoot,'about/avatar/128.jpg')}));
 for(const name of (await fs.readdir('dist-local/signature')).filter(x=>x.endsWith('.html')&&x!=='index.html')){
  await page.setContent(await fs.readFile(path.join('dist-local/signature',name),'utf8'));
  await page.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(img=>img.decode())));
  await page.locator('table').screenshot({path:path.join('dist-local/signature',name.replace('.html','.png')),omitBackground:false});
 }
 await fs.writeFile('dist-local/qa/report.json',JSON.stringify(report,null,2));
 console.log('Mobile hub/CV checks passed; light/dark, no-JavaScript and disclosure verified.');
}finally{await browser.close();server.close();}
