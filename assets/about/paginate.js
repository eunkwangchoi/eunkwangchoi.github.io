/* Fixed elements use sheet coordinates, independent of the flowing page margins. */
(async()=>{
 const config=window.CVPrint;
 const errors=[];
 const warnings=[];
 class CVPages extends Paged.Handler {
  afterPageLayout(pageElement,page){
   const number=page.position+1;
   const sheet=pageElement.querySelector('.pagedjs_sheet')||pageElement;
   const fixed=document.createElement('div');fixed.className='pdf-fixed';
   fixed.innerHTML='<div class="pdf-panel"></div>';
   const clone=id=>document.getElementById(id).content.cloneNode(true);
   fixed.append(clone(number===1?'pdf-cover':'pdf-ghost'));
   const slots=config.sidebar[String(number)]||[];
   if(slots.length){const sidebar=document.createElement('aside');sidebar.className='pdf-sidebar';for(const name of slots){const template=document.getElementById('sidebar-'+name);if(template)sidebar.append(template.content.cloneNode(true));}fixed.append(sidebar);}
   const folio=document.createElement('span');folio.className='pdf-page-number';folio.textContent=String(number);fixed.append(folio);sheet.append(fixed);
  }
 }
 Paged.registerHandlers(CVPages);
 try{
  await document.fonts.ready;
  const source=document.getElementById('pdf-flow');
  // Give Paged.js detached content so only its generated sheets can print.
  const content=document.createDocumentFragment();content.append(source.cloneNode(true));
  source.remove();
  const flow=await new Paged.Previewer().preview(content,undefined,document.body);
  const pages=document.querySelectorAll('.pagedjs_page');
  for(const [i,page] of Array.from(pages).entries()){
   const sheet=page.querySelector('.pagedjs_sheet').getBoundingClientRect();
   // Font line boxes overlap at the reference's tight 30pt leading. Check the
   // visible glyph outlines instead of treating blank ascent/descent as ink.
   const ink=[];
   const canvas=document.createElement('canvas').getContext('2d');
   for(const name of page.querySelectorAll('.pdf-ghost span')){
    const style=getComputedStyle(name),box=name.getBoundingClientRect();
    canvas.font=`${style.fontStyle} ${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
    const m=canvas.measureText(name.textContent);
    const baseline=box.left+(parseFloat(style.lineHeight)-m.fontBoundingBoxAscent-m.fontBoundingBoxDescent)/2+m.fontBoundingBoxAscent;
    const rect={left:baseline-m.actualBoundingBoxAscent,right:baseline+m.actualBoundingBoxDescent,top:box.bottom-m.actualBoundingBoxRight,bottom:box.bottom+m.actualBoundingBoxLeft};
    ink.push(rect);
    if(rect.left<sheet.left-1||rect.top<sheet.top-1||rect.right>sheet.right+1||rect.bottom>sheet.bottom+1)errors.push('Vertical name ink clipped on page '+(i+1)+': '+JSON.stringify({left:rect.left-sheet.left,top:rect.top-sheet.top,right:rect.right-sheet.left,bottom:rect.bottom-sheet.top}));
   }
   if(ink.length===2){
    const [a,b]=ink;
    if(Math.min(a.right,b.right)>Math.max(a.left,b.left)+1&&Math.min(a.bottom,b.bottom)>Math.max(a.top,b.top)+1)errors.push('Vertical name ink overlaps on page '+(i+1));
    if(Math.abs(a.left-sheet.left)>4)errors.push('Vertical name is not flush with the left edge on page '+(i+1));
   }
   const sidebar=page.querySelector('.pdf-sidebar');
   if(sidebar){
    const interests=sidebar.querySelector('.pdf-interests');
    const languages=sidebar.querySelector('.pdf-languages');
    if(interests&&languages&&interests.getBoundingClientRect().bottom>languages.getBoundingClientRect().top-4)errors.push('Sidebar sections overlap on page '+(i+1));
   }
   if(sidebar){for(const node of sidebar.querySelectorAll('p,.pdf-language,.pdf-badge-grid')){if(node.getBoundingClientRect().bottom>sheet.top+(274/297)*sheet.height+1)errors.push('Sidebar overflow on page '+(i+1));}}
   const content=page.querySelector('.pagedjs_page_content');
   if(content){
    const bounds=content.getBoundingClientRect();
    const walker=document.createTreeWalker(content,NodeFilter.SHOW_TEXT);
    let text;
    while((text=walker.nextNode())){
     if(!text.textContent.trim())continue;
     const range=document.createRange();range.selectNodeContents(text);
     for(const rect of range.getClientRects()){
      // Font ascent can extend beyond its line box; use layout boxes for the top edge.
      const box=text.parentElement.getBoundingClientRect();
      if(rect.left<bounds.left-2||rect.right>bounds.right+2||rect.bottom>bounds.bottom+2||box.top<bounds.top-2){
       errors.push('Text overflow on page '+(i+1)+': '+text.textContent.trim().slice(0,60));break;
      }
     }
    }
   }
  }
  for(const key of Object.keys(config.sidebar)){if(Number(key)>pages.length)warnings.push('Sidebar slot '+key+' has no page');}
  if(config.variant==='summary'&&pages.length>2)errors.push('Summary exceeds two pages');
  for(const page of pages){const folio=page.querySelector('.pdf-page-number');folio.textContent+=' / '+pages.length;}
  window.CV_RESULT={pages:pages.length,errors,warnings};window.CV_READY=true;
 }catch(error){window.CV_RESULT={pages:0,errors:[String(error)],warnings};window.CV_READY=true;}
})();
