// CRUD verification against a disposable private fixture, never the owner's CV.
import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {spawn} from 'node:child_process';
const dir=await fs.mkdtemp(path.join(os.tmpdir(),'cv-language-'));
const master=path.join(dir,'master.json');
await fs.writeFile(master,JSON.stringify({schema_version:1,profile_security:{phone:'SECRET-SENTINEL'},records:[{
 definition:'entry',source:'data/cv/entries/history.yaml',web:true,pdf:true,security:{phone:'SECRET-SENTINEL'},
 data:{id:'test-item',kind:'activity',domain:'art',weight:1,status:'active',visibility:'public',period:{start:'2026',precision:'year'},title:{ko:'시험 이력',en:'Test history'}}
}]}));
const server=spawn('python',['scripts/manage_cv.py','--file',master,'--port','0'],{stdio:['ignore','pipe','pipe']});
let browser;
try{
 const url=await new Promise((resolve,reject)=>{let output='';const timer=setTimeout(()=>reject(Error('Server timeout')),15000);server.stdout.on('data',b=>{output+=b.toString();const m=output.match(/http:\/\/127\.0\.0\.1:\d+\//);if(m){clearTimeout(timer);resolve(m[0]);}});server.on('exit',()=>{clearTimeout(timer);reject(Error('Server exited'));});});
 browser=await chromium.launch();const page=await browser.newPage({viewport:{width:390,height:844}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(url);await page.locator('article button').click();
 await page.locator('#editor[open]').waitFor();
 const data=JSON.parse(await page.locator('#korean').inputValue());
 data.title.ko='수정된 한글';data.period.start='2027';
 await page.locator('#korean').fill(JSON.stringify(data));await page.locator('#save-korean').click();
 await page.getByText('title · 한글 변경 후 검토 필요',{exact:true}).waitFor();
 if(await page.locator('#translations textarea').inputValue()!=='Test history')throw Error('Override lost');
 await page.locator('#translations textarea').fill('Reviewed English');
 await page.getByRole('button',{name:'영문 수정·검토 완료 저장'}).click();
 await page.locator('#editor-status').filter({hasText:'영문을 저장했습니다. 한글 원본은 변경되지 않았습니다.'}).waitFor();
 let saved=JSON.parse(await fs.readFile(master,'utf8'));
 if(saved.records[0].data.title.ko!=='수정된 한글'||saved.records[0].data.title.en!=='Reviewed English'||saved.records[0].data.period.start!=='2027')throw Error('One-way edit failed');
 if(saved.records[0].security.phone!=='SECRET-SENTINEL')throw Error('Private store changed');
 if((await page.content()).includes('SECRET-SENTINEL'))throw Error('Private field exposed');
 await page.locator('#close').click();await page.locator('#add').click();
 await page.locator('#editor[open]').waitFor();
 const created=JSON.parse(await page.locator('#korean').inputValue());
 if(created.id==='test-item')throw Error('New item not opened');
 page.once('dialog',dialog=>dialog.accept());await page.locator('#delete').click();
 await page.locator('#status').filter({hasText:'모든 언어에서 이력을 삭제했습니다. 공개본에는 내보내기 후 반영됩니다.'}).waitFor();
 saved=JSON.parse(await fs.readFile(master,'utf8'));
 if(!saved.records.find(r=>r.data.id===created.id)?.deleted)throw Error('Deletion failed');
 if(await page.locator('article').count()!==1||errors.length)throw Error('UI lifecycle failed '+errors.join(';'));
 console.log(JSON.stringify({korean_edit:true,english_one_way:true,manual_override_preserved:true,create_delete:true,security_not_exposed:true}));
}finally{
 if(browser)await browser.close();
 if(server.exitCode===null){const done=new Promise(resolve=>server.once('exit',resolve));server.kill();await done;}
 // mkdtemp is constrained to the OS temporary directory, with a task prefix.
 const resolved=path.resolve(dir);if(!resolved.startsWith(path.resolve(os.tmpdir())+path.sep)||!path.basename(resolved).startsWith('cv-language-'))throw Error('Invalid fixture cleanup path');
 await fs.rm(resolved,{recursive:true,force:true});
}
