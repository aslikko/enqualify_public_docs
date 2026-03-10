/* EnQualify Docs — Her zaman light mode başlat */
(function () {
  // Sayfa yüklenmeden önce localStorage'ı override et
  // Material teması __palette key'ini kullanıyor
  var palette = { index: 0, color: { scheme: "default", primary: "custom", accent: "custom" } };
  localStorage.setItem("__palette", JSON.stringify(palette));

  // data-md-color-scheme attribute'unu da zorla set et
  document.documentElement.setAttribute("data-md-color-scheme", "default");
  document.documentElement.setAttribute("data-md-color-primary", "custom");
})();
