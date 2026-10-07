import {chromium} from 'playwright';
import fs from 'node:fs/promises';
const browser=await chromium.launch();
try{
 const page=await browser.newPage({viewport:{width:390,height:844}});
 await page.goto('http://127.0.0.1:13132/');
 await page.locator('article').first().waitFor();
 const result=await page.evaluate(async()=>{
  const csrf=await fetch('/api/save',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});
  return {records:document.querySelectorAll('article').length,checks:document.querySelectorAll('article input[type=checkbox]').length,overflow:document.documentElement.scrollWidth>innerWidth,unauthorized:csrf.status};
 });
 if(result.records<170||result.checks!==result.records*2||result.overflow||result.unauthorized!==403)throw Error(JSON.stringify(result));
 await page.locator('#search').fill('대구외국어');
 if(await page.locator('article').count()!==1)throw Error('Search failed');
 await page.locator('#search').fill('');
 await page.locator('article button').first().click();
 await page.locator('#editor[open]').waitFor();
 if(!await page.locator('#korean').inputValue())throw Error('Korean editor not loaded');
 if(await page.locator('#translations textarea').count()<1)throw Error('English editor not loaded');
 if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Editor overflows mobile');
 await page.locator('#close').click();
 await fs.mkdir('dist-local/qa',{recursive:true});
 await page.screenshot({path:'dist-local/qa/cv-manager-mobile.png'});
 await fs.writeFile('dist-local/qa/cv-manager.json',JSON.stringify(result,null,2));
 console.log(JSON.stringify(result));
}finally{await browser.close();}
