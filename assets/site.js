(function(){
var CFG={wa:"27636691391",waDisplay:"063 669 1391",email:"laafstylfamily@gmail.com"};
var L=localStorage.getItem('lw_lang')||'af';
function q(s,r){return (r||document).querySelectorAll(s);}
function setLang(l){
  L=l;localStorage.setItem('lw_lang',l);document.documentElement.lang=(l==='af'?'af':'en');
  q('[data-af]').forEach(function(e){e.innerHTML=e.dataset[l];});
  q('[data-ph-af]').forEach(function(e){e.placeholder=l==='af'?e.dataset.phAf:e.dataset.phEn;});
  q('[data-wa-af]').forEach(function(a){a.href='https://wa.me/'+CFG.wa+'?text='+encodeURIComponent(l==='af'?a.dataset.waAf:a.dataset.waEn);});
  var b=document.getElementById('bAf'),c=document.getElementById('bEn');
  if(b){b.classList.toggle('on',l==='af');c.classList.toggle('on',l==='en');b.setAttribute('aria-pressed',l==='af');c.setAttribute('aria-pressed',l==='en');}
}
document.addEventListener('DOMContentLoaded',function(){
  q('[data-cfg]').forEach(function(e){e.textContent=CFG[e.dataset.cfg];});
  q('a[data-mail]').forEach(function(a){a.href='mailto:'+CFG.email;});
  q('a[data-tel]').forEach(function(a){a.href='tel:+'+CFG.wa;});
  var y=document.getElementById('yr');if(y)y.textContent=new Date().getFullYear();
  var bAf=document.getElementById('bAf'),bEn=document.getElementById('bEn');
  if(bAf){bAf.onclick=function(){setLang('af');};bEn.onclick=function(){setLang('en');};}
  var bg=document.getElementById('burger'),mn=document.getElementById('menu');
  if(bg){bg.onclick=function(){var o=mn.classList.toggle('open');bg.setAttribute('aria-expanded',o);};
    q('#menu a').forEach(function(a){a.addEventListener('click',function(){mn.classList.remove('open');bg.setAttribute('aria-expanded',false);});});}
  var f=document.getElementById('qform');
  if(f){f.addEventListener('submit',function(e){e.preventDefault();
    function v(i){return document.getElementById(i).value.trim();}
    var m=L==='af'?('Hallo LaafWeb, ek wil graag \'n webwerf he.\nNaam: '+v('n')+'\nBesigheid: '+v('b')+'\nNommer: '+v('p')+'\nDorp: '+v('t')+'\nBesonderhede: '+v('m')):('Hi LaafWeb, I would like a website.\nName: '+v('n')+'\nBusiness: '+v('b')+'\nNumber: '+v('p')+'\nTown: '+v('t')+'\nDetails: '+v('m'));
    window.open('https://wa.me/'+CFG.wa+'?text='+encodeURIComponent(m),'_blank','noopener');});}
  setLang(L);
});
})();
