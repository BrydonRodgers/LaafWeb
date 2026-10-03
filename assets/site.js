(function(){
var CFG={wa:"27636691391",waDisplay:"063 669 1391",email:"laafstylfamily@gmail.com"};
var LANGS=["en","af","xh","zu"];
var FORM={
 en:{hi:"Hi LaafWeb, I would like a website.",n:"Name",b:"Business",p:"Number",t:"Town",m:"Details"},
 af:{hi:"Hallo LaafWeb, ek wil graag 'n webwerf h\u00ea.",n:"Naam",b:"Besigheid",p:"Nommer",t:"Dorp",m:"Besonderhede"},
 xh:{hi:"Molo LaafWeb, ndifuna iwebhusayithi.",n:"Igama",b:"Ishishini",p:"Inombolo",t:"Idolophu",m:"Iinkcukacha"},
 zu:{hi:"Sawubona LaafWeb, ngifuna iwebhusayithi.",n:"Igama",b:"Ibhizinisi",p:"Inombolo",t:"Idolobha",m:"Imininingwane"}
};
var L="en";
try{var sv=localStorage.getItem('lw_lang');if(sv&&LANGS.indexOf(sv)>-1)L=sv;}catch(e){}
function q(s,r){return (r||document).querySelectorAll(s);}
function cap(x){return x.charAt(0).toUpperCase()+x.slice(1);}
function setLang(l){
  L=l;try{localStorage.setItem('lw_lang',l);}catch(e){}
  document.documentElement.lang=l;
  q('[data-en]').forEach(function(e){e.innerHTML=e.dataset[l]||e.dataset.en;});
  q('[data-ph-en]').forEach(function(e){e.placeholder=e.dataset['ph'+cap(l)]||e.dataset.phEn;});
  q('[data-wa-en]').forEach(function(a){a.href='https://wa.me/'+CFG.wa+'?text='+encodeURIComponent(a.dataset['wa'+cap(l)]||a.dataset.waEn);});
  q('.lang button').forEach(function(b){var on=b.dataset.l===l;b.classList.toggle('on',on);b.setAttribute('aria-pressed',on);});
}
document.addEventListener('DOMContentLoaded',function(){
  q('[data-cfg]').forEach(function(e){e.textContent=CFG[e.dataset.cfg];});
  q('a[data-mail]').forEach(function(a){a.href='mailto:'+CFG.email;});
  q('a[data-tel]').forEach(function(a){a.href='tel:+'+CFG.wa;});
  var y=document.getElementById('yr');if(y)y.textContent=new Date().getFullYear();
  q('.lang button').forEach(function(b){b.onclick=function(){setLang(b.dataset.l);};});
  var bg=document.getElementById('burger'),mn=document.getElementById('menu');
  if(bg){bg.onclick=function(){var o=mn.classList.toggle('open');bg.setAttribute('aria-expanded',o);};
    q('#menu a').forEach(function(a){a.addEventListener('click',function(){mn.classList.remove('open');bg.setAttribute('aria-expanded',false);});});}
  var f=document.getElementById('qform');
  if(f){f.addEventListener('submit',function(e){e.preventDefault();
    function v(i){return document.getElementById(i).value.trim();}
    var F=FORM[L]||FORM.en;
    var m=F.hi+'\n'+F.n+': '+v('n')+'\n'+F.b+': '+v('b')+'\n'+F.p+': '+v('p')+'\n'+F.t+': '+v('t')+'\n'+F.m+': '+v('m');
    window.open('https://wa.me/'+CFG.wa+'?text='+encodeURIComponent(m),'_blank','noopener');});}
  setLang(L);
});
})();
