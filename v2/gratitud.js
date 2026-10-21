// entrada escalonada: quem tem .sobe aparece ao entrar na tela (sem script, tudo fica visível)
document.documentElement.classList.add('js');
(function(){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('visto');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
document.querySelectorAll('.sobe').forEach(function(el,i){el.style.transitionDelay=((el.dataset.ordem||0)*75)+'ms';io.observe(el);});})();
