// Compare visible geometry/styles across the compiler migration; block remote assets.
import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import http from 'node:http';
import path from 'node:path';
const roots={before:path.resolve('.build/modernization/baseline'),after:path.resolve('.build/modernization/final')};
const server=http.createServer(async(req,res)=>{try{
 const [,,version,...parts]=new URL(req.url,'http://localhost').pathname.split('/');
 const root=roots[version];if(!root)throw Error();let file=path.resolve(root,decodeURIComponent(parts.join('/')));
 if(!file.startsWith(root+path.sep))throw Error();if((await fs.stat(file)).isDirectory())file=path.join(file,'index.html');
 res.setHeader('Content-Type',file.endsWith('.html')?'text/html; charset=utf-8':file.endsWith('.jpg')?'image/jpeg':file.endsWith('.png')?'image/png':'application/octet-stream');res.end(await fs.readFile(file));
}catch{res.writeHead(404);res.end();}});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const base='http://127.0.0.1:'+server.address().port;
const browser=await chromium.launch();const report=[];
const inspect=page=>page.evaluate(()=>{
 const selectors=['body','body>nav','main','h1','h2','p','a','img','table','pre','code'];
 return selectors.flatMap(selector=>[...document.querySelectorAll(selector)].slice(0,6).map((el,index)=>{
  const rect=el.getBoundingClientRect(),s=getComputedStyle(el);
  return {selector,index,text:el.textContent.trim().slice(0,100),rect:[rect.x,rect.y,rect.width,rect.height],
   styles:[s.color,s.backgroundColor,s.fontFamily,s.fontSize,s.lineHeight,s.display,s.padding,s.margin]};
 }));
});
try{
 for(const width of [390,1280])for(const route of ['', 'books/','posts/','repos/','arts/','refs/','ko/','ja/','about/','about/cv/','about/cv/en/']){
  const context=await browser.newContext({viewport:{width,height:900}});
  await context.route('**/*',r=>new URL(r.request().url()).origin===base?r.continue():r.abort());
  const before=await context.newPage(),after=await context.newPage();
  await before.goto(`${base}/site/before/${route}`);await after.goto(`${base}/site/after/${route}`);
  const a=await inspect(before),b=await inspect(after);if(a.length!==b.length)throw Error('Element count changed '+route);
  for(let i=0;i<a.length;i++){
   if(a[i].text!==b[i].text||JSON.stringify(a[i].styles)!==JSON.stringify(b[i].styles)||a[i].rect.some((n,j)=>Math.abs(n-b[i].rect[j])>.5))throw Error('Visible regression '+route+' '+width+' '+JSON.stringify({before:a[i],after:b[i]}));
  }
  report.push({route:'/'+route,width,elements:a.length,matched:true});await context.close();
 }
 await fs.mkdir('dist-local/qa',{recursive:true});await fs.writeFile('dist-local/qa/hugo-migration.json',JSON.stringify(report,null,2));
 console.log('Visible geometry, colors, typography and text match in '+report.length+' route/viewport cases.');
}finally{await browser.close();server.close();}
