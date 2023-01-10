const btn = document.querySelector("button");

if (btn) {
  btn.onclick = function() {
    btn.classList.toggle("dipped");
    console.log("heree!"); // will have to open the console cmd+opt+J
  };
}

function tester() {
  console.log("here");
}