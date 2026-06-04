(function () {
  const SESSION_KEY = "demo.session";
  const LOGIN_FLASH_KEY = "demo.loginSuccessMessage";
  const CART_KEY = "demo.cart";
  const PROFILE_KEY = "demo.profile";

  const validUser = {
    email: "test@example.com",
    password: "Password123",
    firstName: "Test",
    lastName: "User",
  };

  const products = [
    { id: "wireless-mouse", name: "Wireless Mouse", price: 24.99 },
    { id: "mechanical-keyboard", name: "Mechanical Keyboard", price: 89.99 },
    { id: "usb-c-hub", name: "USB-C Hub", price: 39.99 },
    { id: "laptop-stand", name: "Laptop Stand", price: 49.99 },
  ];

  document.addEventListener("DOMContentLoaded", init);

  function init() {
    const page = document.body.dataset.page;

    if (page !== "login") {
      if (!requireSession()) return;
      setupLogout();
    }

    if (page === "login") setupLogin();
    if (page === "dashboard") setupDashboard();
    if (page === "products") setupProducts();
    if (page === "cart") setupCart();
    if (page === "profile") setupProfile();
  }

  function requireSession() {
    if (!getSession()) {
      window.location.href = "index.html";
      return false;
    }
    return true;
  }

  function getSession() {
    return readJson(SESSION_KEY, null);
  }

  function setupLogin() {
    const form = document.getElementById("login-form");
    const message = document.getElementById("login-message");

    if (getSession()) {
      window.location.href = "dashboard.html";
      return;
    }

    form.addEventListener("submit", function (event) {
      event.preventDefault();

      const email = form.elements.email.value.trim();
      const password = form.elements.password.value;
      const rememberMe = form.elements.rememberMe.checked;

      if (email === validUser.email && password === validUser.password) {
        localStorage.setItem(
          SESSION_KEY,
          JSON.stringify({
            email,
            firstName: validUser.firstName,
            lastName: validUser.lastName,
            rememberMe,
            loggedInAt: new Date().toISOString(),
          })
        );
        sessionStorage.setItem(LOGIN_FLASH_KEY, "Login successful");
        window.location.href = "dashboard.html";
        return;
      }

      setMessage(message, "Invalid email or password.", "error");
    });
  }

  function setupLogout() {
    const logoutButton = document.querySelector('[data-action="logout"]');
    if (!logoutButton) return;

    logoutButton.addEventListener("click", function () {
      localStorage.removeItem(SESSION_KEY);
      window.location.href = "index.html";
    });
  }

  function setupDashboard() {
    const session = getSession();
    const dashboardMessage = document.getElementById("dashboard-message");
    const welcome = document.getElementById("welcome-message");
    const loginMessage = sessionStorage.getItem(LOGIN_FLASH_KEY);

    if (loginMessage) {
      setMessage(dashboardMessage, loginMessage, "success");
      sessionStorage.removeItem(LOGIN_FLASH_KEY);

      window.setTimeout(function () {
        clearMessage(dashboardMessage);
      }, 2000);
    }

    welcome.textContent = `Welcome, ${session.firstName}. Choose a demo area to test.`;
  }

  function setupProducts() {
    const productList = document.getElementById("product-list");
    const message = document.getElementById("product-message");

    products.forEach(function (product) {
      const card = document.createElement("article");
      card.className = "product-card";
      card.dataset.testid = `product-${product.id}`;

      const heading = document.createElement("h2");
      heading.textContent = product.name;

      const price = document.createElement("p");
      price.className = "price";
      price.textContent = formatPrice(product.price);

      const button = document.createElement("button");
      button.type = "button";
      button.textContent = "Add to Cart";
      button.addEventListener("click", function () {
        addToCart(product);
        setMessage(message, `${product.name} added to cart.`, "success");
      });

      card.append(heading, price, button);
      productList.appendChild(card);
    });
  }

  function setupCart() {
    const checkoutButton = document.getElementById("checkout-button");

    renderCart();

    checkoutButton.addEventListener("click", function () {
      const cart = getCart();
      const message = document.getElementById("cart-message");

      if (cart.length === 0) {
        setMessage(message, "Your cart is empty.", "error");
        return;
      }

      localStorage.setItem(CART_KEY, JSON.stringify([]));
      setMessage(message, "Checkout complete. Your cart has been cleared.", "success");
      renderCart();
    });
  }

  function setupProfile() {
    const session = getSession();
    const form = document.getElementById("profile-form");
    const message = document.getElementById("profile-message");
    const profile = readJson(PROFILE_KEY, {
      firstName: session.firstName,
      lastName: session.lastName,
      email: session.email,
    });

    form.elements.firstName.value = profile.firstName || "";
    form.elements.lastName.value = profile.lastName || "";
    form.elements.email.value = profile.email || "";

    form.addEventListener("submit", function (event) {
      event.preventDefault();

      const updatedProfile = {
        firstName: form.elements.firstName.value.trim(),
        lastName: form.elements.lastName.value.trim(),
        email: form.elements.email.value.trim(),
      };

      localStorage.setItem(PROFILE_KEY, JSON.stringify(updatedProfile));
      setMessage(message, "Profile saved successfully.", "success");
    });
  }

  function addToCart(product) {
    const cart = getCart();
    const existingItem = cart.find(function (item) {
      return item.id === product.id;
    });

    if (existingItem) {
      existingItem.quantity += 1;
    } else {
      cart.push({
        id: product.id,
        name: product.name,
        price: product.price,
        quantity: 1,
      });
    }

    localStorage.setItem(CART_KEY, JSON.stringify(cart));
  }

  function renderCart() {
    const cart = getCart();
    const cartItems = document.getElementById("cart-items");
    const emptyMessage = document.getElementById("empty-cart-message");
    const checkoutButton = document.getElementById("checkout-button");

    cartItems.replaceChildren();
    emptyMessage.hidden = cart.length > 0;
    checkoutButton.disabled = cart.length === 0;

    cart.forEach(function (item) {
      const row = document.createElement("article");
      row.className = "cart-item";
      row.dataset.testid = `cart-item-${item.id}`;

      const details = document.createElement("div");

      const name = document.createElement("h2");
      name.textContent = item.name;

      const quantity = document.createElement("p");
      quantity.textContent = `Quantity: ${item.quantity}`;

      const removeButton = document.createElement("button");
      removeButton.type = "button";
      removeButton.textContent = "Remove";
      removeButton.addEventListener("click", function () {
        removeFromCart(item.id);
        renderCart();
      });

      details.append(name, quantity);
      row.append(details, removeButton);
      cartItems.appendChild(row);
    });
  }

  function removeFromCart(productId) {
    const cart = getCart().filter(function (item) {
      return item.id !== productId;
    });
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
  }

  function getCart() {
    return readJson(CART_KEY, []);
  }

  function setMessage(element, text, type) {
    element.textContent = text;
    element.classList.remove("success", "error");
    element.classList.add(type);
  }

  function clearMessage(element) {
    element.textContent = "";
    element.classList.remove("success", "error");
  }

  function readJson(key, fallback) {
    try {
      const value = localStorage.getItem(key);
      return value ? JSON.parse(value) : fallback;
    } catch (error) {
      return fallback;
    }
  }

  function formatPrice(value) {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
    }).format(value);
  }
})();
