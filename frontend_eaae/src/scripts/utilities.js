// Helper functions
function $(id) {
  return host.shadowRoot.querySelector(id);
}

function $$(id) {
  return host.shadowRoot.querySelectorAll(id);
}

function hide(id) {
  $(id).style.display = "none";
  $(id).style.opacity = 0;
}

function showBlock(id) {
  $(id).style.display = "block";
  $(id).style.opacity = 1;
}

function showFlex(id) {
  $(id).style.display = "flex";
  $(id).style.opacity = 1;
}