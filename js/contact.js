// Builds the email link (address assembled here to deter scrapers).
{
const m=['info','abeng.co'].join('@');
const TAG='[AbengCo enquiry]';
const mb=document.getElementById('mailbtn');
const topic=(mb&&mb.dataset.topic)||'Intro call';
const body='Hi Tania,\n\nName:\nCompany and website:\nInterested in (product audit / AI and automation sprint / fractional product lead / launch and growth):\nBudget range:\nIdeal start date:\nA few lines about your product and goal:\n\n';
const href='mailto:'+m+'?subject='+encodeURIComponent(TAG+' '+topic)+'&body='+encodeURIComponent(body);
if(mb)mb.href=href;
const mt=document.getElementById('mailtext');if(mt){mt.textContent=m;mt.href=href;}
const yr=document.getElementById('yr');if(yr)yr.textContent=new Date().getFullYear();
}
