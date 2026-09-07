/* Homepage city filter. Pure client-side; no data leaves the browser and the
   full list is in the HTML, so it degrades to nothing if JS is off. */
(function () {
  var input = document.getElementById("city-search");
  if (!input) return;
  var status = document.getElementById("city-search-status");
  var links = Array.prototype.slice.call(document.querySelectorAll("#cities a.city-link"));
  var blocks = Array.prototype.slice.call(document.querySelectorAll("#cities .county-block"));
  var total = links.length;

  function norm(s) {
    return (s || "").toLowerCase().replace(/[^a-z0-9 ]/g, " ").replace(/\s+/g, " ").trim();
  }

  function apply() {
    var q = norm(input.value);
    var shown = 0;
    links.forEach(function (a) {
      var hay = [a.getAttribute("data-city"), a.getAttribute("data-county"),
                 a.getAttribute("data-zips"), a.getAttribute("data-hood")].join(" ");
      var hit = !q || norm(hay).indexOf(q) !== -1;
      a.style.display = hit ? "" : "none";
      if (hit) shown++;
    });
    blocks.forEach(function (b) {
      var any = Array.prototype.some.call(b.querySelectorAll("a.city-link"), function (a) {
        return a.style.display !== "none";
      });
      b.style.display = any ? "" : "none";
    });
    if (!q) {
      status.textContent = total + " cities covered across " + blocks.length + " counties.";
    } else if (shown) {
      status.textContent = shown + (shown === 1 ? " match" : " matches") + ".";
    } else {
      status.textContent = "No match. Call and ask \u2014 we cover more than what is listed, and we " +
                           "will tell you honestly if we do not reach your address.";
    }
  }

  input.addEventListener("input", apply);
  apply();
})();
