(function(){
var CFG={wa:"27636691391",waDisplay:"063 669 1391",email:"laafstylfamily@gmail.com"};
var LANGS=["en","af","xh","zu"];
var FORM={
 en:{hi:"Hi LaafWeb, I would like a website.",n:"Name",b:"Business",p:"Number",t:"Town",m:"Details"},
 af:{hi:"Hallo LaafWeb, ek wil graag \u2019n webwerf h\u00ea.",n:"Naam",b:"Besigheid",p:"Nommer",t:"Dorp",m:"Besonderhede"},
 xh:{hi:"Molo LaafWeb, ndifuna iwebhusayithi.",n:"Igama",b:"Ishishini",p:"Inombolo",t:"Idolophu",m:"Iinkcukacha"},
 zu:{hi:"Sawubona LaafWeb, ngifuna iwebhusayithi.",n:"Igama",b:"Ibhizinisi",p:"Inombolo",t:"Idolobha",m:"Imininingwane"}
};
var page=document.documentElement.lang||"en";
function q(s,r){return (r||document).querySelectorAll(s);}
function store(l){try{localStorage.setItem('lw_lang',l);}catch(e){}}
function stored(){try{var v=localStorage.getItem('lw_lang');return LANGS.indexOf(v)>-1?v:null;}catch(e){return null;}}
// remember a visitor's language and send returning visitors from the English page to their language
var s=stored(),p=location.pathname;
if(page==="en"&&s&&s!=="en"&&/^\/(index\.html|pricing\.html|contact\.html)?$/.test(p)&&!location.search){
  location.replace("/"+s+(p==="/index.html"?"/":p));return;
}
document.addEventListener('DOMContentLoaded',function(){
  q('[data-cfg]').forEach(function(e){e.textContent=CFG[e.dataset.cfg];});
  q('a[data-mail]').forEach(function(a){a.href='mailto:'+CFG.email;});
  q('a[data-tel]').forEach(function(a){a.href='tel:+'+CFG.wa;});
  var y=document.getElementById('yr');if(y)y.textContent=new Date().getFullYear();
  q('.lang a').forEach(function(a){a.addEventListener('click',function(){store(a.dataset.l);});});
  if(LANGS.indexOf(page)>-1&&page!=="en"&&!stored())store(page);
  var bg=document.getElementById('burger'),mn=document.getElementById('menu');
  if(bg){bg.onclick=function(){var o=mn.classList.toggle('open');bg.setAttribute('aria-expanded',o);};
    q('#menu a').forEach(function(a){a.addEventListener('click',function(){mn.classList.remove('open');bg.setAttribute('aria-expanded',false);});});}
  var f=document.getElementById('qform');
  if(f){f.addEventListener('submit',function(e){e.preventDefault();
    function v(i){return document.getElementById(i).value.trim();}
    var F=FORM[page]||FORM.en;
    var m=F.hi+'\n'+F.n+': '+v('n')+'\n'+F.b+': '+v('b')+'\n'+F.p+': '+v('p')+'\n'+F.t+': '+v('t')+'\n'+F.m+': '+v('m');
    window.open('https://wa.me/'+CFG.wa+'?text='+encodeURIComponent(m),'_blank','noopener');});}
});
})();
