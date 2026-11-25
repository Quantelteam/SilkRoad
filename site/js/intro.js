// The 30-second intro video in the header. Nothing shows until assets/intro.mp4
// actually loads, so the page looks finished before the video is exported.
// It plays muted while on screen, at every width, with its own Pause and Sound buttons.
import { byId } from './dom.js';
import { t } from './i18n.js';

const SRC = 'assets/intro.mp4';
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');

const figure = byId('intro');
const video = /** @type {HTMLVideoElement} */ (byId('intro-video'));
const toggle = byId('intro-toggle');
const sound = byId('intro-sound');
const openBtn = byId('intro-open');
const dialog = /** @type {HTMLDialogElement} */ (byId('intro-dialog'));
const dialogVideo = /** @type {HTMLVideoElement} */ (byId('intro-dialog-video'));

let userPaused = reduceMotion.matches; // people who asked for less motion start it themselves
// Phones on a data saver don't autoplay the 2 MB clip; the Play button still works.
const saveData = Boolean(/** @type {any} */ (navigator).connection?.saveData);

video.addEventListener('loadeddata', () => {
  figure.hidden = false;
  openBtn.hidden = false;
  watchVisibility();
  sync();
}, { once: true });
// A missing file just leaves the intro hidden.
video.addEventListener('error', () => { figure.hidden = true; openBtn.hidden = true; }, { once: true });
video.src = SRC;

/** Plays only while the video is on screen. */
function watchVisibility() {
  if (!('IntersectionObserver' in window)) return playIfAllowed(true);
  new IntersectionObserver(([entry]) => playIfAllowed(entry.isIntersecting), { threshold: 0.4 }).observe(video);
}

function playIfAllowed(visible) {
  if (visible && !userPaused && !saveData) video.play().catch(() => { userPaused = true; sync(); });
  else video.pause();
}

function sync() {
  const playing = !video.paused;
  toggle.textContent = playing ? t('intro.pause') : t('intro.play');
  toggle.setAttribute('aria-pressed', String(!playing));
  sound.textContent = video.muted ? t('intro.soundOn') : t('intro.soundOff');
  sound.setAttribute('aria-pressed', String(!video.muted));
}

video.addEventListener('play', sync);
video.addEventListener('pause', sync);

toggle.addEventListener('click', () => {
  userPaused = !video.paused;
  if (userPaused) video.pause();
  else video.play().catch(() => {});
});

sound.addEventListener('click', () => {
  video.muted = !video.muted;
  if (!video.muted && video.paused) { userPaused = false; video.play().catch(() => {}); }
  sync();
});


// Narrow screens: open the video in a dialog, with sound and the browser's own controls.
openBtn.addEventListener('click', () => {
  if (!dialogVideo.src) dialogVideo.src = SRC;
  video.pause();
  dialog.showModal();
  dialogVideo.play().catch(() => {});
});
byId('intro-close').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', (e) => { if (e.target === dialog) dialog.close(); });
dialog.addEventListener('close', () => dialogVideo.pause());
