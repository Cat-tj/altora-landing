/* Shared Altora shell; locale-aware without overwriting the homepage's source shell. */
(function(){
'use strict';
var path=location.pathname.replace(/\.html$/,'').replace(/\/$/,'')||'/';
var isId=true;
var localeRoot='';
var route=path;
var asset='/assets';
var icon=asset+'/img/altora-logo-icon-v2.svg?v=20260919-padded';
var t=isId?{
 services:'Layanan',about:'Tentang',support:'Support',consult:'Konsultasi',careers:'Karier',contact:'Kontak',privacy:'Privasi',terms:'Ketentuan',explore:'Jelajahi',get:'Hubungi Kami',start:'Mulai konsultasi →',desc:'Altora membantu organisasi merancang, membangun, dan mengintegrasikan teknologi—mulai dari AI dan CCTV analytics sampai software, data, IoT, cloud, serta jaringan.',tag:'Tinggalkan cara lama. Masuk ke ritme yang baru.'
}:{
 services:'Services',about:'About',support:'Support',consult:'Consult',careers:'Careers',contact:'Contact',privacy:'Privacy',terms:'Terms',explore:'Explore',get:'Get in touch',start:'Start a consultation →',desc:'Altora helps organisations design, build, and integrate technology—from AI and CCTV analytics to software, data, IoT, cloud, and networks.',tag:'Leave old ways behind. Find a new rhythm.'
};
function href(slug){return localeRoot+(slug==='/'?'/':slug)}
function active(slug){return route===slug||(slug!=='/'&&route.indexOf(slug+'/')===0)?' aria-current="page"':''}
var nav='<header class="nav-wrap universal-shell" id="nav"><nav class="nav" aria-label="Primary"><a class="brand" href="'+href('/')+'"><img src="'+icon+'" alt="Altora" width="34" height="30"><span>ALTORA</span></a><ul class="nav-links"><li><a class="nav-link"'+active('/services')+' href="'+href('/services')+'">'+t.services+'</a></li><li><a class="nav-link"'+active('/produk')+' href="'+href('/produk')+'">Produk</a></li><li><a class="nav-link"'+active('/portfolio')+' href="'+href('/portfolio')+'">Portofolio</a></li><li><a class="nav-link"'+active('/about')+' href="'+href('/about')+'">'+t.about+'</a></li><li><a class="nav-link"'+active('/support')+' href="'+href('/support')+'">'+t.support+'</a></li></ul><div class="nav-cta"><a class="btn btn-green" href="'+href('/contact')+'">'+t.consult+' <span aria-hidden="true">→</span></a></div><button class="burger" type="button" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button></nav><div class="mobile-menu"><a'+active('/services')+' href="'+href('/services')+'">'+t.services+'</a><a'+active('/produk')+' href="'+href('/produk')+'">Produk</a><a'+active('/portfolio')+' href="'+href('/portfolio')+'">Portofolio</a><a'+active('/about')+' href="'+href('/about')+'">'+t.about+'</a><a'+active('/support')+' href="'+href('/support')+'">'+t.support+'</a><a href="'+href('/careers')+'">'+t.careers+'</a><div class="mobile-menu-cta"><a class="btn btn-green" href="'+href('/contact')+'">'+t.consult+' <span aria-hidden="true">→</span></a></div></div></header>';
/* Homepage owns its existing shell. Secondary pages use a stable shared shell. */
var isHomepage=route==='/';
if(!isHomepage){var oldHeader=document.querySelector('.company-nav,.project-nav,#nav');if(oldHeader)oldHeader.outerHTML=nav;}
var shell=document.querySelector('.universal-shell');if(!shell)return;
var burger=shell.querySelector('.burger'),menu=shell.querySelector('.mobile-menu');
burger.addEventListener('click',function(){var open=burger.getAttribute('aria-expanded')==='true';burger.setAttribute('aria-expanded',String(!open));menu.classList.toggle('open',!open)});
menu.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){burger.setAttribute('aria-expanded','false');menu.classList.remove('open')})});
window.addEventListener('scroll',function(){shell.classList.toggle('stuck',window.scrollY>16)},{passive:true});
})();