gsap.registerPlugin(ScrollTrigger);

const lenis = new Lenis();
lenis.on("scroll", ScrollTrigger.update);
gsap.ticker.add((time) => { lenis.raf(time * 1000); });
gsap.ticker.lagSmoothing(0);

gsap.timeline({ defaults: { ease: "power3.out" } })
  .from(".eyebrow", { opacity: 0, y: 20, duration: 0.6 })
  .from(".hero-title", { opacity: 0, y: 30, duration: 0.8 }, "-=0.3")
  .from(".hero-sub", { opacity: 0, y: 20, duration: 0.7 }, "-=0.5")
  .from(".btn-primary", { opacity: 0, y: 20, duration: 0.6 }, "-=0.4");

gsap.to(".product-card", {
  rotateY: 360,
  ease: "none",
  scrollTrigger: {
    trigger: ".showcase",
    start: "top top",
    end: "bottom bottom",
    scrub: 1
  }
});

gsap.from(".showcase-copy", {
  opacity: 0,
  y: 40,
  duration: 0.8,
  ease: "power3.out",
  scrollTrigger: {
    trigger: ".showcase-copy",
    start: "top 80%"
  }
});
