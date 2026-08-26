async function loadProducts() {
  const grid = document.getElementById("shop-grid");
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
        <h3 class="shop-card-name">${p.name}</h3>
        <p class="shop-card-price">$${parseFloat(p.price).toFixed(2)}</p>
      </div>
    `).join("");

    gsap.from(".shop-card", {
      opacity: 0, y: 30, duration: 0.6, ease: "power3.out", stagger: 0.12,
      scrollTrigger: { trigger: ".shop-grid", start: "top 80%" }
    });
    ScrollTrigger.refresh();
  } catch (err) {
    grid.innerHTML = '<p class="shop-empty">Could not load products right now.</p>';
    console.error(err);
  }
}

document.addEventListener("DOMContentLoaded", loadProducts);
