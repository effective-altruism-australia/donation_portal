// Helper functions
function $(id) {
  return host.shadowRoot.getElementById(id);;
}

function hide(id) {
  $(id).style.display = "none";
}

function showBlock(id) {
  $(id).style.display = "block";
}

function showFlex(id) {
  $(id).style.display = "flex";
}