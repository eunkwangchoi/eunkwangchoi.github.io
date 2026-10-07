import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {chromium} from 'playwright';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const preview=process.argv.includes('--preview');
const publicArg=process.argv.find(x=>x.startsWith('--public='));
const selectionArg=process.argv.find(x=>x.startsWith('--selection='));
const publicRoot=path.resolve(root,publicArg?publicArg.slice(9):(selectionArg?'dist-local/private-pdf-site':'public'));
if(!publicRoot.startsWith(root+path.sep))throw new Error('Output directory must be inside the workspace');
if(selectionArg&&!publicRoot.startsWith(path.join(root,'dist-local')+path.sep))throw new Error('Selected private PDFs must stay inside ignored dist-local');
const python=process.env.CV_PYTHON||'python';
function run(command,args){const result=spawnSync(command,args,{cwd:root,stdio:'inherit',env:{...process.env,HUGO_CACHEDIR:path.join(root,'.build/hugo-cache')}});if(result.status!==0)throw new Error(command+' failed');}
run(python,['scripts/validate_about.py']);
const printRoot=path.join(publicRoot,'about/cv/_print');
try{
 run(python,['scripts/prepare_pdf.py',...(selectionArg?['--selection',selectionArg.slice(12)]:[])]);
 run(python,['scripts/run_hugo.py','--config','hugo.toml,.build/pdf.toml','--destination',publicRoot,'--environment','production']);
}catch(error){
 if(selectionArg)await fs.rm(path.join(root,'.build/private-print-data'),{recursive:true,force:true});
 await fs.rm(printRoot,{recursive:true,force:true});
 throw error;
}
await fs.mkdir(printRoot,{recursive:true});
await fs.copyFile(path.join(root,'node_modules/pagedjs/dist/paged.polyfill.js'),path.join(printRoot,'paged.polyfill.js'));
await fs.copyFile(path.join(root,'assets/about/paginate.js'),path.join(printRoot,'paginate.js'));
const cv=JSON.parse(await fs.readFile(path.join(publicRoot,'about/cv.json'),'utf8'));
const report=[];
const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css','.jpg':'image/jpeg','.png':'image/png','.svg':'image/svg+xml','.woff2':'font/woff2','.json':'application/json'};
const server=http.createServer(async(req,res)=>{
 try{const url=new URL(req.url,'http://localhost');const name=decodeURIComponent(url.pathname);let file=path.resolve(publicRoot,'.'+name);if(!file.startsWith(publicRoot+path.sep))throw new Error('Invalid path');if((await fs.stat(file)).isDirectory())file=path.join(file,'index.html');res.setHeader('Content-Type',mime[path.extname(file)]||'application/octet-stream');res.end(await fs.readFile(file));}catch{res.writeHead(404);res.end('Not found');}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const base='http://127.0.0.1:'+server.address().port;
let browser;
try{
 browser=await chromium.launch({headless:true,...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH?{executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH}:{})});
 for(const variant of cv.profile.pdf.variants){for(const lang of ['ko','en']){
  const page=await browser.newPage();const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`${base}/about/cv/_print/${variant}-${lang}/`,{waitUntil:'networkidle'});
  await page.waitForFunction(()=>window.CV_READY===true,null,{timeout:60000});
  const result=await page.evaluate(async()=>{
   const config=window.CVPrint;const failures=[];
   if(config.fonts.mode==='web'&&!config.fonts.web_pdf_permitted)failures.push('Web-kit PDF licensing has not been confirmed; use local fonts or confirm the configuration.');
   for(const [role,font] of Object.entries(config.fonts.roles)){
    if(!font.langs.includes(config.lang))continue;
    if(!font.family){failures.push('Unconfigured font role: '+role);continue;}
    try{const loaded=await document.fonts.load(`${font.style} ${font.weight} 16px "${font.family}"`,config.lang==='ko'?'최은광 About me':'Eunkwang Choi');if(!loaded.length||!loaded.every(f=>f.status==='loaded')||!document.fonts.check(`${font.style} ${font.weight} 16px "${font.family}"`))failures.push('Font did not load: '+role);}catch{failures.push('Font did not load: '+role);}
   }
   return {...window.CV_RESULT,font_failures:failures};
  });
  result.errors.push(...errors);
  report.push({variant,lang,...result});
  if(preview){
   const dir=path.join(root,'dist-local/pdf-preview');await fs.mkdir(dir,{recursive:true});
   await page.locator('.pagedjs_page').first().screenshot({path:path.join(dir,`${variant}-${lang}-page-1.png`)});
  }else{
   if(result.errors.length||result.font_failures.length)throw new Error(`${variant}-${lang}: ${[...result.errors,...result.font_failures].join('; ')}`);
   const target=path.join(publicRoot,`about/cv-${variant}-${lang}.pdf`);
   const stage=path.join(root,'.build',`cv-${variant}-${lang}.pdf`);
   await page.pdf({path:stage,preferCSSPageSize:true,printBackground:true,tagged:true});
   run(python,['scripts/check_cv_pdf.py',stage,'--lang',lang,'--variant',variant,'--expected-pages',String(result.pages),'--final',target]);
  }
  await page.close();
 }}
}finally{
 if(browser)await browser.close();server.close();
 await fs.mkdir(path.join(root,'dist-local/pdf-preview'),{recursive:true});
 await fs.writeFile(path.join(root,'dist-local/pdf-preview',preview?'report.json':'validation.json'),JSON.stringify(report,null,2));
 // Print pages are intermediate artifacts, never part of the deployment.
 await fs.rm(printRoot,{recursive:true,force:true});
 if(selectionArg)await fs.rm(path.join(root,'.build/private-print-data'),{recursive:true,force:true});
}
console.log(preview?'Draft layout previews generated; see font/overflow failures in report.json.':'All CV PDFs passed validation.');
