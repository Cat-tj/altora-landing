/* Perilaku top bar bersama. Markup header & footer ditulis statis dari partials/ (scripts/apply_shell.py). */
(function(){
'use strict';
var shell=document.querySelector('.universal-shell');if(!shell)return;
var burger=shell.querySelector('.burger'),menu=shell.querySelector('.mobile-menu');
if(burger&&menu){
 var setOpen=function(open){menu.classList.toggle('open',open);burger.setAttribute('aria-expanded',String(open));burger.setAttribute('aria-label',open?'Tutup menu':'Buka menu')};
 burger.addEventListener('click',function(){setOpen(burger.getAttribute('aria-expanded')!=='true')});
 menu.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){setOpen(false)})});
 document.addEventListener('keydown',function(e){if(e.key==='Escape')setOpen(false)});
}
var onScroll=function(){shell.classList.toggle('stuck',window.scrollY>12)};
window.addEventListener('scroll',onScroll,{passive:true});onScroll();
})();
