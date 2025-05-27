$(function () {
  $(".btn-number").click(function (e) {
    e.preventDefault();
    var $button = $(this); // Cache the button
    var fieldName = $button.attr("data-field");
    var type = $button.attr("data-type");
    var $input = $("input[name='" + fieldName + "']");
    var currentVal = parseInt($input.val());
    var min = parseInt($input.attr("min"));
    var max = parseInt($input.attr("max"));
    if (type === "minus") {
      if (currentVal > min) {
        $input.val(currentVal - 1).change();
      }
      // Disable if new value is min
      if (parseInt($input.val()) === min) {
        $button.attr("disabled", true);
      }
      // Enable the plus button if it was disabled
      $input
        .closest(".input-group")
        .find('[data-type="plus"]')
        .attr("disabled", false);
    } else if (type === "plus") {
      if (currentVal < max) {
        $input.val(currentVal + 1).change();
      }
      // Disable if new value is max
      if (parseInt($input.val()) === max) {
        $button.attr("disabled", true);
      }
      // Enable the minus button if it was disabled
      $input
        .closest(".input-group")
        .find('[data-type="minus"]')
        .attr("disabled", false);
    }
  });
});
