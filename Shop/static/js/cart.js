function getCookie(name) {
  let cookieArray = document.cookie.split(";");
  for (let i = 0; i < cookieArray.length; i++) {
    let cookiePair = cookieArray[i].split("=");
    if (name == cookiePair[0].trim()) {
      return decodeURIComponent(cookiePair[1]);
    }
  }
  return null;
}

let cart = JSON.parse(getCookie("cart"));
if (cart == undefined) {
  ///creating a cart, then specifiying it to current domain instead of creating in every page
  cart = {};
  document.cookie = `cart=${JSON.stringify(cart)};domain=;path=/`;
}

//////////////

function updateCookieCart(productId, action) {
  if (action == "add") {
    if (cart[productId] == undefined) {
      cart[productId] = { quantity: 1 };
    } else {
      cart[productId]["quantity"] += 1;
    }
  } else if (action == "remove") {
    if (cart[productId]["quantity"] == 1) {
      delete cart[productId];
    } else {
      cart[productId]["quantity"] -= 1;
    }
  }
  document.cookie = `cart=${JSON.stringify(cart)};domain=;path=/`;
  location.reload();
}

function updateAuthenticatedCart(productId, action) {
  let url = "/update_user_cart/";
  let requestInfo = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ id: productId, action: action }),
  };

  fetch(url, requestInfo)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      location.reload();
    });
}
//////////////

function updateCart(btn) {
  let productId = this.dataset.productid;
  let action = this.dataset.action;

  if (user === "AnonymousUser") {
    updateCookieCart(productId, action);
  } else {
    updateAuthenticatedCart(productId, action);
  }
}

let cartUpdateButtons = document.getElementsByClassName("update-cart");
for (i = 0; i < cartUpdateButtons.length; i++) {
  cartUpdateButtons[i].addEventListener("click", updateCart);
}
