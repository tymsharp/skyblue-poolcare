/* Show the drawn mark + wordmark if the logo image can't load. */
(function () {
  document.querySelectorAll(".brand-logo").forEach(function (img) {
    function fail() { img.closest(".brand").classList.add("nologo"); img.remove(); }
    if (img.complete && !img.naturalWidth) fail();
    else img.addEventListener("error", fail);
  });
})();
