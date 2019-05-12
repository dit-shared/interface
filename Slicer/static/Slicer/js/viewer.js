let DICOM_PALLETE = "";

slider.addEventListener('mouseout', function () {
  getSlice(slider.noUiSlider.get());
});
slider.addEventListener('click', function () {
  getSlice(slider.noUiSlider.get());
});
slider.addEventListener('mousemove', function () {
  getSlice(slider.noUiSlider.get());
});

$("#changePallete").change(function() {
  var str = "";
  $( "#changePallete option:selected" ).each(function() {
    str = $( this ).text();
  });
  if (str == "Стандартная") {
    DICOM_PALLETE = "";
  } else {
    DICOM_PALLETE = str;
  }
  getSlice(slider.noUiSlider.get());
});