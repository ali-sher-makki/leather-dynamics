async function loadProducts() {
  const grid = document.getElementById("shop-grid");
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  try {
    const res = await fetch("/api/products/");
    const products = await res.json();

    if (!products.length) {
      grid.innerHTML = '<p class="shop-empty">New pieces coming soon.</p>';
      return;
    }

    grid.innerHTML = products.map(p => `
      <div class="shop-card">
        <div class="shop-card-image" style="${p.image ? `background-image:url('${p.image}');background-size:cover;background-position:center;` : ""}"></div>
        ${p.category ? `<p class="shop-card-category">${p.category}</p>` : ""}
        <h3 class="shop-card-name">${p.name}</h3>
        <p class="shop-card-price">${p.price ? "$" + parseFloat(p.price).toFixed(2) : "Contact for Pricing"}</p>
      </div>
    `).join("");

    if (!prefersReducedMotion) {
      gsap.from(".shop-card", {
        opacity: 0, y: 30, duration: 0.6, ease: "power3.out", stagger: 0.12,
        scrollTrigger: { trigger: ".shop-grid", start: "top 80%" }
      });
      ScrollTrigger.refresh();
    }
  } catch (err) {
    grid.innerHTML = '<p class="shop-empty">Could not load products right now.</p>';
    console.error(err);
  }
}

document.addEventListener("DOMContentLoaded", loadProducts);
