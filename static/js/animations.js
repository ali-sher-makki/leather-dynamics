gsap.registerPlugin(ScrollTrigger);

const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

const themeToggle = document.getElementById("theme-toggle");
function updateThemeIcon() {
  const isLight = document.documentElement.getAttribute("data-theme") === "light";
  if (themeToggle) themeToggle.innerHTML = isLight ? "&#9728;" : "&#127769;";
}
if (themeToggle) {
  updateThemeIcon();
  themeToggle.addEventListener("click", () => {
    const isLight = document.documentElement.getAttribute("data-theme") === "light";
    if (isLight) {
      document.documentElement.removeAttribute("data-theme");
      localStorage.setItem("theme", "dark");
    } else {
      document.documentElement.setAttribute("data-theme", "light");
      localStorage.setItem("theme", "light");
    }
    updateThemeIcon();
  });
}

ScrollTrigger.create({
  start: "top -80",
  onUpdate: (self) => {
    const nav = document.querySelector(".floating-nav");
    if (nav) nav.classList.toggle("scrolled", self.scroll() > 80);
  }
});

const navToggle = document.getElementById("nav-toggle");
const mobileMenu = document.getElementById("mobile-menu");
if (navToggle && mobileMenu) {
  navToggle.addEventListener("click", () => {
    navToggle.classList.toggle("open");
    mobileMenu.classList.toggle("open");
  });
  mobileMenu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navToggle.classList.remove("open");
      mobileMenu.classList.remove("open");
    });
  });
}

if (!prefersReducedMotion) {
  const lenis = new Lenis();
  lenis.on("scroll", ScrollTrigger.update);
  gsap.ticker.add((time) => { lenis.raf(time * 1000); });
  gsap.ticker.lagSmoothing(0);

  gsap.from(".floating-nav", { opacity: 0, y: -20, duration: 0.8, ease: "power3.out", delay: 0.1 });

  gsap.timeline({ defaults: { ease: "power3.out" } })
    .from(".eyebrow", { opacity: 0, y: 20, duration: 0.6 }, 0.3)
    .from(".hero-title", { opacity: 0, y: 30, duration: 0.8 }, "-=0.3")
    .from(".hero-sub", { opacity: 0, y: 20, duration: 0.7 }, "-=0.5")
    .from(".hero-actions", { opacity: 0, y: 20, duration: 0.6 }, "-=0.4")
    .from(".hero-image img", { opacity: 0, scale: 0.85, duration: 1 }, "-=0.8");

  gsap.to(".hero-image img", { y: 15, duration: 2.5, ease: "sine.inOut", repeat: -1, yoyo: true });

  gsap.from(".story-content", {
    opacity: 0, y: 40, duration: 0.9, ease: "power3.out",
    scrollTrigger: { trigger: ".story", start: "top 75%" }
  });

  gsap.to(".product-card", {
    rotateY: 360, ease: "none",
    scrollTrigger: { trigger: ".showcase", start: "top top", end: "bottom bottom", scrub: 1 }
  });

  gsap.from(".showcase-copy", {
    opacity: 0, y: 40, duration: 0.8, ease: "power3.out",
    scrollTrigger: { trigger: ".showcase-copy", start: "top 80%" }
  });

  gsap.from(".why-card", {
    opacity: 0, y: 30, duration: 0.6, ease: "power3.out", stagger: 0.1,
    scrollTrigger: { trigger: ".why-choose-grid", start: "top 80%" }
  });

  gsap.from(".custom-orders-inner", {
    opacity: 0, y: 30, duration: 0.8, ease: "power3.out",
    scrollTrigger: { trigger: ".custom-orders", start: "top 80%" }
  });

  gsap.from(".category-card", {
    opacity: 0, y: 30, duration: 0.6, ease: "power3.out", stagger: 0.1,
    scrollTrigger: { trigger: ".category-grid", start: "top 80%" }
  });
}
