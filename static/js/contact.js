document.getElementById("contact-form").addEventListener("submit", async function (e) {
  e.preventDefault();
  const form = e.target;
  const status = document.getElementById("form-status");
  const data = {
    name: form.name.value,
    email: form.email.value,
    message: form.message.value
  };

  status.textContent = "Sending...";
  status.className = "form-status";

  try {
    const res = await fetch("/api/contact/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    if (res.ok) {
      status.textContent = "Message sent - we will get back to you soon.";
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
