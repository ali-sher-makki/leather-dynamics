document.getElementById("contact-form").addEventListener("submit", async function (e) {
  e.preventDefault();
  const form = e.target;
  const status = document.getElementById("form-status");
  const data = {
    name: form.name.value,
    company_name: form.company_name.value,
    country: form.country.value,
    contact_info: form.contact_info.value,
    product_required: form.product_required.value,
    quantity: form.quantity.value,
    customization_requirements: form.customization_requirements.value,
    message: form.message.value
  };

  status.textContent = "Sending...";
  status.className = "form-status";

  try {
    const res = await fetch("/api/quote/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    if (res.ok) {
      status.textContent = "Request sent - we will get back to you soon.";
      status.classList.add("success");
      form.reset();
    } else {
      status.textContent = "Something went wrong. Please try again.";
      status.classList.add("error");
    }
  } catch (err) {
    status.textContent = "Something went wrong. Please try again.";
    status.classList.add("error");
    console.error(err);
  }
});
