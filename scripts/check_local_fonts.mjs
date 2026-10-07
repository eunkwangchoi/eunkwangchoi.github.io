// Check activated OS fonts through Chromium; never copy or extract font files.
import {chromium} from 'playwright';
import {spawnSync} from 'node:child_process';
import fs from 'node:fs/promises';
const result=spawnSync(process.env.CV_PYTHON||'python',['-c',"import json,yaml; print(json.dumps(yaml.safe_load(open('data/me/fonts.yaml',encoding='utf-8'))['roles']))"],{encoding:'utf8'});
if(result.status!==0)throw Error('Cannot read font configuration');
const roles=JSON.parse(result.stdout);
const browser=await chromium.launch();
try{
 const page=await browser.newPage();
 const report=await page.evaluate(async roles=>{
  const out=[];
  for(const [role,font]of Object.entries(roles)){
   let loaded=false;
   try{const face=new FontFace('Probe-'+role,`local(${JSON.stringify(font.local_name)})`);await face.load();loaded=face.status==='loaded';}catch{}
   out.push({role,local_name:font.local_name,loaded});
  }
  return out;
 },roles);
 await fs.mkdir('dist-local/qa',{recursive:true});
 await fs.writeFile('dist-local/qa/local-fonts.json',JSON.stringify(report,null,2));
 console.log(JSON.stringify(report,null,2));
 if(report.some(font=>!font.loaded))process.exitCode=1;
}finally{await browser.close();}
