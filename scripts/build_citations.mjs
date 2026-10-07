import fs from 'node:fs/promises';
import path from 'node:path';
import CSL from 'citeproc';
const input=process.argv[2]||'public/about/cv.json';
const cv=JSON.parse(await fs.readFile(input,'utf8'));
const style=await fs.readFile('assets/about/cv.csl','utf8');
const kinds={article:'article-journal',thesis:'thesis',book:'book',talk:'speech'};
const records=[];
for(const work of cv.works){
 if(!kinds[work.type])continue;
 const localized={};
 for(const lang of ['ko','en']){
  const org=id=>cv.orgs[id]?.name?.[lang]||cv.orgs[id]?.name?.ko||'';
  const record={id:work.id,type:kinds[work.type],title:work.title[lang]||work.title.ko||work.title.en,author:[{family:'Choi',given:'Eunkwang Ryan'}],issued:{'date-parts':[String(work.date).split('-').map(Number)]},publisher:(work.publisher||[]).map(org).join('; '),'container-title':work.venue?org(work.venue):'',volume:work.volume,issue:work.issue,page:work.pages,DOI:work.ids?.doi,ISBN:work.ids?.isbn,URL:work.archive_url||work.links?.[0]?.url};
  localized[lang]=Object.fromEntries(Object.entries(record).filter(([,value])=>value!==undefined&&value!==null&&value!==''));
 }
 records.push(localized);
}
const output={};
for(const lang of ['ko','en']){
 const bibliography=Object.fromEntries(records.map(r=>[r[lang].id,r[lang]]));
 const locale=await fs.readFile('node_modules/citeproc/locales/locales-'+(lang==='ko'?'ko-KR':'en-US')+'.xml','utf8').catch(()=>null);
 // The package contains the processor only; minimal locale data is stored locally.
 const localized=locale||await fs.readFile('assets/about/locale-'+lang+'.xml','utf8');
 const engine=new CSL.Engine({retrieveLocale:()=>localized,retrieveItem:id=>bibliography[id]},style,lang==='ko'?'ko-KR':'en-US');
 engine.setOutputFormat('html');
 for(const record of Object.values(bibliography)){
  engine.updateItems([record.id]);
  const [,entries]=engine.makeBibliography();
  output[record.id]??={};output[record.id][lang]=entries[0].trim();
 }
}
await fs.mkdir('data/generated',{recursive:true});
await fs.writeFile('data/generated/citations.json',JSON.stringify(output,null,2));
await fs.mkdir('dist-local/citations',{recursive:true});
await fs.writeFile('dist-local/citations/csl.json',JSON.stringify(records.map(r=>r.ko),null,2));
for(const lang of ['ko','en'])await fs.writeFile(`dist-local/citations/csl-${lang}.json`,JSON.stringify(records.map(r=>r[lang]),null,2));
console.log('Generated shared CSL references for '+records.length+' works.');
