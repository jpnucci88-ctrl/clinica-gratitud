/* Som ambiente cinematográfico gerado ao vivo (Web Audio: sem arquivo, sem direito autoral).
   Estilo "trilha de cinema": grave contínuo que cresce, cordas (ondas desafinadas em par),
   filtro que respira devagar, reverberação longa de sala e notas espaçadas por cima.
   Lê window.SOM_TEMA = {
     vol, corte,                                   // volume final (0.05–0.12) e brilho base (Hz)
     drone: "D2",                                  // nota grave contínua (opcional)
     pad: {acordes:[["D3","A3","F4"],...], dur, onda},   // cordas (onda: "sawtooth" | "triangle" | "sine")
     notas: {lista:[...], passo, dens, decai, onda, sino, ordem},  // notas por cima
     pulso: {nota:"D2", bpm:60}                    // batida grave (opcional)
   }
   - começa no primeiro toque/clique/tecla (navegadores bloqueiam som antes disso);
   - botão .som no menu liga/desliga; a escolha vale para as outras páginas (localStorage). */
(function () {
  var T = window.SOM_TEMA; if (!T) return;
  var KEY = 'somAmbiente', ligado = true;
  try { ligado = localStorage.getItem(KEY) !== 'off'; } catch (e) {}
  var reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ctx, master, filtro, sala, timers = [], fontes = [];
  var btn = document.querySelector('.som');

  function hz(n) { // "A4" -> 440 ; aceita "F#3" e "Bb2"
    var m = /^([A-G])([#b]?)(-?\d)$/.exec(n); if (!m) return +n;
    var s = { C: -9, D: -7, E: -5, F: -4, G: -2, A: 0, B: 2 }[m[1]] + (m[2] === '#' ? 1 : m[2] === 'b' ? -1 : 0);
    return 440 * Math.pow(2, (s + (m[3] - 4) * 12) / 12);
  }
  function respostaSala(seg) { // reverberação: ruído que decai, em estéreo
    var len = ctx.sampleRate * seg, b = ctx.createBuffer(2, len, ctx.sampleRate);
    for (var c = 0; c < 2; c++) {
      var d = b.getChannelData(c);
      for (var i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, 2.6);
    }
    return b;
  }
  function voz(f, onda, ini, ataque, dura, ganho, destino, detune) {
    var o = ctx.createOscillator(), g = ctx.createGain();
    o.type = onda; o.frequency.value = f; if (detune) o.detune.value = detune;
    g.gain.setValueAtTime(0.0001, ini);
    g.gain.exponentialRampToValueAtTime(ganho, ini + ataque);
    g.gain.exponentialRampToValueAtTime(0.0001, ini + ataque + dura);
    o.connect(g); g.connect(destino); o.start(ini); o.stop(ini + ataque + dura + 0.2);
  }
  function drone() {
    if (!T.drone) return;
    var f = hz(T.drone), g = ctx.createGain(); g.gain.value = 0.0001; g.connect(filtro);
    [[f, 'sine', 0], [f / 2, 'sine', 0], [f, 'sawtooth', 5], [f, 'sawtooth', -5]].forEach(function (v) {
      var o = ctx.createOscillator(); o.type = v[1]; o.frequency.value = v[0]; o.detune.value = v[2];
      var gv = ctx.createGain(); gv.gain.value = v[1] === 'sine' ? 0.5 : 0.08;
      o.connect(gv); gv.connect(g); o.start(); fontes.push(o);
    });
    g.gain.exponentialRampToValueAtTime(0.22, ctx.currentTime + (reduz ? 1 : 8)); // cresce devagar
  }
  function pad() {
    if (!T.pad) return;
    var i = 0, d = T.pad.dur || 10, onda = T.pad.onda || 'sawtooth';
    (function prox() {
      if (!ctx) return;
      var t = ctx.currentTime, acorde = T.pad.acordes[i++ % T.pad.acordes.length], g = 0.16 / acorde.length;
      acorde.forEach(function (n) { // cada nota = 2 vozes desafinadas (efeito de naipe de cordas)
        voz(hz(n), onda, t, d * 0.45, d * 0.85, g, filtro, -7);
        voz(hz(n), onda, t, d * 0.5, d * 0.8, g, filtro, 7);
      });
      timers.push(setTimeout(prox, d * 1000 * 0.72));
    })();
  }
  function notas() {
    if (!T.notas) return;
    var N = T.notas, k = 0;
    timers.push(setInterval(function () {
      if (!ctx || Math.random() > (N.dens || 0.4)) return;
      var n = N.ordem ? N.lista[k++ % N.lista.length] : N.lista[Math.floor(Math.random() * N.lista.length)];
      var f = hz(n), t = ctx.currentTime, destino = sala.entrada;
      if (T.espacial && ctx.createStereoPanner) { // 3D: cada nota nasce num ponto diferente do espaço
        var pan = ctx.createStereoPanner(); pan.pan.value = Math.sin(t * 2.3) * 0.75; pan.connect(sala.entrada); destino = pan;
      }
      voz(f, N.onda || 'sine', t, 0.02, N.decai || 3, 0.1, destino);
      if (N.sino) voz(f * N.sino, 'sine', t, 0.005, (N.decai || 3) * 0.4, 0.03, destino);
    }, N.passo || 1600));
  }
  function pulso() {
    if (!T.pulso) return;
    var f = hz(T.pulso.nota || 'D2'), ms = 60000 / (T.pulso.bpm || 60);
    timers.push(setInterval(function () {
      if (!ctx) return;
      var t = ctx.currentTime, o = ctx.createOscillator(), g = ctx.createGain();
      o.frequency.setValueAtTime(f * 2, t); o.frequency.exponentialRampToValueAtTime(f, t + 0.25);
      g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.35, t + 0.02);
      g.gain.exponentialRampToValueAtTime(0.0001, t + 1.2);
      o.connect(g); g.connect(master); o.start(t); o.stop(t + 1.3);
    }, ms));
  }
  function batida() { // batida leve (bumbo, palma, chimbal) — T.batida = {bpm, chimbal, palma}
    if (!T.batida || reduz) return;
    var B = T.batida, ms = 60000 / (B.bpm || 96) / 2, passo = 0;
    var ruido = ctx.createBuffer(1, ctx.sampleRate * 0.3, ctx.sampleRate), d = ruido.getChannelData(0);
    for (var i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
    function bate(freq, dur, ganho, tipo) {
      var t = ctx.currentTime, s = ctx.createBufferSource(), f = ctx.createBiquadFilter(), g = ctx.createGain();
      s.buffer = ruido; f.type = tipo; f.frequency.value = freq;
      g.gain.setValueAtTime(ganho, t); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
      s.connect(f); f.connect(g); g.connect(sala.entrada); s.start(t); s.stop(t + dur);
    }
    timers.push(setInterval(function () {
      if (!ctx) return;
      var t = ctx.currentTime, p = passo++ % 8;
      if (p === 0 || p === 3 || p === 4) { // bumbo
        var o = ctx.createOscillator(), g = ctx.createGain();
        o.frequency.setValueAtTime(120, t); o.frequency.exponentialRampToValueAtTime(45, t + 0.18);
        g.gain.setValueAtTime(0.5, t); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.45);
        o.connect(g); g.connect(master); o.start(t); o.stop(t + 0.5);
      }
      if (B.palma && (p === 2 || p === 6)) bate(1500, 0.18, 0.18, 'bandpass');
      if (B.chimbal) bate(8000, 0.05, p % 2 ? 0.05 : 0.08, 'highpass');
    }, ms));
  }
  function iniciar() {
    if (ctx || !ligado) return;
    ctx = new (window.AudioContext || window.webkitAudioContext)();
    master = ctx.createGain(); master.gain.value = 0.0001; master.connect(ctx.destination);
    var rev = ctx.createConvolver(); rev.buffer = respostaSala(5);
    var molhado = ctx.createGain(); molhado.gain.value = 0.55; rev.connect(molhado); molhado.connect(master);
    sala = { entrada: ctx.createGain() };
    sala.entrada.connect(rev); sala.entrada.connect(master);
    filtro = ctx.createBiquadFilter(); filtro.type = 'lowpass'; filtro.Q.value = 0.7;
    var base = T.corte || 1400; filtro.frequency.value = base;
    filtro.connect(sala.entrada);
    if (!reduz) { // filtro "respira": abre e fecha a cada ~20 s
      var lfo = ctx.createOscillator(), prof = ctx.createGain();
      lfo.frequency.value = 0.05; prof.gain.value = base * 0.45;
      lfo.connect(prof); prof.connect(filtro.frequency); lfo.start(); fontes.push(lfo);
    }
    master.gain.exponentialRampToValueAtTime(T.vol || 0.08, ctx.currentTime + (reduz ? 0.8 : 4));
    drone(); pad(); notas(); pulso(); batida();
  }
  function parar() {
    if (!ctx) return;
    var c = ctx, m = master; ctx = null;
    timers.forEach(function (x) { clearTimeout(x); clearInterval(x); }); timers = [];
    m.gain.setTargetAtTime(0.0001, c.currentTime, 0.4);
    setTimeout(function () { fontes.forEach(function (o) { try { o.stop(); } catch (e) {} }); fontes = []; c.close(); }, 1500);
  }
  function marcar() {
    if (!btn) return;
    btn.setAttribute('aria-pressed', ligado ? 'true' : 'false');
    btn.setAttribute('aria-label', ligado ? 'Desligar som ambiente' : 'Ligar som ambiente');
    btn.dataset.on = ligado ? '1' : '0';
  }
  function primeiroGesto(e) {
    if (btn && btn.contains(e.target)) return; // o clique no botão é tratado por ele
    ['pointerdown', 'keydown', 'touchstart'].forEach(function (n) { removeEventListener(n, primeiroGesto, true); });
    if (ligado) iniciar();
  }
  if (btn) btn.addEventListener('click', function () {
    ligado = !ligado;
    try { localStorage.setItem(KEY, ligado ? 'on' : 'off'); } catch (er) {}
    marcar(); ligado ? iniciar() : parar();
  });
  marcar();
  ['pointerdown', 'keydown', 'touchstart'].forEach(function (n) { addEventListener(n, primeiroGesto, true); });
  addEventListener('pagehide', parar);
})();
